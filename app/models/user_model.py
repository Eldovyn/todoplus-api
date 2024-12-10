import mongoengine as me


class UserModel(me.Document):
    username = me.StringField(required=True, unique=True)
    email = me.StringField(required=True, unique=True)
    password = me.StringField(required=True)
    is_active = me.BooleanField(required=True, default=False)

    meta = {"collection": "users"}
