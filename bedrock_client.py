import boto3

def summarize_article(html: str) -> str:
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

    prompt = f"""
        以下の内容を要約して
        {html}
    """

    resp = bedrock.converse(
        modelId="anthropic.claude-3-5-haiku-20241022-v1:0",
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ]
    )

    answer = resp["output"]["message"]["content"][0]["text"]
    
    print(answer)