from flask import Blueprint, request, jsonify, render_template, redirect
from werkzeug.security import generate_password_hash
from controllers import ResetPasswordController
from utils import TokenResetPassword
from databases import UserDatabase, ResetPasswordDatabase
import datetime
from config import todoplus_url
import re

reset_password_router = Blueprint("reset_password_router", __name__)
reset_password_controller = ResetPasswordController()


@reset_password_router.post("/todoplus/reset-password")
async def user_reset_password():
    data = request.json
    email = data.get("email")
    return await reset_password_controller.user_reset_password(email)


@reset_password_router.route(
    "/todoplus/reset-password/<string:token>", methods=["GET", "POST"]
)
async def link_reset_password(token):
    return await reset_password_controller.user_reset_password_page(token)
