import os
import requests

# Secretsから安全に取得
APP_ID = os.environ.get("RAKUTEN_APP_ID")
ACCESS_KEY = os.environ.get("RAKUTEN_ACCESS_KEY")
AFFILIATE_ID = os.environ.get("RAKUTEN_AFFILIATE_ID")

API_URL = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20220601"

def fetch_items():
    params = {
        "applicationId": APP_ID,
        "accessKey": ACCESS_KEY,
        "affiliateId": AFFILIATE_ID,
        "keyword": "おすすめ",
        "format": "json",
        "hits": 3
    }
    headers = {
        "Referer": "https://google.com/",
        "Origin": "https://google.com",
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        res = requests.get(API_URL, params=params, headers=headers)
        res.raise_for_status()
        data = res.json()
        print("=== 取得成功 ===")
        print(f"取得件数: {len(data.get('Items', []))}件")
        for item in data.get("Items", []):
            i = item.get("Item", {})
            print(f"- {i.get('itemName')} ({i.get('itemPrice')}円)")
            print(f"  {i.get('affiliateUrl')}")
    except Exception as e:
        print(f"エラー発生: {e}")

if __name__ == "__main__":
    fetch_items()
