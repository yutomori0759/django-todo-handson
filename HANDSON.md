# ハンズオン手順書：Webアプリケーションをデプロイしてみよう【EC2 × Docker × RDS】

操作の詳しい説明はスライドを見てください。この手順書は **コピペ用** です。`コードブロック` の中身はそのままコピーして実行できます。

## 使うリンク

| 用途 | URL |
| --- | --- |
| アプリのリポジトリ | https://github.com/yutomori0759/aws-webapp-deploy-ec2-rds |
| CloudFormation テンプレート | https://github.com/yutomori0759/aws-webapp-deploy-ec2-rds/blob/main/cfn/template.yaml |
| AWS マネジメントコンソール | https://console.aws.amazon.com/ |

## メモ欄（作業中に埋めていく）

```
DBPassword : 
AppUrl     : 
DBHost     : 
InstanceId : 
```

---

## STEP 1. CloudFormation でスタックを作成する（コンソール操作）

リージョンは **東京（ap-northeast-1）**。入力する値：

```
スタック名 : handson-webapp
DBPassword : 英数字8文字以上（メモ欄に控える）
```

## STEP 2. 出力タブの値を控える（コンソール操作）

`AppUrl` / `DBHost` / `InstanceId` をメモ欄に控える。

## STEP 3. Session Manager で EC2 に接続する（コンソール操作）

以降のコマンドは、Session Manager のターミナルで実行します。

---

## STEP 4. 実行環境を入れる

```bash
sudo su - ec2-user
```

```bash
sudo dnf install -y docker git
sudo systemctl start docker
```

```bash
docker --version
git --version
```

## STEP 5. コードを置く

```bash
git clone https://github.com/yutomori0759/aws-webapp-deploy-ec2-rds.git
cd aws-webapp-deploy-ec2-rds
ls
```

## STEP 6. 設定を書く（.env）

```bash
vim .env
```

書き込む内容（`（ ）` はかっこごとメモ欄の値に置き換える）：

```
DB_HOST=（DBHost の値）
DB_NAME=todo
DB_USER=admin
DB_PASSWORD=（DBPassword の値）
```

vim の操作：`i` → 貼り付け → `Esc` → `:wq` + Enter（保存せずにやめるときは `:q!`）

```bash
cat .env
```

## STEP 7. アプリを起動する

```bash
sudo docker build -t todo-app .
```

```bash
sudo docker run -d --name todo -p 80:8000 --env-file .env todo-app
```

```bash
sudo docker ps
```

## STEP 8. マイグレーションを実行する（1回目）

```bash
sudo docker exec todo python manage.py migrate
```

## STEP 9. セキュリティグループを修正する（コンソール操作）

<details>
<summary>講義で原因を確認してから開いてください</summary>

```
対象      : handson-db-sg のインバウンドルール
変更前    : 5432（PostgreSQL）
変更後    : MYSQL/Aurora（3306）
```

</details>

## STEP 10. マイグレーションを実行する（2回目）

```bash
sudo docker exec todo python manage.py migrate
```

実行された SQL を見る：

```bash
sudo docker exec todo python manage.py sqlmigrate todo 0001
```

データベースの中を見る：

```bash
sudo docker exec todo python manage.py sql "SHOW TABLES"
```

```bash
sudo docker exec todo python manage.py sql "DESCRIBE todo_todo"
```

```bash
sudo docker exec todo python manage.py sql "SELECT * FROM django_migrations"
```

## STEP 11. アプリを使ってみる

`AppUrl` をブラウザで開いて TODO を登録したあと：

```bash
sudo docker exec todo python manage.py sql "SELECT * FROM todo_todo"
```

**デプロイ完了です！**

---

## Extra. 機能を追加する（時間があれば）

### E-1. v2 のコードをデプロイする

```bash
git fetch
git checkout v2
```

```bash
sudo docker build -t todo-app .
sudo docker rm -f todo
sudo docker run -d --name todo -p 80:8000 --env-file .env todo-app
```

### E-2. 未実行のマイグレーションを確認する

```bash
sudo docker exec todo python manage.py showmigrations todo
```

### E-3. 0002 で実行される SQL を見る

```bash
sudo docker exec todo python manage.py sqlmigrate todo 0002
```

### E-4. マイグレーションを実行する

```bash
sudo docker exec todo python manage.py migrate
```

```bash
sudo docker exec todo python manage.py sql "DESCRIBE todo_todo"
```

```bash
sudo docker exec todo python manage.py sql "SELECT * FROM todo_todo"
```

---

## 最後に：リソースを削除する（必ず実施）

CloudFormation でスタック **`handson-webapp`** を削除し、**`DELETE_COMPLETE`** になるまで確認する。

> 今日の構成は1時間あたり約0.15ドル。消し忘れて1か月放置すると **約110ドル** かかります（2026年11月時点、東京リージョン）。

---

## 困ったとき

状態を確認する：

```bash
sudo docker ps -a
```

```bash
sudo docker logs --tail 30 todo
```

```bash
cat .env
```

`.env` や `docker run` を間違えた（コンテナを作り直す）：

```bash
sudo docker rm -f todo
sudo docker run -d --name todo -p 80:8000 --env-file .env todo-app
```

`.env` を直す：

```bash
vim .env
```

よくあるエラー：

| エラー | 原因 |
| --- | --- |
| `permission denied ... docker.sock` | `sudo` の付け忘れ |
| `The container name "/todo" is already in use` | 同じ名前のコンテナが残っている → 上の「作り直す」を実行 |
| `Name or service not known` | `.env` の `DB_HOST` が間違っている |
| `(timed out)` | 通信が届いていない（セキュリティグループ） |
| `Access denied for user` | `.env` のユーザー名かパスワードが違う |
| ブラウザで 502 Bad Gateway | コンテナが動いていない、または `-p 80:8000` の指定ミス |
| ブラウザで開けない | URL が `https://` になっていないか確認（`http://` で開く） |

---

## 用語メモ

| 用語 | 意味 |
| --- | --- |
| CloudFormation | テンプレート（設計図）から AWS リソースを自動で作るサービス |
| スタック | テンプレートから作られたリソースのまとまり |
| ALB | 受付。インターネットからのアクセスを受けて EC2 に渡す |
| EC2 | アプリが動くサーバー |
| NAT Gateway | プライベートな EC2 が外に出るための出口 |
| RDS | MySQL などのデータベースを AWS が運用してくれるサービス |
| Session Manager | 鍵なし・22番ポートなしで EC2 に入れる仕組み |
| セキュリティグループ | 「どこから」「何番ポートへ」の通信を許可するかのルール |
| マイグレーション | コードが期待するテーブルの形に、データを残したまま DB を合わせること（中身は SQL の実行） |

お疲れ様でした！講義後のアンケートへのご協力もお願いします。
