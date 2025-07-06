#!/usr/bin/env python3
"""
建立獨立執行檔的主程式
這個版本包含了所有必要的依賴檢查和安裝
"""

import sys
import subprocess
import os
import platform
from pathlib import Path

def install_packages():
    """安裝必要的套件"""
    required_packages = ['pandas>=1.5.0', 'openpyxl>=3.0.0', 'xlrd>=2.0.1']
    
    for package in required_packages:
        try:
            __import__(package.split('>=')[0].split('==')[0])
        except ImportError:
            print(f"安裝 {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def main():
    """主程式入口"""
    print("淨膚寶薪水計算小程式")
    print("=" * 40)
    
    # 檢查並安裝依賴
    try:
        install_packages()
        print("✅ 所有依賴套件已準備就緒")
    except Exception as e:
        print(f"❌ 套件安裝失敗: {e}")
        input("按 Enter 鍵退出...")
        return
    
    # 匯入並執行主程式
    try:
        # 匯入主程式模組
        import auto_salary_calculator
        
        # 執行薪資計算
        auto_salary_calculator.main()
        
    except Exception as e:
        print(f"❌ 程式執行錯誤: {e}")
        import traceback
        traceback.print_exc()
    
    input("按 Enter 鍵退出...")

if __name__ == "__main__":
    main()
