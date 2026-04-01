from huggingface_hub import InferenceClient
import os
from openai import OpenAI

# Ensure token is set
os.environ["HF_TOKEN"] = "<token here>"

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)


def chunk_text(text, max_chars=2000):
    """Split text into smaller chunks for API requests"""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks


def call_hf_summarization_agent(prompt, file_content):
    chunks = chunk_text(file_content)
    summaries = []
    for chunk in chunks:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3.2-Exp:novita",
            messages=[{"role": "user", "content": prompt + "\n" + chunk}]
        )
        summaries.append(response.choices[0].message.content)
    # Combine chunk summaries into one
    return "\n".join(summaries)



