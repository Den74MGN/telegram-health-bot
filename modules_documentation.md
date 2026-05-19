# Документация Модулей

## module_content.py

### Класс ContentGenerator

#### `__init__(openai_api_key: str)`
Инициализирует генератор контента с API ключом OpenAI.

**Параметры:**
- `openai_api_key` (str): API ключ OpenAI для доступа к GPT

#### `generate_text_post(topic: str = "health and fitness") -> Dict[str, str]`
Генерирует текстовый пост с заголовком и основным содержанием с использованием ИИ.

**Параметры:**
- `topic` (str): Тема контента. По умолчанию: "health and fitness"

**Возвращает:**
- `Dict[str, str]`: Словарь с ключами 'title' и 'body'

#### `generate_video_content(text_content: Dict[str, str], duration: int = 30) -> Optional[str]`
Создает короткое видео с субтитрами из текстового контента.

**Параметры:**
- `text_content` (Dict[str, str]): Словарь с ключами 'title' и 'body'
- `duration` (int): Длительность видео в секундах. По умолчанию: 30

**Возвращает:**
- `Optional[str]`: Путь к сгенерированному видеофайлу или None при неудаче

### Функции

#### `get_stock_video_url(query: str = "fitness") -> Optional[str]`
Получает URL стокового видео для фонового контента.

**Параметры:**
- `query` (str): Поисковый запрос. По умолчанию: "fitness"

**Возвращает:**
- `Optional[str]`: URL видео или None

## module_scheduler.py

### Класс ContentScheduler

#### `__init__()`
Инициализирует планировщик с хранилищем заданий в памяти.

#### `start_scheduler()`
Запускает экземпляр APScheduler.

#### `stop_scheduler()`
Останавливает планировщик и ждет завершения заданий.

#### `schedule_content_generation(func: Callable, interval_hours: int = 2) -> str`
Планирует генерацию контента через регулярные интервалы.

**Параметры:**
- `func` (Callable): Функция для выполнения
- `interval_hours` (int): Часы между выполнениями. По умолчанию: 2

**Возвращает:**
- `str`: ID задания

#### `schedule_publishing(func: Callable, interval_hours: int = 2) -> str`
Планирует публикацию контента через регулярные интервалы.

**Параметры:**
- `func` (Callable): Функция для выполнения
- `interval_hours` (int): Часы между выполнениями. По умолчанию: 2

**Возвращает:**
- `str`: ID задания

#### `add_job(func: Callable, trigger: Any, job_id: str, name: str) -> str`
Добавляет пользовательское задание в планировщик.

**Параметры:**
- `func` (Callable): Функция для выполнения
- `trigger` (Any): Объект триггера APScheduler
- `job_id` (str): Уникальный идентификатор задания
- `name` (str): Человеко-читаемое имя задания

**Возвращает:**
- `str`: ID задания

#### `remove_job(job_id: str) -> bool`
Удаляет задание из планировщика.

**Параметры:**
- `job_id` (str): ID задания для удаления

**Возвращает:**
- `bool`: True при успешном удалении

#### `get_jobs() -> list`
Получает список всех запланированных заданий.

**Возвращает:**
- `list`: Список объектов заданий

#### `run_once(func: Callable, *args, **kwargs)`
Выполняет функцию один раз асинхронно.

**Параметры:**
- `func` (Callable): Функция для запуска
- `*args`: Позиционные аргументы
- `**kwargs`: Именованные аргументы

## module_publisher.py

### Класс TelegramPublisher

#### `__init__(bot_token: str, channel_id: str, admin_chat_id: Optional[str] = None)`
Инициализирует Telegram публикатора.

**Параметры:**
- `bot_token` (str): Токен Telegram бота
- `channel_id` (str): ID целевого канала
- `admin_chat_id` (Optional[str]): ID чата администратора для уведомлений

#### `publish_text_post(content: Dict[str, str], ad_content: Optional[Dict[str, Any]] = None) -> bool`
Публикует текстовый пост в канал с опциональной рекламой.

**Параметры:**
- `content` (Dict[str, str]): Контент с 'title' и 'body'
- `ad_content` (Optional[Dict[str, Any]]): Данные рекламы

**Возвращает:**
- `bool`: True при успешной публикации

#### `publish_video_post(video_path: str, caption: str, ad_content: Optional[Dict[str, Any]] = None) -> bool`
Публикует видеопост в канал с опциональной рекламой.

**Параметры:**
- `video_path` (str): Путь к видеофайлу
- `caption` (str): Подпись к видео
- `ad_content` (Optional[Dict[str, Any]]): Данные рекламы

**Возвращает:**
- `bool`: True при успешной публикации

#### `test_connection() -> bool`
Тестирует подключение к Telegram API.

**Возвращает:**
- `bool`: True при успешном подключении

## module_ads.py

### Класс AdsIntegrator

#### `__init__(api_key: str, api_secret: str, base_url: str = "https://api.telega.in")`
Инициализирует интегратор рекламы.

**Параметры:**
- `api_key` (str): API ключ Telega.in
- `api_secret` (str): API секрет Telega.in
- `base_url` (str): Базовый URL API. По умолчанию: "https://api.telega.in"

#### `get_advertisement(category: str = "health", budget_min: int = 500) -> Optional[Dict[str, Any]]`
Получает доступную рекламу с маркетплейса.

**Параметры:**
- `category` (str): Категория рекламы. По умолчанию: "health"
- `budget_min` (int): Минимальный бюджет за пост. По умолчанию: 500

**Возвращает:**
- `Optional[Dict[str, Any]]`: Данные рекламы или None

#### `report_ad_performance(ad_id: str, post_id: Optional[str] = None, views: int = 0) -> bool`
Отчитывается о производительности рекламы после публикации.

**Параметры:**
- `ad_id` (str): ID рекламы
- `post_id` (Optional[str]): ID поста в Telegram
- `views` (int): Количество просмотров. По умолчанию: 0

**Возвращает:**
- `bool`: True при успешном отчете

#### `get_ad_statistics(ad_id: str) -> Optional[Dict[str, Any]]`
Получает статистику для конкретной рекламы.

**Параметры:**
- `ad_id` (str): ID рекламы

**Возвращает:**
- `Optional[Dict[str, Any]]`: Данные статистики или None

#### `validate_ad_content(ad_content: Dict[str, Any]) -> bool`
Валидирует рекламный контент перед публикацией.

**Параметры:**
- `ad_content` (Dict[str, Any]): Данные рекламы

**Возвращает:**
- `bool`: True если контент валиден

#### `get_available_budget() -> Optional[int]`
Получает доступный бюджет для рекламы.

**Возвращает:**
- `Optional[int]`: Доступный бюджет в рублях или None