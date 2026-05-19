@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ================================================
echo CREATING PROJECT BACKUP
echo ================================================
echo.

:: Get timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set timestamp=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%_%datetime:~8,2%-%datetime:~10,2%-%datetime:~12,2%

:: Set paths
set SOURCE=C:\Users\denk0\telegram_health_bot\telegram_health_bot
set DEST=C:\Users\denk0\Desktop\Проекты\telegram_health_bot_backup_%timestamp%

echo Source: %SOURCE%
echo Destination: %DEST%
echo.

:: Create destination directory
echo Creating directory...
mkdir "%DEST%" 2>nul

:: Copy files using robocopy
echo Copying files...
robocopy "%SOURCE%" "%DEST%" /E /XD .git __pycache__ cache backups /XF *.pyc *.pyo /NFL /NDL /NJH /NJS /NP

if %ERRORLEVEL% LEQ 7 (
    echo.
    echo ================================================
    echo BACKUP CREATED SUCCESSFULLY!
    echo ================================================
    echo.
    echo Location: %DEST%
    echo.
    
    :: Show size
    for /f "tokens=3" %%a in ('dir "%DEST%" /s /-c ^| find "File(s)"') do set size=%%a
    echo Size: !size! bytes
    
    :: Count files
    for /f %%a in ('dir "%DEST%" /s /b /a-d ^| find /c /v ""') do set count=%%a
    echo Files: !count!
    echo.
    echo Backup is ready to use!
) else (
    echo.
    echo ERROR CREATING BACKUP
    echo Error code: %ERRORLEVEL%
)

echo.
pause
