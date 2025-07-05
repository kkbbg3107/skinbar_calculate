#!/usr/bin/env python3
"""
Excel 檔案問題診斷與修復工具
專門處理 OLE2 compound document 錯誤
"""

import os
import pandas as pd
from auto_salary_calculator import SalaryCalculator

def diagnose_excel_problem():
    """診斷 Excel 檔案問題"""
    print("🏥 Excel 檔案診斷工具")
    print("=" * 50)
    
    # 測試路徑
    test_paths = [
        "/Users/ben_kuo/skinbar_report/skinbar202506.xlsx",
        "/Users/ben_kuo/skinbar_report/skinbar202506.xls",
        "/Users/ben_kuo/Desktop/skinbar202506.xlsx",
        "/Users/ben_kuo/Downloads/skinbar202506.xlsx"
    ]
    
    calculator = SalaryCalculator()
    
    for path in test_paths:
        print(f"\n🔍 檢查: {path}")
        
        if not os.path.exists(path):
            print("❌ 檔案不存在")
            continue
            
        file_size = os.path.getsize(path)
        print(f"📏 檔案大小: {file_size:,} bytes")
        
        if file_size == 0:
            print("❌ 檔案大小為 0，可能是空檔案")
            continue
            
        # 測試讀取
        try:
            print("🧪 測試使用安全讀取功能...")
            xl_file = pd.ExcelFile(path)
            print("✅ 成功讀取 Excel 檔案")
            print(f"📋 工作表數量: {len(xl_file.sheet_names)}")
            
            # 檢查必要的工作表
            if '月報表彙整' in xl_file.sheet_names:
                print("✅ 找到「月報表彙整」工作表")
            else:
                print("❌ 缺少「月報表彙整」工作表")
                print(f"   現有工作表: {xl_file.sheet_names}")
            
            # 測試讀取月報表彙整
            try:
                df = calculator.safe_read_excel(path, sheet_name='月報表彙整', header=None)
                print(f"✅ 成功讀取月報表彙整，大小: {df.shape}")
                return path  # 找到可用的檔案
            except Exception as read_error:
                print(f"❌ 讀取月報表彙整失敗: {read_error}")
                
        except Exception as e:
            print(f"❌ 讀取失敗: {e}")
            
            if "OLE2" in str(e) or "compound document" in str(e):
                print("🔧 這是 OLE2 compound document 錯誤")
                suggest_ole2_fix(path)
    
    print("\n❌ 所有測試路徑都無法正常讀取")
    print("請提供正確的 Excel 檔案路徑")
    return None

def suggest_ole2_fix(file_path):
    """提供 OLE2 錯誤的修復建議"""
    print("\n💡 OLE2 錯誤修復建議:")
    print("1. 在 Microsoft Excel 中開啟檔案")
    print("2. 點選「檔案」→「另存新檔」")
    print("3. 選擇「Excel 活頁簿 (*.xlsx)」格式")
    print("4. 儲存為新檔案")
    
    new_path = str(file_path).replace('.xls', '_fixed.xlsx')
    print(f"5. 建議新檔案名稱: {new_path}")
    
    print("\n⚠️  常見原因:")
    print("- 檔案在傳輸過程中損壞")
    print("- 檔案格式與副檔名不符")
    print("- 舊版 Excel 格式相容性問題")

def create_test_excel():
    """創建一個測試用的 Excel 檔案"""
    print("\n🔧 創建測試 Excel 檔案...")
    
    try:
        # 創建測試數據
        test_data = {
            'A': [1, 2, 3, 4, 5],
            'B': ['測試', '數據', '用於', '驗證', 'Excel'],
            'C': [100, 200, 300, 400, 500]
        }
        
        df = pd.DataFrame(test_data)
        test_path = "/Users/ben_kuo/skinbar_money/test_excel.xlsx"
        
        df.to_excel(test_path, index=False, sheet_name='測試工作表')
        print(f"✅ 測試檔案已創建: {test_path}")
        
        # 測試讀取
        calculator = SalaryCalculator()
        test_df = calculator.safe_read_excel(test_path, sheet_name='測試工作表')
        print(f"✅ 測試檔案讀取成功，大小: {test_df.shape}")
        
        return test_path
        
    except Exception as e:
        print(f"❌ 創建測試檔案失敗: {e}")
        return None

if __name__ == "__main__":
    print("🚀 開始診斷 Excel 檔案問題...")
    
    # 診斷現有檔案
    working_file = diagnose_excel_problem()
    
    if not working_file:
        # 如果沒有找到可用檔案，創建測試檔案
        print("\n🔧 沒有找到可用的 Excel 檔案，創建測試檔案...")
        test_file = create_test_excel()
        
        if test_file:
            print(f"\n✅ 您可以使用測試檔案進行程式測試: {test_file}")
    else:
        print(f"\n✅ 找到可用的 Excel 檔案: {working_file}")
        print("現在可以執行薪資計算程式了！")
