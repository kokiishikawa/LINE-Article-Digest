import boto3

def summarize_article(html: str) -> str:
    bedrock = boto3.client("bedrock-runtime", region_name="ap-northeast-1")

    prompt = f"""
        以下の内容を要約して
        {html}
    """

    resp = bedrock.converse(
        modelId="arn:aws:bedrock:ap-northeast-1:315208930945:inference-profile/jp.anthropic.claude-haiku-4-5-20251001-v1:0",
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
    
    print(answer)