from django.test import TestCase

from task.models import Tag, Task


class ModelTests(TestCase):
    def test_tag_str(self):
        tag = Tag.objects.create(name="test-tag")
        self.assertEqual(str(tag), tag.name)

    def test_task_str(self):
        task = Task.objects.create(
            content="test-content",
        )
        self.assertEqual(
            str(task),
            f"{task.content} | {task.creation_date}"
        )

    def test_create_task_with_tags(self):
        tag1 = Tag.objects.create(name="tag1")
        tag2 = Tag.objects.create(name="tag2")
        task = Task.objects.create(content="test-content")
        task.tags.set([tag1, tag2])

        self.assertEqual(task.content, "test-content")
        self.assertEqual(
            [tag.name for tag in task.tags.all()],
            ["tag1", "tag2"]
        )
