from .database import Database
from models import AccountActiveModel, UserModel
import datetime
from utils import DataNotFoundError, TokenAccountActiveEmail, TokenAccountActiveWeb


class AccountActiveDatabase(Database):
    @staticmethod
    async def insert(user_id, email_token, web_token, expired_at):
        if user_data := UserModel.objects(id=user_id).first():
            if token_data := AccountActiveModel.objects(user=user_data).first():
                created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
                expired_at = created_at + 300
                email_token = await TokenAccountActiveEmail.insert(
                    f"{user_data.id}", int(created_at)
                )
                web_token = await TokenAccountActiveWeb.insert(
                    f"{user_data.id}", int(created_at)
                )
                token_data.expired_at = expired_at
                token_data.web_token = f"{web_token}"
                token_data.email_token = f"{email_token}"
                token_data.save()
                return token_data
            reset_password = AccountActiveModel(
                user=user_data,
                email_token=email_token,
                web_token=web_token,
                expired_at=expired_at,
            )
            reset_password.save()
            return reset_password
        raise DataNotFoundError("user not found")

    @staticmethod
    async def get(category, **kwargs):
        user_id = kwargs.get("user_id")
        web_token = kwargs.get("web_token")
        email_token = kwargs.get("email_token")
        if category == "account_active":
            if user_data := UserModel.objects(id=user_id).first():
                return AccountActiveModel.objects(
                    user=user_data, web_token=web_token
                ).first()
        if category == "account_active_email":
            if user_data := UserModel.objects(id=user_id).first():
                return AccountActiveModel.objects(
                    user=user_data, email_token=email_token
                ).first()

    @staticmethod
    async def delete(category, **kwargs):
        user_id = kwargs.get("user_id")
        if category == "user_id":
            if user_data := UserModel.objects(id=user_id).first():
                return AccountActiveModel.objects(user=user_data).delete()

    @staticmethod
    async def update(category, **kwargs):
        user_id = kwargs.get("user_id")
        if category == "user_id":
            if user_data := UserModel.objects(id=user_id).first():
                if token_data := AccountActiveModel.objects(user=user_data).first():
                    user_data.is_active = True
                    user_data.save()
                    token_data.delete()
                    return user_data
