from django.db import models


class Todo(models.Model):
    PRIORITY_CHOICES = [(1, "高"), (2, "中"), (3, "低")]

    title = models.CharField("タイトル", max_length=200)
    done = models.BooleanField("完了", default=False)
    priority = models.IntegerField("優先度", choices=PRIORITY_CHOICES, default=2)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    class Meta:
        ordering = ["done", "-created_at"]

    def __str__(self):
        return self.title
