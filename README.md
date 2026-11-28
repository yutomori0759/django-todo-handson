# django-todo-handson

AWS ハンズオン「Webアプリケーションをデプロイしてみよう」用の TODO アプリです。

- Django 5.2 / Python 3.12 / Docker
- DB: RDS for MySQL 8.4（`DB_HOST` を指定しない場合は SQLite）
- `cfn/template.yaml`: ハンズオン用の CloudFormation テンプレート

## ブランチ

| ブランチ | 内容 |
|---|---|
| `main` | v1: TODO の追加・完了・削除 |
| `v2` | v2: 優先度（priority）の列を追加。マイグレーション `0002_add_priority` を含む |

## 起動方法（自分のPC）

DB は SQLite（コンテナの中のファイル）になります。コンテナを消すとデータも消えます。

```
docker build -t todo-app .
docker run -d --name todo-local -p 3000:8000 todo-app
docker exec todo-local python manage.py migrate
# → http://localhost:3000
```

## 起動方法（EC2 上）

```
cat > .env << 'EOF'
DB_HOST=（RDSのエンドポイント）
DB_NAME=todo
DB_USER=admin
DB_PASSWORD=（パスワード）
EOF

sudo docker build -t todo-app .
sudo docker run -d --name todo -p 80:8000 --env-file .env todo-app
sudo docker exec todo python manage.py migrate
```

## ハンズオン用コマンド

```
# SQL を実行して結果を表示する
sudo docker exec todo python manage.py sql "SHOW TABLES"
```

## 注意

ハンズオン用に `DEBUG=True`（エラー内容を画面に表示）になっています。本番環境では使わないでください。
