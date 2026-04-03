"""
README generation service
Generates professional README files from code summaries
"""
from typing import List
import requests
from openai import OpenAI
from ..config import settings


class ReadmeGenerator:
    """Service for generating README files from code summaries"""
    
    README_PROMPT_TEMPLATE = """
You are an intelligent documentation generator.
I will provide you with structured summaries of all files from a GitHub repository.

Your task is to analyze all the provided information and generate a clean, well-formatted,
and professional **README.md** for the repository.

### The README should include:
1. **Project Title and Overview**
2. **Key Features**
3. **Tech Stack**
4. **Project Structure**
5. **Setup Instructions**
6. **Usage**
7. **Contributing (Optional)**
8. **License (Optional)**

### Important Rules:
- Output **only the README.md content**, with no explanations or meta-comments.
- Do not include phrases like "based on the information provided" or "this README includes".
- Write in a concise, clear, and professional tone.
- Insert code blocks where relevant.

Here are the summarized file details:
{summaries_text}

Generate the README now.
"""

    def _prepare_summaries_text(self, summaries: List[str]) -> str:
        """Bound the total summary payload to prevent over-budget requests."""
        cleaned = [s for s in summaries if s and "\"error\"" not in s.lower()]
        if not cleaned:
            cleaned = summaries

        collected: List[str] = []
        used_chars = 0
        for item in cleaned:
            item_len = len(item)
            if used_chars + item_len > settings.README_MAX_SUMMARY_CHARS:
                break
            collected.append(item)
            used_chars += item_len

        return "\n\n".join(collected)
    
    def __init__(self, use_hf: bool = False):
        """
        Initialize README generator with OpenRouter or HuggingFace client
        
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
    
    def generate(self, summaries: List[str]) -> str:
        """
        Generate README from file summaries
        
        Args:
            summaries: List of file summaries (usually JSON strings)
            
        Returns:
            Generated README content
        """
        summaries_text = self._prepare_summaries_text(summaries)
        prompt = self.README_PROMPT_TEMPLATE.format(summaries_text=summaries_text)
        
        try:
            if self.use_hf:
                return self._generate_hf(prompt)

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=settings.README_MAX_OUTPUT_TOKENS,
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
            raise ValueError(f"Error generating README: {error_text}")
    
    def _generate_hf(self, prompt: str) -> str:
        """Generate README using Hugging Face router with direct HTTP."""
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": settings.README_MAX_OUTPUT_TOKENS,
                "temperature": 0.2,
            },
            timeout=120,
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
