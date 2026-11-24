from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Todo


def index(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            Todo.objects.create(title=title)
        return redirect("index")
    return render(request, "todo/index.html", {
        "todos": Todo.objects.all(),
        "version": settings.APP_VERSION,
        "db_host": settings.DATABASES["default"].get("HOST") or "SQLite（ローカル）",
    })


@require_POST
def toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.done = not todo.done
    todo.save()
    return redirect("index")


@require_POST
def delete(request, pk):
    get_object_or_404(Todo, pk=pk).delete()
    return redirect("index")


def health(request):
    """ALB のヘルスチェック用。DB には接続しない"""
    return HttpResponse("ok")
