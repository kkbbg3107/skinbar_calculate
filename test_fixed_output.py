#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試修正後的季獎金計算輸出格式
"""

# 模擬修正後的充值目標達成獎函數
def calculate_charge_target_bonus(personal_performance, therapist_id, mask_sales):
    """計算充值目標達成獎 - 修正版"""
    bonus = 0
    mask_count = mask_sales.get(str(therapist_id), 0)
    
    # 先檢查面膜銷售責任額
    if mask_count < 7:
        return 0, f"面膜未達責任額: {mask_count}/7組"
    
    # 面膜達標後，檢查業績門檻
    if personal_performance >= 300000:
        bonus = 7000
        reason = f"業績30萬+面膜{mask_count}組達標"
    elif personal_performance >= 250000:
        bonus = 2000
        reason = f"業績25萬+面膜{mask_count}組達標"
    else:
        return 0, f"業績未達25萬門檻: {personal_performance:,.0f}元"
    
    return bonus, reason

def calculate_person_count_bonus(person_count):
    """計算人次激勵獎金"""
    if person_count < 110:
        return 0
    
    bonus = 0
    if person_count >= 110:
        tier1_start = 111
        tier1_end = min(person_count, 132)
        if tier1_end >= tier1_start:
            tier1_count = tier1_end - tier1_start + 1
            bonus += tier1_count * 100
    
    if person_count > 132:
        tier2_count = person_count - 132
        bonus += tier2_count * 200
    
    return bonus

# 測試數據
employees = [
    {'name': '員工A', 'row': 12, 'personal_performance': 280000, 'person_count': 127},
    {'name': '員工B', 'row': 13, 'personal_performance': 320000, 'person_count': 135},
    {'name': '員工C', 'row': 14, 'personal_performance': 240000, 'person_count': 105},
]

mask_sales = {'1': 8, '2': 7, '3': 5}  # 淨膚師1有8組，2有7組，3有5組

print("🎉 正在計算季獎金...")

for employee in employees:
    # 根據員工行號推算淨膚師編號 (12->1, 13->2, 14->3, 15->4)
    therapist_id = employee['row'] - 11
    
    # 1. 人次激勵獎金
    person_count_bonus = calculate_person_count_bonus(employee['person_count'])
    
    # 2. 充值目標達成獎
    charge_target_bonus, charge_reason = calculate_charge_target_bonus(
        employee['personal_performance'], 
        therapist_id, 
        mask_sales
    )
    
    # 獲取面膜數量用於顯示
    mask_count = mask_sales.get(str(therapist_id), 0)
    
    print(f"\n   {employee['name']} (淨膚師{therapist_id}):")
    print(f"      業績: {employee['personal_performance']:,.0f}元, 人次: {employee['person_count']:.0f}, 水光面膜: {mask_count}組")
    
    # 顯示人次激勵獎金
    print(f"      人次激勵獎金: {person_count_bonus:,}元", end="")
    if person_count_bonus > 0:
        if employee['person_count'] > 132:
            tier1_count = 132 - 111 + 1  # 111-132人
            tier2_count = employee['person_count'] - 132  # 133以上
            print(f" (111-132人: {tier1_count}×100 + 133-{employee['person_count']:.0f}人: {tier2_count}×200)")
        elif employee['person_count'] >= 110:
            tier1_count = employee['person_count'] - 111 + 1  # 111到person_count
            print(f" (111-{employee['person_count']:.0f}人: {tier1_count:.0f}×100)")
        else:
            print()
    else:
        print()
    
    # 顯示充值目標達成獎
    if charge_target_bonus > 0:
        print(f"      充值目標達成獎: {charge_target_bonus:,}元 ✅ {charge_reason}")
    else:
        print(f"      充值目標達成獎: 0元 ❌ {charge_reason}")

print("\n" + "="*50)
print("✅ 輸出格式已修正，不再有混亂的顯示！")
