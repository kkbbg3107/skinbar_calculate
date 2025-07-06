# 🎯 淨膚寶薪資計算程式 - 完整打包指南

## 📦 快速開始

### macOS/Linux 使用者

```bash
# 一鍵式打包（推薦）
./one_click_build.sh

# 或使用原有腳本
./build_macos.sh
```

### Windows 使用者

```cmd
REM 一鍵式打包（推薦）
one_click_build.bat

REM 或使用原有腳本
build_windows.bat
```

## 🔥 新增功能

### ✨ 一鍵式打包 (`one_click_build.sh` / `one_click_build.bat`)

**特色：**
- 🚀 完全自動化的打包流程
- 🔍 自動檢查環境和依賴
- 📦 自動建立分發包
- 📝 自動生成使用說明
- 🎨 彩色終端輸出和進度提示
- ❌ 智能錯誤處理和故障排除

**優勢：**
- 無需手動步驟
- 包含完整的錯誤檢查
- 生成專業的分發包
- 支援多平台

### 🔧 智能環境管理

**自動化功能：**
- Python 環境檢查和建立
- 虛擬環境自動配置
- 依賴套件自動安裝
- PyInstaller 自動配置

### 📋 完整的分發包

**包含內容：**
```
release/
├── macOS/ (或 Windows/)
│   ├── 淨膚寶薪資計算程式[.exe]    # 主執行檔
│   ├── 使用說明.txt                # 詳細使用說明
│   └── 啟動程式.sh[.bat]           # 便利啟動腳本
└── 分發說明.txt                    # 完整分發指南
```

## 🎮 使用方法

### 步驟一：選擇打包方式

| 方式 | 優點 | 適用情況 |
|------|------|----------|
| 一鍵式打包 | 完全自動，零配置 | **推薦給所有使用者** |
| 傳統腳本 | 可自訂步驟 | 需要客製化配置時 |
| 手動打包 | 完全控制 | 除錯或特殊需求 |

### 步驟二：執行打包

```bash
# macOS/Linux 一鍵式打包
chmod +x one_click_build.sh
./one_click_build.sh

# 查看結果
ls -la release/
```

```cmd
REM Windows 一鍵式打包
one_click_build.bat

REM 查看結果
dir release
```

### 步驟三：測試執行檔

```bash
# macOS/Linux 測試
cd release/macOS/  # 或 Linux/
./淨膚寶薪資計算程式
```

```cmd
REM Windows 測試
cd release\Windows
淨膚寶薪資計算程式.exe
```

### 步驟四：分發給使用者

1. 壓縮 `release/` 資料夾
2. 分享壓縮檔
3. 使用者解壓後執行對應平台的執行檔

## 📊 打包檔案說明

### 核心檔案

| 檔案 | 用途 | 說明 |
|------|------|------|
| `standalone_main.py` | 獨立執行入口 | 包含依賴檢查和自動安裝 |
| `portable_launcher.py` | 可攜式啟動器 | 輕量級啟動方案 |
| `salary_calculator.spec` | PyInstaller 配置 | 打包設定和依賴定義 |

### 打包腳本

| 腳本 | 平台 | 特色 |
|------|------|------|
| `one_click_build.sh` | macOS/Linux | 🌟 一鍵式完整打包 |
| `one_click_build.bat` | Windows | 🌟 一鍵式完整打包 |
| `build_macos.sh` | macOS | 傳統打包腳本 |
| `build_windows.bat` | Windows | 傳統打包腳本 |
| `build_all.sh` | 跨平台 | 通用打包腳本 |

### 測試工具

| 工具 | 用途 |
|------|------|
| `test_build_env.py` | 環境檢查 |
| `save_analysis.py` | 分析工具 |

## ⚙️ 打包配置

### PyInstaller 設定

```python
# salary_calculator.spec 重點配置
hiddenimports=[
    'pandas', 'openpyxl', 'xlrd', 'numpy',
    'pandas._libs.tslibs.timedeltas',
    'pandas._libs.tslibs.np_datetime',
    # ... 更多隱藏依賴
]
```

### 自動依賴管理

```python
# standalone_main.py 核心功能
def install_packages():
    required_packages = [
        'pandas>=1.5.0', 
        'openpyxl>=3.0.0', 
        'xlrd>=2.0.1'
    ]
    # 自動檢查和安裝
```

## 🔧 客製化選項

### 修改執行檔名稱

編輯 `salary_calculator.spec`：
```python
exe = EXE(
    # ...
    name='你的自訂名稱',  # 修改此行
    # ...
)
```

### 新增圖示

編輯 `salary_calculator.spec`：
```python
exe = EXE(
    # ...
    icon='path/to/your/icon.ico',  # 新增此行
    # ...
)
```

### 修改建立的目錄結構

編輯打包腳本中的 `create_release_package()` 函數。

## 🚨 故障排除

### 常見問題

**Q: 打包後執行檔太大**
```bash
# 解決方案：使用 portable_launcher.py
cp portable_launcher.py main.py
# 然後分發 main.py + auto_salary_calculator.py + requirements.txt
```

**Q: macOS 安全性警告**
```bash
# 解決方案：
# 1. 系統偏好設定 → 安全性與隱私權 → 允許
# 2. 或使用終端執行：
xattr -d com.apple.quarantine 淨膚寶薪資計算程式
```

**Q: Windows Defender 警告**
```cmd
REM 解決方案：
REM 1. 選擇「其他資訊」→「仍要執行」
REM 2. 或新增到排除清單
```

**Q: 依賴安裝失敗**
```bash
# 解決方案：手動安裝
pip install --upgrade pip
pip install pandas openpyxl xlrd pyinstaller
```

### 除錯模式

```bash
# 開啟詳細輸出
./one_click_build.sh 2>&1 | tee build.log

# 檢查建置日誌
cat build.log
```

### 手動檢查

```bash
# 檢查 Python 環境
python3 --version
pip list

# 檢查檔案完整性
ls -la auto_salary_calculator.py standalone_main.py requirements.txt

# 測試主程式
python3 auto_salary_calculator.py
```

## 📈 效能優化

### 減少執行檔大小

1. **使用 UPX 壓縮**（在 spec 檔案中已啟用）
2. **排除不必要的模組**
3. **使用可攜式啟動器代替完整打包**

### 提升啟動速度

1. **優化 hiddenimports 清單**
2. **減少自動安裝的套件**
3. **使用 console=False 建立 GUI 版本**

## 🎉 部署建議

### 企業分發

1. **建立內部分發伺服器**
2. **使用數位簽章**（Windows）
3. **建立自動更新機制**

### 個人使用

1. **雲端儲存分享**（Google Drive、Dropbox）
2. **USB 隨身碟分發**
3. **電子郵件附件**

## 📞 技術支援

### 取得協助

1. **檢查 `DEPLOYMENT_GUIDE.md`**
2. **查看 release/ 資料夾中的說明檔案**
3. **聯繫程式開發者**

### 回報問題

請提供：
- 作業系統版本
- Python 版本
- 錯誤訊息
- 建置日誌

---

🚀 **享受自動化薪資計算的便利！**
