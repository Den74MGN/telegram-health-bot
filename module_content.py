"""
Улучшенный Модуль Генерации Контента

Этот модуль обрабатывает генерацию премиум текстового и видео контента по темам здоровья и wellness.
Использует бесплатные модели через OpenRouter API для генерации текста и MoviePy для создания видео.
Поддерживает несколько ИИ моделей для лучшего качества и надежности.
"""

import os
import logging
import json
import random
from typing import Dict, Optional, List, Tuple
import requests
import requests
from datetime import datetime, timedelta
from free_image_generator import generate_image

logger = logging.getLogger(__name__)

class ContentGenerator:
    """Расширенный генератор контента с использованием бесплатных ИИ моделей."""

    def __init__(self, openrouter_api_key: str = None):
        """Инициализация с API ключом OpenRouter."""
        self.openrouter_api_key = openrouter_api_key or os.getenv('OPENROUTER_API_KEY')
        self.session = None

        # Бесплатные модели для разных задач
        self.models = {
            'text_generation': [
                'meta-llama/llama-3.3-70b-instruct:free',
                'microsoft/wizardlm-2-8x22b',
                'meta-llama/llama-3.3-70b-instruct:free',
                'mistralai/mixtral-8x7b-instruct',
                'anthropic/claude-3-haiku:beta'
            ],
            'title_generation': [
                'meta-llama/llama-3.3-70b-instruct:free',
                'microsoft/wizardlm-2-8x22b',
                'meta-llama/llama-3.3-70b-instruct:free'
            ],
            'seo_optimization': [
                'meta-llama/llama-3.3-70b-instruct:free',
                'mistralai/mixtral-8x7b-instruct'
            ]
        }

        # Темы для контента
        self.topics = [
            'здоровое питание', 'фитнес упражнения', 'ментальное здоровье',
            'йога и медитация', 'профилактика заболеваний', 'здоровый сон',
            'витамины и добавки', 'детское здоровье', 'спортивное питание',
            'антистресс техники', 'иммунитет', 'правильное дыхание'
        ]

        # Ключевые слова для SEO
        self.seo_keywords = [
            'здоровье', 'фитнес', 'ЗОЖ', 'правильное питание', 'тренировки',
            'витамины', 'иммунитет', 'йога', 'медитация', 'сон', 'стресс'
        ]

    def _make_openrouter_request(self, messages: List[Dict], model: str, max_tokens: int = 500) -> Optional[str]:
        """Сделать синхронный запрос к OpenRouter API."""
        try:
            headers = {
                'Authorization': f'Bearer {self.openrouter_api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://telegram-health-bot.com',
                'X-Title': 'Telegram Health Bot'
            }

            payload = {
                'model': model,
                'messages': messages,
                'max_tokens': max_tokens,
                'temperature': 0.7
            }

            try:
                response = requests.post(
                    'https://openrouter.ai/api/v1/chat/completions',
                    headers=headers,
                    json=payload,
                    timeout=30
                )
            except requests.exceptions.RequestException as e:
                logger.error(f"Network error: {e}")
                return None

            # Debug logging
            if response.status_code != 200:
                logger.error(f"OpenRouter response: {response.status_code} - {response.text}")

            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content'].strip()
            else:
                logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error calling OpenRouter API: {e}")
            return None
    
    def _get_fallback_content(self, topic: str) -> Dict[str, str]:
        """Возвращает запасной контент при сбое API."""
        fallback_content = {
            "здоровое питание": {
                "title": "5 простых правил здорового питания",
                "body": "🥗 Здоровое питание - основа хорошего самочувствия!\n\n1️⃣ Пейте достаточно воды - минимум 1.5-2 литра в день\n2️⃣ Ешьте больше овощей и фруктов\n3️⃣ Выбирайте цельнозерновые продукты\n4️⃣ Ограничьте сахар и соль\n5️⃣ Питайтесь регулярно, не пропускайте завтрак\n\n💪 Начните с малого - внедряйте по одной привычке в неделю!"
            },
            "фитнес упражнения": {
                "title": "Эффективная тренировка за 15 минут",
                "body": "🏃‍♀️ Нет времени на спортзал? Попробуйте эту быструю тренировку!\n\n✅ Приседания - 3 подхода по 15 раз\n✅ Отжимания - 3 подхода по 10 раз\n✅ Планка - 3 подхода по 30 секунд\n✅ Выпады - 3 подхода по 12 раз на каждую ногу\n\n💡 Делайте эту тренировку 3-4 раза в неделю, и результат не заставит себя ждать!"
            },
            "default": {
                "title": "Здоровый образ жизни: с чего начать?",
                "body": "🌟 Хотите улучшить свое здоровье? Начните с этих простых шагов:\n\n💧 Пейте больше воды\n🚶‍♂️ Больше двигайтесь\n😴 Высыпайтесь (7-8 часов)\n🥗 Питайтесь сбалансированно\n🧘‍♀️ Управляйте стрессом\n\n✨ Помните: маленькие шаги ведут к большим переменам!"
            }
        }
        
        content = fallback_content.get(topic, fallback_content["default"])
        return {
            "title": content["title"],
            "body": content["body"],
            "seo_keywords": ["здоровье", "фитнес", "ЗОЖ"],
            "hashtags": ["#здоровье", "#фитнес", "#ЗОЖ", "#мотивация"],
            "topic": topic
        }

    def _select_best_model(self, task_type: str) -> str:
        """Выбрать лучшую доступную модель для задачи."""
        available_models = self.models.get(task_type, self.models['text_generation'])
        return random.choice(available_models)

    def generate_text_post(self, topic: str = None) -> Dict[str, str]:
        """
        Генерирует премиум текстовый пост с заголовком и основным текстом.

        Args:
            topic (str): Тема для генерации контента. Если None, выбирается автоматически.

        Returns:
            Dict[str, str]: Словарь с ключами 'title', 'body', 'seo_keywords', 'hashtags'.
        """
        try:
            # Выбираем тему если не указана
            if topic is None:
                topic = random.choice(self.topics)

            # Генерируем УЛУЧШЕННЫЙ заголовок
            title_prompt = f"""
            КРИТИЧЕСКИ ВАЖНО: Отвечай ИСКЛЮЧИТЕЛЬНО на русском языке!
            
            Создай МАКСИМАЛЬНО привлекательный и кликабельный заголовок для статьи о здоровье на тему "{topic}".
            
            ОБЯЗАТЕЛЬНЫЕ требования к заголовку:
            - Длина: 30-50 символов (оптимально для Telegram)
            - ОБЯЗАТЕЛЬНО содержит цифры (3, 5, 7, 10) ИЛИ вопрос
            - Интригующий, вызывающий любопытство
            - Обещает конкретную пользу
            - Простой и понятный язык
            - ТОЛЬКО на русском языке, без английских слов

            ЛУЧШИЕ примеры заголовков (используй как образец):
            
            С цифрами:
            - "5 упражнений для идеальной осанки"
            - "7 продуктов для крепкого иммунитета"
            - "3 минуты йоги для снятия стресса"
            - "10 правил здорового завтрака"
            
            С вопросами:
            - "Как улучшить сон за 7 дней?"
            - "Почему вода важнее витаминов?"
            - "Что съесть перед тренировкой?"
            - "Когда лучше заниматься спортом?"
            
            Комбинированные:
            - "5 причин пить воду утром"
            - "3 ошибки в питании: как исправить?"
            - "7 способов победить усталость"
            
            Создай ОДИН заголовок, который:
            - Цепляет внимание с первого взгляда
            - Обещает быстрый и понятный результат
            - Мотивирует прочитать пост
            
            Верни ТОЛЬКО заголовок на русском языке, без кавычек, пояснений и дополнительного текста!
            """

            title_model = self._select_best_model('title_generation')
            title_messages = [{"role": "user", "content": title_prompt}]

            title = self._make_openrouter_request(title_messages, title_model, max_tokens=100)
            if not title:
                title = f"Эффективные советы по {topic}"

            # Генерируем основной текст (УЛУЧШЕННЫЙ оптимизированный для Telegram)
            body_prompt = f"""
            КРИТИЧЕСКИ ВАЖНО: Пиши ИСКЛЮЧИТЕЛЬНО на русском языке! Ни одного английского слова!
            
            Напиши увлекательную и полезную статью о "{topic}" для русскоязычного Telegram канала о здоровье и wellness.

            СТРОГОЕ ОГРАНИЧЕНИЕ - Telegram: максимум 600 символов!

            ОБЯЗАТЕЛЬНЫЕ требования к контенту:
            - Длина: 400-600 символов (строго!)
            - 3-5 конкретных, практичных и применимых советов
            - Короткие энергичные абзацы (2-3 предложения)
            - Простой, живой и понятный русский язык
            - Используй 2-3 подходящих эмодзи: 💪🏃‍♀️🥗🧘‍♀️💧🌟✨🔥⚡️
            - Мотивирующий призыв к действию в конце
            - Дружелюбный и вдохновляющий тон
            - Избегай медицинского жаргона

            ИДЕАЛЬНАЯ структура:
            1. Яркое вступление с вопросом или фактом (1-2 предложения)
            2. Нумерованный список практических советов с эмодзи (3-5 пунктов)
            3. Мотивирующий призыв к действию (1 предложение)

            ПРИМЕРЫ отличного контента:

            Пример 1:
            "💪 Хотите больше энергии каждый день? Вот 4 простых привычки:
            
            1️⃣ Начинайте утро со стакана воды с лимоном
            2️⃣ Делайте 10-минутную зарядку после пробуждения
            3️⃣ Ешьте белковый завтрак в течение часа
            4️⃣ Гуляйте 20 минут на свежем воздухе
            
            ⚡️ Попробуйте хотя бы одну привычку завтра - почувствуйте разницу!"

            Пример 2:
            "🌟 Знаете ли вы, что качество сна влияет на всё? Улучшите его за 3 шага:
            
            1️⃣ Ложитесь спать в одно время каждый день
            2️⃣ Проветривайте спальню перед сном
            3️⃣ Откажитесь от гаджетов за час до сна
            
            💤 Начните сегодня - ваше тело скажет спасибо!"
            
            Пиши КРАТКО, ЭНЕРГИЧНО, МОТИВИРУЮЩЕ и ТОЛЬКО на русском языке!
            Каждое слово должно быть ценным и полезным для читателя!
            """

            body_model = self._select_best_model('text_generation')
            body_messages = [{"role": "user", "content": body_prompt}]

            body = self._make_openrouter_request(body_messages, body_model, max_tokens=500)
            if not body:
                body = f"Изучайте основы {topic} для улучшения вашего здоровья. Начните с малого и постепенно внедряйте полезные привычки в свою жизнь."
            
            # Обрезаем текст если слишком длинный (оставляем место для заголовка и хэштегов)
            if len(body) > 700:
                body = body[:697] + "..."
                logger.warning(f"Body text truncated to 700 characters")

            # Генерируем SEO ключевые слова
            seo_keywords = self._generate_seo_keywords(topic)

            # Генерируем хэштеги (максимум 5 для компактности)
            hashtags = self._generate_hashtags(topic)[:5]

            # Генерируем изображение для поста с улучшенным промптом
            image_bytes = None
            try:
                # Создаем детальный промпт для качественного изображения
                image_prompt = self._create_image_prompt(title, topic)
                logger.info(f"Generating image with prompt: {image_prompt[:100]}...")
                image_bytes = generate_image(image_prompt)
                if image_bytes:
                    logger.info(f"Successfully generated image ({len(image_bytes)} bytes)")
                else:
                    logger.warning("Image generation returned None")
            except Exception as e:
                logger.error(f"Error generating image: {e}")
                # Продолжаем без изображения, текстовый контент важнее

            return {
                "title": title.strip('"\''),
                "body": body,
                "seo_keywords": seo_keywords,
                "hashtags": hashtags,
                "topic": topic,
                "image_bytes": image_bytes
            }

        except Exception as e:
            logger.error(f"Не удалось сгенерировать текстовый контент: {e}")
            # Возвращаем запасной контент
            return {
                "title": "Полезные советы для вашего здоровья",
                "body": "Поддерживайте здоровый образ жизни с помощью регулярных физических упражнений и сбалансированного питания. Начните с малого - даже 15 минут активности в день могут значительно улучшить ваше самочувствие.",
                "seo_keywords": ["здоровье", "фитнес", "ЗОЖ"],
                "hashtags": ["#здоровье", "#фитнес", "#ЗОЖ"],
                "topic": "здоровье"
            }
    
    def _create_image_prompt(self, title: str, topic: str) -> str:
        """
        Создает улучшенный детальный промпт для генерации качественного изображения.
        
        Args:
            title: Заголовок поста
            topic: Тема поста
            
        Returns:
            str: Детальный промпт для генерации изображения
        """
        # МАКСИМАЛЬНО УЛУЧШЕННЫЕ стили с особым вниманием к анатомии человека
        topic_styles = {
            'здоровое питание': 'vibrant fresh organic fruits and vegetables arranged beautifully on rustic wooden table, colorful healthy food flat lay top view, natural daylight photography, appetizing food styling, nutritious meal composition, farm-to-table aesthetic, clean eating concept, NO people, focus on food only',
            
            'фитнес упражнения': 'professional fitness photography: athletic person with PERFECT ANATOMICALLY CORRECT body proportions doing exercise, REALISTIC human anatomy with correct number of fingers (5 per hand), proper arm and leg positioning, natural facial features with symmetrical eyes and nose, dynamic fitness action shot, modern gym or outdoor park setting, motivational sports photography, energetic movement, professional athletic lighting, inspiring workout scene, photorealistic human body',
            
            'ментальное здоровье': 'serene peaceful meditation scene with person in calm contemplative state, CORRECT facial anatomy with natural expression, properly proportioned hands in meditation mudra (5 fingers each), soft natural lighting, tranquil zen atmosphere, mindfulness concept, gentle pastel colors, mental wellness imagery, peaceful natural environment, photorealistic human features',
            
            'йога и медитация': 'graceful yoga practitioner with PERFECT HUMAN ANATOMY in asana pose, CORRECT body proportions and limb positioning, natural facial features with realistic skin texture, properly formed hands and feet (5 fingers, 5 toes), peaceful yoga studio or nature setting, soft warm lighting, zen minimalist aesthetic, spiritual wellness concept, balanced composition, calming atmosphere, photorealistic human body',
            
            'профилактика заболеваний': 'modern healthcare wellness concept, clean medical illustration or abstract health imagery, preventive medicine concept, bright clinical aesthetic, trust and care atmosphere, medical professionalism, AVOID showing people to prevent anatomy issues, focus on medical symbols and abstract concepts',
            
            'здоровый сон': 'cozy peaceful bedroom with comfortable bed, soft bedding in calming blue and white tones, gentle evening lighting, relaxing sleep environment, tranquil bedroom interior, restful atmosphere, sleep hygiene concept, empty bed or person sleeping with face partially hidden by pillow (to avoid facial anatomy issues)',
            
            'витамины и добавки': 'colorful array of vitamins and natural supplements beautifully arranged, healthy lifestyle products, bright clean product photography, wellness and nutrition concept, vibrant health imagery, NO people, focus on products only',
            
            'детское здоровье': 'happy healthy children playing actively with CORRECT child anatomy, natural facial expressions, properly proportioned bodies and limbs, realistic hands with 5 fingers each, joyful family wellness moment, bright cheerful colors, safe nurturing environment, positive childhood health concept, warm family atmosphere, photorealistic children',
            
            'спортивное питание': 'nutritious protein-rich healthy foods artfully arranged on modern plate, athletic meal prep concept, fresh wholesome ingredients, fitness nutrition photography, clean eating for athletes, energizing food composition, NO people, focus on food presentation',
            
            'антистресс техники': 'peaceful stress relief scene with person relaxing, CORRECT human anatomy if person shown, natural facial features, properly formed hands (5 fingers), soothing colors and soft lighting, wellness and relaxation concept, tranquil stress-free atmosphere, mindful moment, OR abstract relaxation imagery without people',
            
            'иммунитет': 'vibrant immune system boost concept with fresh fruits and vegetables, healthy lifestyle imagery, wellness and vitality theme, energetic bright colors, strong health visualization, natural immunity concept, NO people, focus on healthy foods and abstract health symbols',
            
            'правильное дыхание': 'person practicing breathing exercises with CORRECT facial anatomy and natural expression, properly proportioned body, realistic hands positioned naturally, peaceful setting, mindful breathing technique, calm serene atmosphere, wellness and meditation concept, fresh air and nature imagery, photorealistic human features'
        }
        
        # Получаем улучшенный стиль для темы или используем общий
        style = topic_styles.get(topic, 'professional health and wellness concept photography, clean modern aesthetic, inspiring lifestyle imagery, vibrant natural colors, motivational wellness scene')
        
        # Создаем МАКСИМАЛЬНО УЛУЧШЕННЫЙ промпт с критическим вниманием к анатомии
        prompt = f"""Professional high-quality health and wellness photography: {title}. 

Visual style: {style}

CRITICAL HUMAN ANATOMY REQUIREMENTS (if people present):
- PERFECT anatomically correct human body proportions
- EXACTLY 5 fingers on each hand, clearly visible and naturally positioned
- EXACTLY 5 toes on each foot if visible
- Symmetrical facial features: 2 eyes, 1 nose, 1 mouth, 2 ears
- Natural realistic skin texture and tone
- Correct limb proportions and joint positioning
- Natural human poses without distortion
- Realistic hair and facial features
- Professional model-quality human representation
- NO extra limbs, NO missing fingers, NO distorted faces
- NO anatomical abnormalities or mutations

Technical requirements:
- Ultra high resolution, 8K quality, photorealistic rendering
- Professional studio lighting or natural golden hour light
- Sharp focus on subject, perfect exposure, balanced composition
- Vibrant saturated colors, appealing color grading
- Clean uncluttered background, modern aesthetic
- Instagram-worthy, magazine cover quality
- Motivational, inspiring, and uplifting mood
- Professional commercial photography standard
- No text, no watermarks, no logos, no UI elements

Negative prompt (what to AVOID):
- Deformed hands or fingers
- Extra or missing limbs
- Distorted facial features
- Unrealistic body proportions
- Blurry or low quality
- Cartoon or anime style
- Artificial or fake looking
- Bad anatomy

Style: modern, clean, professional, photorealistic, appealing, motivational, wellness-focused, anatomically perfect"""
        
        return prompt

    def _generate_seo_keywords(self, topic: str) -> List[str]:
        """Генерирует SEO ключевые слова для контента."""
        try:
            prompt = f"""
            ВАЖНО: Отвечай ТОЛЬКО на русском языке! Никакого английского или других языков!
            
            Придумай 5-7 ключевых слов на русском языке для статьи о "{topic}".
            Ключевые слова должны быть:
            - ОБЯЗАТЕЛЬНО на русском языке
            - Релевантными теме
            - Популярными в поиске
            
            Верни только ключевые слова через запятую, без английских слов.
            Пример: здоровье, фитнес, питание, тренировки, витамины
            """

            model = self._select_best_model('seo_optimization')
            messages = [{"role": "user", "content": prompt}]

            response = self._make_openrouter_request(messages, model, max_tokens=150)
            if response:
                keywords = [kw.strip() for kw in response.split(',') if kw.strip()]
                # Фильтруем только русские слова
                russian_keywords = [kw for kw in keywords if any(ord(c) >= 1040 and ord(c) <= 1103 for c in kw)]
                if russian_keywords:
                    return russian_keywords[:7]

            return ["здоровье", "фитнес", "ЗОЖ"]

        except Exception as e:
            logger.error(f"Ошибка генерации SEO ключевых слов: {e}")
            return ["здоровье", "фитнес", "ЗОЖ"]

    def _generate_hashtags(self, topic: str) -> List[str]:
        """Генерирует хэштеги для поста."""
        try:
            base_hashtags = ["#здоровье", "#фитнес", "#ЗОЖ", "#мотивация"]
            topic_hashtags = [f"#{topic.replace(' ', '')}", f"#{topic.split()[0]}"]

            # Добавляем случайные тематические хэштеги
            additional_hashtags = [
                "#спорт", "#питание", "#красота", "#энергия",
                "#саморазвитие", "#активность", "#баланс"
            ]

            all_hashtags = base_hashtags + topic_hashtags + random.sample(additional_hashtags, 3)
            return list(set(all_hashtags))[:8]  # Максимум 8 хэштегов

        except Exception as e:
            logger.error(f"Ошибка генерации хэштегов: {e}")
            return ["#здоровье", "#фитнес", "#ЗОЖ"]

    def generate_video_content(self, text_content: Dict[str, str], duration: int = 30) -> Optional[str]:
        """
        Генерация видео отключена - требует установки moviepy и ffmpeg.
        
        Args:
            text_content (Dict[str, str]): Контент с заголовком и текстом
            duration (int): Длительность видео в секундах

        Returns:
            Optional[str]: Путь к созданному видео (всегда None)
        """
        logger.info("ℹ️ Генерация видео отключена (требует установки moviepy и ffmpeg)")
        return None

    def generate_content_series(self, days: int = 7) -> List[Dict]:
        """
        Генерирует серию контента для публикации.

        Args:
            days (int): Количество дней для планирования

        Returns:
            List[Dict]: Список контента для публикации
        """
        content_series = []

        for day in range(days):
            # Выбираем тему для каждого дня
            topic = random.choice(self.topics)

            # Генерируем контент
            content = self.generate_text_post(topic)

            # Добавляем метаданные для планирования
            content['scheduled_date'] = datetime.now() + timedelta(days=day)
            content['priority'] = random.choice(['high', 'medium', 'low'])
            content['target_audience'] = random.choice(['general', 'beginners', 'advanced'])

            content_series.append(content)

        return content_series

    def optimize_content_for_engagement(self, content: Dict[str, str]) -> Dict[str, str]:
        """
        Оптимизирует контент для максимального вовлечения аудитории.

        Args:
            content (Dict[str, str]): Исходный контент

        Returns:
            Dict[str, str]: Оптимизированный контент
        """
        try:
            # Анализируем длину текста
            word_count = len(content['body'].split())

            if word_count < 150:
                # Добавляем больше деталей
                enhancement_prompt = f"""
                Расширь этот текст о здоровье, добавив больше практических советов:

                Исходный текст: {content['body']}

                Добавь:
                - 2-3 конкретных примера
                - Рекомендации экспертов
                - Мотивационный призыв к действию
                """
                model = self._select_best_model('text_generation')
                enhanced_body = self._make_openrouter_request(
                    [{"role": "user", "content": enhancement_prompt}],
                    model,
                    max_tokens=600
                )
                if enhanced_body:
                    content['body'] = enhanced_body

            # Оптимизируем заголовок для кликабельности
            if '?' not in content['title'] and any(char.isdigit() for char in content['title']) == False:
                # Добавляем цифры или вопрос для лучшего CTR
                content['title'] = content['title'].replace(
                    'Как', '5 способов, как'
                ).replace(
                    'Что', 'Что делать, если'
                ).replace(
                    'Почему', '7 причин, почему'
                )

            return content

        except Exception as e:
            logger.error(f"Ошибка оптимизации контента: {e}")
            return content

    def get_content_analytics(self) -> Dict:
        """
        Возвращает аналитику по контенту.

        Returns:
            Dict: Статистика по контенту
        """
        try:
            # Читаем статистику из файла если существует
            stats_file = 'logs/content_stats.json'
            if os.path.exists(stats_file):
                with open(stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {
                    'total_posts': 0,
                    'average_engagement': 0,
                    'top_topics': [],
                    'best_time_to_post': '10:00'
                }
        except Exception as e:
            logger.error(f"Ошибка чтения аналитики: {e}")
            return {}

def get_stock_video_url(query: str = "fitness") -> Optional[str]:
    """
    Получает URL стокового видео для фонового контента.
    Использует бесплатные источники стокового видео.

    Args:
        query (str): Поисковый запрос для видео

    Returns:
        Optional[str]: URL к стоковому видео
    """
    try:
        # Бесплатные источники стокового видео
        free_video_sources = [
            f"https://www.pexels.com/search/videos/{query}/",
            f"https://pixabay.com/videos/search/{query}/"
        ]

        # В будущем можно интегрировать с бесплатными API
        # Пока возвращаем None для использования текстового видео
        return None

    except Exception as e:
        logger.error(f"Ошибка получения стокового видео: {e}")

        return None


