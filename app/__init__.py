from flask import Flask
from flask_mail import Mail
from flask_mongoengine import MongoEngine
from .config import *
from flask_jwt_extended import JWTManager
from .models import UserModel
from .celery_app import celery_init_app
from .models import ResetPasswordModel, UserModel, AccountActiveModel
from celery.schedules import crontab
import datetime

mail = Mail()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config["MONGODB_SETTINGS"] = {
        "db": mongodb,
        "host": mongodb_url,
        "alias": "default",
    }
    app.config.from_mapping(
        CELERY=dict(
            broker_url=broker_url,
            result_backend=result_backend,
            task_ignore_result=True,
        ),
    )
    app.config.from_prefixed_env()
    app.config["JWT_SECRET_KEY"] = secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
    app.config["MAIL_SERVER"] = smtp_host
    app.config["MAIL_PORT"] = smtp_port
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_USERNAME"] = smtp_username
    app.config["MAIL_PASSWORD"] = smtp_password
    app.config["MAIL_DEFAULT_SENDER"] = smtp_email

    db = MongoEngine()
    db.init_app(app)
    jwt = JWTManager(app)
    celery_app = celery_init_app(app)

    @celery_app.task(name="periode_task")
    def periode_task():
        expired_at = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        if data := ResetPasswordModel.objects().all():
            for item1 in data:
                if item1.expired_at <= expired_at:
                    item1.delete()
        if data := AccountActiveModel.objects().all():
            for item2 in data:
                if item2.expired_at <= expired_at:
                    item2.delete()
        return f"Task executed at {int(datetime.datetime.now(datetime.timezone.utc).timestamp())}"

    celery_app.conf.beat_schedule = {
        "run-every-5-minutes": {
            "task": "periode_task",
            "schedule": crontab(minute="*/5"),
        },
    }

    with app.app_context():
        from .api.register_api import register_router
        from .api.login_api import login_router
        from .api.task_api import task_router
        from .api.me_api import me_router
        from .api.update_profile_api import update_profile_router
        from .api.reset_password_api import reset_password_router
        from .api.account_active import account_active_router

        app.register_blueprint(register_router)
        app.register_blueprint(login_router)
        app.register_blueprint(task_router)
        app.register_blueprint(me_router)
        app.register_blueprint(update_profile_router)
        app.register_blueprint(reset_password_router)
        app.register_blueprint(account_active_router)

    @app.after_request
    async def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        )
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return UserModel.objects(id=identity, is_active=True).first()

    @jwt.invalid_token_loader
    def invalid_token_callback(error_message):
        return {"message": "authorization invalid"}, 401

    @jwt.user_lookup_error_loader
    def missing_token_callback(jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return {
            "message": "user account is inactive",
            "data": {"user_id": identity},
        }, 403

    return app
