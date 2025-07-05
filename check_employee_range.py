#!/usr/bin/env python3
"""
檢查實際的員工數據範圍
確認員工數據從A12到A17還是更多
"""

import pandas as pd
import os
from auto_salary_calculator import SalaryCalculator

def check_employee_range():
    """檢查實際員工數據範圍"""
    print("🔍 檢查實際員工數據範圍")
    print("=" * 50)
    
    # 測試路徑
    test_paths = [
        "/Users/ben_kuo/skinbar_report/skinbar202506.xlsx",
        "/Users/ben_kuo/skinbar_report/skinbar202506.xls"
    ]
    
    for file_path in test_paths:
        if os.path.exists(file_path):
            print(f"📁 檢查檔案: {file_path}")
            
            try:
                calculator = SalaryCalculator()
                
                # 讀取月報表彙整
                df = calculator.safe_read_excel(file_path, sheet_name='月報表彙整', header=None)
                print(f"✅ 成功讀取，共 {df.shape[0]} 行 {df.shape[1]} 列")
                
                # 檢查A12-A20範圍的數據
                print("\n📋 員工數據範圍檢查 (A12-A20):")
                print("-" * 40)
                
                for row in range(12, min(21, df.shape[0] + 1)):  # 檢查到第20行或資料結束
                    try:
                        # A行：員工姓名
                        a_value = df.iloc[row-1, 0] if row <= df.shape[0] else "超出範圍"
                        
                        # B行：個人業績
                        b_value = df.iloc[row-1, 1] if row <= df.shape[0] and df.shape[1] > 1 else "無資料"
                        
                        # 格式化輸出
                        a_display = str(a_value) if pd.notna(a_value) else "空值"
                        
                        if pd.notna(b_value) and isinstance(b_value, (int, float)):
                            b_display = f"{b_value:,.0f}" if b_value != 0 else "0"
                        else:
                            b_display = str(b_value) if pd.notna(b_value) else "空值"
                        
                        print(f"第{row:2d}行: A={a_display:12s} B={b_display:12s}")
                        
                        # 判斷是否應該停止
                        if pd.notna(b_value) and b_value == 0:
                            print(f"       ↑ B{row}為0，按邏輯應在此停止")
                        elif pd.isna(a_value) and (pd.isna(b_value) or b_value == 0):
                            print(f"       ↑ A{row}和B{row}都無資料，可能在此停止")
                            
                    except Exception as e:
                        print(f"第{row:2d}行: 讀取錯誤 - {e}")
                
                # 使用動態檢測功能
                print("\n🎯 使用動態檢測功能:")
                employee_rows = calculator.get_dynamic_employee_rows(df, start_row=12)
                
                print("\n📊 總結:")
                print(f"   實際找到的員工行號: {employee_rows}")
                print(f"   員工數量: {len(employee_rows)} 位")
                
                return True
                
            except Exception as e:
                print(f"❌ 讀取失敗: {e}")
                
    print("❌ 沒有找到可讀取的Excel檔案")
    return False

def test_manual_range():
    """手動測試不同的員工範圍"""
    print("\n🧪 手動測試不同員工範圍")
    print("-" * 30)
    
    # 模擬你說的情況：員工到A17
    test_data = {
        'A': [None] * 11 + ['員工1', '員工2', '員工3', '員工4', '員工5', '員工6', None, None],  # A12-A17
        'B': [None] * 11 + [250000, 180000, 320000, 150000, 200000, 280000, 0, None],      # B18為0
    }
    
    # 填充其他必要欄位
    for col in ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']:
        test_data[col] = [None] * 19
    
    df = pd.DataFrame(test_data)
    calculator = SalaryCalculator()
    
    print("模擬數據（員工到A17）:")
    for row in range(12, 19):
        a_val = test_data['A'][row] if row < len(test_data['A']) else None
        b_val = test_data['B'][row] if row < len(test_data['B']) else None
        a_display = str(a_val) if a_val else "空值"
        b_display = f"{b_val:,.0f}" if isinstance(b_val, (int, float)) and b_val != 0 else str(b_val)
        print(f"第{row}行: A={a_display:8s} B={b_display}")
    
    employee_rows = calculator.get_dynamic_employee_rows(df, start_row=12)
    print(f"\n檢測結果: {employee_rows}")
    print("預期結果: [12, 13, 14, 15, 16, 17] (6位員工)")

if __name__ == "__main__":
    # 檢查實際檔案
    found_file = check_employee_range()
    
    # 如果沒找到檔案，做手動測試
    if not found_file:
        test_manual_range()
