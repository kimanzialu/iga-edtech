from datetime import datetime, timezone
from .base import db


class Course(db.Model):
    __tablename__ = "courses"

    id           = db.Column(db.Integer, primary_key=True)
    teacher_id   = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title        = db.Column(db.String(200), nullable=False)
    description  = db.Column(db.Text, nullable=True)
    guidelines   = db.Column(db.Text, nullable=True)
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    created_at   = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at   = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                             onupdate=lambda: datetime.now(timezone.utc))

    teacher     = db.relationship("User", foreign_keys=[teacher_id])
    modules     = db.relationship("Module", back_populates="course",
                                  cascade="all, delete-orphan", order_by="Module.order")
    enrollments = db.relationship("Enrollment", back_populates="course",
                                  cascade="all, delete-orphan")
    assessments = db.relationship("Assessment", back_populates="course",
                                  cascade="all, delete-orphan")

    def to_dict(self, include_modules=False):
        data = {
            "id":           self.id,
            "teacher_id":   self.teacher_id,
            "teacher_name": self.teacher.full_name if self.teacher else None,
            "title":        self.title,
            "description":  self.description,
            "guidelines":   self.guidelines,
            "is_published": self.is_published,
            "module_count": len(self.modules),
            "created_at":   self.created_at.isoformat() if self.created_at else None,
        }
        if include_modules:
            data["modules"] = [m.to_dict(include_lessons=True) for m in self.modules]
        return data


class Module(db.Model):
    __tablename__ = "modules"

    id          = db.Column(db.Integer, primary_key=True)
    course_id   = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    order       = db.Column(db.Integer, default=1)
    created_at  = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    course  = db.relationship("Course", back_populates="modules")
    lessons = db.relationship("Lesson", back_populates="module",
                              cascade="all, delete-orphan", order_by="Lesson.order")

    def to_dict(self, include_lessons=False):
        data = {
            "id":          self.id,
            "course_id":   self.course_id,
            "title":       self.title,
            "description": self.description,
            "order":       self.order,
        }
        if include_lessons:
            data["lessons"] = [l.to_dict() for l in self.lessons]
        return data


class Lesson(db.Model):
    __tablename__ = "lessons"

    id         = db.Column(db.Integer, primary_key=True)
    module_id  = db.Column(db.Integer, db.ForeignKey("modules.id"), nullable=False)
    title      = db.Column(db.String(200), nullable=False)
   
    file_type  = db.Column(db.String(20), nullable=True, default="video")
    file_url   = db.Column(db.String(500), nullable=True)
    order      = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    module = db.relationship("Module", back_populates="lessons")

    def to_dict(self):
        return {
            "id":        self.id,
            "module_id": self.module_id,
            "title":     self.title,
            "file_type": self.file_type,
            "file_url":  self.file_url,
            "order":     self.order,
        }


class Enrollment(db.Model):
    __tablename__ = "enrollments"
    __table_args__ = (db.UniqueConstraint("student_id", "course_id"),)

    id          = db.Column(db.Integer, primary_key=True)
    student_id  = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    course_id   = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    enrolled_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    student = db.relationship("User", foreign_keys=[student_id])
    course  = db.relationship("Course", back_populates="enrollments")

    def to_dict(self):
        return {
            "id":           self.id,
            "student_id":   self.student_id,
            "course_id":    self.course_id,
            "course_title": self.course.title if self.course else None,
            "enrolled_at":  self.enrolled_at.isoformat() if self.enrolled_at else None,
        }


class Assessment(db.Model):
    __tablename__ = "assessments"

    id           = db.Column(db.Integer, primary_key=True)
    course_id    = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    teacher_id   = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title        = db.Column(db.String(200), nullable=False)
    description  = db.Column(db.Text, nullable=True)
    time_limit   = db.Column(db.Integer, nullable=True)
    max_attempts = db.Column(db.Integer, default=1)
    is_published = db.Column(db.Boolean, default=False)
    created_at   = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    course      = db.relationship("Course", back_populates="assessments")
    teacher     = db.relationship("User", foreign_keys=[teacher_id])
    questions   = db.relationship("Question", back_populates="assessment",
                                  cascade="all, delete-orphan", order_by="Question.order")
    submissions = db.relationship("Submission", back_populates="assessment",
                                  cascade="all, delete-orphan")

    def to_dict(self, include_questions=False):
        data = {
            "id":             self.id,
            "course_id":      self.course_id,
            "course_title":   self.course.title if self.course else None,
            "teacher_id":     self.teacher_id,
            "title":          self.title,
            "description":    self.description,
            "time_limit":     self.time_limit,
            "max_attempts":   self.max_attempts,
            "is_published":   self.is_published,
            "question_count": len(self.questions),
            "created_at":     self.created_at.isoformat() if self.created_at else None,
        }
        if include_questions:
            data["questions"] = [q.to_dict() for q in self.questions]
        return data


class Question(db.Model):
    __tablename__ = "questions"

    id             = db.Column(db.Integer, primary_key=True)
    assessment_id  = db.Column(db.Integer, db.ForeignKey("assessments.id"), nullable=False)
    question_type  = db.Column(db.String(20), nullable=False, default="mcq")
    text           = db.Column(db.Text, nullable=False)
    options        = db.Column(db.Text, nullable=True)
    
    correct_answer = db.Column(db.Text, nullable=True)
    allow_multiple = db.Column(db.Boolean, default=False, nullable=False)
    order          = db.Column(db.Integer, default=1)
    points         = db.Column(db.Integer, default=1)

    assessment = db.relationship("Assessment", back_populates="questions")

    def to_dict(self, include_answer=False):
        import json
        try:
            correct = json.loads(self.correct_answer) if self.correct_answer else []
        except Exception:
            correct = [self.correct_answer] if self.correct_answer else []

        data = {
            "id":             self.id,
            "assessment_id":  self.assessment_id,
            "question_type":  self.question_type,
            "text":           self.text,
            "options":        json.loads(self.options) if self.options else [],
            "allow_multiple": self.allow_multiple,
            "order":          self.order,
            "points":         self.points,
        }
        if include_answer:
            data["correct_answer"] = correct
        return data


class LessonCompletion(db.Model):
 
    __tablename__ = "lesson_completions"
    __table_args__ = (db.UniqueConstraint("student_id", "lesson_id"),)

    id         = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    lesson_id  = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False)
    completed_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    student = db.relationship("User", foreign_keys=[student_id])
    lesson  = db.relationship("Lesson", foreign_keys=[lesson_id])

    def to_dict(self):
        return {
            "lesson_id":    self.lesson_id,
            "student_id":   self.student_id,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


class Submission(db.Model):
    __tablename__ = "submissions"

    id              = db.Column(db.Integer, primary_key=True)
    assessment_id   = db.Column(db.Integer, db.ForeignKey("assessments.id"), nullable=False)
    student_id      = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    answers         = db.Column(db.Text, nullable=False, default="{}")
    score           = db.Column(db.Float, nullable=True)
    max_score       = db.Column(db.Float, nullable=True)
  
    manual_scores   = db.Column(db.Text, nullable=True, default="{}")

    manual_comments = db.Column(db.Text, nullable=True, default="{}")
    attempt_number  = db.Column(db.Integer, default=1)
    submitted_at    = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    graded_at       = db.Column(db.DateTime(timezone=True), nullable=True)

    assessment = db.relationship("Assessment", back_populates="submissions")
    student    = db.relationship("User", foreign_keys=[student_id])

    def to_dict(self):
        import json
        pct = round((self.score / self.max_score) * 100, 1) if self.score is not None and self.max_score else None
        return {
            "id":               self.id,
            "assessment_id":    self.assessment_id,
            "assessment_title": self.assessment.title if self.assessment else None,
            "course_title":     self.assessment.course.title if self.assessment and self.assessment.course else None,
            "student_id":       self.student_id,
            "student_name":     self.student.full_name if self.student else None,
            "score":            self.score,
            "max_score":        self.max_score,
            "percentage":       pct,
            "attempt_number":   self.attempt_number,
            "submitted_at":     self.submitted_at.isoformat() if self.submitted_at else None,
            "graded_at":        self.graded_at.isoformat() if self.graded_at else None,
            "status":           "graded" if self.graded_at else "pending_review",
            "manual_scores":    self.manual_scores,
            "manual_comments":  self.manual_comments,
        }