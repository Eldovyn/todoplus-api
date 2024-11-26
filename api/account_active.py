from flask import Blueprint, request
from controllers import AccountActiveController

account_active_router = Blueprint("account_active_router", __name__)
account_active_controller = AccountActiveController()


@account_active_router.post("/todoplus/account-active")
async def account_active_email():
    data = request.json
    email = data.get("email", "")
    return await account_active_controller.user_account_active(email)


@account_active_router.get("/todoplus/account-active")
async def account_active_email_verification():
    data = request.args
    token = data.get("token", "")
    return await account_active_controller.user_account_active_verification(token)


@account_active_router.get("/todoplus/account-active/verification")
async def account_active_page():
    data = request.args
    user_id = data.get("user_id", "")
    token = data.get("token", "")
    return await account_active_controller.user_account_active_page(user_id, token)
