from flask import Blueprint, request
from ..controllers import UserController

register_router = Blueprint("register_router", __name__)
user_controller = UserController()


@register_router.post("/todoplus/register")
async def user_register():
    data = request.json
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    return await UserController().user_register(email, username, password)
