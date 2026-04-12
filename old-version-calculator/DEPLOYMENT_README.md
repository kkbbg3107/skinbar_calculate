# 淨膚寶薪資計算工具 - 部署指南

## 🌟 推薦方案：雲端部署（Streamlit Cloud）

### 優點
- 🆓 **完全免費**
- 🌐 **任何人都能通過網址直接使用**
- 🔄 **自動更新**：修改代碼後自動重新部署
- 📱 **手機友好**：支援手機、平板使用
- 🔒 **數據安全**：檔案上傳後立即處理，不會永久儲存

### 部署步驟

1. **準備 GitHub Repository**
   ```bash
   # 1. 在 GitHub 創建新的 repository
   # 2. 將以下文件上傳：
   - streamlit_salary_calculator.py
   - auto_salary_calculator.py
   - requirements.txt
   ```

2. **部署到 Streamlit Cloud**
   - 訪問：https://share.streamlit.io
   - 使用 GitHub 帳號登入
   - 點擊 "New app"
   - 選擇你的 repository
   - 主文件選擇：`streamlit_salary_calculator.py`
   - 點擊 "Deploy"

3. **獲得公開網址**
   - 部署完成後會得到類似：`https://yourapp.streamlit.app`
   - 分享這個網址給需要使用的人

---

## 💻 本地安裝方案

### 方案 A：Python 環境安裝

**適合對象**：有基本電腦操作能力的用戶

#### Windows 用戶
1. **安裝 Python**
   - 下載：https://python.org/downloads
   - 安裝時勾選 "Add Python to PATH"

2. **下載工具檔案**
   - 下載整個專案資料夾
   - 解壓縮到任意位置

3. **安裝依賴套件**
   ```bash
   # 在專案資料夾中開啟命令提示字元
   pip install -r requirements.txt
   ```

4. **啟動工具**
   ```bash
   streamlit run streamlit_salary_calculator.py
   ```

#### Mac 用戶
```bash
# 安裝 Homebrew（如果還沒安裝）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安裝 Python
brew install python

# 下載專案並安裝依賴
cd /path/to/project
pip3 install -r requirements.txt

# 啟動工具
streamlit run streamlit_salary_calculator.py
```

### 方案 B：一鍵啟動腳本

我會創建簡化的啟動腳本，雙擊即可運行。

---

## 🐳 Docker 容器化方案

**適合對象**：IT 部門或有 Docker 經驗的用戶

### 優點
- 環境完全隔離
- 一次設定，到處運行
- 不影響系統其他軟體

### 使用方法
```bash
# 1. 安裝 Docker Desktop
# 2. 運行容器
docker run -p 8501:8501 your-salary-calculator

# 3. 瀏覽器開啟
http://localhost:8501
```

---

## 📊 方案比較

| 方案 | 優點 | 缺點 | 適合對象 |
|------|------|------|----------|
| **Streamlit Cloud** | 免費、簡單、自動更新 | 需要網路 | 🌟 最推薦 |
| **本地安裝** | 私密、離線使用 | 需要安裝配置 | 內部使用 |
| **Docker** | 環境一致、專業 | 需要技術知識 | IT 部門 |

---

## 🚀 快速開始建議

1. **第一選擇**：使用 Streamlit Cloud 部署
   - 5分鐘內完成部署
   - 獲得永久網址
   - 任何人都能直接使用

2. **備選方案**：如果需要完全私密處理
   - 使用本地安裝方案
   - 提供一鍵啟動腳本

---

## ❓ 常見問題

**Q: 雲端部署安全嗎？**
A: 是的。Streamlit Cloud 不會永久儲存用戶上傳的檔案，處理完成後立即刪除。

**Q: 可以限制使用者嗎？**
A: Streamlit Cloud 部署的應用是公開的。如需限制存取，建議使用本地部署。

**Q: 如何更新應用？**
A: 雲端部署：直接修改 GitHub 代碼即可自動更新
A: 本地部署：重新下載最新版本檔案

**Q: 支援多人同時使用嗎？**
A: 是的。雲端部署支援多人同時使用，每個用戶有獨立的會話。

---

需要幫助？請聯繫開發者或查看詳細技術文檔。