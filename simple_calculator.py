#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
淨膚寶薪水計算小程式 - 簡化版
適用於快速計算和驗證
"""

def calculate_team_bonus():
    """計算團獎的簡化版本"""
    team_rules = {
        2: (500000, 5000),   # 2位：50萬業績，5000元獎金
        3: (750000, 5600),   # 3位：75萬業績，5600元獎金  
        4: (1000000, 6000),  # 4位：100萬業績，6000元獎金
        5: (1250000, 6250),  # 5位：125萬業績，6250元獎金
        6: (1500000, 6500),  # 6位：150萬業績，6500元獎金
    }
    
    print("團獎計算器")
    print("-" * 40)
    
    try:
        num_staff = int(input("請輸入正式淨膚師人數 (2-6): "))
        if num_staff not in team_rules:
            print("人數必須在2-6之間")
            return
        
        performance = float(input("請輸入當月業績 (元): "))
        consumption = float(input("請輸入當月消耗 (元): "))
        
        required_performance, bonus = team_rules[num_staff]
        consumption_rate = (consumption / performance * 100) if performance > 0 else 0
        
        print(f"\n業績要求: {required_performance:,} 元")
        print(f"實際業績: {performance:,} 元")
        print(f"消耗比例: {consumption_rate:.1f}%")
        print("要求比例: 75%")
        
        if performance >= required_performance and consumption_rate >= 75:
            print("\n✅ 達到團獎條件！")
            print(f"每位正式淨膚師可獲得團獎: {bonus:,} 元")
        else:
            print("\n❌ 未達到團獎條件")
            if performance < required_performance:
                print(f"   業績差額: {required_performance - performance:,} 元")
            if consumption_rate < 75:
                print(f"   消耗比例不足: 需要75%，目前{consumption_rate:.1f}%")
        
    except ValueError:
        print("請輸入有效的數字")

def calculate_individual_salary():
    """計算個人薪水"""
    print("\n個人薪資計算器")
    print("-" * 40)
    
    base_salary = 25590  # 底薪
    meal_allowance = 3000  # 伙食費
    overtime_pay = 2461.4  # 加班費
    
    try:
        name = input("員工姓名: ")
        skill_bonus = float(input("手技獎金累計 (元): "))
        is_formal = input("是否為正式淨膚師？ (y/n): ").lower() == 'y'
        
        team_bonus = 0
        if is_formal:
            team_bonus = float(input("團獎金額 (元，如未達標請輸入0): "))
        
        total = base_salary + meal_allowance + overtime_pay + skill_bonus + team_bonus
        
        print(f"\n{name} 薪資明細:")
        print(f"底薪: {base_salary:,} 元")
        print(f"伙食費: {meal_allowance:,} 元")
        print(f"加班費: {overtime_pay:,} 元") 
        print(f"手技獎金: {skill_bonus:,} 元")
        print(f"團獎: {team_bonus:,} 元")
        print(f"總薪資: {total:,} 元")
        
    except ValueError:
        print("請輸入有效的數字")

def main():
    while True:
        print("\n" + "="*50)
        print("淨膚寶薪水計算小程式")
        print("="*50)
        print("1. 計算團獎")
        print("2. 計算個人薪資") 
        print("3. 結束程式")
        
        choice = input("\n請選擇功能 (1-3): ")
        
        if choice == '1':
            calculate_team_bonus()
        elif choice == '2':
            calculate_individual_salary()
        elif choice == '3':
            print("程式結束，謝謝使用！")
            break
        else:
            print("請輸入有效的選項 (1-3)")

if __name__ == "__main__":
    main()
