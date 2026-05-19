"""
Модульные тесты для всех модулей.
"""

import unittest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import os
import tempfile

# Import modules
from module_content import ContentGenerator
from module_publisher import TelegramPublisher
from module_ads import AdsIntegrator
from module_scheduler import ContentScheduler

class TestContentGenerator(unittest.TestCase):
    """Test content generation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = ContentGenerator("fake_api_key")

    @patch('module_content.OpenAI')
    def test_generate_text_post_success(self, mock_openai):
        """Test successful text post generation."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test Title\n\nTest body content."
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        result = self.generator.generate_text_post()

        self.assertIsInstance(result, dict)
        self.assertIn('title', result)
        self.assertIn('body', result)
        self.assertEqual(result['title'], 'Test Title')

    @patch('module_content.OpenAI')
    def test_generate_text_post_failure(self, mock_openai):
        """Test text post generation failure."""
        mock_openai.return_value.chat.completions.create.side_effect = Exception("API Error")

        result = self.generator.generate_text_post()

        # Should return fallback content
        self.assertIsInstance(result, dict)
        self.assertIn('title', result)
        self.assertIn('body', result)

class TestTelegramPublisher(unittest.IsolatedAsyncioTestCase):
    """Test Telegram publishing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.publisher = TelegramPublisher(
            bot_token="fake_token",
            channel_id="@test_channel"
        )

    @patch('module_publisher.Bot')
    async def test_publish_text_post_success(self, mock_bot_class):
        """Test successful text post publishing."""
        mock_bot = Mock()
        mock_bot.send_message = AsyncMock()
        mock_bot_class.return_value = mock_bot

        content = {"title": "Test Title", "body": "Test body"}
        result = await self.publisher.publish_text_post(content)

        self.assertTrue(result)
        mock_bot.send_message.assert_called_once()

    @patch('module_publisher.Bot')
    async def test_publish_text_post_failure(self, mock_bot_class):
        """Test text post publishing failure."""
        mock_bot = Mock()
        mock_bot.send_message = AsyncMock(side_effect=Exception("Network error"))
        mock_bot_class.return_value = mock_bot

        content = {"title": "Test Title", "body": "Test body"}
        result = await self.publisher.publish_text_post(content)

        self.assertFalse(result)

class TestAdsIntegrator(unittest.TestCase):
    """Test ads integration functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.ads = AdsIntegrator("fake_key", "fake_secret")

    @patch('module_ads.requests.Session')
    def test_get_advertisement_success(self, mock_session_class):
        """Test successful advertisement retrieval."""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            'ads': [{'id': '123', 'advertiser_id': '456', 'text': 'Test ad', 'budget': 500}]
        }
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        result = self.ads.get_advertisement()

        self.assertIsInstance(result, dict)
        self.assertEqual(result['id'], '123')

    @patch('module_ads.requests.Session')
    def test_get_advertisement_no_ads(self, mock_session_class):
        """Test when no advertisements are available."""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {'ads': []}
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        result = self.ads.get_advertisement()

        self.assertIsNone(result)

class TestContentScheduler(unittest.TestCase):
    """Test scheduler functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.scheduler = ContentScheduler()

    def test_scheduler_initialization(self):
        """Test scheduler initialization."""
        self.assertIsNotNone(self.scheduler.scheduler)

    def test_schedule_content_generation(self):
        """Test content generation scheduling."""
        def dummy_func():
            pass

        job_id = self.scheduler.schedule_content_generation(dummy_func)
        self.assertIsInstance(job_id, str)

        jobs = self.scheduler.get_jobs()
        self.assertEqual(len(jobs), 1)

if __name__ == '__main__':
    # Create test directories
    os.makedirs('logs', exist_ok=True)

    # Run tests
    unittest.main(verbosity=2)