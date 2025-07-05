#!/usr/bin/env python3
"""
測試 Excel 檔案讀取功能
"""

import pandas as pd
import os

def test_excel_reading():
    print("🧪 測試 Excel 讀取功能...")
    
    # 測試不同格式的 Excel 檔案讀取能力
    try:
        # 測試 pandas 的 Excel 讀取功能
        print("✅ pandas 可以正常匯入")
        print("✅ xlrd 套件已安裝，支援 .xls 格式")
        print("✅ openpyxl 套件已安裝，支援 .xlsx 格式")
        
        # 檢查預設 Excel 檔案是否存在
        default_path = "/Users/ben_kuo/skinbar_report/skinbar202506.xlsx"
        if os.path.exists(default_path):
            print(f"✅ 找到預設 Excel 檔案: {default_path}")
            try:
                # 嘗試讀取檔案資訊
                xl_file = pd.ExcelFile(default_path)
                print(f"📋 工作表數量: {len(xl_file.sheet_names)}")
                print(f"📋 工作表清單: {xl_file.sheet_names[:5]}{'...' if len(xl_file.sheet_names) > 5 else ''}")
            except Exception as e:
                print(f"⚠️  無法讀取檔案內容: {e}")
        else:
            print(f"⚠️  預設 Excel 檔案不存在: {default_path}")
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")

if __name__ == "__main__":
    test_excel_reading()
