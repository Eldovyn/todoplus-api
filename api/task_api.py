from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers import TaskController

task_router = Blueprint("task_router", __name__)
task_controllers = TaskController()


@task_router.get("/todoplus/task/page")
@jwt_required()
async def task_page():
    current_user = get_jwt_identity()
    data = request.args
    limit = data.get("limit", "0")
    current_page = data.get("current_page", "1")
    per_page = data.get("per_page", "5")
    return await task_controllers.task_page(current_user, limit, current_page, per_page)


@task_router.post("/todoplus/task")
@jwt_required()
async def create_task():
    current_user = get_jwt_identity()
    data = request.json
    title = data.get("title")
    limit = data.get("limit")
    return await task_controllers.add_task(current_user, title, limit)


@task_router.get("/todoplus/task/<string:category>")
@jwt_required()
async def get_task_by_category(category):
    current_user = get_jwt_identity()
    data = request.args
    limit = data.get("limit", "0")
    title = data.get("title", "")
    task_id = data.get("id", "")
    if category == "all":
        return await task_controllers.get_task_all(current_user, limit)
    if category == "title":
        return await task_controllers.get_task_title(current_user, title, limit)
    if category == "id":
        return await task_controllers.get_task_id(current_user, task_id)
    return jsonify({"message": "endpoint not found"}), 404


@task_router.delete("/todoplus/task/<string:category>")
@jwt_required()
async def delete_task(category):
    current_user = get_jwt_identity()
    body = request.json
    params = request.args
    id = body.get("id")
    limit = body.get("limit")
    per_page = params.get("per_page", "5")
    if category == "id":
        return await task_controllers.delete_task_id(current_user, id, limit, per_page)
    elif category == "all":
        return await task_controllers.delete_task_all(current_user)
    return jsonify({"message": "endpoint not found"}), 404


@task_router.patch("/todoplus/task/<string:category>")
@jwt_required()
async def update_task(category):
    current_user = get_jwt_identity()
    body = request.json
    params = request.args
    id = body.get("id")
    new_title = body.get("new_title")
    limit = body.get("limit")
    status = body.get("status")
    per_page = params.get("per_page", "5")
    if category == "title":
        return await task_controllers.update_title_id(
            current_user, id, new_title, limit, per_page
        )
    if category == "is_completed":
        return await task_controllers.update_is_completed(
            current_user, id, status, limit, per_page
        )
    return jsonify({"message": "endpoint not found"}), 404
