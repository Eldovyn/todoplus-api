from flask import Blueprint, request, Response
from ..models import UserModel

image_router = Blueprint("image_router", __name__)


@image_router.get("/todoplus/avatar")
async def get_avatar():
    data = request.args
    username = data.get("username", "")
    if data := UserModel.objects(username=username).first():
        return Response(data.avatar, mimetype="image/jpeg")
