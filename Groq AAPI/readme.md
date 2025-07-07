# 🔍 Query-Based Retrieval & Response using Google Gemini Embedding + Groq LLM (on AWS Lambda)

This project implements a **RAG (Retrieval-Augmented Generation)** system using [Google Gemini Embedding](w) for semantic search and [Groq](w)’s `Deepseek-R1-Distill-Llama-70b` model for generation. The system is hosted on an [AWS Lambda](w) function with an [API Gateway](w) frontend. It retrieves relevant context from a pre-embedded corpus stored in [Amazon S3](w) and generates answers strictly based on that context.

---


## 🔧 Architecture Overview

### ☁️ AWS Components

* **API Gateway** – Accepts user input via POST `/ask`
* **AWS Lambda** – Main processing unit (runtime: Python 3.12, architecture: x86\_64)

  * Timeout: ⏱️ **5 minutes** (must be set or function may timeout)
* **Amazon S3** – Stores pickled documents and corresponding embeddings
* **External APIs**:

  * **Google Gemini API** – For embedding user query
  * **Groq LLM API** – For generating context-aware answers

---

## 🧠 RAG Pipeline

```
                        +-------------------------+
                        |     API Gateway         |
                        | (POST /ask with query)  |
                        +------------+------------+
                                     |
                                invokes
                                     ↓
                    +-------------------------------+
                    |         AWS Lambda            |
                    |-------------------------------|
                    | 1. Load vector & text data    |
                    |    from S3 (.pkl files)       |
                    | 2. Embed query using Gemini   |
                    | 3. Cosine similarity ranking  |
                    | 4. Retrieve top-k context     |
                    | 5. Generate answer using Groq |
                    +-------------------------------+
                                     ↓
                          Returns JSON response
```

---

## 📂 Folder Structure

```
.
├── lambda_function.py       # Lambda handler and core logic
├── README.md                # Project documentation
```

---

## 📦 Requirements

### 🛠️ Services & APIs

* [Amazon S3](w): Stores:

  * `batman.pkl` (list of vector embeddings)
  * `batman_text.pkl` (list of associated documents)
* [Google Gemini API](w) for `embedding-001`
* [Groq API](w) for text generation using `Deepseek-R1-Distill-Llama-70b`

### 🧾 AWS Lambda Configuration

* **Runtime**: `Python 3.12`
* **Architecture**: `x86_64`
* **Timeout**: **5 minutes** (❗ must be set manually)
* **Permissions**:

  * `AmazonS3ReadOnlyAccess` or custom access to bucket `picklesdata`

---

## 🔐 Secrets Required

Replace placeholders in code with your actual keys:

```python
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
API_KEY = "YOUR_GEMINI_API_KEY"
```

---

## 📥 Sample API Request

### Endpoint

```
POST /ask
```

### Request Body

```json
{
  "query": "What are Batman’s core motivations?"
}
```

---

## 📤 Sample Response

```json
{
  "statusCode": 200,
  "body": "Blog Generation is completed: <context-aware answer here>"
}
```

---

## 🔍 Internal Processing

### 1. **Load Pickles from S3**

```python
text_list = load_pickle_from_s3('picklesdata', 'batman_text.pkl')
loaded_list = load_pickle_from_s3('picklesdata', 'batman.pkl')
```

### 2. **Embed Query Using Gemini API**

Calls:

```
https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent
```

### 3. **Compute Cosine Similarity**

Ranks documents against the query vector.

### 4. **Generate Answer from Groq**

Sends the following prompt:

```
QUESTION: {Your Question}
CONTEXT: {Top-k retrieved passages}
```

---

## ✅ Future Enhancements

* Switch to streaming responses for long answers
* Cache embeddings for repeated queries
* Add user authentication & API metering
* Add support for dynamic top-k tuning

---

## 📄 License

MIT License — Free to use and modify for educational or non-commercial purposes.

