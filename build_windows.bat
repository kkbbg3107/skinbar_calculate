@echo off
REM Windows 自動打包腳本

echo 🚀 開始建立 Windows 執行檔...
echo ==================================

REM 檢查是否在正確的目錄
if not exist "auto_salary_calculator.py" (
    echo ❌ 錯誤：找不到 auto_salary_calculator.py
    echo 請確認在正確的專案目錄中執行此腳本
    pause
    exit /b 1
)

REM 建立 Python 虛擬環境（如果不存在）
if not exist ".venv" (
    echo 📦 建立 Python 虛擬環境...
    python -m venv .venv
)

REM 啟動虛擬環境
echo 🔧 啟動虛擬環境...
call .venv\Scripts\activate.bat

REM 升級 pip
echo 📈 升級 pip...
python -m pip install --upgrade pip

REM 安裝依賴套件
echo 📦 安裝依賴套件...
pip install -r requirements.txt

REM 安裝 PyInstaller
echo 🛠️  安裝 PyInstaller...
pip install pyinstaller

REM 清理之前的建置
echo 🧹 清理之前的建置...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec.bak" del "*.spec.bak"

REM 使用 PyInstaller 建立執行檔
echo 🔨 建立執行檔...
pyinstaller salary_calculator.spec

REM 檢查建置結果
if exist "dist\淨膚寶薪資計算程式.exe" (
    echo ✅ Windows 執行檔建立成功！
    echo 📁 執行檔位置: dist\淨膚寶薪資計算程式.exe
    
    REM 建立分發資料夾
    echo 📦 建立分發資料夾...
    if not exist "release\Windows" mkdir "release\Windows"
    copy "dist\淨膚寶薪資計算程式.exe" "release\Windows\"
    
    REM 建立使用說明
    echo 淨膚寶薪資計算程式 - Windows 版本 > "release\Windows\使用說明.txt"
    echo. >> "release\Windows\使用說明.txt"
    echo 使用方法： >> "release\Windows\使用說明.txt"
    echo 1. 雙擊「淨膚寶薪資計算程式.exe」執行 >> "release\Windows\使用說明.txt"
    echo 2. 如果 Windows Defender 提示警告，請選擇「仍要執行」 >> "release\Windows\使用說明.txt"
    echo 3. 或在命令提示字元中執行：淨膚寶薪資計算程式.exe >> "release\Windows\使用說明.txt"
    echo. >> "release\Windows\使用說明.txt"
    echo 注意事項： >> "release\Windows\使用說明.txt"
    echo - 首次執行時程式會自動安裝必要的 Python 套件 >> "release\Windows\使用說明.txt"
    echo - 請確保系統已安裝 Python 3.7 或更新版本 >> "release\Windows\使用說明.txt"
    echo - 執行檔已包含所有必要的程式碼和依賴 >> "release\Windows\使用說明.txt"
    echo. >> "release\Windows\使用說明.txt"
    echo 技術支援： >> "release\Windows\使用說明.txt"
    echo 如有問題請聯繫程式開發者 >> "release\Windows\使用說明.txt"
    
    echo ✅ 分發資料夾建立完成: release\Windows\
    
) else (
    echo ❌ 執行檔建立失敗
    echo 請檢查錯誤訊息並重試
    pause
    exit /b 1
)

echo.
echo 🎉 Windows 打包完成！
echo ==================================
echo 執行檔位置: release\Windows\淨膚寶薪資計算程式.exe
echo 使用說明: release\Windows\使用說明.txt
pause
