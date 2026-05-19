#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Простой launcher для обхода проблем с кодировкой

import sys
import os

# Устанавливаем кодировку
if sys.platform == 'win32':
    os.system('chcp 65001 >nul')

# Импортируем и запускаем main
try:
    import main
    main.main()
except KeyboardInterrupt:
    print("\n⚠️ Бот остановлен пользователем")
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
