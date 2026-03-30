
from marshmallow import Schema, fields, validate

FILE_TYPES = ["video", "pdf", "slides", "document", "image"]


class CourseSchema(Schema):
    title              = fields.Str(required=True, validate=validate.Length(min=2, max=200))
    description        = fields.Str(load_default=None)
    guidelines         = fields.Str(load_default=None)
    is_published       = fields.Bool(load_default=False)
    module_title       = fields.Str(load_default=None)
    module_description = fields.Str(load_default=None)
    lesson_title       = fields.Str(load_default=None)
    file_type          = fields.Str(load_default="video", validate=validate.OneOf(FILE_TYPES))
    file_url           = fields.Str(load_default=None, validate=validate.Length(max=500))


class ModuleSchema(Schema):
    title       = fields.Str(required=True, validate=validate.Length(min=2, max=200))
    description = fields.Str(load_default=None)


class LessonSchema(Schema):
    title     = fields.Str(required=True, validate=validate.Length(min=2, max=200))
    file_type = fields.Str(load_default="video", validate=validate.OneOf(FILE_TYPES))
    file_url  = fields.Str(load_default=None, validate=validate.Length(max=500))


class EnrollSchema(Schema):
    course_id = fields.Int(required=True)


class QuestionSchema(Schema):
    question_type  = fields.Str(required=True,
                                validate=validate.OneOf(["mcq", "true_false", "short_answer"]))
    text           = fields.Str(required=True, validate=validate.Length(min=1))
    options        = fields.List(fields.Str(), load_default=[])
    correct_answer = fields.Raw(load_default=None)
    allow_multiple = fields.Bool(load_default=False)
    points         = fields.Int(load_default=1, validate=validate.Range(min=1))


class AssessmentSchema(Schema):
    title        = fields.Str(required=True, validate=validate.Length(min=2, max=200))
    description  = fields.Str(load_default=None)
    time_limit   = fields.Int(load_default=None, validate=validate.Range(min=1))
    max_attempts = fields.Int(load_default=1, validate=validate.Range(min=1, max=10))
    is_published = fields.Bool(load_default=False)
    questions    = fields.List(fields.Nested(QuestionSchema), load_default=[])


class SubmissionSchema(Schema):
    answers = fields.Dict(keys=fields.Str(), values=fields.Raw(), required=True)


class GradeItemSchema(Schema):
    score   = fields.Float(required=True, validate=validate.Range(min=0))
    comment = fields.Str(load_default="")


class GradeShortAnswerSchema(Schema):
   
    grades = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(GradeItemSchema),
        required=True
    )