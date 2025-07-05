#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試新客成交率70%獎金邏輯
包含人次132人 + 新客成交率70%雙重條件檢查
"""

def calculate_new_customer_rate_bonus(person_count, new_customer_rate):
    """計算新客成交率70%獎金
    條件：客人數量達132人 + 新客實際成交率70%
    獎金：4000元（需人工檢查出勤狀況）
    """
    bonus = 0
    reason = ""
    
    # 檢查人次是否達132人
    person_count_ok = person_count >= 132
    
    # 檢查新客成交率是否達70%
    # I行的數據可能是百分比格式或小數格式，需要處理
    if new_customer_rate > 1:
        # 如果大於1，假設是百分比格式（如70表示70%）
        actual_rate = new_customer_rate / 100
    else:
        # 如果小於等於1，假設是小數格式（如0.7表示70%）
        actual_rate = new_customer_rate
    
    rate_ok = actual_rate >= 0.7
    
    if person_count_ok and rate_ok:
        bonus = 4000
        reason = f"人次{person_count:.0f}人+成交率{actual_rate*100:.1f}%達標（需人工檢查出勤狀況）"
    else:
        missing = []
        if not person_count_ok:
            missing.append(f"人次{person_count:.0f}/132人")
        if not rate_ok:
            missing.append(f"成交率{actual_rate*100:.1f}%/70%")
        reason = f"未達標準: {', '.join(missing)}"
    
    return bonus, reason

print("🎯 新客成交率70%獎金計算邏輯測試")
print("規則：人次132人 + 新客成交率70%")
print("="*60)

# 測試案例
test_cases = [
    {
        'name': '淨膚師A',
        'person_count': 135,
        'new_customer_rate': 75,  # 百分比格式
        'expected': 4000,
        'description': '135人次+75%成交率'
    },
    {
        'name': '淨膚師B', 
        'person_count': 132,
        'new_customer_rate': 0.7,  # 小數格式
        'expected': 4000,
        'description': '132人次+70%成交率(剛好達標)'
    },
    {
        'name': '淨膚師C',
        'person_count': 140,
        'new_customer_rate': 65,  # 百分比格式，成交率不足
        'expected': 0,
        'description': '140人次+65%成交率(成交率不足)'
    },
    {
        'name': '淨膚師D',
        'person_count': 130,
        'new_customer_rate': 0.8,  # 小數格式，人次不足
        'expected': 0,
        'description': '130人次+80%成交率(人次不足)'
    },
    {
        'name': '淨膚師E',
        'person_count': 120,
        'new_customer_rate': 60,  # 百分比格式，都不足
        'expected': 0,
        'description': '120人次+60%成交率(都不達標)'
    },
    {
        'name': '淨膚師F',
        'person_count': 150,
        'new_customer_rate': 0.78,  # 小數格式，都達標
        'expected': 4000,
        'description': '150人次+78%成交率(都超標)'
    }
]

all_passed = True

for i, case in enumerate(test_cases, 1):
    print(f"\n測試 {i}: {case['description']}")
    print(f"   {case['name']}: 人次{case['person_count']}, 成交率{case['new_customer_rate']}")
    
    result, reason = calculate_new_customer_rate_bonus(
        case['person_count'],
        case['new_customer_rate']
    )
    
    status = "✅" if result > 0 else "❌"
    print(f"   🎯 新客成交率70%獎金: {result:,}元 {status} {reason}")
    
    if result == case['expected']:
        print(f"   ✅ 通過: 實際{result}元 = 預期{case['expected']}元")
    else:
        print(f"   ❌ 失敗: 實際{result}元 ≠ 預期{case['expected']}元")
        all_passed = False

print("\n" + "="*60)
if all_passed:
    print("🎉 所有測試通過！新客成交率70%獎金邏輯正確")
else:
    print("⚠️ 部分測試失敗")

print("\n📋 新客成交率70%獎金邏輯摘要:")
print("1. 條件：人次達132人 + 新客成交率達70%")
print("2. 獎金：固定4000元")
print("3. 備註：需人工檢查出勤狀況")
print("4. 數據來源：D行(人次) + I行(新客成交率)")
print("5. 支持百分比格式(70)和小數格式(0.7)")

print("\n🏆 全部七個季獎金細項已完成！")
print("1. 📈 人次激勵獎金")
print("2. 🎯 充值目標達成獎")
print("3. 💧 個人消耗獎勵")
print("4. 🎪 消耗充值雙達標獎")
print("5. 📚 進階課程工獎")
print("6. 🛍️ 產品銷售供獎")
print("7. 🎯 新客成交率70%獎金")
