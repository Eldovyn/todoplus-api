from flask import Blueprint, request, jsonify, render_template, redirect
from werkzeug.security import generate_password_hash
from controllers import ResetPasswordController
from utils import TokenResetPassword
from databases import UserDatabase, ResetPasswordDatabase
import datetime
from config import todoplus_url
import re

reset_password_router = Blueprint("reset_password_router", __name__)
reset_password_controller = ResetPasswordController()


@reset_password_router.post("/todoplus/reset-password")
async def user_reset_password():
    data = request.json
    email = data.get("email")
    return await reset_password_controller.user_reset_password(email)


@reset_password_router.route(
    "/todoplus/reset-password/<string:token>", methods=["GET", "POST"]
)
async def link_reset_password(token):
    valid_token = await TokenResetPassword.get(token)
    created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
    if request.method == "GET":
        if not valid_token or not "user_id" in valid_token:
            return jsonify({"message": "invalid token"}), 400
        if not (
            user := await ResetPasswordDatabase.get(
                "user_id", user_id=valid_token["user_id"]
            )
        ):
            return jsonify({"message": "user not found"}), 404
        else:
            if user.expired_at <= created_at:
                await ResetPasswordDatabase.delete(
                    "user_id", user_id=valid_token["user_id"]
                )
                return jsonify({"message": "token expired"}), 400
        return render_template("reset_password.html")
    if request.method == "POST":
        data = request.form
        password = data.get("password")

        errors = {}
        if len(password.strip()) == 0:
            if "password" in errors:
                errors["password"].append("password cant be empety")
            else:
                errors["password"] = ["password cant be empety"]
        if len(password) < 8:
            if "password" in errors:
                errors["password"].append("minimum 8 characters")
            else:
                errors["password"] = ["minimum 8 characters"]
        if not re.search("[a-z]", password):
            if "password" in errors:
                errors["password"].append("password must contain lowercase")
            else:
                errors["password"] = ["password must contain lowercase"]
        if not re.search("[A-Z]", password):
            if "password" in errors:
                errors["password"].append("password must contain uppercase")
            else:
                errors["password"] = ["password must contain uppercase"]
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            if "password" in errors:
                errors["password"].append("password contains special character(s)")
            else:
                errors["password"] = ["password contains special character(s)"]
        if not errors:
            password = generate_password_hash(password)
            await UserDatabase.update(
                "password", new_password=password, user_id=valid_token["user_id"]
            )
            await ResetPasswordDatabase.delete(
                "user_id", user_id=valid_token["user_id"]
            )
            return redirect(todoplus_url)
        return render_template(
            "reset_password.html",
            errors=errors["password"],
            error_length=len(errors["password"]),
            password=password,
        )
