@echo off
REM 一鍵式完整打包解決方案 - Windows 版本

setlocal enabledelayedexpansion

echo 🚀 淨膚寶薪資計算程式 - 一鍵式打包 (Windows)
echo ================================================

REM 檢查必要檔案
echo ℹ️  檢查必要檔案...
set REQUIRED_FILES=auto_salary_calculator.py standalone_main.py requirements.txt

for %%f in (%REQUIRED_FILES%) do (
    if not exist "%%f" (
        echo ❌ 缺少必要檔案: %%f
        pause
        exit /b 1
    ) else (
        echo ✅ 找到 %%f
    )
)

REM 檢查 Python
echo ℹ️  檢查 Python 環境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到 Python！請先安裝 Python 3.7+
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo ✅ 找到 Python: %%i
)

REM 建立虛擬環境
echo ℹ️  設置 Python 環境...
if not exist ".venv" (
    echo 📦 建立虛擬環境...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ❌ 建立虛擬環境失敗
        pause
        exit /b 1
    )
    echo ✅ 虛擬環境建立完成
) else (
    echo ✅ 虛擬環境已存在
)

REM 啟動虛擬環境
echo ℹ️  啟動虛擬環境...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ 啟動虛擬環境失敗
    pause
    exit /b 1
)
echo ✅ 虛擬環境已啟動

REM 安裝依賴
echo ℹ️  安裝依賴套件...
.venv\Scripts\pip.exe install --upgrade pip --quiet
.venv\Scripts\pip.exe install -r requirements.txt --quiet
.venv\Scripts\pip.exe install pyinstaller --quiet

if %errorlevel% neq 0 (
    echo ❌ 依賴安裝失敗
    pause
    exit /b 1
)
echo ✅ 所有依賴安裝完成

REM 建立執行檔
echo ℹ️  建立執行檔...

REM 清理之前的建置
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM 使用 PyInstaller 建立執行檔
.venv\Scripts\pyinstaller.exe salary_calculator.spec --clean --noconfirm

if %errorlevel% neq 0 (
    echo ❌ 執行檔建立失敗
    pause
    exit /b 1
)

REM 檢查建置結果
if exist "dist\淨膚寶薪資計算程式.exe" (
    echo ✅ 執行檔建立成功: dist\淨膚寶薪資計算程式.exe
) else (
    echo ❌ 找不到執行檔
    pause
    exit /b 1
)

REM 建立分發包
echo ℹ️  建立分發包...
if not exist "release\Windows" mkdir "release\Windows"

copy "dist\淨膚寶薪資計算程式.exe" "release\Windows\" >nul

REM 建立使用說明
(
echo 淨膚寶薪資計算程式 - Windows 版本
echo.
echo 📋 使用方法：
echo 1. 雙擊「淨膚寶薪資計算程式.exe」執行程式
echo 2. 按照提示選擇 Excel 檔案
echo 3. 輸入正式淨膚師人數和行號
echo 4. 程式會自動計算薪資和季獎金
echo.
echo ⚠️  注意事項：
echo - 首次執行可能需要3-5秒載入時間
echo - 請確保 Excel 檔案格式正確
echo - 如遇 Windows Defender 警告，請選擇「仍要執行」
echo.
echo 🔧 系統需求：
echo - Windows 10 或更新版本
echo - 至少 200MB 硬碟空間
echo - 1GB 以上記憶體
echo.
echo 📞 技術支援：
echo 如有問題請聯繫程式開發者
echo.
echo 📅 建立資訊：
echo 建立日期: %date% %time%
echo 建立系統: Windows
) > "release\Windows\使用說明.txt"

REM 建立啟動批次檔
(
echo @echo off
echo cd /d "%%~dp0"
echo 淨膚寶薪資計算程式.exe
echo pause
) > "release\Windows\啟動程式.bat"

REM 建立完整說明文件
if not exist "release\分發說明.txt" (
    (
    echo 淨膚寶薪資計算程式 - 分發包
    echo =============================
    echo.
    echo 此分發包包含以下內容：
    echo.
    echo 📁 目錄結構：
    echo release\
    echo ├── Windows\                        # Windows 版本執行檔
    echo │   ├── 淨膚寶薪資計算程式.exe      # 主執行檔
    echo │   ├── 使用說明.txt               # 使用說明
    echo │   └── 啟動程式.bat               # 啟動批次檔
    echo └── 分發說明.txt                   # 本檔案
    echo.
    echo 🎯 程式功能：
    echo - 自動讀取 Excel 薪資檔案
    echo - 計算基本薪資（底薪、伙食費、加班費、手技獎金）
    echo - 計算團隊獎金
    echo - 計算七項季獎金
    echo - 動態偵測員工數據
    echo - 生成詳細的薪資報表
    echo.
    echo 💻 支援系統：
    echo - Windows 10/11 （64-bit）
    echo - macOS （需要使用 macOS 版打包腳本）
    echo - Linux （需要使用 Linux 版打包腳本）
    echo.
    echo 📦 分發方式：
    echo 1. 將整個 release 資料夾壓縮成 ZIP
    echo 2. 分享給需要使用的人員
    echo 3. 解壓後選擇對應系統的執行檔
    echo.
    echo 🔧 建立資訊：
    echo 建立日期: %date% %time%
    echo 建立平台: Windows
    echo 建立者: 自動打包腳本 v2.0
    echo.
    echo 🆘 故障排除：
    echo 1. 如果執行檔無法開啟：
    echo    - 檢查檔案是否被防毒軟體阻擋
    echo    - 嘗試在命令提示字元中執行
    echo    - 查看錯誤訊息
    echo.
    echo 2. 如果出現 Windows Defender 警告：
    echo    - 選擇「其他資訊」然後「仍要執行」
    echo    - 或將程式新增到排除清單
    echo.
    echo 3. 如果程式執行錯誤：
    echo    - 檢查 Excel 檔案格式
    echo    - 確認工作表名稱正確
    echo    - 查看錯誤訊息提示
    echo.
    echo 📞 技術支援：
    echo 如需協助請聯繫程式開發者
    ) > "release\分發說明.txt"
)

echo ✅ 分發包建立完成: release\Windows\

echo.
echo 🎉 打包完成！
echo ======================================
echo ✅ 執行檔位置: release\Windows\
echo ✅ 分發包位置: release\

REM 顯示檔案大小
for %%f in ("release\Windows\淨膚寶薪資計算程式.exe") do (
    echo ℹ️  執行檔大小: %%~zf bytes
)

echo.
echo ℹ️  接下來你可以：
echo   1. 測試執行檔: cd release\Windows ^&^& 淨膚寶薪資計算程式.exe
echo   2. 壓縮分發包: 右鍵 release 資料夾選擇「傳送到」^>「壓縮資料夾」
echo   3. 分享給其他使用者

pause
