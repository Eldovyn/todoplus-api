import mongoengine as me
from .user_model import UserModel


class AvatarModel(me.Document):
    user = me.ReferenceField(
        UserModel, required=True, reverse_delete_rule=me.CASCADE, unique=True
    )
    avatar = me.BinaryField(required=True)

    meta = {"collection": "user_avatar"}
