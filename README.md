# 朝のニュースまとめアプリ

毎朝7時（日本時間）に生成AIと美容業界の最新情報を自動収集して表示するWebアプリケーションです。

## 機能

- 📰 **自動ニュース収集**: 毎朝7時に自動実行
- 🤖 **生成AIトレンド**: 重要度順に3件の最新情報
- 💄 **美容業界情報**: 重要度順に3件の最新情報
- 🔄 **手動更新機能**: ボタンクリックで即座に更新可能
- 🇯🇵 **日本語対応**: 全ての情報が日本語で表示

## セットアップ

### 1. 必要なパッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. アプリケーションの起動

```bash
python app.py
```

### 3. ブラウザでアクセス

```
http://localhost:5000
```

## 使い方

1. アプリケーションを起動すると、毎朝7時（日本時間）に自動でニュースを取得します
2. ブラウザで `http://localhost:5000` にアクセスすると、最新のニュースが表示されます
3. 「今すぐ更新」ボタンをクリックすると、手動で最新情報を取得できます

## ファイル構成

```
morning-news-app/
├── app.py                 # メインアプリケーション
├── templates/
│   └── index.html        # Webページのテンプレート
├── requirements.txt      # 必要なパッケージ
├── news_data.json       # ニュースデータ（自動生成）
└── README.md            # このファイル
```

## 注意事項

- このアプリケーションは24時間稼働させる必要があります
- 本番環境では、より安定したWSGIサーバー（gunicorn等）の使用を推奨します
- 実際のニュース取得機能は、適切なAPI統合が必要です

## カスタマイズ

### 実行時刻の変更

`app.py` の以下の部分を編集してください：

```python
scheduler.add_job(func=fetch_news, trigger="cron", hour=7, minute=0)
```

### 取得する情報の追加

`fetch_news()` 関数内で、新しいカテゴリを追加できます。

## 本番環境へのデプロイ

### Herokuの場合

1. `Procfile` を作成:
```
web: gunicorn app:app
```

2. `runtime.txt` を作成:
```
python-3.11.0
```

3. デプロイ:
```bash
heroku create your-app-name
git push heroku main
```

### その他のホスティングサービス

- Render
- Railway
- AWS EC2
- Google Cloud Run

など、様々なプラットフォームで動作します。

## ライセンス

MIT License
