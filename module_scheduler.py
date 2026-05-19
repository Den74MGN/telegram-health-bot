"""
Модуль Планировщика

Этот модуль управляет временным выполнением задач генерации контента и публикации.
Использует APScheduler для надежного планирования с обработкой ошибок.
"""

import logging
import asyncio
from typing import Callable, Any
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor

logger = logging.getLogger(__name__)

class ContentScheduler:
    """Manages scheduled content generation and publishing."""

    def __init__(self):
        """Initialize the scheduler with memory job store."""
        self.scheduler = AsyncIOScheduler(
            jobstores={
                'default': MemoryJobStore()
            },
            executors={
                'default': AsyncIOExecutor()
            },
            job_defaults={
                'coalesce': True,
                'max_instances': 1,
                'misfire_grace_time': 30
            }
        )

    def start_scheduler(self):
        """Start the scheduler."""
        if not self.scheduler.running:
                    # Create event loop for AsyncIOScheduler
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)                                    
            self.scheduler.start()
            logger.info("Scheduler started successfully")

    def stop_scheduler(self):
        """Stop the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown(wait=True)
            logger.info("Scheduler stopped")

    def schedule_content_generation(self, func: Callable, interval_hours: int = 2) -> str:
        """
        Schedule content generation at regular intervals.

        Args:
            func (Callable): The function to call for content generation.
            interval_hours (int): Hours between executions. Defaults to 2.

        Returns:
            str: Job ID for the scheduled task.
        """
        job = self.scheduler.add_job(
            func,
            trigger=IntervalTrigger(hours=interval_hours),
            id='content_generation',
            name='Generate Health Content',
            replace_existing=True
        )
        logger.info(f"Content generation scheduled every {interval_hours} hours")
        return job.id

    def schedule_publishing(self, func: Callable, interval_hours: int = 2) -> str:
        """
        Schedule content publishing at regular intervals.

        Args:
            func (Callable): The function to call for publishing.
            interval_hours (int): Hours between executions. Defaults to 2.

        Returns:
            str: Job ID for the scheduled task.
        """
        job = self.scheduler.add_job(
            func,
            trigger=IntervalTrigger(hours=interval_hours),
            id='content_publishing',
            name='Publish Health Content',
            replace_existing=True
        )
        logger.info(f"Content publishing scheduled every {interval_hours} hours")
        return job.id

    def add_job(self, func: Callable, trigger: Any, job_id: str, name: str) -> str:
        """
        Add a custom job to the scheduler.

        Args:
            func (Callable): The function to execute.
            trigger (Any): APScheduler trigger object.
            job_id (str): Unique job identifier.
            name (str): Human-readable job name.

        Returns:
            str: Job ID.
        """
        job = self.scheduler.add_job(
            func,
            trigger=trigger,
            id=job_id,
            name=name,
            replace_existing=True
        )
        logger.info(f"Job '{name}' added with ID: {job_id}")
        return job.id

    def remove_job(self, job_id: str) -> bool:
        """
        Remove a job from the scheduler.

        Args:
            job_id (str): The job ID to remove.

        Returns:
            bool: True if job was removed, False if not found.
        """
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Job {job_id} removed")
            return True
        except Exception as e:
            logger.error(f"Failed to remove job {job_id}: {e}")
            return False

    def get_jobs(self) -> list:
        """
        Get list of all scheduled jobs.

        Returns:
            list: List of job objects.
        """
        return self.scheduler.get_jobs()

    async def run_once(self, func: Callable, *args, **kwargs):
        """
        Run a function once asynchronously.

        Args:
            func (Callable): The function to run.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.
        """
        try:
            if hasattr(func, '__call__'):
                await func(*args, **kwargs)
        except Exception as e:

            logger.error(f"Error running function {func.__name__}: {e}")


