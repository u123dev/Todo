from datetime import datetime

from django.test import TestCase

from task.forms import TaskCreationForm
from task.models import Task, Tag


class TaskFormsTests(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="TAG1")
        self.tag2 = Tag.objects.create(name="TAG2")
        self.task1 = Task.objects.create(
            content="Test_TASK_1", is_done="False",
            deadline=datetime.strptime("2024/04/11", "%Y/%m/%d").date()
        )
        self.data = {
            "content": self.task1.content, "deadline": self.task1.deadline,
            "is_done": self.task1.is_done, "tags": Tag.objects.all(),
        }

    def test_task_fields_form(self):
        form = TaskCreationForm()
        self.assertIn("content", form.fields)
        self.assertIn("deadline", form.fields)
        self.assertIn("is_done", form.fields)
        self.assertIn("tags", form.fields)

    def test_task_valid_form(self):
        form = TaskCreationForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_task_invalid_form(self):
        self.data["content"] = ""
        form = TaskCreationForm(data=self.data)
        self.assertFalse(form.is_valid())
