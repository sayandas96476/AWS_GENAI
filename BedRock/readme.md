
# 📝 Blog Generator using AWS Lambda, Amazon Bedrock, and API Gateway


> 📺 **Reference Video**: [YouTube - AWS Bedrock Lambda Blog Generator](https://www.youtube.com/watch?v=3OP39y4dO_Y&list=PLZoTAELRMXVP5zpBfH7pab4aB1LbmCM1z&index=7)

This project automatically generates a 200-word blog on a given topic using [Amazon Bedrock](w) (specifically the `amazon.nova-lite-v1` model) and serves it via an [AWS Lambda](w) function behind an [API Gateway](w). Optionally, the generated blog can be saved to [Amazon S3](w).

---

## 🔧 Architecture

* **API Gateway** – Exposes a REST endpoint for blog generation.
* **AWS Lambda** – Executes Python code to interact with Bedrock (runtime: `Python 3.12`, architecture: `x86_64`).
* **Amazon Bedrock** – Uses `amazon.nova-lite-v1` for LLM inference (region: `eu-north-1`).
* **Amazon S3** – (Optional) Used to persist the generated blogs.

---

## 📂 Folder Structure

```
.
├── lambda_function.py     # Lambda function source code
├── requirements.txt       # Contains required Python modules
├── README.md              # Project documentation
```

---

## 📦 Requirements

Ensure the following AWS services and configurations are in place:

### AWS Services

* [Amazon Bedrock](w) access in region `eu-north-1`
* [Amazon S3](w) bucket (e.g., `aws_bedrock_course1`) if saving blogs
* API Gateway (HTTP) configured to trigger the Lambda
* Lambda Layer including libraries like `boto3` (if not using built-in)

### Lambda Configuration

* **Runtime**: `Python 3.12`
* **Architecture**: `x86_64`
* **IAM Permissions**:

  * `bedrock:InvokeModel`
  * `s3:PutObject` (if saving to S3)
  * Attach managed policy: `AmazonBedrockFullAccess`
* **Lambda Layer**:

  * Optional: compatible with Python `3.11`, `3.12`, `3.13` if using external libraries

---

## 🚀 Deployment Steps

### 1. Upload the Lambda Function

Deploy `lambda_function.py` to the Lambda console under a new or existing function.

### 2. Configure API Gateway

* Create an **HTTP API** in API Gateway.
* Define a `POST` route (e.g., `/generate-blog`).
* Link the route to the Lambda function.

### 3. IAM & Permissions

Make sure your Lambda execution role includes:

* `AmazonBedrockFullAccess`
* `AmazonS3FullAccess` (optional)

No environment variables are required.

---

## 📥 Sample API Request

```http
POST /generate-blog
Content-Type: application/json

{
  "blog_topic": "AI in Healthcare"
}
```

---

## 📤 Sample Response

```json
{
  "statusCode": 200,
  "body": "Blog Generation is completed: <generated_text_here>"
}
```

---

## 🧠 Notes

* **Model Used**: `amazon.nova-lite-v1`
* **Region**: `eu-north-1`
* **Blog Storage** (Optional): `s3://aws_bedrock_course1/blog-output/`

To enable S3 saving, uncomment this line in `lambda_handler`:

```python
# save_blog_details_s3(s3_key, s3_bucket, generate_blog)
```

---

## ✅ Future Enhancements

* Support multiple Bedrock models via config
* User-defined blog length and style
* Blog storage in a database or vector store
* API key-based authentication

---

## 📄 License

MIT License — Free to use and modify for educational or non-commercial purposes.

---
