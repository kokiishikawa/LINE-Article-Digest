import requests
from bs4 import BeautifulSoup

def fetch_article_text(url: str) -> str:
    """指定 URL から記事の本文テキストを取得する

    Args:
        url: スクレイピング対象の記事 URL

    Returns:
        str: HTML タグを除去した本文テキスト

    Raises:
        requests.HTTPError: HTTP エラーが発生した場合
        requests.RequestException: 接続エラーなどが発生した場合
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)

    # 空行を圧縮
    lines = [line for line in text.splitlines() if line.strip()]
    text = "\n".join(lines)
    return text