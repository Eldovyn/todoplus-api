import mongoengine as me
from .user_model import UserModel


class ResetPasswordModel(me.Document):
    user = me.ReferenceField(UserModel, required=True, reverse_delete_rule=me.CASCADE)
    token = me.StringField(required=True, unique=True)
    expired_at = me.IntField(required=True)

    meta = {"collection": "reset_password"}
