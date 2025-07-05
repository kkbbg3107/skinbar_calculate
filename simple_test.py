#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡單測試充值目標達成獎邏輯
"""

def calculate_charge_target_bonus(personal_performance, therapist_id, mask_sales):
    """計算充值目標達成獎
    條件：同時達成業績門檻 AND 水光面膜銷售7組以上
    - 業績25萬 + 面膜7組 → 2000元
    - 業績30萬 + 面膜7組 → 7000元
    - 面膜不到7組則無獎金
    """
    bonus = 0
    
    # 獲取該淨膚師的水光面膜銷售數量
    mask_count = mask_sales.get(str(therapist_id), 0)
    
    print(f"      淨膚師{therapist_id}: 業績{personal_performance:,.0f}元, 水光面膜{mask_count}組")
    
    # 先檢查面膜銷售責任額（必須7組以上才能有獎金）
    if mask_count < 7:
        print(f"      ❌ 水光面膜未達責任額: {mask_count}/7組 → 無充值目標達成獎")
        return 0
    
    # 面膜達標後，檢查業績門檻
    if personal_performance >= 300000:
        bonus = 7000  # 30萬業績 + 7組面膜 = 7000元
        print(f"      ✅ 業績30萬+面膜7組達標 → 充值目標達成獎: {bonus}元")
    elif personal_performance >= 250000:
        bonus = 2000  # 25萬業績 + 7組面膜 = 2000元  
        print(f"      ✅ 業績25萬+面膜7組達標 → 充值目標達成獎: {bonus}元")
    else:
        print(f"      ❌ 業績未達25萬門檻: {personal_performance:,.0f}元 → 無充值目標達成獎")
    
    return bonus

# 測試案例
test_cases = [
    # (業績, 淨膚師ID, 面膜銷售數, 預期獎金, 說明)
    (350000, "1", 8, 7000, "30萬業績+8組面膜 → 7000元"),
    (280000, "2", 7, 2000, "28萬業績+7組面膜 → 2000元"),
    (250000, "3", 7, 2000, "25萬業績+7組面膜(剛好達標) → 2000元"),
    (300000, "4", 6, 0, "30萬業績+6組面膜(面膜未達標) → 0元"),
    (240000, "5", 10, 0, "24萬業績+10組面膜(業績未達標) → 0元"),
]

print("🎯 充值目標達成獎計算測試")
print("=" * 60)

all_passed = True

for i, (performance, therapist_id, mask_count, expected, description) in enumerate(test_cases, 1):
    # 模擬面膜銷售數據
    mask_sales = {therapist_id: mask_count}
    
    print(f"\n測試 {i}: {description}")
    result = calculate_charge_target_bonus(performance, therapist_id, mask_sales)
    
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
