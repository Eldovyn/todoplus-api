from flask import jsonify, render_template
import datetime
from databases import AccountActiveDatabase, UserDatabase
from utils import TokenAccountActive, send_email
from config import todoplus_url


class AccountActiveController:
    @staticmethod
    async def user_account_active_page(user_id, token):
        if len(user_id.strip()) == 0 or len(token.strip()) == 0:
            return jsonify({"message": "invalid token"}), 404
        if not (user := await AccountActiveDatabase.get("user_id", user_id=user_id)):
            return jsonify({"message": "invalid token"}), 404
        if user.token != token:
            return jsonify({"message": "invalid token"}), 404
        return render_template("verification.html", email=user.user.email)

    @staticmethod
    async def user_account_active(email):
        errors = {}
        if len(email.strip()) == 0:
            errors["email"] = ["email cannot be empty"]
        if errors:
            return (
                jsonify(
                    {
                        "message": "input is not valid",
                        "errors": errors,
                    }
                ),
                400,
            )
        if not (user := await UserDatabase.get("email", email=email)):
            return (
                jsonify({"message": "authorization invalid"}),
                401,
            )
        if user.is_active:
            return (
                jsonify(
                    {
                        "message": "user already active",
                        "data": {
                            "id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "is_active": user.is_active,
                        },
                    }
                ),
                409,
            )
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        expired_at = created_at + 300
        token = await TokenAccountActive.insert(f"{user.id}", int(created_at))
        await AccountActiveDatabase.insert(f"{user.id}", token, int(expired_at))
        await send_email(
            user.email,
            "Account Active",
            f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
</head>
<body>
    <p>Hello {user.username},</p>
    <p>Someone has requested a link to verification your account, and you can do this through the link below.</p>
    <p>
        <a href="http://localhost:5000/todoplus/account-active?token={token}">
            http://localhost:5000/todoplus/account-active?token={token}
        </a>
    </p>
    <p>If you didn't request this, please ignore this email.</p>
</body>
</html>
""",
        )
        return (
            jsonify(
                {
                    "message": "success send email active account",
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "is_active": user.is_active,
                        "token": token,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def user_account_active_verification(token):
        if len(token.strip()) == 0:
            return jsonify({"message": "invalid token"}), 404
        valid_token = await TokenAccountActive.get(token)
        if (
            not valid_token
            or not "user_id" in valid_token
            or not "created_at" in valid_token
        ):
            return jsonify({"message": "invalid token"}), 404
        if not (
            user := await AccountActiveDatabase.get(
                "user_id", user_id=valid_token["user_id"]
            )
        ):
            return jsonify({"message": "user not found"}), 404
        await AccountActiveDatabase.update("user_id", user_id=valid_token["user_id"])
        return render_template(
            "account_verification.html",
            username=user.user.username,
            todoplus_url=todoplus_url,
        )
