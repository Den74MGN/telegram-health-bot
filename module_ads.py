"""
Модуль Интеграции Рекламы

Этот модуль обрабатывает получение и интеграцию рекламы с платформы Telega.in.
"""

import logging
import requests
from typing import Dict, Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AdsIntegrator:
    """Handles advertisement fetching and integration from Telega.in."""

    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.telega.in"):
        """
        Initialize the ads integrator.

        Args:
            api_key (str): Telega.in API key.
            api_secret (str): Telega.in API secret.
            base_url (str): Base URL for Telega.in API. Defaults to "https://api.telega.in".
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def get_advertisement(self, category: str = "health", budget_min: int = 500) -> Optional[Dict[str, Any]]:
        """
        Fetch an available advertisement from the marketplace.

        Args:
            category (str): Advertisement category. Defaults to "health".
            budget_min (int): Minimum budget per post in rubles. Defaults to 500.

        Returns:
            Optional[Dict[str, Any]]: Advertisement data or None if no ads available.
        """
        try:
            endpoint = f"{self.base_url}/ads/available"
            params = {
                'category': category,
                'budget_min': budget_min,
                'limit': 1
            }

            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get('ads') and len(data['ads']) > 0:
                ad = data['ads'][0]
                logger.info(f"Retrieved advertisement: {ad.get('id', 'unknown')}")
                return {
                    'id': ad.get('id'),
                    'advertiser_id': ad.get('advertiser_id'),
                    'text': ad.get('text'),
                    'budget': ad.get('budget'),
                    'category': ad.get('category')
                }
            else:
                logger.info("No advertisements available")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch advertisement: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_advertisement: {e}")
            return None

    def report_ad_performance(self, ad_id: str, post_id: Optional[str] = None, views: int = 0) -> bool:
        """
        Report advertisement performance after publishing.

        Args:
            ad_id (str): Advertisement ID.
            post_id (Optional[str]): Telegram post ID.
            views (int): Number of views. Defaults to 0.

        Returns:
            bool: True if reported successfully, False otherwise.
        """
        try:
            endpoint = f"{self.base_url}/ads/{ad_id}/performance"
            payload = {
                'post_id': post_id,
                'views': views,
                'timestamp': datetime.utcnow().isoformat()
            }

            response = self.session.post(endpoint, json=payload, timeout=10)
            response.raise_for_status()

            logger.info(f"Performance reported for ad {ad_id}")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to report ad performance: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error in report_ad_performance: {e}")
            return False

    def get_ad_statistics(self, ad_id: str) -> Optional[Dict[str, Any]]:
        """
        Get statistics for a specific advertisement.

        Args:
            ad_id (str): Advertisement ID.

        Returns:
            Optional[Dict[str, Any]]: Statistics data or None if failed.
        """
        try:
            endpoint = f"{self.base_url}/ads/{ad_id}/stats"

            response = self.session.get(endpoint, timeout=10)
            response.raise_for_status()

            stats = response.json()
            logger.info(f"Retrieved stats for ad {ad_id}")
            return stats

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get ad statistics: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_ad_statistics: {e}")
            return None

    def validate_ad_content(self, ad_content: Dict[str, Any]) -> bool:
        """
        Validate advertisement content before publishing.

        Args:
            ad_content (Dict[str, Any]): Advertisement data.

        Returns:
            bool: True if content is valid, False otherwise.
        """
        required_fields = ['id', 'text']
        for field in required_fields:
            if field not in ad_content or not ad_content[field]:
                logger.warning(f"Missing or empty required field: {field}")
                return False

        # Check text length (Telegram limit is 4096 characters)
        if len(ad_content['text']) > 4000:
            logger.warning("Advertisement text too long")
            return False

        return True

    def get_available_budget(self) -> Optional[int]:
        """
        Get available budget for advertisements.

        Returns:
            Optional[int]: Available budget in rubles, or None if failed.
        """
        try:
            endpoint = f"{self.base_url}/budget/available"

            response = self.session.get(endpoint, timeout=10)
            response.raise_for_status()

            data = response.json()
            budget = data.get('available_budget', 0)
            logger.info(f"Available budget: {budget} RUB")
            return budget

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get available budget: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_available_budget: {e}")
            return None