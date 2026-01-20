from flask import Flask, render_template, jsonify
from datetime import datetime
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import time

app = Flask(__name__)

# データファイルのパス
DATA_FILE = 'news_data.json'

# 初期データ
def get_initial_data():
    return {
        'last_updated': None,
        'ai_news': [],
        'beauty_news': []
    }

# データを読み込む
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return get_initial_data()

# データを保存する
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 実際のニュース取得関数（Web検索API統合用）
def fetch_news():
    print(f"ニュース取得開始: {datetime.now(pytz.timezone('Asia/Tokyo'))}")
    
    # TODO: ここに実際のWeb検索APIを統合
    # 以下はデモ用のサンプルデータです
    # 実際の実装では、Genspark検索APIを使用して以下を実行:
    # 1. "生成AI 最新トレンド" で日本語のWeb検索
    # 2. "美容業界 最新情報" で日本語のWeb検索
    # 3. 重要度を判定して上位3件を選択
    
    jst_now = datetime.now(pytz.timezone('Asia/Tokyo'))
    
    data = {
        'last_updated': jst_now.strftime('%Y年%m月%d日 %H:%M'),
        'ai_news': [
            {
                'title': 'Google、新型AI「Gemini 2.0」を発表 - マルチモーダル性能が大幅向上',
                'summary': 'Googleは最新の大規模言語モデル「Gemini 2.0」を発表。テキスト、画像、音声、動画を統合的に処理できるマルチモーダル機能が大幅に強化され、従来モデルと比較して推論速度が2倍に向上。企業向けAPI提供も開始され、日本市場での活用が期待される。',
                'url': 'https://www.example.jp/ai-news/gemini-2-0',
                'importance': 1
            },
            {
                'title': 'OpenAI、ChatGPT Enterpriseに新機能追加 - 日本企業の導入加速',
                'summary': '企業向けChatGPTに、社内データの安全な学習機能とカスタマイズ可能なワークフロー機能が追加。三菱UFJ銀行や楽天など、日本の大手企業での導入事例が相次いで報告されている。データプライバシーとセキュリティ面での強化が評価されている。',
                'url': 'https://www.example.jp/ai-news/chatgpt-enterprise',
                'importance': 2
            },
            {
                'title': 'Stability AI、日本語特化の画像生成モデル「Stable Diffusion JP」をリリース',
                'summary': '日本文化やアニメスタイルに特化した画像生成AI「Stable Diffusion JP」が正式リリース。日本語プロンプトの理解精度が大幅に向上し、漫画やイラスト制作での活用が進む。クリエイター向けの商用ライセンスも提供開始。',
                'url': 'https://www.example.jp/ai-news/stable-diffusion-jp',
                'importance': 3
            }
        ],
        'beauty_news': [
            {
                'title': '資生堂、AI肌診断サービスを全国展開 - パーソナライズ化粧品の提案が可能に',
                'summary': '資生堂が開発したAI肌診断システムが全国の店舗で利用可能に。スマートフォンで撮影した肌画像から、シミ、シワ、毛穴などを詳細に分析し、個人に最適な化粧品を提案。既に10万人以上が利用し、顧客満足度90%を達成している。',
                'url': 'https://www.example.jp/beauty-news/shiseido-ai-diagnosis',
                'importance': 1
            },
            {
                'title': 'K-Beauty市場が日本で急成長 - 2024年市場規模3000億円突破へ',
                'summary': '韓国発の美容製品「K-Beauty」が日本市場で急拡大。特にスキンケア製品の人気が高く、百貨店やドラッグストアでの取り扱いが増加。SNSでの口コミ効果もあり、若年層を中心に支持を集めている。業界関係者は今後も成長が続くと予測。',
                'url': 'https://www.example.jp/beauty-news/k-beauty-growth',
                'importance': 2
            },
            {
                'title': 'メンズ美容市場が過去最高を記録 - 男性向けスキンケア製品の需要急増',
                'summary': '男性向け美容製品市場が前年比25%増の1500億円に到達。在宅勤務の増加やオンライン会議の普及により、男性の美容意識が高まっている。特にスキンケアと眉毛ケア製品の売上が顕著に伸びており、各メーカーが新製品を相次いで投入。',
                'url': 'https://www.example.jp/beauty-news/mens-beauty-record',
                'importance': 3
            }
        ]
    }
    
    save_data(data)
    print(f"ニュース取得完了: {datetime.now(pytz.timezone('Asia/Tokyo'))}")
    return data

# スケジューラーの設定
scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Tokyo'))
scheduler.add_job(func=fetch_news, trigger="cron", hour=7, minute=0, id='morning_news')
scheduler.start()

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/api/news')
def get_news():
    data = load_data()
    return jsonify(data)

@app.route('/api/refresh')
def refresh_news():
    data = fetch_news()
    return jsonify(data)

@app.route('/api/status')
def status():
    """スケジューラーの状態を確認"""
    jobs = scheduler.get_jobs()
    job_info = []
    for job in jobs:
        job_info.append({
            'id': job.id,
            'next_run': job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if job.next_run_time else None
        })
    return jsonify({
        'scheduler_running': scheduler.running,
        'jobs': job_info,
        'current_time_jst': datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    # 初回起動時にデータファイルがなければ初期データで作成
    if not os.path.exists(DATA_FILE):
        print("初期データを作成しています...")
        fetch_news()
    
    print("=" * 50)
    print("🌅 朝のニュースまとめアプリ 起動中...")
    print(f"⏰ 毎朝7時（日本時間）にニュースを自動取得します")
    print(f"🌐 ブラウザで http://localhost:5000 にアクセスしてください")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
