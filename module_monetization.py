"""
Расширенный Модуль Монетизации

Этот модуль интегрирует множественные источники монетизации:
- Реклама через Telega.in
- Партнерские программы
- Аффилиат маркетинг
- Спонсорский контент
- Донаты и подписки
"""

import os
import json
import logging
import random
from typing import Dict, List, Optional, Any
import aiohttp
import asyncio
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class MonetizationManager:
    """Управление множественными источниками монетизации."""

    def __init__(self, telegain_api_key: str = None, telegain_api_secret: str = None):
        """Инициализация менеджера монетизации."""
        self.telegain_api_key = telegain_api_key or os.getenv('TELEGIN_API_KEY')
        self.telegain_api_secret = telegain_api_secret or os.getenv('TELEGIN_API_SECRET')

        # Проверяем, отключена ли монетизация
        self.monetization_enabled = (self.telegain_api_key not in ['disabled', None, ''] and
                                   self.telegain_api_secret not in ['disabled', None, ''])

        # Партнерские программы
        self.affiliate_programs = {
            'fitness_equipment': {
                'name': 'Спорттовары',
                'base_url': 'https://partner.sport.com',
                'commission': 0.15,
                'categories': ['тренажеры', 'спортивное питание', 'одежда']
            },
            'health_supplements': {
                'name': 'Витамины и добавки',
                'base_url': 'https://partner.health.com',
                'commission': 0.20,
                'categories': ['витамины', 'пробиотики', 'омега-3']
            },
            'online_courses': {
                'name': 'Онлайн курсы',
                'base_url': 'https://partner.courses.com',
                'commission': 0.30,
                'categories': ['йога', 'медитация', 'питание']
            }
        }

        # Спонсорский контент
        self.sponsored_content = [
            {
                'brand': 'Fitness Pro',
                'product': 'Протеиновые батончики',
                'message': '💪 Попробуйте новые протеиновые батончики Fitness Pro - идеальный перекус для активных людей!',
                'payment': 800
            },
            {
                'brand': 'Yoga Studio',
                'product': 'Онлайн занятия йогой',
                'message': '🧘‍♀️ Присоединяйтесь к онлайн занятиям йогой в Yoga Studio - гибкое тело за 30 дней!',
                'payment': 1200
            },
            {
                'brand': 'Vitamin Plus',
                'product': 'Комплекс витаминов',
                'message': '🌿 Укрепите иммунитет с комплексом витаминов Vitamin Plus - натуральная защита организма!',
                'payment': 600
            }
        ]

        # Ключевые слова для монетизации
        self.monetization_keywords = {
            'фитнес': ['тренажеры', 'спортивное питание', 'одежда'],
            'питание': ['витамины', 'пробиотики', 'здоровое питание'],
            'йога': ['коврики', 'онлайн курсы', 'медитация'],
            'здоровье': ['витамины', 'диагностика', 'профилактика']
        }

    def get_monetization_opportunities(self, content_topic: str) -> List[Dict]:
        """
        Получает возможности монетизации для контента.

        Args:
            content_topic (str): Тема контента

        Returns:
            List[Dict]: Список возможностей монетизации
        """
        # Проверяем, включена ли монетизация
        if not self.monetization_enabled:
            logger.info("Монетизация отключена - возвращаем пустой список")
            return []

        opportunities = []

        try:
            # Партнерские ссылки (бесплатные)
            affiliate_links = self._get_affiliate_links(content_topic)
            opportunities.extend(affiliate_links)

            # Спонсорский контент (бесплатные)
            sponsored_content = self._get_sponsored_content(content_topic)
            opportunities.extend(sponsored_content)

            # Сортируем по потенциальному доходу
            opportunities.sort(key=lambda x: x.get('potential_revenue', 0), reverse=True)

            return opportunities[:3]  # Возвращаем топ 3 возможности

        except Exception as e:
            logger.error(f"Ошибка получения возможностей монетизации: {e}")
            return []

    def _get_telega_ads(self, topic: str) -> List[Dict]:
        """Получает рекламу через Telega.in."""
        # Проверяем, включена ли монетизация
        if not self.monetization_enabled:
            return []

        ads = []

        try:
            # Имитируем получение рекламы через Telega.in
            # В реальности здесь будет API вызов

            mock_ads = [
                {
                    'type': 'telega_in',
                    'advertiser': 'Fitness Brand',
                    'message': 'Специальное предложение для любителей фитнеса! Скидка 20% на спортивное питание.',
                    'payment': 750,
                    'potential_revenue': 750,
                    'requirements': '1000+ подписчиков'
                },
                {
                    'type': 'telega_in',
                    'advertiser': 'Health Store',
                    'message': 'Натуральные витамины для иммунитета - укрепите здоровье всей семьи!',
                    'payment': 500,
                    'potential_revenue': 500,
                    'requirements': '500+ подписчиков'
                }
            ]

            # Фильтруем по теме
            for ad in mock_ads:
                if any(keyword in topic for keyword in ['фитнес', 'питание', 'здоровье']):
                    ads.append(ad)

            return ads

        except Exception as e:
            logger.error(f"Ошибка получения Telega.in рекламы: {e}")
            return []

    def _get_affiliate_links(self, topic: str) -> List[Dict]:
        """Получает партнерские ссылки."""
        links = []

        try:
            # Находим подходящие партнерские программы
            for program_name, program_data in self.affiliate_programs.items():
                for category in program_data['categories']:
                    if category in topic:
                        link = {
                            'type': 'affiliate',
                            'program': program_data['name'],
                            'product': f'Лучшие товары для {topic}',
                            'affiliate_url': f"{program_data['base_url']}/ref/healthbot",
                            'commission': program_data['commission'],
                            'potential_revenue': 300,  # Ожидаемый доход
                            'message': f'🔗 Рекомендую проверенные товары для {topic} с партнерской скидкой!'
                        }
                        links.append(link)
                        break

            return links

        except Exception as e:
            logger.error(f"Ошибка получения партнерских ссылок: {e}")
            return []

    def _get_sponsored_content(self, topic: str) -> List[Dict]:
        """Получает спонсорский контент."""
        sponsored = []

        try:
            # Фильтруем спонсорский контент по теме
            for content in self.sponsored_content:
                if any(keyword in topic for keyword in ['фитнес', 'йога', 'здоровье', 'питание']):
                    sponsored.append({
                        'type': 'sponsored',
                        'brand': content['brand'],
                        'message': content['message'],
                        'payment': content['payment'],
                        'potential_revenue': content['payment']
                    })

            return sponsored

        except Exception as e:
            logger.error(f"Ошибка получения спонсорского контента: {e}")
            return []

    def integrate_monetization_into_content(self, content: Dict, monetization_options: List[Dict]) -> Dict:
        """
        Интегрирует монетизацию в контент.

        Args:
            content (Dict): Исходный контент
            monetization_options (List[Dict]): Варианты монетизации

        Returns:
            Dict: Контент с монетизацией
        """
        try:
            if not monetization_options:
                return content

            # Выбираем лучший вариант монетизации
            best_option = monetization_options[0]

            # Интегрируем в зависимости от типа
            if best_option['type'] == 'telega_in':
                content['body'] += f"\n\n📢 *Реклама*\n{best_option['message']}"

            elif best_option['type'] == 'affiliate':
                content['body'] += f"\n\n{best_option['message']}\n🔗 {best_option['affiliate_url']}"

            elif best_option['type'] == 'sponsored':
                content['body'] += f"\n\n💎 *Спонсорский контент*\n{best_option['message']}"

            # Добавляем метаданные монетизации
            content['monetization'] = {
                'type': best_option['type'],
                'revenue': best_option['potential_revenue'],
                'brand': best_option.get('brand', ''),
                'timestamp': datetime.now().isoformat()
            }

            return content

        except Exception as e:
            logger.error(f"Ошибка интеграции монетизации: {e}")
            return content

    async def track_revenue(self, post_id: str, monetization_data: Dict):
        """
        Отслеживает доход от монетизации.

        Args:
            post_id (str): ID поста
            monetization_data (Dict): Данные монетизации
        """
        try:
            revenue_record = {
                'post_id': post_id,
                'timestamp': datetime.now().isoformat(),
                'monetization_type': monetization_data.get('type'),
                'revenue': monetization_data.get('revenue', 0),
                'brand': monetization_data.get('brand', ''),
                'status': 'tracked'
            }

            # Сохраняем в файл для аналитики
            revenue_file = 'logs/revenue_tracking.json'
            existing_data = []

            if os.path.exists(revenue_file):
                try:
                    with open(revenue_file, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                except:
                    existing_data = []

            existing_data.append(revenue_record)

            with open(revenue_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)

            logger.info(f"Отслежен доход: {monetization_data.get('revenue', 0)} RUB от {monetization_data.get('type', 'unknown')}")

        except Exception as e:
            logger.error(f"Ошибка отслеживания дохода: {e}")

    def get_revenue_report(self) -> Dict:
        """
        Генерирует отчет по доходам.

        Returns:
            Dict: Статистика доходов
        """
        try:
            revenue_file = 'logs/revenue_tracking.json'

            if not os.path.exists(revenue_file):
                return self._get_empty_revenue_report()

            with open(revenue_file, 'r', encoding='utf-8') as f:
                revenue_data = json.load(f)

            if not revenue_data:
                return self._get_empty_revenue_report()

            # Анализируем доходы
            total_revenue = sum(record.get('revenue', 0) for record in revenue_data)
            revenue_by_type = defaultdict(float)

            for record in revenue_data:
                monetization_type = record.get('monetization_type', 'unknown')
                revenue_by_type[monetization_type] += record.get('revenue', 0)

            # Доходы за последние 30 дней
            thirty_days_ago = datetime.now() - timedelta(days=30)
            recent_revenue = sum(
                record.get('revenue', 0)
                for record in revenue_data
                if datetime.fromisoformat(record['timestamp']) > thirty_days_ago
            )

            return {
                'total_revenue': total_revenue,
                'monthly_revenue': recent_revenue,
                'revenue_by_type': dict(revenue_by_type),
                'total_monetized_posts': len(revenue_data),
                'average_per_post': total_revenue / len(revenue_data) if revenue_data else 0,
                'last_updated': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Ошибка генерации отчета по доходам: {e}")
            return self._get_empty_revenue_report()

    def _get_empty_revenue_report(self) -> Dict:
        """Возвращает пустой отчет по доходам."""
        return {
            'total_revenue': 0,
            'monthly_revenue': 0,
            'revenue_by_type': {},
            'total_monetized_posts': 0,
            'average_per_post': 0,
            'last_updated': datetime.now().isoformat()
        }

    def optimize_content_for_monetization(self, content: Dict) -> Dict:
        """
        Оптимизирует контент для лучшей монетизации.

        Args:
            content (Dict): Исходный контент

        Returns:
            Dict: Оптимизированный контент
        """
        try:
            topic = content.get('topic', '')

            # Добавляем ключевые слова для монетизации
            monetization_keywords = []
            for keyword, related_terms in self.monetization_keywords.items():
                if keyword in topic:
                    monetization_keywords.extend(related_terms)

            # Добавляем в контент
            if monetization_keywords:
                keywords_text = ', '.join(monetization_keywords[:3])
                content['body'] += f"\n\n🔍 Популярные запросы: {keywords_text}"

            # Добавляем призыв к действию для монетизации
            cta_phrases = [
                "\n\n💡 Хотите улучшить результаты? Ознакомьтесь с рекомендациями экспертов!",
                "\n\n🏆 Готовы к новым достижениям? Узнайте о лучших практиках!",
                "\n\n⭐ Интересуют проверенные решения? Смотрите рекомендации ниже!"
            ]

            content['body'] += random.choice(cta_phrases)

            return content

        except Exception as e:
            logger.error(f"Ошибка оптимизации контента для монетизации: {e}")
            return content

    async def get_monetization_forecast(self, days: int = 30) -> Dict:
        """
        Прогнозирует будущие доходы.

        Args:
            days (int): Количество дней для прогноза

        Returns:
            Dict: Прогноз доходов
        """
        try:
            # Получаем исторические данные
            current_report = self.get_revenue_report()

            if current_report['total_monetized_posts'] == 0:
                return {
                    'forecast_revenue': 0,
                    'confidence': 0,
                    'recommendations': ['Накопите статистику для прогноза']
                }

            # Рассчитываем средний доход в день
            avg_daily_revenue = current_report['monthly_revenue'] / 30

            # Прогноз с учетом роста
            growth_factor = 1.1  # Предполагаемый рост 10%
            forecast_revenue = avg_daily_revenue * days * growth_factor

            return {
                'forecast_revenue': forecast_revenue,
                'confidence': 75,  # Процент уверенности
                'based_on_posts': current_report['total_monetized_posts'],
                'growth_assumption': growth_factor,
                'recommendations': [
                    'Увеличивайте аудиторию для роста доходов',
                    'Экспериментируйте с разными типами монетизации',
                    'Оптимизируйте контент под партнерские программы'
                ]
            }

        except Exception as e:
            logger.error(f"Ошибка прогноза доходов: {e}")
            return {
                'forecast_revenue': 0,
                'confidence': 0,
                'recommendations': ['Ошибка при расчете прогноза']
            }