from django.test import TestCase
from django.urls import reverse

from task.models import Tag, Task


class TagTest(TestCase):
    def test_retrieve_tag(self):
        Tag.objects.create(name="test-tag1")
        Tag.objects.create(name="test-tag2")
        url = reverse("task:tag-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        tags = Tag.objects.all()
        self.assertEqual(list(response.context["tag_list"]),
                         list(tags))

        self.assertTemplateUsed(response, "task/tag_list.html")


class TaskTest(TestCase):
    def test_retrieve_task(self):
        task1 = Task.objects.create(content="test-content1")
        task2 = Task.objects.create(content="test-content2",
                                    deadline="2023-04-01")
        tag1 = Tag.objects.create(name="tag1")
        tag2 = Tag.objects.create(name="tag2")
        tag3 = Tag.objects.create(name="tag3")

        task1.tags.set([tag1, tag2])
        task2.tags.set([tag1, tag3])

        url = reverse("task:task-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        tasks = Task.objects.all()
        self.assertEqual(list(response.context["task_list"]),
                         list(tasks))

        self.assertTemplateUsed(response, "task/task_list.html")

    def test_toggle_task_status(self):
        task1 = Task.objects.create(
            content="test-content1", deadline="2024-04-08")
        tag1 = Tag.objects.create(name="tag1")
        tag2 = Tag.objects.create(name="tag2")
        task1.tags.set([tag1, tag2])

        url_toggle = reverse("task:task-set-done", args=[task1.id])

        # toggle-task-done
        response = self.client.post(url_toggle)
        self.assertEqual(response.status_code, 302)
        task1.refresh_from_db()

        self.assertEqual(task1.is_done, True)

        # toggle-task-undo done
        response = self.client.post(url_toggle)
        task1.refresh_from_db()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(task1.is_done, False)
