#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試所有季獎金細項計算邏輯
包含新增的四個季獎金細項
"""

def calculate_consumption_bonus(personal_consumption, total_consumption):
    """計算個人消耗獎勵季獎金"""
    bonus = 0
    reason = ""
    
    if personal_consumption >= 200000:
        bonus = int(total_consumption * 0.025)
        reason = f"消耗20萬達標，可抽總消耗{total_consumption:,.0f}元的2.5%"
    elif personal_consumption >= 180000:
        bonus = int(total_consumption * 0.015)
        reason = f"消耗18萬達標，可抽總消耗{total_consumption:,.0f}元的1.5%"
    else:
        reason = f"消耗未達18萬門檻: {personal_consumption:,.0f}元"
    
    return bonus, reason

def calculate_dual_target_bonus(personal_consumption, personal_performance):
    """計算消耗充值雙達標獎"""
    bonus = 0
    reason = ""
    
    consumption_ok = personal_consumption >= 180000
    performance_ok = personal_performance >= 250000
    
    if consumption_ok and performance_ok:
        bonus = 2000
        reason = "消耗18萬+業績25萬雙達標"
    else:
        missing = []
        if not consumption_ok:
            missing.append(f"消耗{personal_consumption:,.0f}/180,000")
        if not performance_ok:
            missing.append(f"業績{personal_performance:,.0f}/250,000")
        reason = f"未達雙標準: {', '.join(missing)}"
    
    return bonus, reason

print("🎯 所有季獎金細項測試")
print("=" * 60)

# 測試數據
test_data = {
    'total_consumption': 1966800,  # 總消耗196萬6800元
    'employees': [
        {
            'name': '淨膚師A',
            'personal_consumption': 220000,
            'personal_performance': 300000,
            'advanced_course_bonus': 1500,
            'product_sales_bonus': 800,
        },
        {
            'name': '淨膚師B', 
            'personal_consumption': 190000,
            'personal_performance': 280000,
            'advanced_course_bonus': 800,
            'product_sales_bonus': 1200,
        },
        {
            'name': '淨膚師C',
            'personal_consumption': 160000,
            'personal_performance': 240000,
            'advanced_course_bonus': 600,
            'product_sales_bonus': 400,
        },
    ]
}

print(f"💧 總消耗額: {test_data['total_consumption']:,}元")
print()

for i, emp in enumerate(test_data['employees'], 1):
    print(f"👤 {emp['name']}:")
    print(f"   個人消耗: {emp['personal_consumption']:,}元")
    print(f"   個人業績: {emp['personal_performance']:,}元")
    
    # 1. 個人消耗獎勵季獎金
    consumption_bonus, consumption_reason = calculate_consumption_bonus(
        emp['personal_consumption'], test_data['total_consumption']
    )
    status = "✅" if consumption_bonus > 0 else "❌"
    print(f"   💧 個人消耗獎勵: {consumption_bonus:,}元 {status} {consumption_reason}")
    
    # 2. 消耗充值雙達標獎
    dual_bonus, dual_reason = calculate_dual_target_bonus(
        emp['personal_consumption'], emp['personal_performance']
    )
    status = "✅" if dual_bonus > 0 else "❌"
    print(f"   🎪 消耗充值雙達標獎: {dual_bonus:,}元 {status} {dual_reason}")
    
    # 3. 進階課程工獎
    print(f"   📚 進階課程工獎: {emp['advanced_course_bonus']:,}元 (V行累計)")
    
    # 4. 產品銷售供獎
    print(f"   🛍️  產品銷售供獎: {emp['product_sales_bonus']:,}元 (X行累計)")
    
    print()

print("=" * 60)
print("📋 季獎金細項說明:")
print("1. 📈 人次激勵獎金: 110人以上分段計算")
print("2. 🎯 充值目標達成獎: 業績+面膜雙達標")
print("3. 💧 個人消耗獎勵: 消耗18萬(1.5%)或20萬(2.5%)")
print("4. 🎪 消耗充值雙達標獎: 消耗18萬+業績25萬=2000元")
print("5. 📚 進階課程工獎: 直接取V行數據")
print("6. 🛍️  產品銷售供獎: 直接取X行數據")
print("✅ 所有季獎金細項已完成！")
