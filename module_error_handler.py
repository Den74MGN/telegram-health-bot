"""
Модуль централизованной обработки ошибок с fallback на бесплатные AI модели
Использует OpenRouter.ai, Hugging Face, Google Gemini Flash (бесплатно)
"""

import logging
import json
import os
import time
from functools import wraps
from datetime import datetime
from typing import List, Callable, Any, Optional
import requests

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FreeAIModels:
    """Бесплатные AI модели для fallback"""
    
    # OpenRouter.ai - бесплатные модели
    OPENROUTER_FREE = [
        "meta-llama/llama-3.2-3b-instruct:free",
        "google/gemma-2-9b-it:free",
        "mistralai/mistral-7b-instruct:free",
        "qwen/qwen-2-7b-instruct:free"
    ]
    
    # Hugging Face Inference API
    HUGGINGFACE_FREE = [
        "mistralai/Mistral-7B-Instruct-v0.2",
        "meta-llama/Meta-Llama-3-8B-Instruct",
        "google/gemma-7b-it"
    ]
    
    # Google Gemini Flash (бесплатно с лимитами)
    GEMINI_FREE = "gemini-2.0-flash-exp"


class ErrorHandler:
    """
    Централизованный обработчик ошибок с fallback на бесплатные модели
    """
    
    def __init__(
        self,
        fallback_models: List[str] = None,
        draft_dir: str = "drafts",
        error_log_file: str = "logs/errors.jsonl",
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        self.fallback_models = fallback_models or FreeAIModels.OPENROUTER_FREE
        self.draft_dir = draft_dir
        self.error_log_file = error_log_file
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.error_log = []
        
        # Создать директории если не существуют
        os.makedirs(self.draft_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.error_log_file), exist_ok=True)
    
    def with_fallback(self, func: Callable) -> Callable:
        """
        Декоратор для автоматического fallback между моделями
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            
            for model in self.fallback_models:
                for attempt in range(self.max_retries):
                    try:
                        logger.info(f"Trying model: {model} (attempt {attempt + 1}/{self.max_retries})")
                        result = func(*args, model=model, **kwargs)
                        logger.info(f"Success with model: {model}")
                        return result
                    
                    except Exception as e:
                        last_error = e
                        error_msg = f"Error with {model} (attempt {attempt + 1}): {str(e)}"
                        logger.error(error_msg)
                        self.log_error(func.__name__, str(e), model, attempt + 1)
                        
                        if attempt < self.max_retries - 1:
                            time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
                        continue
            
            # Все модели упали - создать черновик
            draft_path = self.create_draft(func.__name__, args, kwargs)
            self.notify_admin(func.__name__, last_error, draft_path)
            
            raise Exception(f"All fallback models failed. Draft saved to: {draft_path}")
        
        return wrapper
    
    def log_error(self, function: str, error: str, context: str, attempt: int) -> None:
        """Логирование ошибки в JSONL формате"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'function': function,
            'error': error,
            'context': context,
            'attempt': attempt
        }
        self.error_log.append(entry)
        
        # Запись в файл
        try:
            with open(self.error_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        except Exception as e:
            logger.error(f"Failed to write error log: {e}")
    
    def create_draft(self, function_name: str, args: tuple, kwargs: dict) -> str:
        """Создание черновика при ошибке"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        draft_path = os.path.join(self.draft_dir, f'draft_{function_name}_{timestamp}.json')
        
        draft_data = {
            'function': function_name,
            'timestamp': timestamp,
            'args': str(args),
            'kwargs': {k: str(v) for k, v in kwargs.items()}
        }
        
        try:
            with open(draft_path, 'w', encoding='utf-8') as f:
                json.dump(draft_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Draft created: {draft_path}")
        except Exception as e:
            logger.error(f"Failed to create draft: {e}")
        
        return draft_path
    
    def notify_admin(self, function: str, error: Exception, draft_path: str) -> None:
        """Уведомление администратора (заглушка)"""
        logger.critical(
            f"\n{'='*50}\n"
            f"CRITICAL ERROR in {function}\n"
            f"Error: {error}\n"
            f"Draft: {draft_path}\n"
            f"{'='*50}"
        )
        # TODO: Добавить уведомление через Telegram, Email или другой канал


# Глобальный экземпляр
error_handler = ErrorHandler()


if __name__ == "__main__":
    # Пример использования
    @error_handler.with_fallback
    def test_function(prompt: str, model: str):
        print(f"Testing with model: {model}")
        if "fail" in model:
            raise Exception(f"Simulated error with {model}")
        return f"Success with {model}: {prompt}"
    
    try:
        result = test_function(prompt="Hello, world!")
        print(result)
    except Exception as e:
        print(f"Final error: {e}")
