# 淨膚寶薪資計算程式 - 打包部署指南

## 🎯 概述

這個指南將幫你建立跨平台的獨立執行檔，讓其他人可以在沒有 Python 環境的情況下直接使用薪資計算程式。

## 📦 打包方案

### 方案一：PyInstaller 完全獨立執行檔 ⭐️ 推薦
- **優點**：完全獨立，不需要 Python 環境
- **缺點**：檔案較大（約 50-100MB）
- **適用**：需要分享給完全沒有技術背景的使用者

### 方案二：可攜式啟動器
- **優點**：檔案小，自動處理環境
- **缺點**：需要系統有 Python 3.7+
- **適用**：分享給有基本 Python 環境的使用者

## 🚀 使用方法

### macOS 打包

```bash
# 方法一：使用 macOS 專用腳本
./build_macos.sh

# 方法二：使用跨平台腳本
./build_all.sh
```

### Windows 打包

```cmd
REM 在 Windows 命令提示字元中執行
build_windows.bat
```

### 手動打包步驟

如果自動腳本無法執行，可以手動進行：

```bash
# 1. 建立虛擬環境
python -m venv .venv

# 2. 啟動虛擬環境
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 3. 安裝依賴
pip install -r requirements.txt
pip install pyinstaller

# 4. 建立執行檔
pyinstaller salary_calculator.spec

# 5. 檢查結果
ls dist/  # macOS/Linux
dir dist  # Windows
```

## 📁 輸出結構

打包完成後，會產生以下結構：

```
release/
├── macOS/                          # macOS 版本
│   ├── 淨膚寶薪資計算程式           # 主執行檔
│   └── 使用說明.txt                # 使用說明
├── Windows/                        # Windows 版本
│   ├── 淨膚寶薪資計算程式.exe      # 主執行檔
│   └── 使用說明.txt                # 使用說明
└── README.txt                      # 總體說明
```

## 🔧 檔案說明

### 核心檔案
- `standalone_main.py` - 獨立執行的主程式入口
- `portable_launcher.py` - 可攜式啟動器
- `salary_calculator.spec` - PyInstaller 設定檔

### 打包腳本
- `build_macos.sh` - macOS 自動打包腳本
- `build_windows.bat` - Windows 自動打包腳本
- `build_all.sh` - 跨平台自動打包腳本

## ⚙️ 打包特色

### 🔄 自動依賴管理
- 執行檔會自動檢查並安裝必要的 Python 套件
- 包含完整的 pandas、openpyxl、xlrd 依賴
- 自動處理版本相容性

### 🛡️ 錯誤處理
- 完整的錯誤捕捉和使用者友善的錯誤訊息
- 自動檢查 Python 版本需求
- 優雅的程式退出機制

### 📱 跨平台支援
- 支援 macOS (Intel/Apple Silicon)
- 支援 Windows (64-bit)
- 支援 Linux (64-bit)

## 🚨 注意事項

### 安全性警告
- **macOS**: 可能會出現「無法驗證開發者」警告
  - 解決方法：系統偏好設定 → 安全性與隱私權 → 允許執行
- **Windows**: 可能會被 Windows Defender 標記
  - 解決方法：選擇「仍要執行」或新增到排除清單

### 系統需求
- **Python**: 3.7 或更新版本（使用可攜式啟動器時）
- **記憶體**: 至少 1GB 可用記憶體
- **硬碟**: 至少 200MB 可用空間

### 效能考量
- 第一次執行較慢（需要初始化環境）
- 後續執行速度正常
- PyInstaller 執行檔啟動時間約 3-5 秒

## 🔄 更新流程

當程式有更新時：

1. 更新原始碼
2. 重新執行打包腳本
3. 將新的執行檔分發給使用者
4. 使用者只需替換執行檔即可

## 📞 技術支援

### 常見問題

**Q: 執行檔太大怎麼辦？**
A: 使用 `portable_launcher.py` 代替完整打包，檔案會小很多。

**Q: 無法執行怎麼辦？**
A: 檢查系統是否有 Python 3.7+，或使用完整的 PyInstaller 版本。

**Q: 如何自訂執行檔圖示？**
A: 在 `salary_calculator.spec` 中修改 `icon` 參數。

### 除錯模式

如果遇到問題，可以在終端機中執行：

```bash
# macOS/Linux
./淨膚寶薪資計算程式

# Windows
淨膚寶薪資計算程式.exe
```

這樣可以看到詳細的錯誤訊息。

## 🎉 部署完成

打包完成後，你可以：

1. 將 `release/` 資料夾壓縮成 ZIP 檔案
2. 分享給需要使用的人員
3. 提供對應平台的使用說明

享受自動化薪資計算的便利！ 🚀
