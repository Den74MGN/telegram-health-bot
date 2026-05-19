"""
Модуль Публикации

Этот модуль обрабатывает публикацию контента в Telegram-каналы с обработкой ошибок и логикой повторов.
"""

import logging
import asyncio
from typing import Dict, Optional, Any
from telegram import Bot
from telegram.error import TelegramError, NetworkError, TimedOut
from telegram.constants import ParseMode

logger = logging.getLogger(__name__)

class TelegramPublisher:
    """Handles Telegram channel publishing with robust error handling."""

    def __init__(self, bot_token: str, channel_id: str, admin_chat_id: Optional[str] = None):
        """
        Initialize the publisher.

        Args:
            bot_token (str): Telegram bot token.
            channel_id (str): Target channel ID (e.g., '@channelname' or '-1001234567890').
            admin_chat_id (Optional[str]): Admin chat ID for error notifications.
        """
        self.bot = Bot(token=bot_token)
        self.channel_id = channel_id
        self.admin_chat_id = admin_chat_id
        self.max_retries = 3
        self.retry_delay = 5  # seconds

    async def publish_text_post(self, content: Dict[str, str], ad_content: Optional[Dict[str, Any]] = None) -> bool:
        """
        Publish a text post to the channel.

        Args:
            content (Dict[str, str]): Content dictionary with 'title' and 'body' keys.
            ad_content (Optional[Dict[str, Any]]): Advertisement content to include.

        Returns:
            bool: True if published successfully, False otherwise.
        """
        try:
            # Format the message
            message = f"*{content['title']}*\n\n{content['body']}"

            # Add advertisement if available
            if ad_content:
                ad_text = f"\n\n📢 *Реклама*\n{ad_content.get('text', '')}"
                message += ad_text

            # Publish with retry logic
            for attempt in range(self.max_retries):
                try:
                    await self.bot.send_message(
                        chat_id=self.channel_id,
                        text=message,
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=True
                    )
                    logger.info("Text post published successfully")
                    return True

                except (NetworkError, TimedOut) as e:
                    if attempt < self.max_retries - 1:
                        logger.warning(f"Publishing attempt {attempt + 1} failed: {e}. Retrying in {self.retry_delay}s...")
                        await asyncio.sleep(self.retry_delay)
                        self.retry_delay *= 2  # Exponential backoff
                    else:
                        logger.error(f"Failed to publish text post after {self.max_retries} attempts: {e}")
                        await self._notify_admin(f"❌ Failed to publish text post: {str(e)}")
                        return False

                except TelegramError as e:
                    logger.error(f"Telegram API error: {e}")
                    await self._notify_admin(f"❌ Telegram API error: {str(e)}")
                    return False

        except Exception as e:
            logger.error(f"Unexpected error in publish_text_post: {e}")
            await self._notify_admin(f"❌ Unexpected error: {str(e)}")
            return False

    async def publish_video_post(self, video_path: str, caption: str, ad_content: Optional[Dict[str, Any]] = None) -> bool:
        """
        Publish a video post to the channel.

        Args:
            video_path (str): Path to the video file.
            caption (str): Video caption.
            ad_content (Optional[Dict[str, Any]]): Advertisement content to include.

        Returns:
            bool: True if published successfully, False otherwise.
        """
        try:
            # Add advertisement to caption if available
            if ad_content:
                ad_text = f"\n\n📢 *Реклама*\n{ad_content.get('text', '')}"
                caption += ad_text

            # Publish with retry logic
            for attempt in range(self.max_retries):
                try:
                    with open(video_path, 'rb') as video_file:
                        await self.bot.send_video(
                            chat_id=self.channel_id,
                            video=video_file,
                            caption=caption,
                            parse_mode=ParseMode.MARKDOWN,
                            supports_streaming=True
                        )
                    logger.info("Video post published successfully")
                    return True

                except (NetworkError, TimedOut) as e:
                    if attempt < self.max_retries - 1:
                        logger.warning(f"Video publishing attempt {attempt + 1} failed: {e}. Retrying in {self.retry_delay}s...")
                        await asyncio.sleep(self.retry_delay)
                        self.retry_delay *= 2
                    else:
                        logger.error(f"Failed to publish video after {self.max_retries} attempts: {e}")
                        await self._notify_admin(f"❌ Failed to publish video: {str(e)}")
                        return False

                except TelegramError as e:
                    logger.error(f"Telegram API error: {e}")
                    await self._notify_admin(f"❌ Telegram API error: {str(e)}")
                    return False

        except Exception as e:
            logger.error(f"Unexpected error in publish_video_post: {e}")
            await self._notify_admin(f"❌ Unexpected error: {str(e)}")
            return False

    async def publish_photo_post(self, image_bytes: bytes, caption: str, ad_content: Optional[Dict[str, Any]] = None) -> bool:
        """
        Publish a photo post to the channel.

        Args:
            image_bytes (bytes): Photo image data (from image generator).
            caption (str): Photo caption text.
            ad_content (Optional[Dict[str, Any]]): Advertisement content to include.

        Returns:
            bool: True if published successfully, False otherwise.
        """
        try:
            # Add advertisement if available
            if ad_content:
                ad_text = f"\n\n🔔 *Реклама*\n{ad_content.get('text', '')}"
                caption += ad_text
            
            # Telegram ограничивает подпись до 1024 символов
            if len(caption) > 1024:
                caption = caption[:1020] + "..."
                logger.warning(f"Caption truncated to 1024 characters")

            # Publish with retry logic
            for attempt in range(self.max_retries):
                try:
                    await self.bot.send_photo(
                        chat_id=self.channel_id,
                        photo=image_bytes,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    logger.info("Photo post published successfully")
                    return True

                except (NetworkError, TimedOut) as e:
                    if attempt < self.max_retries - 1:
                        logger.warning(f"Photo publishing attempt {attempt + 1} failed: {e}. Retrying in {self.retry_delay}s")
                        await asyncio.sleep(self.retry_delay)
                        self.retry_delay *= 2  # Exponential backoff
                    else:
                        logger.error(f"Failed to publish photo after {self.max_retries} attempts: {e}")
                        await self._notify_admin(f"❌ Failed to publish photo: {str(e)}")
                        return False

                except TelegramError as e:
                    logger.error(f"Telegram API error: {e}")
                    await self._notify_admin(f"❌ Telegram API error: {str(e)}")
                    return False

        except Exception as e:
            logger.error(f"Unexpected error in publish_photo_post: {e}")
            await self._notify_admin(f"❌ Unexpected error: {str(e)}")
            return False

    async def _notify_admin(self, message: str):
        """
        Send notification to admin chat if configured.

        Args:
            message (str): Notification message.
        """
        if self.admin_chat_id and self.admin_chat_id != 'YOUR_PERSONAL_TELEGRAM_ID':
            try:
                await self.bot.send_message(
                    chat_id=self.admin_chat_id,
                    text=message,
                    parse_mode=ParseMode.MARKDOWN
                )
            except Exception as e:
                logger.error(f"Failed to notify admin: {e}")
        else:
            logger.info(f"Admin notification skipped (ID not configured): {message[:100]}")

    async def test_connection(self) -> bool:
        """
        Test connection to Telegram API.

        Returns:
            bool: True if connection successful, False otherwise.
        """
        try:
            bot_info = await self.bot.get_me()
            logger.info(f"Bot connected successfully: @{bot_info.username}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Telegram API: {e}")

            return False
