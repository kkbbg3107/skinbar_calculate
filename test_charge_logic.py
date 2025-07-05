#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試充值目標達成獎完整邏輯
包含業績門檻 + 水光面膜責任額檢查
"""

# 模擬充值目標達成獎計算函數
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
    
    print(f"   淨膚師{therapist_id}: 業績{personal_performance:,.0f}元, 水光面膜{mask_count}組")
    
    # 先檢查面膜銷售責任額（必須7組以上才能有獎金）
    if mask_count < 7:
        print(f"   ❌ 水光面膜未達責任額: {mask_count}/7組 → 無充值目標達成獎")
        return 0
    
    # 面膜達標後，檢查業績門檻
    if personal_performance >= 300000:
        bonus = 7000  # 30萬業績 + 7組面膜 = 7000元
        print(f"   ✅ 業績30萬+面膜7組達標 → 充值目標達成獎: {bonus}元")
    elif personal_performance >= 250000:
        bonus = 2000  # 25萬業績 + 7組面膜 = 2000元  
        print(f"   ✅ 業績25萬+面膜7組達標 → 充值目標達成獎: {bonus}元")
    else:
        print(f"   ❌ 業績未達25萬門檻: {personal_performance:,.0f}元 → 無充值目標達成獎")
    
    return bonus

# 測試案例
print("🎯 充值目標達成獎計算邏輯測試")
print("規則：業績25萬/30萬 + 水光面膜7組")
print("="*50)

test_cases = [
    {
        'therapist_id': 1,
        'performance': 350000,
        'mask_count': 8,
        'expected': 7000,
        'description': '30萬業績+8組面膜'
    },
    {
        'therapist_id': 2,
        'performance': 280000,
        'mask_count': 7,
        'expected': 2000,
        'description': '28萬業績+7組面膜(剛好)'
    },
    {
        'therapist_id': 3,
        'performance': 250000,
        'mask_count': 7,
        'expected': 2000,
        'description': '25萬業績+7組面膜(最低門檻)'
    },
    {
        'therapist_id': 4,
        'performance': 300000,
        'mask_count': 6,
        'expected': 0,
        'description': '30萬業績+6組面膜(面膜不足)'
    },
    {
        'therapist_id': 5,
        'performance': 240000,
        'mask_count': 10,
        'expected': 0,
        'description': '24萬業績+10組面膜(業績不足)'
    },
    {
        'therapist_id': 6,
        'performance': 200000,
        'mask_count': 5,
        'expected': 0,
        'description': '20萬業績+5組面膜(都不足)'
    }
]

all_passed = True

for i, case in enumerate(test_cases, 1):
    print(f"\n測試 {i}: {case['description']}")
    
    # 模擬面膜銷售數據
    mask_sales = {str(case['therapist_id']): case['mask_count']}
    
    result = calculate_charge_target_bonus(
        case['performance'],
        case['therapist_id'],
        mask_sales
    )
    
    if result == case['expected']:
        print(f"✅ 通過: 實際{result}元 = 預期{case['expected']}元")
    else:
        print(f"❌ 失敗: 實際{result}元 ≠ 預期{case['expected']}元")
        all_passed = False

print("\n" + "="*50)
if all_passed:
    print("🎉 所有測試通過！充值目標達成獎邏輯正確")
else:
    print("⚠️ 部分測試失敗")

print("\n📋 充值目標達成獎邏輯摘要:")
print("1. 必須同時達成業績門檻和面膜責任額")
print("2. 業績25萬 + 面膜7組 → 2000元")
print("3. 業績30萬 + 面膜7組 → 7000元")
print("4. 面膜不到7組或業績不達標 → 0元")
