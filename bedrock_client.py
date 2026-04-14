import boto3

def summarize_article(text: str) -> str:
    bedrock = boto3.client("bedrock-runtime", region_name="ap-northeast-1")

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
    usage = resp["usage"]
    cost_usd = (usage["inputTokens"] / 1_000_000 * 0.80) + (usage["outputTokens"] / 1_000_000 * 4.00)

    return answer, cost_usd