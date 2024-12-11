from flask import Blueprint, request
from ..controllers import ImageController

image_router = Blueprint("image_router", __name__)


@image_router.get("/todoplus/avatar")
async def get_avatar():
    data = request.args
    user_id = data.get("user_id", "")
    return await ImageController.get_avatar(user_id)
