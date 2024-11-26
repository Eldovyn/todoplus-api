from flask import jsonify
from databases import TaskDatabase, UserDatabase
import datetime
import mongoengine


class TaskController:
    @staticmethod
    async def update_is_completed(user_id, id, status, limit):
        if (
            len(id.strip()) == 0
            or not isinstance(status, bool)
            or not isinstance(limit, int)
            or len(user_id.strip()) == 0
        ):
            errors = {}
            if len(id.strip()) == 0:
                errors["id"] = ["id cannot be empty"]
            if not isinstance(status, bool):
                errors["status"] = ["status must be boolean"]
            if not isinstance(limit, int):
                errors["limit"] = ["limit must be an integer"]
            if len(user_id.strip()) == 0:
                errors["user_id"] = ["user id cannot be empty"]
            return (
                jsonify(
                    {
                        "message": "input invalid",
                        "errors": errors,
                    }
                ),
                400,
            )
        if not (user_database := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization failed"}),
                401,
            )
        if not (
            data_task := await TaskDatabase.update(
                "status", task_id=id, user_id=user_id, status=status
            )
        ):
            return (jsonify({"message": "task not found", "data": {"id": id}}), 404)
        if new_task := await TaskDatabase.get("all", user_id=user_id, limit=limit):
            return (
                jsonify(
                    {
                        "message": "success update task",
                        "data": {
                            "id": data_task.id,
                            "title": data_task.title,
                            "created_at": data_task.created_at,
                            "new_status": status,
                            "is_completed": data_task.created_at,
                        },
                        "new_task": [
                            {
                                "title": i.title,
                                "created_at": i.created_at,
                                "id": i.id,
                                "is_completed": i.is_completed,
                            }
                            for i in new_task
                        ],
                    }
                ),
                201,
            )
        return jsonify(
            {
                "message": "success update task",
                "data": {
                    "title": data_task.title,
                    "id": data_task.id,
                    "is_completed": data_task.is_completed,
                    "new_status": status,
                    "created_at": data_task.created_at,
                },
            }
        )

    @staticmethod
    async def update_title_id(user_id, id, new_title, limit):
        if (
            len(id.strip()) == 0
            or len(new_title.strip()) == 0
            or not isinstance(limit, int)
            or len(user_id.strip()) == 0
        ):
            errors = {}
            if len(id.strip()) == 0:
                errors["id"] = ["id cannot be empty"]
            if len(new_title.strip()) == 0:
                errors["new_title"] = ["new title cannot be empty"]
            if not isinstance(limit, int):
                errors["limit"] = ["limit must be an integer"]
            if len(user_id.strip()) == 0:
                errors["user_id"] = ["user id cannot be empty"]
            return (
                jsonify(
                    {
                        "message": "input invalid",
                        "errors": errors,
                    }
                ),
                400,
            )
        if not (user_database := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization failed"}),
                401,
            )
        if not (data_task := await TaskDatabase.get("id", task_id=id, user_id=user_id)):
            return (jsonify({"message": "task not found", "data": {"id": id}}), 404)
        new_data_task = await TaskDatabase.update(
            "id", task_id=id, new_title=new_title, user_id=user_id
        )
        if new_task := await TaskDatabase.get("all", user_id=user_id, limit=limit):
            return (
                jsonify(
                    {
                        "message": "success update task",
                        "data": {
                            "id": data_task.id,
                            "title": data_task.title,
                            "created_at": data_task.created_at,
                            "new_title": new_data_task.title,
                            "is_completed": data_task.created_at,
                        },
                        "new_task": [
                            {
                                "title": i.title,
                                "created_at": i.created_at,
                                "id": i.id,
                                "is_completed": i.is_completed,
                            }
                            for i in new_task
                        ],
                    }
                ),
                201,
            )
        return jsonify(
            {
                "message": "success update task",
                "data": {
                    "title": data_task.title,
                    "new_title": new_data_task.title,
                    "id": data_task.id,
                    "is_completed": data_task.is_completed,
                    "created_at": data_task.created_at,
                },
            }
        )

    @staticmethod
    async def delete_task_all(user_id):
        if len(user_id.strip()) == 0:
            return jsonify(
                {
                    "message": "input invalid",
                    "errors": {"user_id": ["user id cannot be empty"]},
                }
            )
        if not (user_database := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization failed"}),
                401,
            )
        await TaskDatabase.delete("user_id", user_id=user_id)
        return (
            jsonify(
                {
                    "message": "success delete task",
                }
            ),
            201,
        )

    @staticmethod
    async def delete_task_id(user_id, id, limit):
        try:
            if (
                not isinstance(limit, int)
                or len(id.strip()) == 0
                or len(user_id.strip()) == 0
            ):
                errors = {}
                if not isinstance(limit, int):
                    errors["limit"] = ["limit must be an integer"]
                if len(id.strip()) == 0:
                    errors["id"] = ["id cannot be empty"]
                if len(user_id.strip()) == 0:
                    errors["user_id"] = ["user id cannot be empty"]
                return (
                    jsonify(
                        {
                            "message": "input invalid",
                            "errors": errors,
                        }
                    ),
                    400,
                )
            if not (
                user_database := await UserDatabase.get("user_id", user_id=user_id)
            ):
                return jsonify({"message": "authorization failed"}), 401

            if not (
                data_task := await TaskDatabase.get("id", task_id=id, user_id=user_id)
            ):
                return (jsonify({"message": "task not found", "data": {"id": id}}), 404)
            await TaskDatabase.delete("id", task_id=id, user_id=user_id)
            new_task = await TaskDatabase.get("all", user_id=user_id, limit=limit)
            return (
                jsonify(
                    {
                        "message": "success delete task",
                        "data": {
                            "title": data_task.title,
                            "created_at": data_task.created_at,
                            "id": data_task.id,
                            "is_completed": data_task.is_completed,
                        },
                        "new_task": [
                            {
                                "title": i.title,
                                "created_at": i.created_at,
                                "id": i.id,
                                "is_completed": i.is_completed,
                            }
                            for i in new_task
                        ],
                    }
                ),
                201,
            )
        except mongoengine.errors.ValidationError:
            return (
                jsonify(
                    {
                        "message": "task not found",
                        "errors": {"id": id},
                    }
                ),
                404,
            )

    @staticmethod
    async def get_task_id(user_id, task_id):
        if len(user_id.strip()) == 0 or len(task_id.strip()) == 0:
            errors = {}
            if len(user_id.strip()) == 0:
                errors["user_id"] = ["user id cannot be empty"]
            if len(task_id.strip()) == 0:
                errors["id"] = ["id cannot be empty"]
            return jsonify({"message": "input invalid", "errors": errors}), 400
        if not (user_database := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization failed"}),
                401,
            )
        if not (task := await TaskDatabase.get("id", user_id=user_id, task_id=task_id)):
            return (
                jsonify({"message": "task not found", "data": {"id": task_id}}),
                404,
            )
        return (
            jsonify(
                {
                    "message": "success get task",
                    "data": {
                        "id": task.id,
                        "title": task.title,
                        "is_completed": task.is_completed,
                        "created_at": task.created_at,
                    },
                }
            ),
            200,
        )

    @staticmethod
    async def get_task_title(user_id, title, limit):
        if (
            len(user_id.strip()) == 0
            or len(title.strip()) == 0
            or len(limit.strip()) == 0
        ):
            errors = {}
            if len(user_id.strip()) == 0:
                errors["user_id"] = ["user id cannot be empty"]
            if len(title.strip()) == 0:
                errors["title"] = ["title cannot be empty"]
            if len(limit.strip()) == 0 or not limit.isdigit():
                if len(limit.strip()) == 0:
                    if "limit" in errors:
                        errors["limit"].append("limit cannot be empty")
                    if "limit" not in errors:
                        errors["limit"] = []
                        errors["limit"].append("limit cannot be empty")
                if not limit.isdigit():
                    if "limit" in errors:
                        errors["limit"].append("limit must be an integer")
                    if "limit" not in errors:
                        errors["limit"] = []
                        errors["limit"].append("limit must be an integer")
            return jsonify({"message": "input invalid", "errors": errors}), 400
        if not (user_database := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization failed"}),
                401,
            )
        if not limit.isdigit():
            return (
                jsonify(
                    {
                        "message": "limit must be an integer",
                        "data": {"limit": limit},
                        "errors": {"limit": ["limit must be an integer"]},
                    }
                ),
                400,
            )
        limit = int(limit)
        task = await TaskDatabase.get(
            "title", user_id=user_id, title=title, limit=limit
        )
        return (
            jsonify(
                {
                    "message": "success get task",
                    "data": [
                        {
                            "id": i.id,
                            "title": i.title,
                            "is_completed": i.is_completed,
                            "created_at": i.created_at,
                        }
                        for i in task
                    ],
                }
            ),
            200,
        )

    @staticmethod
    async def get_task_all(user_id, limit):
        if not (user_database := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization failed"}),
                401,
            )
        if not limit.isdigit():
            return (
                jsonify(
                    {
                        "message": "limit must be an integer",
                        "data": {"limit": limit},
                        "errors": {"limit": ["limit must be an integer"]},
                    }
                ),
                400,
            )
        limit = int(limit)
        if not (task := await TaskDatabase.get("all", user_id=user_id, limit=limit)):
            return (
                jsonify({"message": "task not found", "data": {"limit": limit}}),
                404,
            )
        return (
            jsonify(
                {
                    "message": "success get task",
                    "data": [
                        {
                            "id": i.id,
                            "title": i.title,
                            "is_completed": i.is_completed,
                            "created_at": i.created_at,
                        }
                        for i in task
                    ],
                }
            ),
            200,
        )

    @staticmethod
    async def add_task(user_id, title, limit):
        if len(title.strip()) == 0 or not isinstance(limit, int):
            errors = {}
            if len(title.strip()) == 0:
                errors["title"] = ["title cannot be empty"]
            if not isinstance(limit, int):
                errors["limit"] = ["limit must be an integer"]
            return (
                jsonify(
                    {
                        "message": "input invalid",
                        "errors": errors,
                    }
                ),
                400,
            )
        if not (user_database := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization failed"}),
                401,
            )
        task = await TaskDatabase.insert(
            user_database.username,
            title,
            int(datetime.datetime.now(datetime.timezone.utc).timestamp()),
        )
        if new_task := await TaskDatabase.get("all", user_id=user_id, limit=limit):
            return (
                jsonify(
                    {
                        "message": "success create task",
                        "data": {
                            "title": task.title,
                            "id": task.id,
                            "is_completed": task.is_completed,
                            "created_at": task.created_at,
                        },
                        "new_task": [
                            {
                                "id": i.id,
                                "title": i.title,
                                "is_completed": i.is_completed,
                                "created_at": i.created_at,
                            }
                            for i in new_task
                        ],
                    }
                ),
                201,
            )
        return (
            jsonify(
                {
                    "message": "success create task",
                    "data": {
                        "title": task.title,
                        "id": task.id,
                        "is_completed": task.is_completed,
                        "created_at": task.created_at,
                    },
                }
            ),
            201,
        )
