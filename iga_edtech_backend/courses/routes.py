
import json
from datetime import datetime, timezone
from io import BytesIO

from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from marshmallow import ValidationError

from models.base import db
from models.course import (
    Assessment, Course, Enrollment, Lesson, LessonCompletion, Module, Question, Submission
)
from models.user import User
from utils.decorators import student_required, teacher_required

from .schemas import (
    AssessmentSchema, CourseSchema, GradeShortAnswerSchema,
    ModuleSchema, QuestionSchema, SubmissionSchema,
)

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")


def _ok(message, data=None, status=200):
    body = {"success": True, "message": message}
    if data is not None:
        body["data"] = data
    return jsonify(body), status


def _err(message, status=400, errors=None):
    body = {"success": False, "message": message}
    if errors:
        body["errors"] = errors
    return jsonify(body), status


def _load(schema_cls):
    raw = request.get_json(silent=True) or {}
    try:
        return schema_cls().load(raw), None
    except ValidationError as e:
        return None, e.messages


def _teacher_owns(course):
    uid  = int(get_jwt_identity())
    role = get_jwt().get("role")
    if role == "admin":
        return True
    return course.teacher_id == uid


def _best_submission(student_id, assessment_id):
    
    subs = Submission.query.filter_by(
        student_id=student_id, assessment_id=assessment_id
    ).all()
    if not subs:
        return None
    graded = [s for s in subs if s.graded_at]
    pool   = graded if graded else subs
    return max(pool, key=lambda s: (s.score or 0))


@courses_bp.route("", methods=["GET"])
@jwt_required()
def list_courses():
    uid  = int(get_jwt_identity())
    role = get_jwt().get("role")
    if role == "student":
        courses = Course.query.filter_by(is_published=True).all()
    elif role == "teacher":
        courses = Course.query.filter_by(teacher_id=uid).all()
    else:
        courses = Course.query.all()
    return _ok("Courses retrieved.", [c.to_dict() for c in courses])


@courses_bp.route("/<int:course_id>", methods=["GET"])
@jwt_required()
def get_course(course_id):
    course = db.session.get(Course, course_id)
    if not course:
        return _err("Course not found.", 404)
    return _ok("Course retrieved.", course.to_dict(include_modules=True))


@courses_bp.route("", methods=["POST"])
@teacher_required
def create_course():
    data, errors = _load(CourseSchema)
    if errors:
        return _err("Validation failed.", 422, errors)

    uid    = int(get_jwt_identity())
    course = Course(
        teacher_id=uid,
        title=data["title"],
        description=data.get("description"),
        guidelines=data.get("guidelines"),
        is_published=data.get("is_published", False),
    )
    db.session.add(course)
    db.session.flush()

    if data.get("module_title"):
        module = Module(
            course_id=course.id,
            title=data["module_title"],
            description=data.get("module_description"),
            order=1,
        )
        db.session.add(module)
        db.session.flush()

        if data.get("lesson_title"):
            lesson = Lesson(
                module_id=module.id,
                title=data["lesson_title"],
                file_type=data.get("file_type", "video"),
                file_url=data.get("file_url"),
                order=1,
            )
            db.session.add(lesson)

    db.session.commit()
    return _ok("Course created.", course.to_dict(include_modules=True), 201)


@courses_bp.route("/<int:course_id>", methods=["PUT"])
@teacher_required
def update_course(course_id):
    course = db.session.get(Course, course_id)
    if not course:
        return _err("Course not found.", 404)
    if not _teacher_owns(course):
        return _err("Not authorised.", 403)

    data, errors = _load(CourseSchema)
    if errors:
        return _err("Validation failed.", 422, errors)

    for field in ("title", "description", "guidelines", "is_published"):
        if field in data:
            setattr(course, field, data[field])

    db.session.commit()
    return _ok("Course updated.", course.to_dict(include_modules=True))


@courses_bp.route("/<int:course_id>", methods=["DELETE"])
@teacher_required
def delete_course(course_id):
    course = db.session.get(Course, course_id)
    if not course:
        return _err("Course not found.", 404)
    if not _teacher_owns(course):
        return _err("Not authorised.", 403)
    db.session.delete(course)
    db.session.commit()
    return _ok("Course deleted.")


@courses_bp.route("/<int:course_id>/modules", methods=["POST"])
@teacher_required
def add_module(course_id):
    course = db.session.get(Course, course_id)
    if not course or not _teacher_owns(course):
        return _err("Not found or not authorised.", 404)

    data, errors = _load(ModuleSchema)
    if errors:
        return _err("Validation failed.", 422, errors)

    order  = len(course.modules) + 1
    module = Module(
        course_id=course_id,
        title=data["title"],
        description=data.get("description"),
        order=order,
    )
    db.session.add(module)
    db.session.commit()
    return _ok("Module added.", module.to_dict(), 201)


@courses_bp.route("/modules/<int:module_id>", methods=["DELETE"])
@teacher_required
def delete_module(module_id):
    module = db.session.get(Module, module_id)
    if not module:
        return _err("Module not found.", 404)
    course = db.session.get(Course, module.course_id)
    if not _teacher_owns(course):
        return _err("Not authorised.", 403)
    db.session.delete(module)
    db.session.commit()
    return _ok("Module deleted.")


import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {
    'video':    {'mp4','mkv','avi','mov','webm'},
    'pdf':      {'pdf'},
    'slides':   {'ppt','pptx','odp'},
    'document': {'doc','docx','odt','txt'},
    'image':    {'jpg','jpeg','png','gif','webp','svg'},
}
ALL_ALLOWED = {ext for exts in ALLOWED_EXTENSIONS.values() for ext in exts}

def _upload_dir():
    from flask import current_app
    upload_dir = os.path.join(current_app.root_path, 'uploads', 'lessons')
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir

def _save_file(file, file_type):
   
    from flask import current_app
    filename  = secure_filename(file.filename)
    ext       = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    allowed   = ALLOWED_EXTENSIONS.get(file_type, ALL_ALLOWED)
    if ext not in allowed:
        return None, f"File type .{ext} not allowed for {file_type} lessons."
    
    import uuid
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    save_path   = os.path.join(_upload_dir(), unique_name)
    file.save(save_path)
    return f"/courses/uploads/lessons/{unique_name}", None


@courses_bp.route("/uploads/lessons/<path:filename>", methods=["GET"])
def serve_lesson_file(filename):
    
    import mimetypes
    from flask import send_from_directory
    upload_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'lessons')
    upload_dir = os.path.abspath(upload_dir)
    mime, _    = mimetypes.guess_type(filename)
    response   = send_from_directory(
        upload_dir, filename,
        mimetype=mime or 'application/octet-stream'
    )
   
    response.headers['Content-Disposition'] = f'inline; filename="{filename}"'
   
    response.headers['Access-Control-Allow-Origin']  = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
   
    response.headers['Accept-Ranges'] = 'bytes'
    return response


@courses_bp.route("/modules/<int:module_id>/lessons", methods=["POST"])
@teacher_required
def add_lesson(module_id):
   
    module = db.session.get(Module, module_id)
    if not module:
        return _err("Module not found.", 404)
    course = db.session.get(Course, module.course_id)
    if not _teacher_owns(course):
        return _err("Not authorised.", 403)

    
    if request.content_type and 'multipart' in request.content_type:
        title     = request.form.get("title", "").strip()
        file_type = request.form.get("file_type", "video")
        file_url  = request.form.get("file_url", "").strip() or None
        uploaded  = request.files.get("file")
    else:
        raw       = request.get_json(silent=True) or {}
        title     = raw.get("title", "").strip()
        file_type = raw.get("file_type", "video")
        file_url  = raw.get("file_url") or None
        uploaded  = None

    if not title:
        return _err("Lesson title is required.", 422)

    
    if uploaded and uploaded.filename:
        saved_url, err = _save_file(uploaded, file_type)
        if err:
            return _err(err, 422)
        file_url = saved_url

    order  = len(module.lessons) + 1
    lesson = Lesson(
        module_id=module_id, title=title,
        file_type=file_type, file_url=file_url, order=order,
    )
    db.session.add(lesson)
    db.session.commit()
    return _ok("Lesson added.", lesson.to_dict(), 201)


@courses_bp.route("/lessons/<int:lesson_id>", methods=["PUT"])
@teacher_required
def update_lesson(lesson_id):
    
    lesson = db.session.get(Lesson, lesson_id)
    if not lesson:
        return _err("Lesson not found.", 404)
    module = db.session.get(Module, lesson.module_id)
    course = db.session.get(Course, module.course_id)
    if not _teacher_owns(course):
        return _err("Not authorised.", 403)

    if request.content_type and 'multipart' in request.content_type:
        title     = request.form.get("title", "").strip()
        file_type = request.form.get("file_type", "").strip()
        file_url  = request.form.get("file_url", "").strip() or None
        uploaded  = request.files.get("file")
    else:
        raw       = request.get_json(silent=True) or {}
        title     = raw.get("title", "").strip()
        file_type = raw.get("file_type", "").strip()
        file_url  = raw.get("file_url") or None
        uploaded  = None

    if title:     lesson.title     = title
    if file_type: lesson.file_type = file_type

    if uploaded and uploaded.filename:
        ft = file_type or lesson.file_type
        saved_url, err = _save_file(uploaded, ft)
        if err:
            return _err(err, 422)
        lesson.file_url = saved_url
    elif file_url is not None:
        lesson.file_url = file_url

    db.session.commit()
    return _ok("Lesson updated.", lesson.to_dict())



@courses_bp.route("/lessons/<int:lesson_id>", methods=["DELETE"])
@teacher_required
def delete_lesson(lesson_id):
    lesson = db.session.get(Lesson, lesson_id)
    if not lesson:
        return _err("Lesson not found.", 404)
    module = db.session.get(Module, lesson.module_id)
    course = db.session.get(Course, module.course_id)
    if not _teacher_owns(course):
        return _err("Not authorised.", 403)
    db.session.delete(lesson)
    db.session.commit()
    return _ok("Lesson deleted.")


@courses_bp.route("/<int:course_id>/enroll", methods=["POST"])
@student_required
def enroll(course_id):
    uid    = int(get_jwt_identity())
    course = db.session.get(Course, course_id)
    if not course or not course.is_published:
        return _err("Course not found.", 404)

    existing = Enrollment.query.filter_by(student_id=uid, course_id=course_id).first()
    if existing:
        return _err("Already enrolled in this course.", 409)

    enrollment = Enrollment(student_id=uid, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return _ok("Enrolled successfully.", enrollment.to_dict(), 201)


@courses_bp.route("/my-enrollments", methods=["GET"])
@student_required
def my_enrollments():
    uid         = int(get_jwt_identity())
    enrollments = Enrollment.query.filter_by(student_id=uid).all()
    return _ok("Enrollments retrieved.", [e.to_dict() for e in enrollments])


@courses_bp.route("/<int:course_id>/assessments", methods=["GET"])
@jwt_required()
def list_assessments(course_id):
    role   = get_jwt().get("role")
    course = db.session.get(Course, course_id)
    if not course:
        return _err("Course not found.", 404)
    if role == "student":
        assessments = Assessment.query.filter_by(course_id=course_id, is_published=True).all()
    else:
        assessments = Assessment.query.filter_by(course_id=course_id).all()
    return _ok("Assessments retrieved.", [a.to_dict() for a in assessments])


@courses_bp.route("/assessments/all", methods=["GET"])
@jwt_required()
def all_assessments():
    uid  = int(get_jwt_identity())
    role = get_jwt().get("role")

    if role == "student":
        enrolled_ids = [e.course_id for e in Enrollment.query.filter_by(student_id=uid).all()]
        assessments  = Assessment.query.filter(
            Assessment.course_id.in_(enrolled_ids),
            Assessment.is_published == True
        ).all()
        result = []
        for a in assessments:
            d             = a.to_dict()
            attempt_count = Submission.query.filter_by(assessment_id=a.id, student_id=uid).count()
            d["attempts_used"]      = attempt_count
            d["attempts_remaining"] = max(0, a.max_attempts - attempt_count)
            d["can_attempt"]        = attempt_count < a.max_attempts
            best = _best_submission(uid, a.id)
            d["best_submission"]    = best.to_dict() if best else None
            result.append(d)
        return _ok("Assessments retrieved.", result)

    elif role == "teacher":
        assessments = Assessment.query.filter_by(teacher_id=uid).all()
    else:
        assessments = Assessment.query.all()

    return _ok("Assessments retrieved.", [a.to_dict() for a in assessments])


@courses_bp.route("/assessments/<int:assessment_id>", methods=["GET"])
@jwt_required()
def get_assessment(assessment_id):
    role       = get_jwt().get("role")
    assessment = db.session.get(Assessment, assessment_id)
    if not assessment:
        return _err("Assessment not found.", 404)

    include_answers = role in ("teacher", "admin")
    data            = assessment.to_dict()
    data["questions"] = [q.to_dict(include_answer=include_answers) for q in assessment.questions]
    return _ok("Assessment retrieved.", data)


@courses_bp.route("/<int:course_id>/assessments", methods=["POST"])
@teacher_required
def create_assessment(course_id):
    course = db.session.get(Course, course_id)
    if not course or not _teacher_owns(course):
        return _err("Not found or not authorised.", 404)

    data, errors = _load(AssessmentSchema)
    if errors:
        return _err("Validation failed.", 422, errors)

    uid        = int(get_jwt_identity())
    assessment = Assessment(
        course_id=course_id, teacher_id=uid,
        title=data["title"], description=data.get("description"),
        time_limit=data.get("time_limit"), max_attempts=data.get("max_attempts", 1),
        is_published=data.get("is_published", False),
    )
    db.session.add(assessment)
    db.session.flush()

    for i, q_data in enumerate(data.get("questions", []), 1):
        ca = q_data.get("correct_answer", [])
        if isinstance(ca, str):
            ca = [ca]
        question = Question(
            assessment_id=assessment.id,
            question_type=q_data["question_type"],
            text=q_data["text"],
            options=json.dumps(q_data.get("options", [])),
            correct_answer=json.dumps(ca),
            allow_multiple=q_data.get("allow_multiple", False),
            order=i, points=q_data.get("points", 1),
        )
        db.session.add(question)

    db.session.commit()
    return _ok("Assessment created.", assessment.to_dict(include_questions=True), 201)


@courses_bp.route("/assessments/<int:assessment_id>", methods=["PUT"])
@teacher_required
def update_assessment(assessment_id):
    assessment = db.session.get(Assessment, assessment_id)
    if not assessment:
        return _err("Assessment not found.", 404)
    course = db.session.get(Course, assessment.course_id)
    if not _teacher_owns(course):
        return _err("Not authorised.", 403)


    subs = assessment.submissions
    if subs:
        all_graded = all(s.graded_at is not None for s in subs)
        if all_graded:
            return _err(
                "This assessment has been fully graded and cannot be edited. "
                "Create a new assessment if changes are needed.", 403
            )

    data, errors = _load(AssessmentSchema)
    if errors:
        return _err("Validation failed.", 422, errors)

    for field in ("title", "description", "time_limit", "max_attempts", "is_published"):
        if field in data:
            setattr(assessment, field, data[field])

    db.session.commit()
    return _ok("Assessment updated.", assessment.to_dict())



@courses_bp.route("/assessments/<int:assessment_id>/questions", methods=["POST"])
@teacher_required
def add_question(assessment_id):
    assessment = db.session.get(Assessment, assessment_id)
    if not assessment:
        return _err("Assessment not found.", 404)
    course = db.session.get(Course, assessment.course_id)
    if not _teacher_owns(course):
        return _err("Not authorised.", 403)

    data, errors = _load(QuestionSchema)
    if errors:
        return _err("Validation failed.", 422, errors)

    ca = data.get("correct_answer", [])
    if isinstance(ca, str):
        ca = [ca]
    order    = len(assessment.questions) + 1
    question = Question(
        assessment_id=assessment_id,
        question_type=data["question_type"], text=data["text"],
        options=json.dumps(data.get("options", [])),
        correct_answer=json.dumps(ca),
        allow_multiple=data.get("allow_multiple", False),
        order=order, points=data.get("points", 1),
    )
    db.session.add(question)
    db.session.commit()
    return _ok("Question added.", question.to_dict(include_answer=True), 201)


@courses_bp.route("/questions/<int:question_id>", methods=["PUT"])
@teacher_required
def update_question(question_id):
    question = db.session.get(Question, question_id)
    if not question:
        return _err("Question not found.", 404)

    data, errors = _load(QuestionSchema)
    if errors:
        return _err("Validation failed.", 422, errors)

    for field in ("question_type", "text", "points", "allow_multiple"):
        if field in data:
            setattr(question, field, data[field])
    if "options" in data:
        question.options = json.dumps(data["options"])
    if "correct_answer" in data:
        ca = data["correct_answer"]
        if isinstance(ca, str):
            ca = [ca]
        question.correct_answer = json.dumps(ca)

    db.session.commit()
    return _ok("Question updated.", question.to_dict(include_answer=True))


@courses_bp.route("/questions/<int:question_id>", methods=["DELETE"])
@teacher_required
def delete_question(question_id):
    question = db.session.get(Question, question_id)
    if not question:
        return _err("Question not found.", 404)
    db.session.delete(question)
    db.session.commit()
    return _ok("Question deleted.")


@courses_bp.route("/assessments/<int:assessment_id>/submit", methods=["POST"])
@student_required
def submit_assessment(assessment_id):
    uid        = int(get_jwt_identity())
    assessment = db.session.get(Assessment, assessment_id)
    if not assessment or not assessment.is_published:
        return _err("Assessment not found.", 404)

    attempt_count = Submission.query.filter_by(
        assessment_id=assessment_id, student_id=uid
    ).count()
    if attempt_count >= assessment.max_attempts:
        return _err(f"Maximum attempts ({assessment.max_attempts}) reached.", 403)

    data, errors = _load(SubmissionSchema)
    if errors:
        return _err("Validation failed.", 422, errors)

    answers          = data["answers"]
    score            = 0
    max_score        = 0
    has_short_answer = False

    for question in assessment.questions:
        max_score += question.points
        if question.question_type == "short_answer":
            has_short_answer = True
            continue

        try:
            correct_list = json.loads(question.correct_answer or "[]")
        except Exception:
            correct_list = [question.correct_answer] if question.correct_answer else []
        correct_set = {str(c).strip().lower() for c in correct_list}

        raw = answers.get(str(question.id), "")
        if isinstance(raw, list):
            student_set = {str(a).strip().lower() for a in raw}
        else:
            student_set = {str(raw).strip().lower()} if raw else set()

        if student_set == correct_set:
            score += question.points

    submission = Submission(
        assessment_id=assessment_id, student_id=uid,
        answers=json.dumps(answers), score=score, max_score=max_score,
        attempt_number=attempt_count + 1,
        graded_at=datetime.now(timezone.utc) if not has_short_answer else None,
    )
    db.session.add(submission)
    db.session.commit()
    return _ok("Assessment submitted.", submission.to_dict(), 201)


@courses_bp.route("/my-submissions", methods=["GET"])
@student_required
def my_submissions():
    
    uid = int(get_jwt_identity())

    all_subs = Submission.query.filter_by(student_id=uid).all()
    seen     = set()
    best_subs = []
    for s in all_subs:
        if s.assessment_id not in seen:
            seen.add(s.assessment_id)
            best = _best_submission(uid, s.assessment_id)
            if best:
                best_subs.append(best)

    result = []
    for s in best_subs:
        d          = s.to_dict()
        assessment = db.session.get(Assessment, s.assessment_id)
        if assessment:
            student_answers = json.loads(s.answers) if s.answers else {}
            try:
                manual_comments = json.loads(s.manual_comments or "{}")
            except Exception:
                manual_comments = {}
            try:
                manual_scores = json.loads(s.manual_scores or "{}")
            except Exception:
                manual_scores = {}

            review = []
            for q in assessment.questions:
                try:
                    correct = json.loads(q.correct_answer or "[]")
                except Exception:
                    correct = []
                student_ans = student_answers.get(str(q.id), "")
                if isinstance(student_ans, list):
                    student_set = {str(a).strip().lower() for a in student_ans}
                else:
                    student_set = {str(student_ans).strip().lower()} if student_ans else set()
                correct_set = {str(c).strip().lower() for c in correct}

                is_correct = None
                if q.question_type != "short_answer":
                    is_correct = student_set == correct_set
                elif str(q.id) in manual_scores:
                    is_correct = manual_scores[str(q.id)] > 0

                review.append({
                    "question_id":      q.id,
                    "question_text":    q.text,
                    "question_type":    q.question_type,
                    "options":          json.loads(q.options) if q.options else [],
                    "student_answer":   student_ans,
                    "correct_answer":   correct if q.question_type != "short_answer" else None,
                    "is_correct":       is_correct,
                    "points":           q.points,
                    "points_earned":    manual_scores.get(str(q.id), q.points if is_correct else 0),
                    "teacher_comment":  manual_comments.get(str(q.id)),
                })
            d["review"] = review
        result.append(d)

    return _ok("Submissions retrieved.", result)

@courses_bp.route("/submissions/<int:submission_id>/grade", methods=["POST"])
@teacher_required
def grade_submission(submission_id):
   
    sub = db.session.get(Submission, submission_id)
    if not sub:
        return _err("Submission not found.", 404)

    assessment = db.session.get(Assessment, sub.assessment_id)
    course     = db.session.get(Course, assessment.course_id)
    if not _teacher_owns(course):
        return _err("Not authorised.", 403)

    data, errors = _load(GradeShortAnswerSchema)
    if errors:
        return _err("Validation failed.", 422, errors)

    grades = data["grades"]

    try:
        manual_scores   = json.loads(sub.manual_scores   or "{}")
    except Exception:
        manual_scores   = {}
    try:
        manual_comments = json.loads(sub.manual_comments or "{}")
    except Exception:
        manual_comments = {}

    student_answers = json.loads(sub.answers) if sub.answers else {}
    auto_score  = 0
    max_score   = 0
    manual_total = 0

    for q in assessment.questions:
        max_score += q.points
        if q.question_type == "short_answer":
            if str(q.id) in grades:
                raw_score = float(grades[str(q.id)].get("score", 0))
                pts = max(0.0, min(raw_score, float(q.points)))  # clamp 0..max
                manual_scores[str(q.id)]   = pts
                manual_comments[str(q.id)] = grades[str(q.id)].get("comment", "")
                manual_total += pts
            elif str(q.id) in manual_scores:
                manual_total += manual_scores[str(q.id)]
        else:
            try:
                correct_list = json.loads(q.correct_answer or "[]")
            except Exception:
                correct_list = []
            correct_set = {str(c).strip().lower() for c in correct_list}
            raw = student_answers.get(str(q.id), "")
            if isinstance(raw, list):
                student_set = {str(a).strip().lower() for a in raw}
            else:
                student_set = {str(raw).strip().lower()} if raw else set()
            if student_set == correct_set:
                auto_score += q.points

    sub.score           = auto_score + manual_total
    sub.max_score       = max_score
    sub.manual_scores   = json.dumps(manual_scores)
    sub.manual_comments = json.dumps(manual_comments)
    sub.graded_at       = datetime.now(timezone.utc)
    db.session.commit()

    return _ok("Submission graded.", sub.to_dict())


@courses_bp.route("/teacher/pending-grades", methods=["GET"])
@teacher_required
def pending_grades():
   
    uid        = int(get_jwt_identity())
    courses    = Course.query.filter_by(teacher_id=uid).all()
    course_ids = [c.id for c in courses]

    subs = Submission.query.join(Assessment).filter(
        Assessment.course_id.in_(course_ids),
        Submission.graded_at == None
    ).all()

    result = []
    for s in subs:
        d          = s.to_dict()
        assessment = db.session.get(Assessment, s.assessment_id)
        student_answers = json.loads(s.answers) if s.answers else {}
        short_qs = [q for q in assessment.questions if q.question_type == "short_answer"]
        d["short_answers"] = [
            {
                "question_id":   q.id,
                "question_text": q.text,
                "student_answer": student_answers.get(str(q.id), ""),
                "max_points":    q.points,
            }
            for q in short_qs
        ]
        result.append(d)

    return _ok("Pending grades retrieved.", result)

@courses_bp.route("/teacher/students", methods=["GET"])
@teacher_required
def teacher_students():
    uid        = int(get_jwt_identity())
    courses    = Course.query.filter_by(teacher_id=uid).all()
    course_ids = [c.id for c in courses]

    enrollments = Enrollment.query.filter(
        Enrollment.course_id.in_(course_ids)
    ).all()

    results = []
    for e in enrollments:
        best = None
        for a in Assessment.query.filter_by(course_id=e.course_id).all():
            b = _best_submission(e.student_id, a.id)
            if b and (best is None or (b.score or 0) > (best.score or 0)):
                best = b

        results.append({
            "student_id":   e.student_id,
            "student_name": e.student.full_name,
            "course_id":    e.course_id,
            "course_title": e.course.title,
            "enrolled_at":  e.enrolled_at.isoformat() if e.enrolled_at else None,
            "score":        best.score if best else None,
            "max_score":    best.max_score if best else None,
            "percentage":   best.to_dict()["percentage"] if best else None,
            "status":       best.to_dict()["status"] if best else "not_started",
        })

    return _ok("Student performance retrieved.", results)


@courses_bp.route("/lessons/<int:lesson_id>/complete", methods=["POST"])
@student_required
def mark_lesson_complete(lesson_id):
    
    uid    = int(get_jwt_identity())
    lesson = db.session.get(Lesson, lesson_id)
    if not lesson:
        return _err("Lesson not found.", 404)

    existing = LessonCompletion.query.filter_by(
        student_id=uid, lesson_id=lesson_id
    ).first()
    if existing:
        return _ok("Lesson already marked as done.")

    completion = LessonCompletion(student_id=uid, lesson_id=lesson_id)
    db.session.add(completion)
    db.session.commit()
    return _ok("Lesson marked as done.", completion.to_dict(), 201)


@courses_bp.route("/lessons/<int:lesson_id>/complete", methods=["DELETE"])
@student_required
def unmark_lesson_complete(lesson_id):
  
    uid        = int(get_jwt_identity())
    completion = LessonCompletion.query.filter_by(
        student_id=uid, lesson_id=lesson_id
    ).first()
    if not completion:
        return _err("Lesson not marked as done.", 404)
    db.session.delete(completion)
    db.session.commit()
    return _ok("Lesson unmarked.")


@courses_bp.route("/my-completions", methods=["GET"])
@student_required
def my_completions():
    
    uid         = int(get_jwt_identity())
    completions = LessonCompletion.query.filter_by(student_id=uid).all()
    return _ok("Completions retrieved.", [c.lesson_id for c in completions])


@courses_bp.route("/teacher/students-submissions", methods=["GET"])
@teacher_required
def teacher_student_submissions():
   
    uid       = int(get_jwt_identity())
    student_id = request.args.get("student_id", type=int)
    course_id  = request.args.get("course_id",  type=int)

    if not student_id or not course_id:
        return _err("student_id and course_id are required.", 400)

    course = db.session.get(Course, course_id)
    if not course or not _teacher_owns(course):
        return _err("Not authorised.", 403)

    assessments = Assessment.query.filter_by(course_id=course_id).all()
    results = []
    for a in assessments:
        best = _best_submission(student_id, a.id)
        if best:
            d = best.to_dict()
           
            student_answers = json.loads(best.answers) if best.answers else {}
            try:
                manual_scores   = json.loads(best.manual_scores   or "{}")
            except Exception:
                manual_scores   = {}
            try:
                manual_comments = json.loads(best.manual_comments or "{}")
            except Exception:
                manual_comments = {}
            review = []
            for q in a.questions:
                try:
                    correct = json.loads(q.correct_answer or "[]")
                except Exception:
                    correct = []
                student_ans = student_answers.get(str(q.id), "")
                if isinstance(student_ans, list):
                    student_set = {str(x).strip().lower() for x in student_ans}
                else:
                    student_set = {str(student_ans).strip().lower()} if student_ans else set()
                correct_set = {str(c).strip().lower() for c in correct}
                is_correct  = None
                if q.question_type != "short_answer":
                    is_correct = student_set == correct_set
                elif str(q.id) in manual_scores:
                    is_correct = manual_scores[str(q.id)] > 0
                review.append({
                    "question_id":     q.id,
                    "question_text":   q.text,
                    "question_type":   q.question_type,
                    "options":         json.loads(q.options) if q.options else [],
                    "student_answer":  student_ans,
                    "correct_answer":  correct,
                    "is_correct":      is_correct,
                    "points":          q.points,
                    "points_earned":   manual_scores.get(str(q.id), q.points if is_correct else 0),
                    "teacher_comment": manual_comments.get(str(q.id)),
                })
            d["review"]           = review
            d["assessment_title"] = a.title
            results.append(d)

    return _ok("Submissions retrieved.", results)


@courses_bp.route("/teacher/submission/<int:submission_id>", methods=["GET"])
@teacher_required
def teacher_view_submission(submission_id):
    
    sub = db.session.get(Submission, submission_id)
    if not sub:
        return _err("Submission not found.", 404)

    assessment = db.session.get(Assessment, sub.assessment_id)
    course     = db.session.get(Course, assessment.course_id)
    if not _teacher_owns(course):
        return _err("Not authorised.", 403)

    d               = sub.to_dict()
    student_answers = json.loads(sub.answers) if sub.answers else {}
    try:
        manual_scores   = json.loads(sub.manual_scores   or "{}")
    except Exception:
        manual_scores   = {}
    try:
        manual_comments = json.loads(sub.manual_comments or "{}")
    except Exception:
        manual_comments = {}

    review = []
    for q in assessment.questions:
        try:
            correct = json.loads(q.correct_answer or "[]")
        except Exception:
            correct = []
        student_ans = student_answers.get(str(q.id), "")
        if isinstance(student_ans, list):
            student_set = {str(a).strip().lower() for a in student_ans}
        else:
            student_set = {str(student_ans).strip().lower()} if student_ans else set()
        correct_set = {str(c).strip().lower() for c in correct}

        is_correct = None
        if q.question_type != "short_answer":
            is_correct = student_set == correct_set
        elif str(q.id) in manual_scores:
            is_correct = manual_scores[str(q.id)] > 0

        review.append({
            "question_id":      q.id,
            "question_text":    q.text,
            "question_type":    q.question_type,
            "options":          json.loads(q.options) if q.options else [],
            "student_answer":   student_ans,
            "correct_answer":   correct,
            "is_correct":       is_correct,
            "points":           q.points,
            "points_earned":    manual_scores.get(str(q.id), q.points if is_correct else 0),
            "teacher_comment":  manual_comments.get(str(q.id)),
        })
    d["review"]       = review
    d["student_name"] = sub.student.full_name if sub.student else "—"
    return _ok("Submission retrieved.", d)

@courses_bp.route("/teacher/export-report", methods=["GET"])
@teacher_required
def export_report():
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.platypus import (
            Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
        )
    except ImportError:
        return _err("PDF generation requires reportlab. Run: pip install reportlab", 500)

    uid     = int(get_jwt_identity())
    teacher = db.session.get(User, uid)
    courses = Course.query.filter_by(teacher_id=uid).all()
    course_ids  = [c.id for c in courses]
    enrollments = Enrollment.query.filter(Enrollment.course_id.in_(course_ids)).all()

    buffer   = BytesIO()
    doc      = SimpleDocTemplate(buffer, pagesize=A4,
                                 leftMargin=2*cm, rightMargin=2*cm,
                                 topMargin=2*cm, bottomMargin=2*cm)
    styles   = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Iga EdTech — Student Performance Report", styles["Title"]))
    elements.append(Paragraph(f"Teacher: {teacher.full_name}", styles["Normal"]))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}", styles["Normal"]))
    elements.append(Spacer(1, 0.5*cm))

    headers    = ["Student", "Course", "Status", "Score", "Enrolled On"]
    table_data = [headers]

    for e in enrollments:
        best = None
        for a in Assessment.query.filter_by(course_id=e.course_id).all():
            b = _best_submission(e.student_id, a.id)
            if b and (best is None or (b.score or 0) > (best.score or 0)):
                best = b

        score_str  = f"{best.to_dict()['percentage']}%" if best and best.to_dict()["percentage"] is not None else "—"
        status_str = best.to_dict()["status"].title() if best else "Not started"

        table_data.append([
            e.student.full_name, e.course.title, status_str, score_str,
            e.enrolled_at.strftime("%d/%m/%Y") if e.enrolled_at else "—",
        ])

    table = Table(table_data, colWidths=[4.5*cm, 4.5*cm, 3*cm, 2.5*cm, 3*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  colors.HexColor("#2563EB")),
        ("TEXTCOLOR",     (0,0), (-1,0),  colors.white),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0),  10),
        ("BOTTOMPADDING", (0,0), (-1,0),  8),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [colors.white, colors.HexColor("#f0f7ff")]),
        ("FONTSIZE",      (0,1), (-1,-1), 9),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,1), (-1,-1), 6),
        ("BOTTOMPADDING", (0,1), (-1,-1), 6),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    filename = f"iga_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    return send_file(buffer, mimetype="application/pdf",
                     as_attachment=True, download_name=filename)