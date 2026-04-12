# 淨膚寶薪資計算工具 Docker 容器
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 複製需求文件並安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用文件
COPY streamlit_salary_calculator.py .
COPY auto_salary_calculator.py .

# 創建非 root 用戶
RUN useradd -m -u 1000 streamlit
USER streamlit

# 暴露端口
EXPOSE 8501

# 設定 Streamlit 配置
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 啟動命令
CMD ["streamlit", "run", "streamlit_salary_calculator.py"]