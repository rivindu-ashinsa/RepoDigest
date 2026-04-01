"""
README generation service
Generates professional README files from code summaries
"""
from typing import List
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
    
    def __init__(self, use_hf: bool = False):
        """
        Initialize README generator with OpenRouter or HuggingFace client
        
        Args:
            use_hf: If True, use HuggingFace API; otherwise use OpenRouter
        """
        self.use_hf = use_hf
        
        if use_hf:
            api_key = settings.HF_TOKEN
            base_url = settings.HF_BASE_URL
            model = settings.HF_MODEL
        else:
            api_key = settings.OPENROUTER_API_KEY
            base_url = settings.OPENROUTER_BASE_URL
            model = settings.OPENROUTER_MODEL
        
        if not api_key:
            raise ValueError(f"API key not configured. Use HF: {use_hf}")
        
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
    
    def generate(self, summaries: List[str]) -> str:
        """
        Generate README from file summaries
        
        Args:
            summaries: List of file summaries (usually JSON strings)
            
        Returns:
            Generated README content
        """
        summaries_text = "\n\n".join(summaries)
        prompt = self.README_PROMPT_TEMPLATE.format(summaries_text=summaries_text)
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **(self._get_extra_params() if not self.use_hf else {})
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise ValueError(f"Error generating README: {str(e)}")
    
    def _get_extra_params(self) -> dict:
        """Get extra parameters for OpenRouter API"""
        if self.use_hf:
            return {}
        
        params = {
            "extra_headers": {},
            "extra_body": {}
        }
        
        if settings.SITE_URL:
            params["extra_headers"]["HTTP-Referer"] = settings.SITE_URL
        if settings.SITE_NAME:
            params["extra_headers"]["X-Title"] = settings.SITE_NAME
            
        return params
