from flask import jsonify
from databases import TaskDatabase, UserDatabase
import datetime
import mongoengine


class TaskController:
    @staticmethod
    async def task_page(user_id, limit, current_page, per_page):
        errors = {}
        if len(user_id.strip()) == 0:
            errors["user_id"] = ["user id cannot be empty"]
        if len(limit.strip()) == 0 or not limit.isdigit():
            errors["limit"] = ["limit must be an integer"]
        if len(current_page.strip()) == 0 or not current_page.isdigit():
            errors["current_page"] = ["current page must be an integer"]
        if len(per_page.strip()) == 0 or not per_page.isdigit():
            errors["per_page"] = ["per page must be an integer"]
        if limit.isdigit():
            try:
                limit = int(limit)
            except ValueError:
                if "limit" in errors:
                    errors["limit"].append("limit must be an integer")
                else:
                    errors["limit"] = ["limit must be an integer"]
            else:
                if limit < 0:
                    if "limit" in errors:
                        errors["limit"].append("limit must be greater than 0")
                    else:
                        errors["limit"] = ["limit must be greater than 0"]
        if current_page.isdigit():
            try:
                current_page = int(current_page)
            except ValueError:
                if "current_page" in errors:
                    errors["current_page"].append("current page must be an integer")
                else:
                    errors["current_page"] = ["current page must be an integer"]
            else:
                if current_page < 0:
                    if "current_page" in errors:
                        errors["current_page"].append(
                            "current page must be greater than 0"
                        )
                    else:
                        errors["current_page"] = ["current page must be greater than 0"]
        if per_page.isdigit():
            try:
                per_page = int(per_page)
            except ValueError:
                if "per_page" in errors:
                    errors["per_page"].append("per page must be an integer")
                else:
                    errors["per_page"] = ["per page must be an integer"]
            else:
                if per_page <= 0:
                    if "per_page" in errors:
                        errors["per_page"].append("per page must be greater than 0")
                    else:
                        errors["per_page"] = ["per page must be greater than 0"]
        if errors:
            return jsonify({"message": "input invalid", "errors": errors}), 400
        if not (user_database := await UserDatabase.get("user_id", user_id=user_id)):
            return jsonify({"message": "authorization invalid"}), 401
        if not (
            data_task := await TaskDatabase.get(
                "all",
                user_id=user_id,
                limit=limit,
            )
        ):
            return jsonify({"message": "task not found"}), 404
        data_task = [
            {
                "task_id": task.id,
                "title": task.title,
                "is_completed": task.is_completed,
                "created_at": task.created_at,
            }
            for task in data_task
        ]
        paginated_data = [
            data_task[i : i + per_page] for i in range(0, len(data_task), per_page)
        ]
        return (
            jsonify(
                {
                    "message": "success get task",
                    "data": {
                        "user_id": user_id,
                    },
                    "page": {
                        "total_page": len(paginated_data),
                        "tasks": paginated_data,
                        "size": len(data_task),
                        "current_page": current_page,
                        "limit": limit,
                        "per_page": per_page,
                    },
                }
            ),
            200,
        )

    @staticmethod
    async def update_is_completed(user_id, id, status, limit, per_page):
        errors = {}
        if len(id.strip()) == 0:
            errors["id"] = ["id cannot be empty"]
        if not isinstance(status, bool):
            errors["status"] = ["status must be boolean"]
        if not isinstance(limit, int):
            errors["limit"] = ["limit must be an integer"]
        if len(user_id.strip()) == 0:
            errors["user_id"] = ["user id cannot be empty"]
        if len(per_page.strip()) == 0:
            errors["per_page"] = ["per page cannot be empty"]
        if not per_page.isdigit():
            if "per_page" in errors:
                errors["per_page"].append("per page must be an integer")
            else:
                errors["per_page"] = ["per page must be an integer"]
        else:
            per_page = int(per_page)
        if errors:
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
                jsonify({"message": "authorization invalid"}),
                401,
            )
        if not (
            data_task := await TaskDatabase.update(
                "status", task_id=id, user_id=user_id, status=status
            )
        ):
            return (jsonify({"message": "task not found"}), 404)
        response = {
            "message": "success update task",
            "data": {
                "title": data_task.title,
                "task_id": data_task.id,
                "is_completed": data_task.is_completed,
                "new_status": status,
                "created_at": data_task.created_at,
                "user_id": user_id,
            },
        }
        if new_task := await TaskDatabase.get("all", user_id=user_id, limit=limit):
            data_task = [
                {
                    "task_id": task.id,
                    "title": task.title,
                    "is_completed": task.is_completed,
                    "created_at": task.created_at,
                }
                for task in new_task
            ]
            paginated_data = [
                data_task[i : i + per_page] for i in range(0, len(data_task), per_page)
            ]
            response["new_task"] = [
                {
                    "title": i.title,
                    "created_at": i.created_at,
                    "task_id": i.id,
                    "is_completed": i.is_completed,
                }
                for i in new_task
            ]
            response["page"] = {
                "total_page": len(paginated_data),
                "tasks": paginated_data,
                "size": len(new_task),
                "current_page": 0,
                "per_page": per_page,
                "limit": limit,
            }
        return jsonify(response), 201

    @staticmethod
    async def update_title_id(user_id, id, new_title, limit, per_page):
        errors = {}
        if len(id.strip()) == 0:
            errors["id"] = ["id cannot be empty"]
        if len(new_title.strip()) == 0:
            errors["new_title"] = ["new title cannot be empty"]
        if not isinstance(limit, int):
            errors["limit"] = ["limit must be an integer"]
        if len(user_id.strip()) == 0:
            errors["user_id"] = ["user id cannot be empty"]
        if len(per_page.strip()) == 0:
            errors["per_page"] = ["per page cannot be empty"]
        if not per_page.isdigit():
            if "per_page" in errors:
                errors["per_page"].append("per page must be an integer")
            else:
                errors["per_page"] = ["per page must be an integer"]
        else:
            per_page = int(per_page)
        if errors:
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
                jsonify({"message": "authorization invalid"}),
                401,
            )
        if not (data_task := await TaskDatabase.get("id", task_id=id, user_id=user_id)):
            return (jsonify({"message": "task not found"}), 404)
        new_data_task = await TaskDatabase.update(
            "id", task_id=id, new_title=new_title, user_id=user_id
        )
        response = {
            "message": "success update task",
            "data": {
                "task_id": data_task.id,
                "title": data_task.title,
                "created_at": data_task.created_at,
                "new_title": new_data_task.title,
                "is_completed": data_task.created_at,
                "user_id": user_database.id,
            },
        }
        if new_task := await TaskDatabase.get("all", user_id=user_id, limit=limit):
            data_task = [
                {
                    "task_id": task.id,
                    "title": task.title,
                    "is_completed": task.is_completed,
                    "created_at": task.created_at,
                }
                for task in new_task
            ]
            paginated_data = [
                data_task[i : i + per_page] for i in range(0, len(data_task), per_page)
            ]
            response["new_task"] = [
                {
                    "title": i.title,
                    "created_at": i.created_at,
                    "task_id": i.id,
                    "is_completed": i.is_completed,
                }
                for i in new_task
            ]
            response["page"] = {
                "total_page": len(paginated_data),
                "tasks": paginated_data,
                "size": len(data_task),
                "current_page": 0,
                "per_page": per_page,
                "limit": limit,
            }
        return jsonify(response), 201

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
                jsonify({"message": "authorization invalid"}),
                401,
            )
        await TaskDatabase.delete("user_id", user_id=user_id)
        return (
            jsonify({"message": "success delete task", "data": {"user_id": user_id}}),
            201,
        )

    @staticmethod
    async def delete_task_id(user_id, id, limit, per_page):
        try:
            errors = {}
            if not isinstance(limit, int):
                errors["limit"] = ["limit must be an integer"]
            if len(id.strip()) == 0:
                errors["id"] = ["id cannot be empty"]
            if len(user_id.strip()) == 0:
                errors["user_id"] = ["user id cannot be empty"]
            if len(per_page.strip()) == 0:
                errors["per_page"] = ["per page cannot be empty"]
            if not per_page.isdigit():
                if "per_page" in errors:
                    errors["per_page"].append("per page must be an integer")
                else:
                    errors["per_page"] = ["per page must be an integer"]
            else:
                per_page = int(per_page)
            if errors:
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
                return jsonify({"message": "authorization invalid"}), 401

            if not (
                data_task := await TaskDatabase.get("id", task_id=id, user_id=user_id)
            ):
                return (jsonify({"message": "task not found"}), 404)
            await TaskDatabase.delete("id", task_id=id, user_id=user_id)
            new_task = await TaskDatabase.get("all", user_id=user_id, limit=limit)
            new_data_task = [
                {
                    "task_id": task.id,
                    "title": task.title,
                    "is_completed": task.is_completed,
                    "created_at": task.created_at,
                }
                for task in new_task
            ]
            paginated_data = [
                new_data_task[i : i + per_page]
                for i in range(0, len(new_data_task), per_page)
            ]
            return (
                jsonify(
                    {
                        "message": "success delete task",
                        "data": {
                            "title": data_task.title,
                            "created_at": data_task.created_at,
                            "task_id": data_task.id,
                            "is_completed": data_task.is_completed,
                            "user_id": user_database.id,
                        },
                        "new_task": [
                            {
                                "title": i.title,
                                "created_at": i.created_at,
                                "task_id": i.id,
                                "is_completed": i.is_completed,
                            }
                            for i in new_task
                        ],
                        "page": {
                            "total_page": len(paginated_data),
                            "tasks": paginated_data,
                            "size": len(data_task),
                            "current_page": 0,
                            "per_page": per_page,
                            "limit": limit,
                            "new_size": len(new_task),
                        },
                    }
                ),
                201,
            )
        except mongoengine.errors.ValidationError:
            return (
                jsonify(
                    {
                        "message": "task not found",
                    }
                ),
                404,
            )

    @staticmethod
    async def get_task_id(user_id, task_id):
        errors = {}
        if len(user_id.strip()) == 0:
            errors["user_id"] = ["user id cannot be empty"]
        if len(task_id.strip()) == 0:
            errors["id"] = ["id cannot be empty"]
        if errors:
            return jsonify({"message": "input invalid", "errors": errors}), 400
        if not (user_database := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization invalid"}),
                401,
            )
        if not (task := await TaskDatabase.get("id", user_id=user_id, task_id=task_id)):
            return (
                jsonify({"message": "task not found"}),
                404,
            )
        return (
            jsonify(
                {
                    "message": "success get task",
                    "data": {
                        "user_id": user_id,
                        "task": {
                            "task_id": task.id,
                            "title": task.title,
                            "is_completed": task.is_completed,
                            "created_at": task.created_at,
                        },
                    },
                }
            ),
            200,
        )

    @staticmethod
    async def get_task_title(user_id, title, limit):
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
        if errors:
            return jsonify({"message": "input invalid", "errors": errors}), 400
        if not (user_database := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization invalid"}),
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
                    "data": {
                        "user_id": user_id,
                        "title": title,
                        "limit": limit,
                        "tasks": [
                            {
                                "task_id": i.id,
                                "title": i.title,
                                "is_completed": i.is_completed,
                                "created_at": i.created_at,
                            }
                            for i in task
                        ],
                    },
                }
            ),
            200,
        )

    @staticmethod
    async def get_task_all(user_id, limit):
        if not (user_database := await UserDatabase.get("user_id", user_id=user_id)):
            return (
                jsonify({"message": "authorization invalid"}),
                401,
            )
        if not limit.isdigit():
            return (
                jsonify(
                    {
                        "message": "limit must be an integer",
                        "errors": {"limit": ["limit must be an integer"]},
                    }
                ),
                400,
            )
        limit = int(limit)
        if not (task := await TaskDatabase.get("all", user_id=user_id, limit=limit)):
            return (
                jsonify({"message": "task not found"}),
                404,
            )
        return (
            jsonify(
                {
                    "message": "success get task",
                    "data": {
                        "user_id": user_id,
                        "limit": limit,
                        "tasks": [
                            {
                                "task_id": i.id,
                                "title": i.title,
                                "is_completed": i.is_completed,
                                "created_at": i.created_at,
                            }
                            for i in task
                        ],
                    },
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
                jsonify({"message": "authorization invalid"}),
                401,
            )
        task = await TaskDatabase.insert(
            user_database.username,
            title,
            int(datetime.datetime.now(datetime.timezone.utc).timestamp()),
        )
        response = {
            "message": "success create task",
            "data": {
                "title": task.title,
                "task_id": task.id,
                "is_completed": task.is_completed,
                "created_at": task.created_at,
                "user_id": user_id,
                "limit": limit,
            },
        }
        if new_task := await TaskDatabase.get("all", user_id=user_id, limit=limit):
            response["new_task"] = [
                {
                    "task_id": i.id,
                    "title": i.title,
                    "is_completed": i.is_completed,
                    "created_at": i.created_at,
                }
                for i in new_task
            ]
        return (
            jsonify(response),
            201,
        )
