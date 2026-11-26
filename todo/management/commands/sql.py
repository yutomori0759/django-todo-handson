"""任意のSQLを実行して結果を表示するコマンド（ハンズオン用）

例: python manage.py sql "SHOW TABLES"
"""
import unicodedata

from django.core.management.base import BaseCommand
from django.db import connection


def width(value):
    """表示幅（全角文字は2として数える）"""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in str(value))


class Command(BaseCommand):
    help = "SQLを実行して結果を表示する"

    def add_arguments(self, parser):
        parser.add_argument("query")

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(options["query"])
            if cursor.description is None:
                self.stdout.write(f"OK（{cursor.rowcount}行に影響）")
                return
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
            widths = [max(width(v) for v in [col] + [r[i] for r in rows]) for i, col in enumerate(cols)]
            line = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
            fmt = lambda vals: "| " + " | ".join(str(v) + " " * (w - width(v)) for v, w in zip(vals, widths)) + " |"
            self.stdout.write("\n".join([line, fmt(cols), line, *[fmt(r) for r in rows], line]))
            self.stdout.write(f"{len(rows)}行")
