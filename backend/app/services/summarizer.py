"""
LLM-based code summarization service
Uses OpenRouter or HuggingFace APIs for summarizing code files
"""
import requests
from openai import OpenAI
from ..config import settings


class CodeSummarizer:
    """Service for summarizing code files using LLM APIs"""
    
    SUMMARY_EXTRACTION_PROMPT = """
Summarize the code for README generation.

Return JSON only:
{
  "file_name": "",
  "purpose": "",
  "key_components": [],
  "dependencies": [],
  "inputs_outputs": "",
  "important_logic": "",
  "connections": "",
  "configurations": "",
  "entry_point": ""
}

Guidelines:
- purpose: main role of the file
- key_components: main functions/classes (1-line each)
- dependencies: imports
- inputs_outputs: main I/O
- important_logic: key algorithms/flows
- connections: links to other modules/APIs
- configurations: constants/env vars
- entry_point: how execution starts if any

File:
"""

    def _prepare_content(self, file_content: str) -> str:
        """Trim content to a safe token budget before sending to the LLM."""
        return file_content[:settings.MAX_FILE_CONTENT_CHARS]
    
    def __init__(self, use_hf: bool = False):
        """
        Initialize summarizer with OpenRouter or HuggingFace client
        
        Args:
            use_hf: If True, use HuggingFace API; otherwise use OpenRouter
        """
        self.use_hf = use_hf

        if use_hf:
            self.api_key = settings.HF_TOKEN
            self.base_url = settings.HF_BASE_URL
            self.model = settings.HF_MODEL
            self.client = None
        else:
            self.api_key = settings.OPENROUTER_API_KEY
            self.base_url = settings.OPENROUTER_BASE_URL
            self.model = settings.OPENROUTER_MODEL
            self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)

        if not self.api_key:
            raise ValueError(f"API key not configured. Use HF: {use_hf}")
        
    def summarize_file(self, file_path: str, file_content: str) -> str:
        """
        Summarize a single file using LLM
        
        Args:
            file_path: Path to the file
            file_content: Content of the file
            
        Returns:
            Summary as JSON string
        """
        prepared_content = self._prepare_content(file_content)
        message_content = f"File name: {file_path}\n\n{prepared_content}"
        
        try:
            if self.use_hf:
                return self._summarize_file_hf(message_content)

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": self.SUMMARY_EXTRACTION_PROMPT + message_content
                    }
                ],
                max_tokens=settings.SUMMARIZER_MAX_OUTPUT_TOKENS,
                temperature=0.2,
                **self._get_extra_params()
            )
            return completion.choices[0].message.content
        except Exception as e:
            error_text = str(e)
            if self.use_hf and "401" in error_text:
                raise ValueError(
                    "Hugging Face authentication failed (401). "
                    "Update HF_TOKEN in backend/.env with a valid token that has Inference access."
                )

            print(f"Error summarizing {file_path}: {e}")
            return f"{{\"file_name\": \"{file_path}\", \"error\": \"{error_text}\"}}"
    
    def _summarize_file_hf(self, message_content: str) -> str:
        """Summarize using Hugging Face router with direct HTTP to avoid SDK quirks."""
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": self.SUMMARY_EXTRACTION_PROMPT + message_content,
                    }
                ],
                "max_tokens": settings.SUMMARIZER_MAX_OUTPUT_TOKENS,
                "temperature": 0.2,
            },
            timeout=90,
        )

        if response.status_code == 401:
            raise ValueError(
                "Hugging Face authentication failed (401). "
                "Update HF_TOKEN in backend/.env with a valid token that has Inference access."
            )

        response.raise_for_status()
        payload = response.json()
        return payload["choices"][0]["message"]["content"]

    def _get_extra_params(self) -> dict:
        """Get extra parameters for OpenRouter API"""
        params = {
            "extra_headers": {},
            "extra_body": {}
        }

        if settings.SITE_URL:
            params["extra_headers"]["HTTP-Referer"] = settings.SITE_URL
        if settings.SITE_NAME:
            params["extra_headers"]["X-Title"] = settings.SITE_NAME

        return params
