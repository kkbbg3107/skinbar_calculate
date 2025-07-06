#!/bin/bash
# 一鍵式完整打包解決方案

set -e  # 發生錯誤時停止執行

echo "🚀 淨膚寶薪資計算程式 - 一鍵式打包"
echo "======================================"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 檢查作業系統
OS="$(uname -s)"
case "${OS}" in
    Darwin*)    PLATFORM="macOS";;
    Linux*)     PLATFORM="Linux";;
    *)          PLATFORM="Unknown";;
esac

log_info "檢測到作業系統: $PLATFORM"

# 檢查必要檔案
check_files() {
    log_info "檢查必要檔案..."
    
    required_files=("auto_salary_calculator.py" "standalone_main.py" "requirements.txt")
    
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            log_success "找到 $file"
        else
            log_error "缺少必要檔案: $file"
            exit 1
        fi
    done
}

# 設置 Python 環境
setup_python_env() {
    log_info "設置 Python 環境..."
    
    # 檢查 Python
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        log_error "未找到 Python！請先安裝 Python 3.7+"
        exit 1
    fi
    
    log_success "找到 Python: $PYTHON_CMD"
    
    # 檢查 Python 版本
    python_version=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    log_info "Python 版本: $python_version"
    
    # 建立虛擬環境
    if [ ! -d ".venv" ]; then
        log_info "建立虛擬環境..."
        $PYTHON_CMD -m venv .venv
        log_success "虛擬環境建立完成"
    else
        log_success "虛擬環境已存在"
    fi
    
    # 啟動虛擬環境
    log_info "啟動虛擬環境..."
    case "$PLATFORM" in
        macOS|Linux)
            source .venv/bin/activate
            PIP_CMD=".venv/bin/pip"
            PYTHON_CMD=".venv/bin/python"
            ;;
        *)
            log_error "不支援的作業系統: $PLATFORM"
            exit 1
            ;;
    esac
    
    log_success "虛擬環境已啟動"
}

# 安裝依賴
install_dependencies() {
    log_info "安裝依賴套件..."
    
    # 升級 pip
    $PIP_CMD install --upgrade pip --quiet
    
    # 安裝專案依賴
    $PIP_CMD install -r requirements.txt --quiet
    
    # 安裝 PyInstaller
    $PIP_CMD install pyinstaller --quiet
    
    log_success "所有依賴安裝完成"
}

# 建立執行檔
build_executable() {
    log_info "建立執行檔..."
    
    # 清理之前的建置
    rm -rf build dist *.spec.bak
    
    # 使用 PyInstaller 建立執行檔
    $PYTHON_CMD -m PyInstaller salary_calculator.spec --clean --noconfirm
    
    # 檢查建置結果
    executable_name="淨膚寶薪資計算程式"
    if [ "$PLATFORM" = "Windows" ]; then
        executable_name="${executable_name}.exe"
    fi
    
    if [ -f "dist/$executable_name" ]; then
        log_success "執行檔建立成功: dist/$executable_name"
        
        # 設定執行權限 (macOS/Linux)
        if [ "$PLATFORM" != "Windows" ]; then
            chmod +x "dist/$executable_name"
        fi
        
        return 0
    else
        log_error "執行檔建立失敗"
        return 1
    fi
}

# 建立分發包
create_release_package() {
    log_info "建立分發包..."
    
    release_dir="release/$PLATFORM"
    mkdir -p "$release_dir"
    
    executable_name="淨膚寶薪資計算程式"
    if [ "$PLATFORM" = "Windows" ]; then
        executable_name="${executable_name}.exe"
    fi
    
    # 複製執行檔
    cp "dist/$executable_name" "$release_dir/"
    
    # 建立使用說明
    cat > "$release_dir/使用說明.txt" << EOF
淨膚寶薪資計算程式 - $PLATFORM 版本

📋 使用方法：
1. 雙擊「$executable_name」執行程式
2. 按照提示選擇 Excel 檔案
3. 輸入正式淨膚師人數和行號
4. 程式會自動計算薪資和季獎金

⚠️  注意事項：
- 首次執行可能需要3-5秒載入時間
- 請確保 Excel 檔案格式正確
- 如遇安全性警告，請允許程式執行

🔧 系統需求：
- $PLATFORM 作業系統
- 至少 200MB 硬碟空間
- 1GB 以上記憶體

📞 技術支援：
如有問題請聯繫程式開發者

📅 建立資訊：
建立日期: $(date)
建立系統: $PLATFORM
Python 版本: $(python3 --version 2>/dev/null || python --version 2>/dev/null)
EOF
    
    # 建立啟動腳本（額外的便利功能）
    if [ "$PLATFORM" = "macOS" ] || [ "$PLATFORM" = "Linux" ]; then
        cat > "$release_dir/啟動程式.sh" << EOF
#!/bin/bash
# 啟動腳本
cd "\$(dirname "\$0")"
./淨膚寶薪資計算程式
EOF
        chmod +x "$release_dir/啟動程式.sh"
    fi
    
    log_success "分發包建立完成: $release_dir/"
}

# 建立完整說明文件
create_documentation() {
    log_info "建立說明文件..."
    
    cat > "release/分發說明.txt" << EOF
淨膚寶薪資計算程式 - 分發包
=============================

此分發包包含以下內容：

📁 目錄結構：
release/
├── $PLATFORM/                     # $PLATFORM 版本執行檔
│   ├── 淨膚寶薪資計算程式          # 主執行檔
│   ├── 使用說明.txt               # 使用說明
│   └── 啟動程式.sh                # 啟動腳本（$PLATFORM 專用）
└── 分發說明.txt                   # 本檔案

🎯 程式功能：
- 自動讀取 Excel 薪資檔案
- 計算基本薪資（底薪、伙食費、加班費、手技獎金）
- 計算團隊獎金
- 計算七項季獎金
- 動態偵測員工數據
- 生成詳細的薪資報表

💻 支援系統：
- macOS (Intel/Apple Silicon)
- Linux (64-bit)
- Windows (64-bit) - 需要使用 Windows 版打包腳本

📦 分發方式：
1. 將整個 release 資料夾壓縮成 ZIP
2. 分享給需要使用的人員
3. 解壓後選擇對應系統的執行檔

🔧 建立資訊：
建立日期: $(date)
建立平台: $PLATFORM
建立者: 自動打包腳本 v2.0

🆘 故障排除：
1. 如果執行檔無法開啟：
   - 檢查檔案權限
   - 嘗試在終端機中執行
   - 查看錯誤訊息

2. 如果出現安全性警告：
   - macOS: 系統偏好設定 → 安全性與隱私權 → 允許
   - Linux: 確認檔案有執行權限

3. 如果程式執行錯誤：
   - 檢查 Excel 檔案格式
   - 確認工作表名稱正確
   - 查看錯誤訊息提示

📞 技術支援：
如需協助請聯繫程式開發者
EOF
    
    log_success "說明文件建立完成"
}

# 主要執行流程
main() {
    echo ""
    log_info "開始執行一鍵式打包流程..."
    
    # 執行各個步驟
    check_files
    setup_python_env
    install_dependencies
    
    if build_executable; then
        create_release_package
        create_documentation
        
        echo ""
        echo "🎉 打包完成！"
        echo "======================================"
        log_success "執行檔位置: release/$PLATFORM/"
        log_success "分發包位置: release/"
        
        # 顯示檔案大小資訊
        if [ -f "release/$PLATFORM/淨膚寶薪資計算程式" ]; then
            file_size=$(ls -lh "release/$PLATFORM/淨膚寶薪資計算程式" | awk '{print $5}')
            log_info "執行檔大小: $file_size"
        fi
        
        echo ""
        log_info "接下來你可以："
        echo "  1. 測試執行檔: cd release/$PLATFORM && ./淨膚寶薪資計算程式"
        echo "  2. 壓縮分發包: zip -r salary_calculator_$PLATFORM.zip release/"
        echo "  3. 分享給其他使用者"
        
    else
        log_error "打包失敗"
        exit 1
    fi
}

# 錯誤處理
trap 'log_error "打包過程中發生錯誤，請檢查上方錯誤訊息"' ERR

# 執行主程式
main "$@"
