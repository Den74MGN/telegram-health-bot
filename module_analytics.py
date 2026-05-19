"""
Модуль Аналитики и Оптимизации

Этот модуль анализирует эффективность контента, оптимизирует публикации
и предоставляет insights для улучшения монетизации.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd
from collections import Counter, defaultdict

logger = logging.getLogger(__name__)

class ContentAnalytics:
    """Аналитика и оптимизация контента для максимальной эффективности."""

    def __init__(self):
        """Инициализация системы аналитики."""
        self.analytics_data = []
        self.performance_history = []
        self.content_topics = set()
        self.engagement_metrics = {}

        # Создаем директории для аналитики
        os.makedirs('analytics', exist_ok=True)
        os.makedirs('analytics/charts', exist_ok=True)

    def record_post_performance(self, post_data: Dict, engagement: Dict = None):
        """
        Записывает данные о публикации для анализа.

        Args:
            post_data (Dict): Данные о посте
            engagement (Dict): Метрики вовлеченности
        """
        try:
            # Конвертируем datetime в строку для JSON сериализации
            scheduled_date = post_data.get('scheduled_date')
            if scheduled_date and isinstance(scheduled_date, datetime):
                scheduled_time_str = scheduled_date.isoformat()
            else:
                scheduled_time_str = scheduled_date
            
            record = {
                'timestamp': datetime.now().isoformat(),
                'post_id': post_data.get('post_id'),
                'title': post_data.get('title'),
                'topic': post_data.get('topic'),
                'content_length': len(post_data.get('body', '')),
                'hashtags': post_data.get('hashtags', []),
                'seo_keywords': post_data.get('seo_keywords', []),
                'scheduled_time': scheduled_time_str,
                'engagement': engagement or {},
                'monetization': post_data.get('monetization', {})
            }

            self.analytics_data.append(record)
            self._save_analytics_data()

            logger.info(f"Записана аналитика для поста: {post_data.get('title', 'Unknown')}")

        except Exception as e:
            logger.error(f"Ошибка записи аналитики: {e}")

    def analyze_content_performance(self) -> Dict:
        """
        Анализирует эффективность контента.

        Returns:
            Dict: Отчет по аналитике
        """
        try:
            if not self.analytics_data:
                return self._get_empty_analytics()

            # Конвертируем в DataFrame для анализа
            df = pd.DataFrame(self.analytics_data)

            # Анализ по темам
            topic_performance = self._analyze_topic_performance(df)

            # Анализ по времени публикации
            time_performance = self._analyze_time_performance(df)

            # Анализ вовлеченности
            engagement_analysis = self._analyze_engagement(df)

            # Рекомендации по оптимизации
            recommendations = self._generate_recommendations(df)

            return {
                'total_posts': len(df),
                'average_engagement': engagement_analysis.get('average', 0),
                'top_topics': topic_performance.get('top', []),
                'best_posting_time': time_performance.get('best_time', '10:00'),
                'content_quality_score': self._calculate_quality_score(df),
                'monetization_efficiency': self._analyze_monetization(df),
                'recommendations': recommendations,
                'trends': self._analyze_trends(df)
            }

        except Exception as e:
            logger.error(f"Ошибка анализа контента: {e}")
            return self._get_empty_analytics()

    def _analyze_topic_performance(self, df: pd.DataFrame) -> Dict:
        """Анализирует эффективность по темам."""
        try:
            # Группируем по темам и считаем среднюю вовлеченность
            topic_stats = df.groupby('topic').agg({
                'engagement': lambda x: self._extract_engagement_score(x),
                'timestamp': 'count'
            }).round(2)

            # Сортируем по вовлеченности
            top_topics = topic_stats.sort_values('engagement', ascending=False).head(5)

            return {
                'top': top_topics.index.tolist(),
                'stats': topic_stats.to_dict()
            }
        except Exception as e:
            logger.error(f"Ошибка анализа тем: {e}")
            return {'top': [], 'stats': {}}

    def _analyze_time_performance(self, df: pd.DataFrame) -> Dict:
        """Анализирует лучшее время для публикации."""
        try:
            # Извлекаем час публикации
            df['hour'] = pd.to_datetime(df['timestamp']).dt.hour

            # Группируем по часам
            hourly_performance = df.groupby('hour')['engagement'].apply(
                lambda x: self._extract_engagement_score(x)
            ).round(2)

            # Находим лучшее время
            best_hour = hourly_performance.idxmax()
            best_time = f"{best_hour:02d}:00"

            return {
                'best_time': best_time,
                'hourly_stats': hourly_performance.to_dict()
            }
        except Exception as e:
            logger.error(f"Ошибка анализа времени: {e}")
            return {'best_time': '10:00', 'hourly_stats': {}}

    def _analyze_engagement(self, df: pd.DataFrame) -> Dict:
        """Анализирует метрики вовлеченности."""
        try:
            engagement_scores = []

            for _, row in df.iterrows():
                score = self._extract_engagement_score(row['engagement'])
                if score > 0:
                    engagement_scores.append(score)

            if engagement_scores:
                return {
                    'average': sum(engagement_scores) / len(engagement_scores),
                    'max': max(engagement_scores),
                    'min': min(engagement_scores),
                    'total_interactions': len([s for s in engagement_scores if s > 0])
                }
            else:
                return {'average': 0, 'max': 0, 'min': 0, 'total_interactions': 0}

        except Exception as e:
            logger.error(f"Ошибка анализа вовлеченности: {e}")
            return {'average': 0, 'max': 0, 'min': 0, 'total_interactions': 0}

    def _extract_engagement_score(self, engagement_data) -> float:
        """Извлекает числовой score вовлеченности."""
        try:
            if isinstance(engagement_data, dict):
                # Суммируем все виды вовлеченности
                views = engagement_data.get('views', 0)
                likes = engagement_data.get('likes', 0)
                comments = engagement_data.get('comments', 0)
                shares = engagement_data.get('shares', 0)

                # Взвешенный score
                return views * 0.1 + likes * 1 + comments * 3 + shares * 2
            else:
                return float(engagement_data) if engagement_data else 0
        except:
            return 0

    def _generate_recommendations(self, df: pd.DataFrame) -> List[str]:
        """Генерирует рекомендации по оптимизации."""
        recommendations = []

        try:
            # Анализ длины контента
            avg_length = df['content_length'].mean()
            if avg_length < 200:
                recommendations.append("Увеличивайте длину постов для лучшей вовлеченности")
            elif avg_length > 600:
                recommendations.append("Сокращайте посты для лучшей читаемости")

            # Анализ использования хэштегов
            avg_hashtags = df['hashtags'].apply(len).mean()
            if avg_hashtags < 3:
                recommendations.append("Добавляйте больше хэштегов для охвата")
            elif avg_hashtags > 8:
                recommendations.append("Сокращайте количество хэштегов")

            # Анализ тем
            if len(df['topic'].unique()) < 5:
                recommendations.append("Расширяйте разнообразие тем")

            # Рекомендации по времени
            best_time = self._analyze_time_performance(df)['best_time']
            recommendations.append(f"Публикуйте в {best_time} для максимального охвата")

        except Exception as e:
            logger.error(f"Ошибка генерации рекомендаций: {e}")
            recommendations.append("Продолжайте мониторинг для получения рекомендаций")

        return recommendations

    def _calculate_quality_score(self, df: pd.DataFrame) -> float:
        """Рассчитывает общий quality score контента."""
        try:
            # Множественные факторы качества
            factors = []

            # Длина контента (оптимально 200-500 слов)
            avg_length = df['content_length'].mean()
            length_score = min(100, (avg_length / 400) * 100)
            factors.append(length_score)

            # Разнообразие тем
            topic_diversity = min(100, (len(df['topic'].unique()) / 10) * 100)
            factors.append(topic_diversity)

            # Использование ключевых слов
            seo_usage = df['seo_keywords'].apply(len).mean()
            seo_score = min(100, (seo_usage / 5) * 100)
            factors.append(seo_score)

            # Общий score
            return sum(factors) / len(factors)

        except Exception as e:
            logger.error(f"Ошибка расчета quality score: {e}")
            return 50.0

    def _analyze_monetization(self, df: pd.DataFrame) -> Dict:
        """Анализирует эффективность монетизации."""
        try:
            monetization_data = []

            for record in self.analytics_data:
                if record.get('monetization'):
                    monetization_data.append(record['monetization'])

            if monetization_data:
                total_revenue = sum(m.get('revenue', 0) for m in monetization_data)
                avg_revenue = total_revenue / len(monetization_data)

                return {
                    'total_revenue': total_revenue,
                    'average_per_post': avg_revenue,
                    'monetized_posts': len(monetization_data),
                    'conversion_rate': len(monetization_data) / len(df)
                }
            else:
                return {
                    'total_revenue': 0,
                    'average_per_post': 0,
                    'monetized_posts': 0,
                    'conversion_rate': 0
                }

        except Exception as e:
            logger.error(f"Ошибка анализа монетизации: {e}")
            return {'total_revenue': 0, 'average_per_post': 0, 'monetized_posts': 0, 'conversion_rate': 0}

    def _analyze_trends(self, df: pd.DataFrame) -> Dict:
        """Анализирует тренды в контенте."""
        try:
            # Тренды по темам
            topic_trends = Counter(df['topic']).most_common(5)

            # Тренды по времени
            df['date'] = pd.to_datetime(df['timestamp']).dt.date
            daily_posts = df.groupby('date').size()

            return {
                'popular_topics': [topic for topic, count in topic_trends],
                'posting_frequency': daily_posts.mean(),
                'content_velocity': len(df) / max(1, (datetime.now() - pd.to_datetime(df['timestamp']).min()).days)
            }

        except Exception as e:
            logger.error(f"Ошибка анализа трендов: {e}")
            return {'popular_topics': [], 'posting_frequency': 0, 'content_velocity': 0}

    def generate_analytics_report(self) -> str:
        """
        Генерирует подробный отчет по аналитике.

        Returns:
            str: Текстовый отчет
        """
        try:
            analytics = self.analyze_content_performance()

            report = f"""
📊 ОТЧЕТ ПО АНАЛИТИКЕ КОНТЕНТА
{'='*50}

📈 ОБЩАЯ СТАТИСТИКА:
• Всего постов: {analytics['total_posts']}
• Средняя вовлеченность: {analytics['average_engagement']:.1f}
• Quality Score: {analytics['content_quality_score']:.1f}/100

🎯 ТОП ТЕМ:
{chr(10).join(f"• {topic}" for topic in analytics['top_topics'][:5])}

⏰ ЛУЧШЕЕ ВРЕМЯ ПУБЛИКАЦИИ:
• {analytics['best_posting_time']}

💰 МОНЕТИЗАЦИЯ:
• Доход за все время: {analytics['monetization_efficiency']['total_revenue']:.0f} RUB
• Средний доход за пост: {analytics['monetization_efficiency']['average_per_post']:.0f} RUB
• Конверсия в монетизацию: {analytics['monetization_efficiency']['conversion_rate']*100:.1f}%

📋 РЕКОМЕНДАЦИИ:
{chr(10).join(f"• {rec}" for rec in analytics['recommendations'][:5])}

📈 ТРЕНДЫ:
• Популярные темы: {', '.join(analytics['trends']['popular_topics'][:3])}
• Частота публикаций: {analytics['trends']['posting_frequency']:.1f} постов в день

Отчет сгенерирован: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

            # Сохраняем отчет в файл
            report_file = f"analytics/report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)

            return report

        except Exception as e:
            logger.error(f"Ошибка генерации отчета: {e}")
            return "Ошибка при генерации отчета по аналитике"

    def _save_analytics_data(self):
        """Сохраняет данные аналитики в файл."""
        try:
            with open('logs/content_stats.json', 'w', encoding='utf-8') as f:
                json.dump(self.analytics_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Ошибка сохранения аналитики: {e}")

    def _get_empty_analytics(self) -> Dict:
        """Возвращает пустую аналитику для новых каналов."""
        return {
            'total_posts': 0,
            'average_engagement': 0,
            'top_topics': [],
            'best_posting_time': '10:00',
            'content_quality_score': 50.0,
            'monetization_efficiency': {'total_revenue': 0, 'average_per_post': 0, 'monetized_posts': 0, 'conversion_rate': 0},
            'recommendations': ['Опубликуйте больше контента для получения аналитики'],
            'trends': {'popular_topics': [], 'posting_frequency': 0, 'content_velocity': 0}
        }

    def export_analytics_chart(self, chart_type: str = 'engagement') -> Optional[str]:
        """Экспорт графиков отключен - требует установки matplotlib и seaborn"""
        logger.info("ℹ️ Экспорт графиков отключен (требует установки matplotlib и seaborn)")
        return None
        """
        Экспортирует график аналитики.

        Args:
            chart_type (str): Тип графика ('engagement', 'topics', 'timeline')

        Returns:
            Optional[str]: Путь к файлу графика
        """
        try:
            if not self.analytics_data:
                return None

            df = pd.DataFrame(self.analytics_data)

            plt.figure(figsize=(10, 6))
            plt.style.use('seaborn')

            if chart_type == 'engagement':
                # График вовлеченности по времени
                df['date'] = pd.to_datetime(df['timestamp']).dt.date
                daily_engagement = df.groupby('date')['engagement'].apply(
                    lambda x: self._extract_engagement_score(x)
                ).reset_index()

                plt.plot(daily_engagement['date'], daily_engagement['engagement'])
                plt.title('Динамика Вовлеченности Аудитории')
                plt.xlabel('Дата')
                plt.ylabel('Уровень Вовлеченности')
                plt.xticks(rotation=45)

            elif chart_type == 'topics':
                # График популярности тем
                topic_engagement = df.groupby('topic')['engagement'].apply(
                    lambda x: self._extract_engagement_score(x)
                ).sort_values(ascending=True)

                topic_engagement.plot(kind='barh')
                plt.title('Эффективность Тем')
                plt.xlabel('Уровень Вовлеченности')
                plt.ylabel('Темы')

            plt.tight_layout()

            # Сохраняем график
            chart_file = f"analytics/charts/{chart_type}_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            plt.close()

            return chart_file

        except Exception as e:
            logger.error(f"Ошибка экспорта графика: {e}")
            return None