#!/usr/bin/env python3
"""
簡單的 Excel 檔案測試工具
"""

def test_excel_file():
    import pandas as pd
    import os
    
    # 檢查常見的 Excel 檔案位置
    possible_paths = [
        "/Users/ben_kuo/skinbar_report/skinbar202506.xlsx",
        "/Users/ben_kuo/skinbar_report/skinbar202506.xls",
        "/Users/ben_kuo/skinbar_money/test.xlsx",
        "/Users/ben_kuo/Desktop/skinbar202506.xlsx",
        "/Users/ben_kuo/Downloads/skinbar202506.xlsx"
    ]
    
    print("🔍 搜尋 Excel 檔案...")
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ 找到檔案: {path}")
            file_size = os.path.getsize(path)
            print(f"   大小: {file_size:,} bytes")
            
            # 嘗試讀取
            try:
                # 先嘗試讀取工作表名稱
                xl_file = pd.ExcelFile(path)
                print(f"   工作表: {xl_file.sheet_names[:3]}...")
                return path
            except Exception as e:
                print(f"   ❌ 讀取失敗: {e}")
                
                # 如果是 OLE2 錯誤，嘗試不同方法
                if "OLE2" in str(e) or "compound document" in str(e):
                    print("   🔧 嘗試修復 OLE2 錯誤...")
                    
                    # 檢查是否為 .xls 格式但實際是 .xlsx
                    if path.endswith('.xls'):
                        new_path = path.replace('.xls', '.xlsx')
                        print(f"   💡 建議：將檔案重新命名為 {new_path}")
                    
                    # 或者嘗試指定引擎
                    try:
                        if path.endswith('.xlsx'):
                            pd.read_excel(path, engine='openpyxl', nrows=1)
                            print("   ✅ 使用 openpyxl 引擎成功")
                            return path
                        elif path.endswith('.xls'):
                            pd.read_excel(path, engine='xlrd', nrows=1)
                            print("   ✅ 使用 xlrd 引擎成功")
                            return path
                    except Exception as e2:
                        print(f"   ❌ 指定引擎也失敗: {e2}")
        else:
            print(f"❌ 檔案不存在: {path}")
    
    print("\n💡 建議解決方案:")
    print("1. 檢查 Excel 檔案路徑是否正確")
    print("2. 如果檔案存在但無法讀取，嘗試：")
    print("   - 在 Excel 中開啟檔案，另存為新的 .xlsx 格式")
    print("   - 檢查檔案是否損壞")
    print("   - 確認檔案沒有被其他程序佔用")
    print("3. 提供正確的檔案路徑")
    
    return None

if __name__ == "__main__":
    test_excel_file()
