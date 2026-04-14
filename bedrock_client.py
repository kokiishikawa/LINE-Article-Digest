import boto3

# Lambda の warm start でクライアントを再利用するためモジュールレベルで初期化
bedrock = boto3.client("bedrock-runtime", region_name="ap-northeast-1")


def summarize_article(text: str) -> str:
    """記事テキストを Bedrock (Claude Haiku 4.5) で要約する

    Args:
        text: スクレイピングで取得した記事の本文テキスト

    Returns:
        str: 要約テキスト
    """

    prompt = f"""以下の記事を要約してください。

# 記事内容
{text}

# 出力形式
- 3〜5行の箇条書きで要点をまとめる
- LINEで読みやすいよう簡潔に
- 日本語で出力する
"""

    resp = bedrock.converse(
        modelId="arn:aws:bedrock:ap-northeast-1:315208930945:inference-profile/jp.anthropic.claude-haiku-4-5-20251001-v1:0",
        system=[{"text": "あなたは記事を簡潔に要約するアシスタントです。重要なポイントを抽出し、読みやすい日本語でまとめてください。"}],
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ],
        inferenceConfig={
            "maxTokens": 1024,
            "temperature": 0.5,
        }
    )

    answer = resp["output"]["message"]["content"][0]["text"]

    return answer