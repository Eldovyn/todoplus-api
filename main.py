from flask import Flask
from config import mongodb, mongodb_url, secret_key
from flask_mongoengine import MongoEngine
from api.register_api import register_router
from api.login_api import login_router
from api.task_api import task_router
from api.me_api import me_router
from api.update_profile_api import update_profile_router
from flask_jwt_extended import JWTManager

db = MongoEngine()
app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = {
    "db": mongodb,
    "host": mongodb_url,
}
app.config["JWT_SECRET_KEY"] = secret_key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

db.init_app(app)
jwt = JWTManager(app)


@app.after_request
async def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = (
        "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    )
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


@jwt.invalid_token_loader
def invalid_token_callback(error_message):
    return {"message": "authorization failed"}, 401


app.register_blueprint(register_router)
app.register_blueprint(login_router)
app.register_blueprint(task_router)
app.register_blueprint(me_router)
app.register_blueprint(update_profile_router)
