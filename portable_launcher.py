#!/usr/bin/env python3
"""
可攜式啟動器 - 自動處理環境設置
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

def check_python():
    """檢查 Python 環境"""
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print(f"❌ Python 版本過舊: {python_version.major}.{python_version.minor}")
        print("需要 Python 3.7 或更新版本")
        return False
    
    print(f"✅ Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    return True

def setup_environment():
    """設置可攜式環境"""
    app_dir = Path(__file__).parent
    venv_dir = app_dir / "portable_env"
    
    print(f"🏠 應用程式目錄: {app_dir}")
    print(f"📦 可攜式環境: {venv_dir}")
    
    # 建立可攜式虛擬環境
    if not venv_dir.exists():
        print("📦 建立可攜式 Python 環境...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
            print("✅ 可攜式環境建立成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ 建立環境失敗: {e}")
            return None
    
    # 取得 Python 執行檔路徑
    if platform.system() == "Windows":
        python_exe = venv_dir / "Scripts" / "python.exe"
        pip_exe = venv_dir / "Scripts" / "pip.exe"
    else:
        python_exe = venv_dir / "bin" / "python"
        pip_exe = venv_dir / "bin" / "pip"
    
    return python_exe, pip_exe

def install_requirements(pip_exe):
    """安裝必要套件"""
    requirements = ["pandas>=1.5.0", "openpyxl>=3.0.0", "xlrd>=2.0.1"]
    
    print("📦 檢查並安裝必要套件...")
    
    # 升級 pip
    try:
        subprocess.run([str(pip_exe), "install", "--upgrade", "pip"], 
                      check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        print("⚠️  無法升級 pip，繼續使用現有版本")
    
    # 安裝套件
    for package in requirements:
        try:
            print(f"  安裝 {package}...")
            subprocess.run([str(pip_exe), "install", package], 
                          check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ 安裝 {package} 失敗: {e}")
            return False
    
    print("✅ 所有套件安裝完成")
    return True

def run_main_program(python_exe):
    """執行主程式"""
    main_script = Path(__file__).parent / "auto_salary_calculator.py"
    
    if not main_script.exists():
        print(f"❌ 找不到主程式: {main_script}")
        return False
    
    print("🚀 啟動淨膚寶薪資計算程式...")
    print("=" * 50)
    
    try:
        # 切換到主程式目錄
        os.chdir(Path(__file__).parent)
        
        # 執行主程式
        result = subprocess.run([str(python_exe), str(main_script)], 
                               check=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 執行主程式失敗: {e}")
        return False

def main():
    """主要啟動流程"""
    print("🌟 淨膚寶薪資計算程式 - 可攜式啟動器")
    print("=" * 50)
    
    # 檢查 Python 環境
    if not check_python():
        input("按 Enter 鍵退出...")
        return
    
    # 設置可攜式環境
    env_result = setup_environment()
    if env_result is None:
        input("按 Enter 鍵退出...")
        return
    
    python_exe, pip_exe = env_result
    
    # 安裝依賴套件
    if not install_requirements(pip_exe):
        input("按 Enter 鍵退出...")
        return
    
    # 執行主程式
    success = run_main_program(python_exe)
    
    if not success:
        print("\n程式執行完成")
    
    input("按 Enter 鍵退出...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程式被使用者中斷")
    except Exception as e:
        print(f"\n❌ 啟動器錯誤: {e}")
        import traceback
        traceback.print_exc()
        input("按 Enter 鍵退出...")
