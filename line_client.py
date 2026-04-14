import os
import requests

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]


def send_line_message(summary_text: str, reply_token: str) -> dict:
    """LINEにリプライ返信
    
    Bedrockで要約した内容をLINEに返信
    
    Returns:
        dict: {"code": int, "message": str}
    """


    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        'replyToken': reply_token,
        'messages': [{'type': 'text', 'text': summary_text}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "code": response.status_code,
            "message": "送信完了"
        }
    
    except requests.HTTPError as e:
        return {
            "code": response.status_code,
            "message": f"LINE APIエラー: {e}",
        }
    
    except requests.RequestException as e:
        return {
            "code": 500,
            "message": f"リクエスト失敗: {e}",
        }