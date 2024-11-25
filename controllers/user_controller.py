from databases import UserDatabase
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mongoengine
from flask_jwt_extended import create_access_token
import re


class UserController:
    @staticmethod
    async def update_password(user_id, new_password, confirm_password):
        if (
            len(new_password.strip()) == 0
            or len(confirm_password.strip()) == 0
            or new_password != confirm_password
        ):
            errors = {}
            if len(new_password.strip()) == 0:
                errors["password"] = ["password cannot be empty"]
            if len(confirm_password.strip()) == 0:
                if "confirm_password" in errors:
                    errors["confirm_password"] = ["confirm_password cannot be empty"]
                else:
                    errors["confirm_password"] = ["confirm_password cannot be empty"]
            if new_password != confirm_password:
                if "confirm_password" in errors:
                    errors["confirm_password"].append("confirm password not match")
                else:
                    errors["confirm_password"] = ["confirm password not match"]
            return (
                jsonify(
                    {
                        "message": "input is not valid",
                        "errors": errors,
                    }
                ),
                400,
            )
        if not (user := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization failed"}),
                401,
            )
        new_password = generate_password_hash(new_password)
        await UserDatabase.update(
            "password", user_id=user_id, new_password=new_password
        )
        return (
            jsonify(
                {
                    "message": "success update password",
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "is_active": user.is_active,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def update_user(user_id, username, email):
        if len(username.strip()) == 0 or len(email.strip()) == 0:
            errors = {}
            if len(username.strip()) == 0:
                errors["new_username"] = ["username cannot be empty"]
            if len(email.strip()) == 0:
                errors["new_email"] = ["email cannot be empty"]
            return (
                jsonify(
                    {
                        "message": "input cannot be empty",
                        "errors": errors,
                    }
                ),
                400,
            )
        if not (user := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization failed"}),
                401,
            )
        result = await UserDatabase.update(
            "username_email", user_id=user_id, new_username=username, new_email=email
        )
        data = {
            "id": user.id,
            "username": username,
            "email": email,
            "is_active": user.is_active,
        }
        if result.username != user.username:
            data["new_username"] = username
        if result.email != user.email:
            data["new_email"] = email
        return (
            jsonify(
                {
                    "message": "success update user",
                    "data": data,
                }
            ),
            201,
        )

    @staticmethod
    async def update_user_email(user_id, new_username):
        if len(new_username.strip()) == 0:
            return (
                jsonify(
                    {
                        "message": "input cannot be empty",
                        "errors": {"new_username": ["new username cannot be empty"]},
                    }
                ),
                400,
            )
        if not (user := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization failed"}),
                401,
            )
        await UserDatabase.update(
            "username", user_id=user_id, new_username=new_username
        )
        return (
            jsonify(
                {
                    "message": "success update username",
                    "data": {
                        "new_username": new_username,
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "is_active": user.is_active,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def update_user_email(user_id, new_email):
        if len(new_email.strip()) == 0:
            return (
                jsonify(
                    {
                        "message": "input cannot be empty",
                        "errors": {"new_email": ["new email cannot be empty"]},
                    }
                ),
                400,
            )
        if not (user := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization failed"}),
                401,
            )
        await UserDatabase.update("email", user_id=user_id, new_email=new_email)
        return (
            jsonify(
                {
                    "message": "success update email",
                    "data": {
                        "new_email": new_email,
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "is_active": user.is_active,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def user_me(user_id):
        if not (user := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization failed"}),
                401,
            )
        return (
            jsonify(
                {
                    "message": "success get user",
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "is_active": user.is_active,
                    },
                }
            ),
            200,
        )

    @staticmethod
    async def user_login(email, password):
        if len(email.strip()) == 0 or len(password.strip()) == 0:
            errors = {}
            if len(email.strip()) == 0:
                errors["email"] = "email cannot be empty"
            if len(password.strip()) == 0:
                errors["password"] = "password cannot be empty"
            return jsonify({"message": "input cannot be empty", "errors": errors}), 400
        if not (user := await UserDatabase.get("email", email=email)):
            return jsonify({"message": "failed login", "data": {"email": email}}), 404
        if not check_password_hash(user.password, password):
            return jsonify({"message": "failed login", "data": {"email": email}}), 401
        access_token = create_access_token(identity=user.id)
        return (
            jsonify(
                {
                    "message": "success login",
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "access_token": access_token,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def user_register(email, username, password):
        errors = {}
        if len(email.strip()) == 0:
            if "email" in errors:
                errors["email"].append("email cant be empety")
            else:
                errors["email"] = ["email cant be empety"]
        if len(username.strip()) == 0:
            if "username" in errors:
                errors["username"].append("username cant be empety")
            else:
                errors["username"] = ["username cant be empety"]
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

        if errors:
            return (
                jsonify(
                    {
                        "message": "input invalid",
                        "errors": errors,
                    }
                ),
                400,
            )
        result_password = generate_password_hash(password)
        try:
            user = await UserDatabase.insert(email, username, result_password)
        except mongoengine.errors.NotUniqueError:
            return (
                jsonify(
                    {
                        "message": "username or email already exists",
                        "data": {"username": username, "email": email},
                    },
                ),
                409,
            )
        return (
            jsonify(
                {
                    "message": "success register",
                    "data": {"username": user.username, "email": user.email},
                }
            ),
            201,
        )
