import requests
from bs4 import BeautifulSoup
import sys

def fetch_article_text(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)

    # 空行を圧縮
    lines = [line for line in text.splitlines() if line.strip()]
    text = "\n".join(lines)