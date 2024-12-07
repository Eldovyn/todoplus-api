from .database import Database
from models import UserModel


class UserDatabase(Database):
    @staticmethod
    async def insert(email, username, password):
        user = UserModel(email=email, username=username, password=password)
        user.save()
        return user

    @staticmethod
    async def get(category, **kwargs):
        email = kwargs.get("email")
        user_id = kwargs.get("user_id")
        if category == "email":
            return UserModel.objects(email=email).first()
        if category == "user_id":
            return UserModel.objects(id=user_id).first()

    @staticmethod
    async def delete():
        pass

    @staticmethod
    async def update(category, **kwargs):
        user_id = kwargs.get("user_id")
        new_email = kwargs.get("new_email")
        new_username = kwargs.get("new_username")
        new_password = kwargs.get("new_password")
        if user := UserModel.objects(id=user_id).first():
            if category == "email":
                user.email = new_email
                user.save()
                return user
            if category == "username":
                user.username = new_username
                user.save()
                return user
            if category == "username_email":
                user.email = new_email
                user.username = new_username
                user.save()
                return user
            if category == "password":
                user.password = new_password
                user.save()
                return user
