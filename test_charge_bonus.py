#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試充值目標達成獎計算邏輯
規則：同時達成業績門檻 AND 水光面膜銷售7組以上
- 業績25萬 + 面膜7組 → 2000元
- 業績30萬 + 面膜7組 → 7000元
- 面膜不到7組則無獎金
"""

from auto_salary_calculator import SalaryCalculator

def test_charge_target_bonus():
    calc = SalaryCalculator()
    
    # 測試案例
    test_cases = [
        # (業績, 淨膚師ID, 面膜銷售數, 預期獎金, 說明)
        (350000, "1", 8, 7000, "30萬業績+8組面膜 → 7000元"),
        (280000, "2", 7, 2000, "28萬業績+7組面膜 → 2000元"),
        (250000, "3", 7, 2000, "25萬業績+7組面膜(剛好達標) → 2000元"),
        (300000, "4", 6, 0, "30萬業績+6組面膜(面膜未達標) → 0元"),
        (240000, "5", 10, 0, "24萬業績+10組面膜(業績未達標) → 0元"),
        (200000, "6", 5, 0, "20萬業績+5組面膜(都未達標) → 0元"),
        (320000, "7", 0, 0, "32萬業績+0組面膜(面膜未達標) → 0元"),
        (260000, "8", 15, 2000, "26萬業績+15組面膜(25萬檔) → 2000元"),
    ]
    
    print("🎯 充值目標達成獎計算測試")
    print("=" * 60)
    
    all_passed = True
    
    for i, (performance, therapist_id, mask_count, expected, description) in enumerate(test_cases, 1):
        # 模擬面膜銷售數據
        mask_sales = {therapist_id: mask_count}
        
        print(f"\n測試 {i}: {description}")
        result = calc.calculate_charge_target_bonus(performance, therapist_id, mask_sales)
        
        if result == expected:
            print(f"✅ 通過: 實際{result}元 = 預期{expected}元")
        else:
            print(f"❌ 失敗: 實際{result}元 ≠ 預期{expected}元")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有測試通過！充值目標達成獎計算邏輯正確")
    else:
        print("⚠️ 部分測試失敗，需要檢查邏輯")

if __name__ == "__main__":
    test_charge_target_bonus()
