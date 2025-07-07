import boto3
import botocore.config
import requests
import re
import pickle

import json
import io

import json
import math


GROQ_API_KEY = "YOUR_GROQ_API_KEY"
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "Deepseek-R1-Distill-Llama-70b"


def load_pickle_from_s3(bucket_name, key):

    try:

        s3 = boto3.client('s3')

        response = s3.get_object(Bucket=bucket_name, Key=key)
        content = response['Body'].read()
        return pickle.load(io.BytesIO(content))
        #return "success"
    except Exception as E:
        E = str(E)
        print(E)
        return E

text_list = load_pickle_from_s3('picklesdata', 'batman_text.pkl')
loaded_list = load_pickle_from_s3('picklesdata', 'batman.pkl')

def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0
    return dot / (norm1 * norm2)

def retrieve(query):
    API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with your actual API key

    url = f"https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent?key={API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "model": "models/embedding-001",
        "content": {
            "parts": [
                {"text": query}
            ]
        },
        "task_type": "retrieval_document"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code != 200:
        print("KeyError")
    query_embedding = response.json()["embedding"]["values"]
    #print(query_embedding)
    # Compute cosine similarity with each vector in loaded_list
    similarities = [
        cosine_similarity(query_embedding, vec)
        for vec in loaded_list
    ]

    # Get top-k indexes (e.g., k = 10)
    k = 10
    top_k_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:k]

    # Build the CONTEXT string
    CONTEXT = ""
    for i in top_k_indices:
        CONTEXT += text_list[i] + "\n" + "========" + "\n"

    return CONTEXT




# === Prompt-based generation using Groq API ===
def generation_prompt(QUESTION, CONTEXT):


    prompt = f"""
Please answer question based on Context provided.
Don't add any information from your knowledgebase.
Strictly restrict to the context provided.
If you do not know an answer, please say "I don't know".

QUESTION: {QUESTION}
CONTEXT: {CONTEXT}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "temperature": 0.5,
        
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload)
        result = response.json()
        text = result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Groq API error: {str(e)}\nFull response: {result}"

    clean_text = re.sub(r'<think>.*?</think>\s*', '', text, flags=re.DOTALL)
    return clean_text

def answer(query):
    try:

        context = retrieve(query)
        #print(context)
        ans = generation_prompt(query, context)
        return ans
    except Exception as E:
        return E



def lambda_handler(event, context):

    event=json.loads(event['body'])
    query=event['query']

    generate_ans = answer(query)

    return{
        'statusCode':200,
        'body':json.dumps('Blog Generation is completed'+str(generate_ans))
    }

