import os
import requests

# GitHub Secretsから環境変数を取得
ACCESS_KEY = os.environ.get("ACCESS_KEY")
AFFILIATE_ID = os.environ.get("AFFILIATE_ID")
THREADS_ACCESS_KEY = os.environ.get("THREADS_ACCESS_KEY")
THREADS_USER_ID = os.environ.get("THREADS_USER_ID")

# 楽天API（20220601版 エンドポイント）
RAKUTEN_API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"

def fetch_first_item():
    # 20220601版では accessKey パラメータで認証します
    params = {
        "accessKey": ACCESS_KEY,
        "affiliateId": AFFILIATE_ID,
        "keyword": "おすすめ",
        "format": "json",
        "hits": 1
    }
    
    res = requests.get(RAKUTEN_API_URL, params=params)
    res.raise_for_status()
    data = res.json()
    
    items = data.get("Items", [])
    if not items:
        print("商品が見つかりませんでした。")
        return None
        
    item = items[0].get("Item", {})
    title = item.get("itemName")
    price = item.get("itemPrice")
    url = item.get("affiliateUrl")
    
    post_text = f"【おすすめ商品】\n{title}\n価格: {price}円\n\n詳細はこちら👇\n{url}"
    return post_text

def post_to_threads(text):
    if not THREADS_ACCESS_KEY or not THREADS_USER_ID:
        print("Threads APIの認証情報が不足しています。")
        return

    # ステップ1: コンテナの作成 (下書き作成)
    create_url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads"
    create_params = {
        "media_type": "TEXT",
        "text": text,
        "access_token": THREADS_ACCESS_KEY
    }
    
    res_create = requests.post(create_url, data=create_params)
    res_create.raise_for_status()
    creation_id = res_create.json().get("id")
    print(f"コンテナ作成成功 (ID: {creation_id})")

    # ステップ2: 投稿の公開 (パブリッシュ)
    publish_url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads_publish"
    publish_params = {
        "creation_id": creation_id,
        "access_token": THREADS_ACCESS_KEY
    }
    
    res_publish = requests.post(publish_url, data=publish_params)
    res_publish.raise_for_status()
    print("=== Threadsへの自動投稿が完了しました！ ===")

if __name__ == "__main__":
    try:
        content = fetch_first_item()
        if content:
            post_to_threads(content)
    except requests.exceptions.HTTPError as e:
        print(f"★APIエラー詳細: {e.response.text}")
    except Exception as e:
        print(f"エラー発生: {e}")
        print(f"★楽天APIエラー詳細: {e.response.text}")
    except Exception as e:
        print(f"エラー発生: {e}")
