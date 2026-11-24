from django.db import models


class Todo(models.Model):
    title = models.CharField("タイトル", max_length=200)
    done = models.BooleanField("完了", default=False)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    class Meta:
        ordering = ["done", "-created_at"]

    def __str__(self):
        return self.title
