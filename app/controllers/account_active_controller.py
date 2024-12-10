from flask import jsonify, render_template, redirect
import datetime
from ..databases import AccountActiveDatabase, UserDatabase
from ..utils import TokenAccountActiveEmail, TokenAccountActiveWeb
from ..config import todoplus_url


class AccountActiveController:
    @staticmethod
    async def user_account_active_page(user_id, token):
        if len(user_id.strip()) == 0 or len(token.strip()) == 0:
            return jsonify({"message": "invalid token"}), 404
        if not (
            user := await AccountActiveDatabase.get(
                "account_active", user_id=user_id, web_token=token
            )
        ):
            return redirect(todoplus_url)
        if user.web_token != token:
            return redirect(todoplus_url)
        return render_template(
            "account_active/verification.html", email=user.user.email
        )

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
        email_token = await TokenAccountActiveEmail.insert(
            f"{user.id}", int(created_at)
        )
        web_token = await TokenAccountActiveWeb.insert(f"{user.id}", int(created_at))
        await AccountActiveDatabase.insert(
            f"{user.id}", email_token, web_token, int(expired_at)
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
                        "token": web_token,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def user_account_active_verification(token):
        if len(token.strip()) == 0:
            return jsonify({"message": "invalid token"}), 404
        valid_token = await TokenAccountActiveEmail.get(token)
        if (
            not valid_token
            or not "user_id" in valid_token
            or not "created_at" in valid_token
        ):
            return jsonify({"message": "invalid token"}), 404
        if not (
            user := await AccountActiveDatabase.get(
                "account_active_email",
                user_id=valid_token["user_id"],
                email_token=token,
            )
        ):
            return redirect(todoplus_url)
        await AccountActiveDatabase.update("user_id", user_id=valid_token["user_id"])
        return render_template(
            "account_active/account_verification.html",
            username=user.user.username,
            todoplus_url=todoplus_url,
        )
