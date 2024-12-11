import mongoengine as me
from .user_model import UserModel


class ApiKeyModel(me.Document):
    user = me.ReferenceField(
        UserModel, required=True, reverse_delete_rule=me.CASCADE, unique=True
    )
    api_key = me.StringField(required=True, unique=True)

    meta = {"collection": "api_key"}
