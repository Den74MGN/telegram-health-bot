# 🔧 Исправление Ошибки OpenRouter 404

## ❌ Проблема

При запуске бота вы видите ошибку:
```
❌ OpenRouter ошибка: 404
```

## 🎯 Причины

Ошибка 404 от OpenRouter может возникать по следующим причинам:

1. **Неверный или устаревший API ключ**
2. **Ключ был удален или деактивирован**
3. **Ключ не имеет доступа к API**
4. **Проблемы с аккаунтом OpenRouter**

## ✅ Решение

### Шаг 1: Проверьте Ваш API Ключ

1. Откройте файл `.env`
2. Найдите строку `OPENROUTER_API_KEY=`
3. Убедитесь, что ключ:
   - Начинается с `sk-or-v1-`
   - Не содержит пробелов
   - Скопирован полностью

### Шаг 2: Создайте Новый API Ключ

1. Перейдите на [OpenRouter.ai](https://openrouter.ai)
2. Войдите в аккаунт (или зарегистрируйтесь)
3. Перейдите в **Settings** → **API Keys**
4. Нажмите **Create Key**
5. Скопируйте новый ключ

### Шаг 3: Обновите .env Файл

```env
# Замените старый ключ на новый
OPENROUTER_API_KEY=sk-or-v1-ваш_новый_ключ_здесь
```

### Шаг 4: Протестируйте Подключение

```bash
# Запустите специальный тест OpenRouter
python test_openrouter.py
```

Вы должны увидеть:
```
✅ Подключение успешно!
📊 Найдено бесплатных моделей: X
```

### Шаг 5: Запустите Бота

```bash
python main.py
```

## 🧪 Дополнительная Диагностика

### Проверка 1: Тест API Ключа

```bash
python test_openrouter.py
```

Этот скрипт покажет:
- ✅ Валиден ли ключ
- 📋 Список доступных моделей
- 📝 Тест генерации текста

### Проверка 2: Полный Тест Настройки

```bash
python test_setup.py
```

Проверит все компоненты, включая OpenRouter.

### Проверка 3: Ручной Тест

Откройте Python и выполните:

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENROUTER_API_KEY')

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://openrouter.ai/api/v1/models',
    headers=headers
)

print(f"Статус: {response.status_code}")
print(f"Ответ: {response.text[:500]}")
```

## 💡 Частые Ошибки

### Ошибка: "Ключ не найден"

**Решение**: Убедитесь, что в `.env` есть строка:
```env
OPENROUTER_API_KEY=sk-or-v1-...
```

### Ошибка: "401 Unauthorized"

**Решение**: Ключ неверный или устарел. Создайте новый.

### Ошибка: "404 Not Found"

**Решение**: 
1. Проверьте, что аккаунт активен на OpenRouter.ai
2. Создайте новый API ключ
3. Убедитесь, что ключ имеет доступ к API

### Ошибка: "429 Too Many Requests"

**Решение**: Превышен лимит запросов. Подождите 1-2 минуты.

## 🔍 Проверка Аккаунта OpenRouter

1. Зайдите на [OpenRouter.ai](https://openrouter.ai)
2. Войдите в аккаунт
3. Проверьте:
   - ✅ Аккаунт активен
   - ✅ Email подтвержден
   - ✅ Есть доступ к бесплатным моделям

## 🆓 Бесплатные Модели

OpenRouter предоставляет бесплатный доступ к моделям:

- `meta-llama/llama-3.3-70b-instruct:free`
- `google/gemma-2-9b-it:free`
- `mistralai/mistral-7b-instruct:free`
- `qwen/qwen-2-7b-instruct:free`

Убедитесь, что ваш аккаунт имеет к ним доступ.

## 🔄 Альтернативные Решения

### Вариант 1: Используйте Hugging Face

Если OpenRouter не работает, добавьте в `.env`:

```env
HUGGINGFACE_API_KEY=ваш_ключ_huggingface
```

Получить ключ: [Hugging Face Tokens](https://huggingface.co/settings/tokens)

### Вариант 2: Используйте Google Gemini

Добавьте в `.env`:

```env
GOOGLE_GEMINI_API_KEY=ваш_ключ_gemini
```

Получить ключ: [Google AI Studio](https://makersuite.google.com/app/apikey)

## 📞 Все Еще Не Работает?

1. **Проверьте интернет соединение**:
   ```bash
   ping openrouter.ai
   ```

2. **Проверьте файрвол**: Убедитесь, что Python может делать HTTP запросы

3. **Обновите зависимости**:
   ```bash
   pip install --upgrade requests python-dotenv
   ```

4. **Создайте Issue на GitHub** с логами:
   ```bash
   python test_openrouter.py > openrouter_test.log 2>&1
   ```

## ✅ Контрольный Список

- [ ] Создан новый API ключ на OpenRouter.ai
- [ ] Ключ скопирован в .env файл
- [ ] Файл .env сохранен
- [ ] Запущен `python test_openrouter.py` - успешно
- [ ] Запущен `python test_setup.py` - все тесты пройдены
- [ ] Запущен `python main.py` - бот работает

---

**После выполнения всех шагов бот должен работать!** 🎉

Если проблема сохраняется, создайте Issue на GitHub с результатами `test_openrouter.py`.
