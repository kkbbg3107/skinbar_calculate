# 🎯 淨膚寶薪資計算程式 - 分發指南

## 📦 給別人使用薪資計算程式的檔案清單

### 方案一：完整獨立執行檔（推薦）⭐️

如果你已經執行了打包腳本，給別人這個資料夾：
```
release/
├── macOS/                          # macOS 使用者
│   ├── 淨膚寶薪資計算程式           # 主執行檔
│   └── 使用說明.txt                # 使用說明
├── Windows/                        # Windows 使用者  
│   ├── 淨膚寶薪資計算程式.exe      # 主執行檔
│   └── 使用說明.txt                # 使用說明
└── 分發說明.txt                    # 總體說明
```

**優點**：
- ✅ 使用者不需要安裝 Python
- ✅ 雙擊就能執行
- ✅ 包含所有必要依賴

### 方案二：可攜式 Python 版本

給別人這些檔案：
```
📁 淨膚寶薪資計算程式/
├── portable_launcher.py           # 可攜式啟動器
├── auto_salary_calculator.py      # 主程式
├── requirements.txt               # 依賴清單
└── 使用說明.txt                   # 使用說明
```

**優點**：
- ✅ 檔案小（約 5MB）
- ✅ 自動處理環境設定
- ✅ 自動安裝依賴

**缺點**：
- ❌ 需要系統有 Python 3.7+

### 方案三：原始碼版本（最小）

給別人這些檔案：
```
📁 淨膚寶薪資計算程式/
├── auto_salary_calculator.py      # 主程式
├── requirements.txt               # 依賴清單
├── run_salary_calculator.command  # macOS 啟動器
├── run_salary_calculator.bat      # Windows 啟動器
└── 使用說明.txt                   # 使用說明
```

**適合**：有技術背景的使用者

## 🚀 快速建立分發包

### 步驟一：選擇分發方式

我建議使用**方案一（完整執行檔）**，因為最容易使用。

### 步驟二：執行打包

```bash
# macOS/Linux
./one_click_build.sh

# Windows  
one_click_build.bat
```

### 步驟三：準備分發檔案

打包完成後，你會得到 `release/` 資料夾，直接將此資料夾：
1. 壓縮成 ZIP 檔案
2. 分享給使用者
3. 告訴他們解壓後選擇對應系統的執行檔

## 📋 分發檔案的使用方式

### 給 macOS 使用者：
1. 解壓檔案
2. 進入 `macOS/` 資料夾
3. 雙擊 `淨膚寶薪資計算程式`
4. 如有安全性警告，到「系統偏好設定」→「安全性與隱私權」允許執行

### 給 Windows 使用者：
1. 解壓檔案
2. 進入 `Windows/` 資料夾  
3. 雙擊 `淨膚寶薪資計算程式.exe`
4. 如有 Windows Defender 警告，選擇「仍要執行」

## ⚡ 如果不想打包，直接分發原始碼

如果你不想執行打包程序，可以直接給別人這些檔案：

### 必要檔案：
- `auto_salary_calculator.py` - 主程式
- `requirements.txt` - 依賴清單

### 便利啟動器（選擇性）：
- `portable_launcher.py` - 可攜式啟動器（推薦）
- `run_salary_calculator.command` - macOS 啟動器
- `run_salary_calculator.bat` - Windows 啟動器

### 使用說明：
建立一個 `使用說明.txt`：
```
淨膚寶薪資計算程式使用說明

方法一：使用可攜式啟動器（推薦）
1. 確保電腦有 Python 3.7+
2. 雙擊 portable_launcher.py
3. 程式會自動安裝依賴並執行

方法二：使用啟動器
1. macOS: 雙擊 run_salary_calculator.command
2. Windows: 雙擊 run_salary_calculator.bat

方法三：手動執行（技術人員）
1. 安裝依賴: pip install -r requirements.txt
2. 執行程式: python auto_salary_calculator.py

注意事項：
- 需要準備正確格式的 Excel 檔案
- 檔案中需要有「月報表彙整」工作表
- 按照程式提示輸入正式淨膚師人數和行號
```

## 🎯 建議的分發方式

### 最佳方案：
1. **執行打包腳本** - `./one_click_build.sh`
2. **壓縮 release 資料夾** - `zip -r 薪資計算程式.zip release/`
3. **分享 ZIP 檔案**給使用者

### 簡單方案：
直接給這 3 個檔案：
- `portable_launcher.py`
- `auto_salary_calculator.py`  
- `requirements.txt`

加上一個簡單的使用說明即可！

---
💡 **重點**：使用者收到檔案後，只需要雙擊對應的啟動器就能使用，程式會自動處理所有環境設定！
