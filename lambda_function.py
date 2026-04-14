from scraper import fetch_article_text
from bedrock_client import summarize_article
import json
from line_client import send_line_message
import re
import boto3
from datetime import datetime, timezone, timedelta
from decimal import Decimal

# 1ユーザーあたりの1日の利用上限 (USD)
# DAILY_LIMIT_USD = Decimal("1.00")
DAILY_LIMIT_USD = Decimal("0.01")
# DynamoDB テーブル名
TABLE_NAME = "line-article-digest-usage"

dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, _):
    body = json.loads(event['body'])
    if body.get('events'):
        for ev in body['events']:
            # テキスト以外 (スタンプ・画像など) はスキップ
            if ev.get('message', {}).get('type') != 'text':
                continue

            user_msg = ev['message']['text']
            url = extract_url(user_msg)

            # メッセージに URL が含まれていなければスキップ
            if url is None:
                continue

            reply_token = ev['replyToken']
            user_id = ev['source']['userId']

            # 当日の利用上限を超えていれば上限メッセージを返信
            if is_over_limit(user_id):
                send_line_message("本日の利用上限に達しました。明日またお試しください。", reply_token)
                continue

            # 記事を取得して要約し、利用コストを記録してから返信
            summary_text, cost_usd = summarize_article(fetch_article_text(url))
            record_usage(user_id, cost_usd)
            send_line_message(summary_text, reply_token)

    return {"statusCode": 200, "body": "OK"}


def is_over_limit(user_id: str) -> bool:
    """当日の累積コストが上限に達しているか確認する"""
    today = get_today()
    resp = table.get_item(Key={"userId": user_id, "date": today})
    item = resp.get("Item")
    if not item:
        return False
    return Decimal(str(item["cost_usd"])) >= DAILY_LIMIT_USD


def record_usage(user_id: str, cost_usd: float) -> None:
    """当日の累積コストを DynamoDB に加算する"""
    today = get_today()
    table.update_item(
        Key={"userId": user_id, "date": today},
        UpdateExpression="ADD cost_usd :cost",
        ExpressionAttributeValues={":cost": Decimal(str(cost_usd))},
    )


def get_today() -> str:
    """JST で本日の日付を返す (例: 2026-04-14)"""
    jst = timezone(timedelta(hours=9))
    return datetime.now(jst).strftime("%Y-%m-%d")


def extract_url(text: str) -> str | None:
    """メッセージ内の最初の URL を抽出する

    Return:
        str: 最初に見つかった URL。見つからない場合は None
    """
    match = re.search(r'https?://\S+', text)
    return match.group(0) if match else None
