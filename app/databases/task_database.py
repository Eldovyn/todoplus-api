from .database import Database
from ..models import UserModel, TaskModel
import difflib


class TaskDatabase(Database):
    @staticmethod
    async def insert(username, title, created_at):
        if user_data := UserModel.objects(username=username).first():
            task = TaskModel(title=title, user=user_data, created_at=created_at)
            task.save()
            return task

    @staticmethod
    async def get(category, **kwargs):
        user_id = kwargs.get("user_id")
        title = kwargs.get("title")
        task_id = kwargs.get("task_id")
        limit = kwargs.get("limit")
        if category == "title":
            if user_data := UserModel.objects(id=user_id).first():
                list_task = TaskModel.objects(user=user_data).all()
                titles = [task.title for task in list_task]
                matches = difflib.get_close_matches(title, titles, n=5, cutoff=0.5)
                similar_tasks = TaskModel.objects(
                    title__in=matches, user=user_data
                ).all()
                return similar_tasks
        elif category == "id":
            if user_data := UserModel.objects(id=user_id).first():
                return TaskModel.objects(user=user_data, id=task_id).first()
        elif category == "all":
            if user_data := UserModel.objects(id=user_id).first():
                return (
                    TaskModel.objects(user=user_data)
                    .order_by("-created_at")
                    .limit(limit)
                    .all()
                )

    @staticmethod
    async def delete(category, **kwargs):
        user_id = kwargs.get("user_id")
        task_id = kwargs.get("task_id")
        if category == "id":
            if user_data := UserModel.objects(id=user_id).first():
                return TaskModel.objects(user=user_data, id=task_id).delete()
        elif category == "all":
            if user_data := UserModel.objects(id=user_id).first():
                return TaskModel.objects(user=user_data).delete()

    @staticmethod
    async def update(category, **kwargs):
        user_id = kwargs.get("user_id")
        task_id = kwargs.get("task_id")
        new_title = kwargs.get("new_title")
        status = kwargs.get("status")
        if category == "id":
            if user_data := UserModel.objects(id=user_id).first():
                if task_data := TaskModel.objects(user=user_data, id=task_id).first():
                    task_data.title = new_title
                    task_data.save()
                    return task_data
        if category == "status":
            if user_data := UserModel.objects(id=user_id).first():
                if task_data := TaskModel.objects(user=user_data, id=task_id).first():
                    task_data.is_completed = status
                    task_data.save()
                    return task_data
