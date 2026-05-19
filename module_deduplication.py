"""Content Deduplication Module

This module provides functionality to detect and prevent duplicate content
in published posts. It maintains a history of published content signatures
and validates new content against this history.

Author: Telegram Health Bot
Date: 2025
"""

import hashlib
import json
import logging
from typing import Dict, Set, Optional
from pathlib import Path


class ContentDeduplication:
    """
    Manages content deduplication to ensure unique posts.
    
    This class tracks published content by maintaining hashes of post titles
    and bodies. It provides methods to check if content is duplicate before
    publishing and stores signatures of successfully published content.
    
    Attributes:
        storage_file (Path): Path to file storing published content hashes
        published_hashes (Set[str]): Set of content hashes for published posts
        logger (logging.Logger): Logger instance for this module
    """
    
    def __init__(self, storage_file: str = "published_content_hashes.json"):
        """
        Initialize ContentDeduplication system.
        
        Args:
            storage_file (str): Filename for storing published content hashes.
                               Defaults to 'published_content_hashes.json'.
        """
        self.storage_file = Path(storage_file)
        self.published_hashes: Set[str] = set()
        self.logger = logging.getLogger(__name__)
        
        # Load existing published hashes from storage
        self._load_published_hashes()
        self.logger.info(f"ContentDeduplication initialized with {len(self.published_hashes)} existing hashes")
    
    def _load_published_hashes(self) -> None:
        """
        Load published content hashes from storage file.
        
        If storage file doesn't exist or is corrupted, initializes with empty set.
        Logs any errors encountered during loading.
        """
        try:
            if self.storage_file.exists():
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.published_hashes = set(data.get('hashes', []))
                self.logger.info(f"Loaded {len(self.published_hashes)} published content hashes")
            else:
                self.logger.info("No existing hash storage found, starting fresh")
        except Exception as e:
            self.logger.error(f"Error loading published hashes: {e}")
            self.published_hashes = set()
    
    def _save_published_hashes(self) -> None:
        """
        Save published content hashes to storage file.
        
        Persists the current set of published hashes to disk for future sessions.
        Logs any errors encountered during saving.
        """
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump({'hashes': list(self.published_hashes)}, f, indent=2)
            self.logger.debug(f"Saved {len(self.published_hashes)} hashes to storage")
        except Exception as e:
            self.logger.error(f"Error saving published hashes: {e}")
    
    def calculate_content_hash(self, title: str, body: str) -> str:
        """
        Calculate unique hash signature for content.
        
        Creates a SHA-256 hash based on the combination of title and body text.
        This hash uniquely identifies the content for deduplication purposes.
        
        Args:
            title (str): Post title text
            body (str): Post body text
        
        Returns:
            str: SHA-256 hash string representing the content signature
        """
        # Combine title and body, normalize whitespace
        content = f"{title.strip()}\n{body.strip()}"
        # Calculate SHA-256 hash
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        self.logger.debug(f"Calculated content hash: {content_hash[:16]}...")
        return content_hash
    
    def is_duplicate(self, title: str, body: str) -> bool:
        """
        Check if content has been published before.
        
        Calculates hash of provided content and checks against published history.
        
        Args:
            title (str): Post title to check
            body (str): Post body to check
        
        Returns:
            bool: True if content is duplicate, False if unique
        """
        content_hash = self.calculate_content_hash(title, body)
        is_dup = content_hash in self.published_hashes
        
        if is_dup:
            self.logger.warning(f"Duplicate content detected: {content_hash[:16]}...")
        else:
            self.logger.debug(f"Content is unique: {content_hash[:16]}...")
        
        return is_dup
    
    def add_published_hash(self, title: str, body: str) -> None:
        """
        Record content as published to prevent future duplicates.
        
        Calculates hash of content and adds to published history, then persists
        to storage file.
        
        Args:
            title (str): Title of published post
            body (str): Body of published post
        """
        content_hash = self.calculate_content_hash(title, body)
        self.published_hashes.add(content_hash)
        self._save_published_hashes()
        self.logger.info(f"Recorded published content: {content_hash[:16]}... (Total: {len(self.published_hashes)})")
    
    def get_stats(self) -> Dict[str, int]:
        """
        Get deduplication statistics.
        
        Returns:
            Dict[str, int]: Dictionary containing tracked_hashes count
        """
        return {
            'tracked_hashes': len(self.published_hashes)
        }
    
    def clear_history(self) -> None:
        """
        Clear all published content history.
        
        WARNING: This will reset deduplication tracking. Use with caution.
        Primarily for testing or intentional reset scenarios.
        """
        self.published_hashes.clear()
        self._save_published_hashes()
        self.logger.warning("Cleared all published content history")
