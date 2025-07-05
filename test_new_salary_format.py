#!/usr/bin/env python3
"""
測試新的薪資輸出格式（分離總薪水和季獎金）
"""

def test_new_salary_format():
    """展示新的薪資輸出格式"""
    print("🧪 新的薪資輸出格式預覽")
    print("=" * 70)
    
    # 模擬員工數據
    mock_results = [
        {
            'name': '張小美',
            'is_formal_staff': True,
            'base_salary': 25590,
            'meal_allowance': 3000,
            'overtime_pay': 2461,
            'skill_bonus': 5000,
            'team_bonus': 1500,
            'person_count_bonus': 2000,
            'charge_target_bonus': 7000,
            'consumption_bonus': 1000,
            'dual_target_bonus': 3000,
            'advanced_course_bonus': 500,
            'product_sales_bonus': 800,
            'new_customer_rate_bonus': 4000,
            'total_salary': 56851
        },
        {
            'name': '李小花',
            'is_formal_staff': True,
            'base_salary': 25590,
            'meal_allowance': 3000,
            'overtime_pay': 1200,
            'skill_bonus': 3000,
            'team_bonus': 1500,
            'person_count_bonus': 0,
            'charge_target_bonus': 0,
            'consumption_bonus': 500,
            'dual_target_bonus': 0,
            'advanced_course_bonus': 300,
            'product_sales_bonus': 400,
            'new_customer_rate_bonus': 0,
            'total_salary': 35490
        }
    ]
    
    # 模擬 print_results 的邏輯
    total_all_salary = 0
    total_all_seasonal_bonus = 0
    
    for i, result in enumerate(mock_results, 1):
        staff_type = "正式淨膚師" if result['is_formal_staff'] else "一般員工"
        
        # 計算基本薪資（不含季獎金）
        basic_salary = (
            result['base_salary'] +
            result['meal_allowance'] + 
            result['overtime_pay'] + 
            result['skill_bonus'] + 
            result['team_bonus']
        )
        
        # 計算季獎金總額
        seasonal_bonus_total = (
            result['person_count_bonus'] +
            result['charge_target_bonus'] +
            result['consumption_bonus'] +
            result['dual_target_bonus'] +
            result['advanced_course_bonus'] +
            result['product_sales_bonus'] +
            result['new_customer_rate_bonus']
        )
        
        print(f"\n📋 員工 {i}: {result['name']}")
        print(f"   身份: {staff_type}")
        print(f"   底薪: {result['base_salary']:,} 元")
        print(f"   伙食費: {result['meal_allowance']:,} 元")
        print(f"   加班費: {result['overtime_pay']:,.0f} 元")
        print(f"   手技獎金: {result['skill_bonus']:,.0f} 元")
        print(f"   團獎: {result['team_bonus']:,} 元")
        print("   ─────────────────────────────")
        print(f"   💰 總薪水: {basic_salary:,.0f} 元")
        print()
        print("   🎊 季獎金明細:")
        print(f"   📈 人次激勵獎金: {result['person_count_bonus']:,} 元")
        print(f"   🎯 充值目標達成獎: {result['charge_target_bonus']:,} 元")
        print(f"   💧 個人消耗獎勵: {result['consumption_bonus']:,} 元")
        print(f"   🎪 消耗充值雙達標獎: {result['dual_target_bonus']:,} 元")
        print(f"   📚 進階課程工獎: {result['advanced_course_bonus']:,} 元")
        print(f"   🛍️  產品銷售供獎: {result['product_sales_bonus']:,} 元")
        print(f"   🎯 新客成交率70%獎金: {result['new_customer_rate_bonus']:,} 元")
        print("   ─────────────────────────────")
        print(f"   🎊 季獎金小計: {seasonal_bonus_total:,.0f} 元")
        print("   ─────────────────────────────")
        print(f"   💵 總計: {result['total_salary']:,.0f} 元")
        
        total_all_salary += basic_salary
        total_all_seasonal_bonus += seasonal_bonus_total
    
    print("\n" + "="*70)
    print("📊 全店薪資總覽")
    print("="*70)
    print(f"💰 基本薪資總計: {total_all_salary:,.0f} 元 (底薪+伙食費+加班費+手技獎金+團獎)")
    print(f"🎊 季獎金總計: {total_all_seasonal_bonus:,.0f} 元")
    print("─"*70)
    print(f"💵 全店薪資總額: {total_all_salary + total_all_seasonal_bonus:,.0f} 元")
    print("="*70)

if __name__ == "__main__":
    test_new_salary_format()
