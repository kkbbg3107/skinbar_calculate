#!/bin/bash
# macOS 自動打包腳本

echo "🚀 開始建立 macOS 執行檔..."
echo "=================================="

# 檢查是否在正確的目錄
if [ ! -f "auto_salary_calculator.py" ]; then
    echo "❌ 錯誤：找不到 auto_salary_calculator.py"
    echo "請確認在正確的專案目錄中執行此腳本"
    exit 1
fi

# 建立 Python 虛擬環境（如果不存在）
if [ ! -d ".venv" ]; then
    echo "📦 建立 Python 虛擬環境..."
    python3 -m venv .venv
fi

# 啟動虛擬環境
echo "🔧 啟動虛擬環境..."
source .venv/bin/activate

# 升級 pip
echo "📈 升級 pip..."
pip install --upgrade pip

# 安裝依賴套件
echo "📦 安裝依賴套件..."
pip install -r requirements.txt

# 安裝 PyInstaller
echo "🛠️  安裝 PyInstaller..."
pip install pyinstaller

# 清理之前的建置
echo "🧹 清理之前的建置..."
rm -rf build dist *.spec.bak

# 使用 PyInstaller 建立執行檔
echo "🔨 建立執行檔..."
pyinstaller salary_calculator.spec

# 檢查建置結果
if [ -f "dist/淨膚寶薪資計算程式" ]; then
    echo "✅ macOS 執行檔建立成功！"
    echo "📁 執行檔位置: dist/淨膚寶薪資計算程式"
    
    # 設定執行權限
    chmod +x "dist/淨膚寶薪資計算程式"
    
    # 建立分發資料夾
    echo "📦 建立分發資料夾..."
    mkdir -p "release/macOS"
    cp "dist/淨膚寶薪資計算程式" "release/macOS/"
    
    # 建立使用說明
    cat > "release/macOS/使用說明.txt" << EOF
淨膚寶薪資計算程式 - macOS 版本

使用方法：
1. 雙擊「淨膚寶薪資計算程式」執行
2. 如果系統提示安全性警告，請至「系統偏好設定」>「安全性與隱私權」允許執行
3. 或在終端機中執行：./淨膚寶薪資計算程式

注意事項：
- 首次執行時程式會自動安裝必要的 Python 套件
- 請確保系統已安裝 Python 3.7 或更新版本
- 執行檔已包含所有必要的程式碼和依賴

技術支援：
如有問題請聯繫程式開發者
EOF
    
    echo "✅ 分發資料夾建立完成: release/macOS/"
    
else
    echo "❌ 執行檔建立失敗"
    echo "請檢查錯誤訊息並重試"
    exit 1
fi

echo ""
echo "🎉 macOS 打包完成！"
echo "=================================="
echo "執行檔位置: release/macOS/淨膚寶薪資計算程式"
echo "使用說明: release/macOS/使用說明.txt"
