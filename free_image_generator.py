"""Бесплатная генерация изображений через Pollinations.ai"""

import requests
import logging
from typing import Optional
import time

logger = logging.getLogger(__name__)


class PollinationsImageGenerator:
    """100% БЕСПЛАТНЫЙ генератор изображений через Pollinations.ai
    
    Особенности:
    - Не требует API ключа
    - Абсолютно бесплатно
    - Без ограничений
    - Высокое качество изображений
    """
    
    def __init__(self):
        self.base_url = "https://image.pollinations.ai/prompt"
        self.timeout = 30
        
    def generate_image(self, prompt: str, width: int = 1024, height: int = 1024) -> Optional[bytes]:
        """Генерация изображения через Pollinations.ai
        
        Args:
            prompt: Текстовый промпт
            width: Ширина изображения (default: 1024)
            height: Высота изображения (default: 1024)
            
        Returns:
            bytes: Изображение в виде байтов или None при ошибке
        """
        try:
            # Pollinations.ai - это 100% бесплатный сервис
            url = f"{self.base_url}/{requests.utils.quote(prompt)}"
            params = {
                "width": width,
                "height": height,
                "nologo": "true",
                "enhance": "true"
            }
            
            logger.info(f"Generating FREE image via Pollinations.ai: {prompt[:50]}...")
            
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            logger.info(f"Successfully generated image: {len(response.content)} bytes")
            return response.content
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout generating image: {prompt[:50]}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error generating image: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
            
    def generate_health_image(self, health_topic: str, style: str = "professional") -> Optional[bytes]:
        """Генерация изображения на тему здоровья
        
        Args:
            health_topic: Тема здоровья (например, "hydration", "exercise")
            style: Стиль изображения
            
        Returns:
            bytes: Изображение или None
        """
        prompts = {
            "hydration": f"Professional {style} illustration of water drinking, healthy lifestyle, clean blue water, fresh and vibrant",
            "exercise": f"Professional {style} illustration of fitness and exercise, healthy active person, motivational",
            "nutrition": f"Professional {style} illustration of healthy food, fresh vegetables and fruits, balanced diet",
            "sleep": f"Professional {style} illustration of peaceful sleep, bedroom, relaxation and rest",
            "mental_health": f"Professional {style} illustration of mental wellness, meditation, calm and peaceful",
            "default": f"Professional {style} illustration of healthy lifestyle, wellness and wellbeing"
        }
        
        prompt = prompts.get(health_topic, prompts["default"])
        return self.generate_image(prompt)
        
    def test_connection(self) -> bool:
        """Тест соединения с Pollinations.ai
        
        Returns:
            bool: True если сервис доступен
        """
        try:
            test_prompt = "test"
            url = f"{self.base_url}/{test_prompt}"
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except:
            return False


class HuggingFaceImageGenerator:
    """БЕСПЛАТНЫЙ генератор через Hugging Face Inference API
    
    Требует бесплатный API ключ от Hugging Face
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = "stabilityai/stable-diffusion-2-1"  # Бесплатная модель
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.timeout = 60
        
    def generate_image(self, prompt: str, retry_count: int = 3) -> Optional[bytes]:
        """Генерация изображения через Hugging Face
        
        Args:
            prompt: Текстовый промпт
            retry_count: Количество попыток
            
        Returns:
            bytes: Изображение или None
        """
        for attempt in range(retry_count):
            try:
                logger.info(f"Generating FREE image via Hugging Face (attempt {attempt+1}): {prompt[:50]}...")
                
                payload = {"inputs": prompt}
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 503:
                    # Модель загружается, ждем
                    logger.info("Model loading, waiting 20 seconds...")
                    time.sleep(20)
                    continue
                    
                response.raise_for_status()
                logger.info(f"Successfully generated image: {len(response.content)} bytes")
                return response.content
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error on attempt {attempt+1}: {e}")
                if attempt < retry_count - 1:
                    time.sleep(5)
                    
        return None


class FreeImageManager:
    """Менеджер для работы с БЕСПЛАТНЫМИ генераторами изображений
    
    Автоматический fallback между сервисами
    """
    
    def __init__(self, huggingface_key: Optional[str] = None):
        """Инициализация менеджера
        
        Args:
            huggingface_key: Опциональный API ключ для Hugging Face
        """
        self.pollinations = PollinationsImageGenerator()
        self.huggingface = HuggingFaceImageGenerator(huggingface_key) if huggingface_key else None
        
    def generate(self, prompt: str, preferred_service: str = "pollinations") -> Optional[bytes]:
        """Генерация изображения с автоматическим fallback
        
        Args:
            prompt: Текстовый промпт
            preferred_service: Предпочтительный сервис ("pollinations" или "huggingface")
            
        Returns:
            bytes: Изображение или None
        """
        services = [
            ("pollinations", self.pollinations),
            ("huggingface", self.huggingface)
        ]
        
        # Сортируем по предпочтению
        if preferred_service == "huggingface" and self.huggingface:
            services.reverse()
            
        for service_name, service in services:
            if service is None:
                continue
                
            try:
                logger.info(f"Trying {service_name} for image generation")
                image_data = service.generate_image(prompt)
                
                if image_data:
                    logger.info(f"Successfully generated via {service_name}")
                    return image_data
                else:
                    logger.warning(f"{service_name} failed, trying next service")
                    
            except Exception as e:
                logger.error(f"Error with {service_name}: {e}")
                continue
                
        logger.error("All FREE image generation services failed")
        return None
        

# Глобальный экземпляр
free_image_gen = None


def init_free_image_generator(huggingface_key: Optional[str] = None) -> FreeImageManager:
    """Инициализация глобального генератора изображений
    
    Args:
        huggingface_key: Опциональный ключ для Hugging Face
        
    Returns:
        FreeImageManager: Инициализированный менеджер
    """
    global free_image_gen
    free_image_gen = FreeImageManager(huggingface_key)
    return free_image_gen


def generate_image(prompt: str, width: int = 1024, height: int = 1024) -> Optional[bytes]:
    """Главная функция для генерации изображений (используется в module_content.py)
    
    Args:
        prompt: Текстовый промпт для генерации
        width: Ширина изображения
        height: Высота изображения
        
    Returns:
        bytes: Изображение в виде байтов или None при ошибке
    """
    global free_image_gen
    
    # Инициализируем менеджер если еще не создан
    if free_image_gen is None:
        import os
        huggingface_key = os.getenv('HUGGINGFACE_API_KEY')
        free_image_gen = FreeImageManager(huggingface_key)
    
    # Генерируем изображение
    return free_image_gen.generate(prompt)


if __name__ == "__main__":
    # Тест генерации
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    gen = PollinationsImageGenerator()
    
    print("Testing Pollinations.ai connection...")
    if gen.test_connection():
        print("✓ Pollinations.ai is available (100% FREE!)")
    else:
        print("✗ Pollinations.ai connection failed")
        sys.exit(1)
        
    print("\nGenerating test image...")
    image_data = gen.generate_image("professional illustration of healthy lifestyle")
    
    if image_data:
        print(f"✓ Generated image: {len(image_data)} bytes")
        
        # Сохраняем тестовое изображение
        with open("test_image.jpg", "wb") as f:
            f.write(image_data)
        print("✓ Saved to test_image.jpg")
    else:
        print("✗ Image generation failed")
