#!/usr/bin/env python3
"""
測試動態員工行號檢測功能
"""

import pandas as pd
from auto_salary_calculator import SalaryCalculator

def test_dynamic_employee_detection():
    """測試動態員工檢測功能"""
    print("🧪 測試動態員工行號檢測功能")
    print("=" * 50)
    
    # 創建測試數據，模擬Excel的月報表彙整
    test_data = {
        'A': [None] * 11 + ['員工1', '員工2', '員工3', '員工4', '員工5', None, None],  # 第12-16行有員工
        'B': [None] * 11 + [250000, 180000, 320000, 150000, 0, None, None],  # B16為0，表示停止
        'C': [None] * 11 + [50000, 30000, 60000, 25000, 0, None, None],     # 個人消耗
        'D': [None] * 11 + [120, 85, 150, 70, 0, None, None],               # 人次
        # 其他欄位...
    }
    
    # 填充其他必要的欄位到X列
    for col in ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']:
        test_data[col] = [None] * 18
    
    df = pd.DataFrame(test_data)
    
    calculator = SalaryCalculator()
    
    # 測試動態檢測
    employee_rows = calculator.get_dynamic_employee_rows(df, start_row=12)
    
    print("\n預期結果: [12, 13, 14, 15] (因為第16行B列為0)")
    print(f"實際結果: {employee_rows}")
    
    if employee_rows == [12, 13, 14, 15]:
        print("✅ 動態檢測功能正常！")
    else:
        print("❌ 動態檢測功能有問題")
    
    # 測試獲取員工數據
    if employee_rows:
        print("\n📋 員工數據預覽:")
        employees = calculator.get_employee_data(df, employee_rows)
        for emp in employees:
            print(f"  行號{emp['row']}: {emp['name']} - 業績: {emp['personal_performance']:,.0f}")

def test_edge_cases():
    """測試邊緣情況"""
    print("\n🔍 測試邊緣情況")
    print("-" * 30)
    
    # 情況1: 只有3個員工
    test_data_3 = {
        'A': [None] * 11 + ['員工1', '員工2', '員工3', None],
        'B': [None] * 11 + [250000, 180000, 320000, 0],  # 第15行就為0
    }
    
    for col in ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']:
        test_data_3[col] = [None] * 15
    
    df3 = pd.DataFrame(test_data_3)
    calculator = SalaryCalculator()
    
    employee_rows_3 = calculator.get_dynamic_employee_rows(df3, start_row=12)
    print(f"3個員工測試: {employee_rows_3}")
    
    # 情況2: 有空行但後面還有員工
    test_data_gap = {
        'A': [None] * 11 + ['員工1', '員工2', None, '員工4', None],  # 第14行無姓名，第16行為空
        'B': [None] * 11 + [250000, 180000, 150000, 200000, 0],     # 但B行都有值直到第16行
    }
    
    for col in ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']:
        test_data_gap[col] = [None] * 16
    
    df_gap = pd.DataFrame(test_data_gap)
    employee_rows_gap = calculator.get_dynamic_employee_rows(df_gap, start_row=12)
    print(f"有空行測試: {employee_rows_gap}")

if __name__ == "__main__":
    test_dynamic_employee_detection()
    test_edge_cases()
