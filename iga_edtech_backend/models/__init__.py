from .base import db
from .user import User, StudentProfile, TeacherProfile, OTPCode, TokenBlacklist
from .course import Course, Module, Lesson, Enrollment, Assessment, Question, Submission, LessonCompletion

__all__ = [
    "db",
    "User", "StudentProfile", "TeacherProfile", "OTPCode", "TokenBlacklist",
    "Course", "Module", "Lesson", "Enrollment", "Assessment", "Question", "Submission", "LessonCompletion",
]