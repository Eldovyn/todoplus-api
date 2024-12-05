import mongoengine as me
from .user_model import UserModel


class TaskModel(me.Document):
    user = me.ReferenceField(UserModel, required=True, reverse_delete_rule=me.CASCADE)
    title = me.StringField(required=True)
    is_completed = me.BooleanField(required=True, default=False)
    created_at = me.IntField(required=True)

    meta = {"collection": "tasks"}
