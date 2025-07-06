#!/bin/bash
# 跨平台自動打包腳本

echo "🚀 淨膚寶薪資計算程式 - 跨平台打包工具"
echo "=============================================="

# 檢查作業系統
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "檢測到作業系統: $MACHINE"

# 檢查是否在正確的目錄
if [ ! -f "auto_salary_calculator.py" ]; then
    echo "❌ 錯誤：找不到 auto_salary_calculator.py"
    echo "請確認在正確的專案目錄中執行此腳本"
    exit 1
fi

# 建立通用的打包函數
build_executable() {
    local platform=$1
    echo "🔨 開始建立 $platform 執行檔..."
    
    # 建立或啟動虛擬環境
    if [ ! -d ".venv" ]; then
        echo "📦 建立 Python 虛擬環境..."
        python3 -m venv .venv 2>/dev/null || python -m venv .venv
    fi
    
    # 啟動虛擬環境
    echo "🔧 啟動虛擬環境..."
    if [ "$MACHINE" = "Mac" ] || [ "$MACHINE" = "Linux" ]; then
        source .venv/bin/activate
        PYTHON_CMD=".venv/bin/python"
        PIP_CMD=".venv/bin/pip"
    else
        source .venv/Scripts/activate
        PYTHON_CMD=".venv/Scripts/python"
        PIP_CMD=".venv/Scripts/pip"
    fi
    
    # 升級 pip 並安裝依賴
    echo "📈 升級 pip..."
    $PIP_CMD install --upgrade pip
    
    echo "📦 安裝依賴套件..."
    $PIP_CMD install -r requirements.txt
    
    echo "🛠️  安裝 PyInstaller..."
    $PIP_CMD install pyinstaller
    
    # 清理之前的建置
    echo "🧹 清理之前的建置..."
    rm -rf build dist *.spec.bak
    
    # 建立執行檔
    echo "🔨 使用 PyInstaller 建立執行檔..."
    $PYTHON_CMD -m PyInstaller salary_calculator.spec
    
    return $?
}

# 建立分發資料夾的函數
create_release() {
    local platform=$1
    local executable_name=$2
    
    echo "📦 建立 $platform 分發資料夾..."
    mkdir -p "release/$platform"
    
    if [ -f "dist/$executable_name" ]; then
        cp "dist/$executable_name" "release/$platform/"
        
        if [ "$platform" = "macOS" ]; then
            chmod +x "release/$platform/$executable_name"
        fi
        
        # 建立使用說明
        cat > "release/$platform/使用說明.txt" << EOF
淨膚寶薪資計算程式 - $platform 版本

使用方法：
1. 雙擊執行檔開始使用
2. 首次執行時程式會自動安裝必要的 Python 套件
3. 程式包含完整的薪資計算功能，包括：
   - 基本薪資計算
   - 加班費計算
   - 季獎金計算
   - Excel 檔案讀取與分析

系統需求：
- Python 3.7 或更新版本（如果系統沒有會自動提示安裝）
- 足夠的硬碟空間來安裝依賴套件

注意事項：
- 執行檔已包含所有必要的程式碼
- 如遇到安全性警告，請允許程式執行
- 首次執行可能需要較長時間來安裝依賴套件

技術支援：
如有問題請聯繫程式開發者

版本資訊：
建立日期: $(date)
建立系統: $MACHINE
EOF
        
        echo "✅ $platform 執行檔建立成功！"
        echo "📁 位置: release/$platform/$executable_name"
        return 0
    else
        echo "❌ $platform 執行檔建立失敗"
        return 1
    fi
}

# 主要建置流程
main() {
    echo "開始建置流程..."
    
    # 根據作業系統建立對應的執行檔
    case "$MACHINE" in
        Mac)
            build_executable "macOS"
            if [ $? -eq 0 ]; then
                create_release "macOS" "淨膚寶薪資計算程式"
            fi
            ;;
        Linux)
            build_executable "Linux"
            if [ $? -eq 0 ]; then
                create_release "Linux" "淨膚寶薪資計算程式"
            fi
            ;;
        *)
            echo "⚠️  目前在 $MACHINE 系統上"
            echo "請使用對應的打包腳本："
            echo "- Windows: build_windows.bat"
            echo "- macOS/Linux: build_macos.sh"
            ;;
    esac
    
    # 建立完整的分發包
    if [ -d "release" ]; then
        echo ""
        echo "📦 建立完整分發包..."
        
        # 複製重要檔案到分發資料夾
        cp requirements.txt release/ 2>/dev/null
        cp README.md release/ 2>/dev/null
        cp 使用說明.md release/ 2>/dev/null
        
        # 建立總體說明
        cat > "release/README.txt" << EOF
淨膚寶薪資計算程式 - 分發包

此分發包包含以下內容：

目錄結構：
$(find release -type f | sort)

使用方法：
1. 選擇對應作業系統的資料夾
2. 閱讀該資料夾中的使用說明.txt
3. 執行對應的執行檔

支援的作業系統：
- macOS (64-bit)
- Windows (64-bit)
- Linux (64-bit)

建立資訊：
建立日期: $(date)
建立系統: $MACHINE
Python 版本: $(python3 --version 2>/dev/null || python --version 2>/dev/null || echo "無法檢測")

技術支援：
如有問題請聯繫程式開發者
EOF
        
        echo "✅ 完整分發包建立完成！"
        echo "📁 位置: release/"
    fi
    
    echo ""
    echo "🎉 打包完成！"
    echo "=============================================="
    echo "請查看 release/ 資料夾中的執行檔"
}

# 執行主程式
main
