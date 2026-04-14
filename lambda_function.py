from scraper import fetch_article_text
from bedrock_client import summarize_article
import json
from line_client import send_line_message
import re

def lambda_handler(event, _):
    body = json.loads(event['body'])
    if body.get('events'):
        for ev in body['events']:
            if ev.get('message', {}).get('type') != 'text':
                continue
            user_msg = ev['message']['text']
            url = extract_url(user_msg)
            if url is None:
                continue
            reply_token = ev['replyToken']
            summary_text = summarize_article(fetch_article_text(url))
            send_line_message(summary_text, reply_token)
    return {"statusCode": 200, "body": "OK"}


def extract_url(text: str) -> str | None:
    """メッセージ内のURLを抽出する

    Return:
        str: 最初に見つかった URL。見つからない場合は None
    """
    match = re.search(r'https?://\S+', text)
    return match.group(0) if match else None