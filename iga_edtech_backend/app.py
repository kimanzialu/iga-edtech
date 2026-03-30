
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS

from config import get_config
from models import db
from models.user import TokenBlacklist

mail = Mail()
jwt = JWTManager()


def create_app(config_class=None):
    app = Flask(__name__)

   
    cfg = config_class or get_config()
    app.config.from_object(cfg)

    app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

    CORS(app, origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "null",  
    ], supports_credentials=True)

   
    db.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

  
    from auth import bcrypt
    bcrypt.init_app(app)


    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload.get("jti")
        return db.session.query(
            TokenBlacklist.query.filter_by(jti=jti).exists()
        ).scalar()

    @jwt.revoked_token_loader
    def revoked_token_response(jwt_header, jwt_payload):
        return jsonify({"success": False, "message": "Token has been revoked."}), 401

    @jwt.expired_token_loader
    def expired_token_response(jwt_header, jwt_payload):
        return jsonify({"success": False, "message": "Token has expired."}), 401

    @jwt.invalid_token_loader
    def invalid_token_response(msg):
        return jsonify({"success": False, "message": "Invalid token."}), 422

    @jwt.unauthorized_loader
    def missing_token_response(msg):
        return jsonify({"success": False, "message": "Authentication required."}), 401


    from auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from courses.routes import courses_bp
    app.register_blueprint(courses_bp)

   
    with app.app_context():
        db.create_all()

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "app": "Iga EdTech LMS"})

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, host="0.0.0.0", port=5000)