from scraper import fetch_article_text
from bedrock_client import summarize_article

summarize_article(fetch_article_text("https://note.com/pirokenhris/n/n883b5f5af293"))