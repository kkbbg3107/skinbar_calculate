#!/usr/bin/env python3
"""
測試語法修正是否成功
"""

try:
    from auto_salary_calculator import SalaryCalculator
    print("✅ 語法修正成功！模組可以正常匯入")
    
    # 簡單測試類別實例化
    calculator = SalaryCalculator()
    print("✅ SalaryCalculator 類別可以正常實例化")
    
except Exception as e:
    print(f"❌ 錯誤：{e}")
