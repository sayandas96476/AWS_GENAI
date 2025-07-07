import boto3
import json
from datetime import datetime

def blog_generate_using_bedrock(blogtopic: str) -> str:
    prompt = f"""Write a 200 words blog on the topic {blogtopic}."""

    #bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")
    bedrock_runtime = boto3.client("bedrock-runtime", region_name="eu-north-1")


    body = {
        "inferenceConfig": {
            "max_new_tokens": 1000
        },
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        response = bedrock_runtime.invoke_model(
            modelId="amazon.nova-lite-v1:0",  # ✅ Correct model ID (NO ":0")
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body)
        )

        response_body = json.loads(response["body"].read())

        # Extract response text
        content = response_body.get("output", {}).get("message", {}).get("content", "")
        if not content:
            # fallback for some model variants
            content = response_body.get("generation", {}).get("text", "")

        print("Generated Blog:\n", content)
        return str(content)
    except Exception as E:
        return f"Error: {str(E)}"


def save_blog_details_s3(s3_key, s3_bucket, generate_blog):
    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=generate_blog.encode("utf-8"))
        print("Blog saved to S3:", s3_key)
    except Exception as e:
        print("Error when saving the blog to S3:", str(e))
        return str(e)


def lambda_handler(event, context):
    event = json.loads(event['body'])
    blogtopic = event.get('blog_topic')

    if not blogtopic:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing blog_topic in the request.')
        }

    generate_blog = blog_generate_using_bedrock(blogtopic=blogtopic)

    if generate_blog and not generate_blog.startswith("Error:"):
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f"blog-output/{current_time}.txt"
        s3_bucket = 'aws_bedrock_course1'
        #save_blog_details_s3(s3_key, s3_bucket, generate_blog)
    else:
        print("No blog was generated or an error occurred:", generate_blog)

    return {
        'statusCode': 200,
        'body': json.dumps('Blog Generation is completed'+generate_blog)
    }

