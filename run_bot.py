#!/usr/bin/env python3
"""
Универсальный скрипт запуска бота из любой директории
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Запуск бота с правильными путями"""
    # Получаем текущую директорию скрипта
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    print("🚀 Запуск Telegram бота здоровья...")
    print(f"📁 Рабочая директория: {script_dir}")

    try:
        # Создаем необходимые директории
        dirs = ['logs', 'content', 'analytics', 'analytics/charts', 'backups']
        for dir_name in dirs:
            os.makedirs(dir_name, exist_ok=True)
            print(f"✅ Создана директория: {dir_name}")

        # Проверяем .env файл
        env_file = script_dir / '.env'
        if env_file.exists():
            print("✅ Файл конфигурации найден")
        else:
            print("❌ Файл .env не найден!")
            return

        # Запускаем бота
        print("🎯 Запуск основного приложения...")
        result = subprocess.run([sys.executable, 'main.py'],
                              cwd=script_dir,
                              capture_output=False)

        if result.returncode == 0:
            print("✅ Бот запущен успешно!")
        else:
            print(f"❌ Ошибка запуска: {result.returncode}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("💡 Попробуйте запустить вручную: python main.py")

if __name__ == "__main__":
    main()