import mongoengine as me
from .user_model import UserModel


class TaskModel(me.Document):
    user = me.ReferenceField(UserModel, required=True)
    title = me.StringField(required=True)
    is_completed = me.BooleanField(required=True, default=False)

    meta = {"collection": "api_key"}
