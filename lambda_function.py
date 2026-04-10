import os
from scraper import fetch_article_text
from bedrock_client import summarize_article

# LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
# LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

def lambda_handler(event, context):
    summarize_article(fetch_article_text("https://note.com/pirokenhris/n/n883b5f5af293"))