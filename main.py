from flask import Flask
from config import mongodb, mongodb_url, secret_key
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from celery import Celery, Task
from celery.schedules import crontab
from api.register_api import register_router
from api.login_api import login_router
from api.task_api import task_router
from api.me_api import me_router
from api.update_profile_api import update_profile_router
from api.reset_password_api import reset_password_router
import smtplib
from email.mime.text import MIMEText
from models import ResetPasswordModel
import datetime


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {
    "db": mongodb,
    "host": mongodb_url,
}
app.config["JWT_SECRET_KEY"] = secret_key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/0",
        task_ignore_result=True,
    ),
)

db = MongoEngine()
db.init_app(app)
jwt = JWTManager(app)
celery_app = celery_init_app(app)


@celery_app.task
def periode_task():
    expired_at = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    if data := ResetPasswordModel.objects().all():
        for item in data:
            if item.expired_at <= expired_at:
                item.delete()
    return "Task executed"


celery_app.conf.beat_schedule = {
    "run-every-5-minutes": {
        "task": "main.periode_task",
        "schedule": crontab(minute="*/5"),
    },
}


@app.after_request
async def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = (
        "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    )
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


# JWT Callback
@jwt.invalid_token_loader
def invalid_token_callback(error_message):
    return {"message": "authorization failed"}, 401


# Register Blueprints
app.register_blueprint(register_router)
app.register_blueprint(login_router)
app.register_blueprint(task_router)
app.register_blueprint(me_router)
app.register_blueprint(update_profile_router)
app.register_blueprint(reset_password_router)
