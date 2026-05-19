"""
Бесплатные AI клиенты для генерации текста
Поддержка: OpenRouter.ai, Hugging Face, Google Gemini (все FREE!)
"""

import os
import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class OpenRouterClient:
    """Клиент для OpenRouter.ai (БЕСПЛАТНЫЕ модели)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai"
        self.free_models = [
            "meta-llama/llama-3.2-3b-instruct:free",
            "google/gemma-2-9b-it:free",
            "mistralai/mistral-7b-instruct:free",
            "qwen/qwen-2-7b-instruct:free"
        ]
    
    def generate(self, prompt: str, model: str = None, max_tokens: int = 1000) -> str:
        """Генерация текста через OpenRouter"""
        model = model or self.free_models[0]
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"OpenRouter error: {e}")
            raise


class HuggingFaceClient:
    """Клиент для Hugging Face Inference API (БЕСПЛАТНО!)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('HUGGINGFACE_API_KEY')
        self.base_url = "https://api-inference.huggingface.co/models"
        self.free_models = [
            "mistralai/Mistral-7B-Instruct-v0.2",
            "meta-llama/Meta-Llama-3-8B-Instruct",
            "google/gemma-7b-it"
        ]
    
    def generate(self, prompt: str, model: str = None, max_tokens: int = 1000) -> str:
        """Генерация текста через Hugging Face"""
        model = model or self.free_models[0]
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": 0.7
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/{model}",
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return result[0]["generated_text"] if isinstance(result, list) else result["generated_text"]
        except Exception as e:
            logger.error(f"HuggingFace error: {e}")
            raise


class GeminiClient:
    """Клиент для Google Gemini Flash (БЕСПЛАТНО с лимитами)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GOOGLE_GEMINI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = "gemini-2.0-flash-exp"
    
    def generate(self, prompt: str, model: str = None, max_tokens: int = 1000) -> str:
        """Генерация текста через Gemini"""
        try:
            url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
            
            data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "maxOutputTokens": max_tokens,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            raise


class FreeAIManager:
    """Менеджер для всех бесплатных AI клиентов"""
    
    def __init__(self):
        self.openrouter = OpenRouterClient()
        self.huggingface = HuggingFaceClient()
        self.gemini = GeminiClient()
        
        self.clients = [
            ("openrouter", self.openrouter),
            ("huggingface", self.huggingface),
            ("gemini", self.gemini)
        ]
    
    def generate(self, prompt: str, preferred_client: str = "openrouter", **kwargs) -> str:
        """
        Генерация текста с автоматическим fallback
        """
        # Попробовать предпочитаемый клиент
        for name, client in self.clients:
            if name == preferred_client:
                try:
                    return client.generate(prompt, **kwargs)
                except Exception as e:
                    logger.warning(f"{name} failed, trying fallback: {e}")
                    break
        
        # Fallback на остальные клиенты
        for name, client in self.clients:
            if name != preferred_client:
                try:
                    logger.info(f"Trying fallback client: {name}")
                    return client.generate(prompt, **kwargs)
                except Exception as e:
                    logger.warning(f"{name} fallback failed: {e}")
                    continue
        
        raise Exception("All FREE AI clients failed!")


# Глобальный экземпляр
free_ai = FreeAIManager()


if __name__ == "__main__":
    # Тест
    try:
        result = free_ai.generate("Write a short health tip about drinking water")
        print(f"Generated: {result}")
    except Exception as e:
        print(f"Error: {e}")
