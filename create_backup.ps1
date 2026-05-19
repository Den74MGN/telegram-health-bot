# Скрипт резервного копирования проекта
$ErrorActionPreference = "Stop"

# Параметры
$sourceDir = "C:\Users\denk0\telegram_health_bot\telegram_health_bot"
$destBase = "C:\Users\denk0\Desktop\Проекты"
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$backupName = "telegram_health_bot_backup_$timestamp"
$destDir = Join-Path $destBase $backupName

Write-Host "================================================"
Write-Host "СОЗДАНИЕ РЕЗЕРВНОЙ КОПИИ ПРОЕКТА"
Write-Host "================================================"
Write-Host ""
Write-Host "Источник: $sourceDir"
Write-Host "Назначение: $destDir"
Write-Host ""

# Создаем директорию назначения
Write-Host "Создание директории..."
New-Item -ItemType Directory -Path $destDir -Force | Out-Null

# Копируем файлы (исключая ненужные)
Write-Host "Копирование файлов..."
$excludeDirs = @('.git', '__pycache__', 'cache', 'backups')
$excludeFiles = @('*.pyc', '*.pyo')

# Используем robocopy для быстрого копирования
$robocopyArgs = @(
    $sourceDir,
    $destDir,
    '/E',  # Копировать подкаталоги, включая пустые
    '/XD', '.git', '__pycache__', 'cache', 'backups',  # Исключить директории
    '/XF', '*.pyc', '*.pyo',  # Исключить файлы
    '/NFL',  # Не показывать список файлов
    '/NDL',  # Не показывать список директорий
    '/NJH',  # Без заголовка
    '/NJS',  # Без итогов
    '/NP'    # Без прогресса
)

$result = robocopy @robocopyArgs

# robocopy возвращает код 0-7 при успехе
if ($LASTEXITCODE -le 7) {
    Write-Host ""
    Write-Host "================================================"
    Write-Host "✅ РЕЗЕРВНАЯ КОПИЯ СОЗДАНА УСПЕШНО!"
    Write-Host "================================================"
    Write-Host ""
    Write-Host "Расположение: $destDir"
    Write-Host ""
    
    # Показываем размер
    $size = (Get-ChildItem -Path $destDir -Recurse | Measure-Object -Property Length -Sum).Sum
    $sizeMB = [math]::Round($size / 1MB, 2)
    Write-Host "Размер: $sizeMB MB"
    
    # Показываем количество файлов
    $fileCount = (Get-ChildItem -Path $destDir -Recurse -File).Count
    Write-Host "Файлов: $fileCount"
    
    Write-Host ""
    Write-Host "Резервная копия готова к использованию!"
} else {
    Write-Host ""
    Write-Host "❌ ОШИБКА ПРИ СОЗДАНИИ РЕЗЕРВНОЙ КОПИИ"
    Write-Host "Код ошибки: $LASTEXITCODE"
}
