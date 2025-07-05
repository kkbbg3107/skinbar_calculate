#!/usr/bin/env python3
"""
Excel 檔案診斷工具
診斷 OLE2 compound document 錯誤
"""

import pandas as pd
import os
from pathlib import Path

def diagnose_excel_file(file_path):
    """診斷 Excel 檔案問題"""
    print(f"🔍 診斷 Excel 檔案: {file_path}")
    print("=" * 60)
    
    # 檢查檔案是否存在
    if not os.path.exists(file_path):
        print(f"❌ 檔案不存在: {file_path}")
        return False
    
    # 檢查檔案大小
    file_size = os.path.getsize(file_path)
    print(f"📏 檔案大小: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
    
    # 檢查檔案副檔名
    file_ext = Path(file_path).suffix.lower()
    print(f"📄 檔案格式: {file_ext}")
    
    # 檢查檔案權限
    print(f"🔒 可讀取: {os.access(file_path, os.R_OK)}")
    
    # 嘗試不同的讀取方法
    print("\n🧪 嘗試不同的讀取方法:")
    
    # 方法1: 使用 openpyxl 引擎 (適用於 .xlsx)
    if file_ext == '.xlsx':
        try:
            df = pd.read_excel(file_path, engine='openpyxl', sheet_name=None, nrows=1)
            print(f"✅ openpyxl 引擎成功 - 找到 {len(df)} 個工作表")
            print(f"   工作表名稱: {list(df.keys())[:5]}{'...' if len(df) > 5 else ''}")
            return True
        except Exception as e:
            print(f"❌ openpyxl 引擎失敗: {e}")
    
    # 方法2: 使用 xlrd 引擎 (適用於 .xls)
    if file_ext == '.xls':
        try:
            df = pd.read_excel(file_path, engine='xlrd', sheet_name=None, nrows=1)
            print(f"✅ xlrd 引擎成功 - 找到 {len(df)} 個工作表")
            print(f"   工作表名稱: {list(df.keys())[:5]}{'...' if len(df) > 5 else ''}")
            return True
        except Exception as e:
            print(f"❌ xlrd 引擎失敗: {e}")
    
    # 方法3: 自動偵測引擎
    try:
        df = pd.read_excel(file_path, sheet_name=None, nrows=1)
        print(f"✅ 自動偵測成功 - 找到 {len(df)} 個工作表")
        print(f"   工作表名稱: {list(df.keys())[:5]}{'...' if len(df) > 5 else ''}")
        return True
    except Exception as e:
        print(f"❌ 自動偵測失敗: {e}")
    
    # 方法4: 檢查是否為有效的 Excel 檔案
    try:
        xl_file = pd.ExcelFile(file_path)
        print("✅ ExcelFile 物件建立成功")
        print(f"   工作表: {xl_file.sheet_names}")
        return True
    except Exception as e:
        print(f"❌ ExcelFile 物件建立失敗: {e}")
    
    return False

def suggest_solutions():
    """建議解決方案"""
    print("\n💡 建議解決方案:")
    print("1. 檢查 Excel 檔案是否完整下載/複製")
    print("2. 嘗試在 Excel 中開啟檔案，另存為新的 .xlsx 格式")
    print("3. 檢查檔案是否被其他程序佔用")
    print("4. 如果是 .xls 格式，嘗試轉換為 .xlsx 格式")
    print("5. 檢查檔案路徑是否包含特殊字元")

if __name__ == "__main__":
    # 測試預設路徑
    default_path = "/Users/ben_kuo/skinbar_report/skinbar202506.xlsx"
    
    print("🏥 Excel 檔案診斷工具")
    print("=" * 60)
    
    success = diagnose_excel_file(default_path)
    
    if not success:
        suggest_solutions()
        
        # 尋找其他可能的 Excel 檔案
        print("\n🔍 搜尋其他 Excel 檔案:")
        report_dir = Path("/Users/ben_kuo/skinbar_report/")
        if report_dir.exists():
            excel_files = list(report_dir.glob("*.xlsx")) + list(report_dir.glob("*.xls"))
            if excel_files:
                print("找到的 Excel 檔案:")
                for file in excel_files:
                    print(f"  - {file}")
            else:
                print("  未找到任何 Excel 檔案")
        else:
            print(f"  報告目錄不存在: {report_dir}")
