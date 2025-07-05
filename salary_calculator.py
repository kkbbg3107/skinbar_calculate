#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
淨膚寶薪水計算小程式
"""

import pandas as pd

class SalaryCalculator:
    def __init__(self):
        # 基本薪資設定
        self.base_salary = 25590  # 底薪
        self.meal_allowance = 3000  # 伙食費
        self.overtime_pay = 2461.4  # 加班費
        self.skill_bonus_per_time = 10  # 手技獎金每次
        
        # 團獎設定 (人數: (業績要求, 消耗比例要求, 獎金))
        self.team_bonus_rules = {
            2: (500000, 0.75, 5000),   # 2位正式淨膚師：50萬業績，75%消耗，5000元獎金
            3: (750000, 0.75, 5600),   # 3位正式淨膚師：75萬業績，75%消耗，5600元獎金
            4: (1000000, 0.75, 6000),  # 4位正式淨膚師：100萬業績，75%消耗，6000元獎金
            5: (1250000, 0.75, 6250),  # 5位正式淨膚師：125萬業績，75%消耗，6250元獎金
            6: (1500000, 0.75, 6500),  # 6位正式淨膚師：150萬業績，75%消耗，6500元獎金
        }
    
    def read_excel_data(self, excel_file):
        """讀取Excel文件數據"""
        try:
            # 讀取月報表彙整工作表
            df = pd.read_excel(excel_file, sheet_name='月報表彙整', header=None)
            
            # 先檢查工作表
            excel_data = pd.ExcelFile(excel_file)
            
            # 找出所有日期工作表（排除月報表彙整）
            date_sheets = []
            for sheet_name in excel_data.sheet_names:
                if sheet_name != '月報表彙整':
                    # 檢查是否為日期格式的工作表（數字開頭）
                    if sheet_name.isdigit() or (len(sheet_name) >= 2 and sheet_name[0].isdigit()):
                        date_sheets.append(sheet_name)
            
            date_sheets.sort()  # 按照名稱排序
            print(f"找到日期工作表: {date_sheets}")
            
            # 計算總業績和總消耗
            total_performance = 0
            total_consumption = 0
            
            for sheet_name in date_sheets:
                try:
                    sheet_df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
                    
                    # 讀取 E3 (業績) 和 E5 (消耗)
                    performance_value = sheet_df.iloc[2, 4] if sheet_df.shape[0] > 2 and sheet_df.shape[1] > 4 else 0  # E3
                    consumption_value = sheet_df.iloc[4, 4] if sheet_df.shape[0] > 4 and sheet_df.shape[1] > 4 else 0  # E5
                    
                    # 處理 NaN 值
                    if pd.notna(performance_value):
                        total_performance += float(performance_value)
                    if pd.notna(consumption_value):
                        total_consumption += float(consumption_value)
                        
                except Exception as e:
                    print(f"讀取工作表 '{sheet_name}' 時發生錯誤: {e}")
                    continue
            
            return df, total_performance, total_consumption
            
        except Exception as e:
            print(f"讀取Excel文件時發生錯誤: {e}")
            return None, 0, 0
    
    def get_employee_data(self, df, employee_rows):
        """獲取員工數據"""
        employees = []
        
        for row in employee_rows:
            try:
                # 獲取員工姓名 (A行)
                name = df.iloc[row-1, 0]  # 轉換為0-indexed
                
                # 獲取手計供獎累計 (W行)
                skill_bonus_total = df.iloc[row-1, 22]  # W列是第23列 (0-indexed: 22)
                
                employees.append({
                    'name': name,
                    'skill_bonus_total': skill_bonus_total if pd.notna(skill_bonus_total) else 0,
                    'row': row
                })
                
            except Exception as e:
                print(f"獲取第{row}行員工數據時發生錯誤: {e}")
                
        return employees
    
    def calculate_team_bonus(self, num_formal_staff, total_performance, total_consumption):
        """計算團獎"""
        if num_formal_staff not in self.team_bonus_rules:
            print(f"沒有{num_formal_staff}位正式淨膚師的團獎規則")
            return 0
        
        required_performance, required_consumption_rate, bonus_amount = self.team_bonus_rules[num_formal_staff]
        
        # 檢查是否達到業績要求
        if total_performance < required_performance:
            print(f"業績未達標: 需要{required_performance:,}元，實際{total_performance:,}元")
            return 0
        
        # 檢查消耗比例
        if total_performance > 0:
            consumption_rate = total_consumption / total_performance
            if consumption_rate < required_consumption_rate:
                print(f"消耗比例未達標: 需要{required_consumption_rate*100}%，實際{consumption_rate*100:.1f}%")
                return 0
        
        print(f"達到團獎條件！每位正式淨膚師和幹部可獲得{bonus_amount:,}元團獎")
        return bonus_amount
    
    def calculate_salary(self, employees, team_bonus_per_person, formal_staff_positions):
        """計算薪水"""
        results = []
        
        for employee in employees:
            # 基本薪資組成
            base = self.base_salary
            meal = self.meal_allowance
            overtime = self.overtime_pay
            skill_bonus = employee['skill_bonus_total']
            
            # 判斷是否為正式淨膚師，決定是否有團獎
            is_formal_staff = employee['row'] in formal_staff_positions
            team_bonus = team_bonus_per_person if is_formal_staff else 0
            
            # 計算總薪水
            total_salary = base + meal + overtime + skill_bonus + team_bonus
            
            result = {
                'name': employee['name'],
                'base_salary': base,
                'meal_allowance': meal,
                'overtime_pay': overtime,
                'skill_bonus': skill_bonus,
                'team_bonus': team_bonus,
                'total_salary': total_salary,
                'is_formal_staff': is_formal_staff
            }
            
            results.append(result)
        
        return results
    
    def print_results(self, results, total_performance, total_consumption):
        """輸出結果"""
        print("\n" + "="*60)
        print("🏆 淨膚寶薪水計算結果")
        print("="*60)
        
        print(f"\n💰 當月業績總額: {total_performance:,.0f} 元")
        print(f"🛍️  當月消耗總額: {total_consumption:,.0f} 元")
        if total_performance > 0:
            consumption_rate = (total_consumption / total_performance) * 100
            print(f"📊 消耗比例: {consumption_rate:.1f}%")
        
        print("\n" + "="*60)
        print("👥 員工薪資明細")
        print("="*60)
        
        total_all_salary = 0
        for i, result in enumerate(results, 1):
            staff_type = "正式淨膚師" if result['is_formal_staff'] else "一般員工"
            
            print(f"\n📋 員工 {i}: {result['name']}")
            print(f"   身份: {staff_type}")
            print(f"   底薪: {result['base_salary']:,} 元")
            print(f"   伙食費: {result['meal_allowance']:,} 元")
            print(f"   加班費: {result['overtime_pay']:,.0f} 元")
            print(f"   手技獎金: {result['skill_bonus']:,.0f} 元")
            print(f"   團獎: {result['team_bonus']:,} 元")
            print("   ─────────────────────")
            print(f"   💰 總薪水: {result['total_salary']:,} 元")
            
            total_all_salary += result['total_salary']
        
        print("\n" + "="*60)
        print(f"💵 薪資總計: {total_all_salary:,} 元")
        print("="*60)

def main():
    calculator = SalaryCalculator()
    
    # 獲取Excel文件路徑
    excel_file = input("請輸入Excel文件路徑: ").strip().strip('"')
    
    # 讀取Excel數據
    df, total_performance, total_consumption = calculator.read_excel_data(excel_file)
    if df is None:
        print("無法讀取Excel文件，程式結束")
        return
    
    # 獲取正式淨膚師人數
    try:
        num_formal_staff = int(input("請輸入正式淨膚師人數 (2-6): "))
        if num_formal_staff < 2 or num_formal_staff > 6:
            print("正式淨膚師人數必須在2-6之間")
            return
    except ValueError:
        print("請輸入有效的數字")
        return
    
    # 獲取正式淨膚師的行位置
    formal_staff_positions = []
    print(f"請輸入{num_formal_staff}位正式淨膚師在Excel中的行號:")
    for i in range(num_formal_staff):
        try:
            row = int(input(f"第{i+1}位正式淨膚師的行號: "))
            formal_staff_positions.append(row)
        except ValueError:
            print("請輸入有效的行號")
            return
    
    # 固定讀取A12-A15的員工數據
    employee_rows = [12, 13, 14, 15]  # A12到A15
    employees = calculator.get_employee_data(df, employee_rows)
    
    if not employees:
        print("無法獲取員工數據")
        return
    
    # 計算團獎
    team_bonus_per_person = calculator.calculate_team_bonus(
        num_formal_staff, total_performance, total_consumption
    )
    
    # 計算薪水
    results = calculator.calculate_salary(employees, team_bonus_per_person, formal_staff_positions)
    
    # 輸出結果
    calculator.print_results(results, total_performance, total_consumption)

if __name__ == "__main__":
    main()
