"""ハンズオン用の設定。値はすべて環境変数（.env）から読み込む"""
import os
from pathlib import Path

import pymysql

# PyMySQL を MySQLdb（mysqlclient）の代わりとして使う
pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent

APP_VERSION = "v1"

SECRET_KEY = os.environ.get("SECRET_KEY", "handson-insecure-secret-key")
# ハンズオンではエラー内容を画面で見るため True。本番では必ず False にする
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "todo",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": ["django.template.context_processors.request"]},
    }
]

# 接続先のデータベース（RDS）。DB_HOST を指定しない場合はローカル確認用に SQLite を使う
if os.environ.get("DB_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": os.environ["DB_HOST"],
            "PORT": os.environ.get("DB_PORT", "3306"),
            "NAME": os.environ.get("DB_NAME", "todo"),
            "USER": os.environ.get("DB_USER", "admin"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            # 繋がらないときに早めに失敗させる（秒）
            "OPTIONS": {"connect_timeout": 5, "charset": "utf8mb4"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CSRF_TRUSTED_ORIGINS = ["http://*.elb.amazonaws.com", "https://*.elb.amazonaws.com"]
