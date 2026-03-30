
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def role_required(*roles):
    
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role")
            if user_role not in roles:
                return jsonify({
                    "success": False,
                    "message": "You do not have permission to access this resource.",
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def student_required(fn):
   
    return role_required("student", "admin")(fn)


def teacher_required(fn):
   
    return role_required("teacher", "admin")(fn)


def admin_required(fn):
    
    return role_required("admin")(fn)
