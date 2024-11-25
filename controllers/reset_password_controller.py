from databases import ResetPasswordDatabase, UserDatabase
from flask import jsonify, url_for
import datetime
from utils import TokenResetPassword
from utils import send_email


class ResetPasswordController:
    @staticmethod
    async def user_reset_password(email):
        if len(email.strip()) == 0:
            return (
                jsonify(
                    {
                        "message": "input invalid",
                        "errors": {"email": ["email cannot be empty"]},
                    }
                ),
                400,
            )
        if not (user := await UserDatabase.get("email", email=email)):
            return (
                jsonify({"message": "email not found"}),
                404,
            )
        created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        expired_at = created_at + 300
        token = await TokenResetPassword.insert(f"{user.id}", int(created_at))
        if not (
            user_token := await ResetPasswordDatabase.insert(
                user.id, token, int(expired_at)
            )
        ):
            return (
                jsonify({"message": "email not found"}),
                404,
            )
        send_email(
            email,
            "Reset Password TodoPlus",
            f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
</head>
<body>
    <p>Hello {user.username},</p>
    <p>Someone has requested a link to change your password, and you can do this through the link below.</p>
    <p>
        <a href="http://localhost:5000{url_for('reset_password_router.link_reset_password', token=token)}">
            http://localhost:5000{url_for('reset_password_router.link_reset_password', token=token)}
        </a>
    </p>
    <p>If you didn't request this, please ignore this email.</p>
    <p>Your password won't change until you access the link above and create a new one.</p>
</body>
</html>
""",
        )
        return (
            jsonify(
                {
                    "message": "success send reset password",
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
