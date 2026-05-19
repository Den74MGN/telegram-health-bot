"""Тесты для FREE API клиентов"""

import os
import sys
import logging
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_free_ai_clients():
    """Тест FREE AI клиентов для генерации текста"""
    print("\n" + "="*60)
    print("🧪 Testing FREE AI Clients")
    print("="*60)
    
    try:
        from free_ai_clients import FreeAIManager
        
        # Получаем API ключи из окружения
        openrouter_key = os.getenv('OPENROUTER_API_KEY')
        huggingface_key = os.getenv('HUGGINGFACE_API_KEY')
        gemini_key = os.getenv('GEMINI_API_KEY')
        
        if not any([openrouter_key, huggingface_key, gemini_key]):
            print("\n❌ ERROR: No FREE API keys found in .env file")
            print("Please add at least one of:")
            print("  - OPENROUTER_API_KEY")
            print("  - HUGGINGFACE_API_KEY")
            print("  - GEMINI_API_KEY")
            return False
            
        # Инициализируем менеджер
        manager = FreeAIManager()
        
        # Тестовый промпт
        test_prompt = "Write a short health tip about drinking water (2 sentences)"
        
        print(f"\n📝 Test Prompt: {test_prompt}")
        print("\n🔄 Trying FREE AI providers...")
        
        result = manager.generate(test_prompt)
        
        if result:
            print("\n✅ SUCCESS: Generated text from FREE AI")
            print(f"\n📄 Result ({len(result)} chars):\n")
            print(result)
            print("\n" + "="*60)
            return True
        else:
            print("\n❌ FAILED: All FREE AI providers failed")
            print("Check your API keys and network connection")
            return False
            
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("Make sure free_ai_clients.py is in the same directory")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_free_image_generation():
    """Тест FREE генерации изображений"""
    print("\n" + "="*60)
    print("🎨 Testing FREE Image Generation")
    print("="*60)
    
    try:
        from free_image_generator import PollinationsImageGenerator, FreeImageManager
        
        # Тест Pollinations.ai (не требует API ключа!)
        print("\n🔍 Testing Pollinations.ai (100% FREE, no API key needed)...")
        
        pollinations = PollinationsImageGenerator()
        
        # Проверка подключения
        if pollinations.test_connection():
            print("✅ Pollinations.ai is available")
        else:
            print("⚠️  Pollinations.ai connection test failed (but may still work)")
        
        # Генерация тестового изображения
        test_prompt = "professional illustration of healthy lifestyle"
        print(f"\n📝 Generating image: {test_prompt}")
        print("⏳ This may take 10-30 seconds...")
        
        image_data = pollinations.generate_image(test_prompt, width=512, height=512)
        
        if image_data:
            print(f"\n✅ SUCCESS: Generated {len(image_data)} bytes")
            
            # Сохраняем тестовое изображение
            test_file = "test_free_image.jpg"
            with open(test_file, "wb") as f:
                f.write(image_data)
            print(f"💾 Saved to: {test_file}")
            print("\n" + "="*60)
            return True
        else:
            print("\n❌ FAILED: Image generation failed")
            return False
            
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("Make sure free_image_generator.py is in the same directory")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_error_handler():
    """Тест обработчика ошибок с fallback"""
    print("\n" + "="*60)
    print("🛡️  Testing Error Handler with FREE Fallback")
    print("="*60)
    
    try:
        from module_error_handler import ErrorHandler
        
        handler = ErrorHandler()
        
        print("\n✅ ErrorHandler initialized successfully")
        print("\n📋 Features:")
        print("  - Automatic retry with exponential backoff")
        print("  - Fallback to FREE AI models on failure")
        print("  - Draft creation for manual review")
        print("  - JSONL error logging")
        print("\n" + "="*60)
        return True
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_env_config():
    """Тест конфигурации .env файла"""
    print("\n" + "="*60)
    print("⚙️  Testing .env Configuration")
    print("="*60)
    
    # Проверяем наличие .env файла
    if not os.path.exists('.env'):
        print("\n⚠️  WARNING: .env file not found")
        print("Please copy .env.example to .env and add your FREE API keys")
        return False
    
    print("\n✅ .env file found")
    print("\n🔑 Checking FREE API keys:")
    
    keys_found = 0
    
    # Проверяем Telegram Bot Token
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if telegram_token:
        print("  ✅ TELEGRAM_BOT_TOKEN: Found")
        keys_found += 1
    else:
        print("  ❌ TELEGRAM_BOT_TOKEN: Missing (REQUIRED)")
    
    # Проверяем FREE AI API ключи
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key:
        print("  ✅ GEMINI_API_KEY: Found (FREE tier)")
        keys_found += 1
    else:
        print("  ⚠️  GEMINI_API_KEY: Missing (recommended)")
    
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    if openrouter_key:
        print("  ✅ OPENROUTER_API_KEY: Found (FREE models)")
        keys_found += 1
    else:
        print("  ⚠️  OPENROUTER_API_KEY: Missing (optional)")
    
    huggingface_key = os.getenv('HUGGINGFACE_API_KEY')
    if huggingface_key:
        print("  ✅ HUGGINGFACE_API_KEY: Found (FREE)")
        keys_found += 1
    else:
        print("  ⚠️  HUGGINGFACE_API_KEY: Missing (optional)")
    
    print(f"\n📊 Total keys configured: {keys_found}")
    
    if keys_found >= 2:  # Telegram + at least one AI key
        print("\n✅ Configuration is GOOD for FREE operation!")
        print("\n" + "="*60)
        return True
    else:
        print("\n❌ Insufficient configuration")
        print("Add at least TELEGRAM_BOT_TOKEN + one FREE AI key")
        print("\n" + "="*60)
        return False


def main():
    """Запуск всех тестов"""
    print("\n" + "#"*60)
    print("#" + " "*58 + "#")
    print("#" + "  🎯 FREE TELEGRAM BOT - COMPREHENSIVE TEST SUITE  ".center(58) + "#")
    print("#" + " "*58 + "#")
    print("#"*60)
    
    results = {}
    
    # Тест 1: Конфигурация
    results['env_config'] = test_env_config()
    
    # Тест 2: Error Handler
    results['error_handler'] = test_error_handler()
    
    # Тест 3: FREE AI Clients (только если есть ключи)
    if results['env_config']:
        results['ai_clients'] = test_free_ai_clients()
    else:
        print("\n⏭️  Skipping AI clients test (no API keys)")
        results['ai_clients'] = None
    
    # Тест 4: FREE Image Generation
    results['image_gen'] = test_free_image_generation()
    
    # Итоговый отчет
    print("\n" + "#"*60)
    print("#" + " "*58 + "#")
    print("#" + "  📊 TEST RESULTS SUMMARY  ".center(58) + "#")
    print("#" + " "*58 + "#")
    print("#"*60 + "\n")
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL" if result is False else "⏭️  SKIP"
        print(f"{status}  {test_name.replace('_', ' ').title()}")
        
        if result is True:
            passed += 1
        elif result is False:
            failed += 1
        else:
            skipped += 1
    
    print("\n" + "-"*60)
    print(f"\n📈 Total: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed == 0 and passed > 0:
        print("\n🎉 ALL TESTS PASSED! Your FREE bot is ready to run!")
        print("\n▶️  Start the bot with: python main.py")
    elif failed > 0:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nℹ️  Common issues:")
        print("   1. Missing API keys in .env file")
        print("   2. Network connection issues")
        print("   3. Invalid API keys")
    
    print("\n" + "#"*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
