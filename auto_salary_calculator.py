#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
淨膚寶薪水計算小程式 - 自動化版本（含季獎金）
預設使用 ~/skinbar_report/skinbar202506.xlsx
"""

import pandas as pd
import os
from pathlib import Path

class AutoSalaryCalculator:
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
        
        # 季獎金設定
        self.seasonal_bonus_rules = {
            'person_count_bonus': {
                110: 100,  # 110人以上，100元/人
                132: 200   # 132人以上，200元/人
            },
            'charge_target_bonus': {
                250000: 2000,  # 25萬業績，獎金2000元
                300000: 5000   # 30萬業績，再獎金5000元（總計7000元）
            },
            'mask_sales_max': 7  # 面膜銷售最高7組
        }
        
        # 預設檔案路徑
        self.default_excel_path = Path.home() / "skinbar_report" / "skinbar202506.xlsx"
    
    def get_excel_file_path(self):
        """獲取Excel檔案路徑"""
        print(f"預設Excel檔案路徑: {self.default_excel_path}")
        
        if self.default_excel_path.exists():
            use_default = input("使用預設路徑嗎？ (y/n，直接按Enter使用預設): ").strip().lower()
            if use_default in ['', 'y', 'yes']:
                return str(self.default_excel_path)
        else:
            print("⚠️  預設檔案不存在")
        
        # 手動輸入路徑
        while True:
            excel_file = input("請輸入Excel檔案完整路徑: ").strip().strip('"')
            if excel_file.startswith('~'):
                excel_file = str(Path(excel_file).expanduser())
            
            if os.path.exists(excel_file):
                return excel_file
            else:
                print(f"❌ 檔案不存在: {excel_file}")
                retry = input("要重新輸入嗎？ (y/n): ").strip().lower()
                if retry not in ['y', 'yes']:
                    return None
    
    def read_excel_data(self, excel_file):
        """讀取Excel文件數據"""
        try:
            print(f"📖 正在讀取: {excel_file}")
            
            # 先檢查工作表
            excel_data = pd.ExcelFile(excel_file)
            print(f"📋 可用工作表: {excel_data.sheet_names}")
            
            # 讀取月報表彙整工作表
            if '月報表彙整' not in excel_data.sheet_names:
                print("❌ 找不到「月報表彙整」工作表")
                print("請確認Excel檔案中有此工作表名稱")
                return None, 0, 0, []
            
            df = pd.read_excel(excel_file, sheet_name='月報表彙整', header=None)
            print(f"✅ 成功讀取Excel，共 {df.shape[0]} 行 {df.shape[1]} 列")
            
            # 找出所有日期工作表（排除月報表彙整）
            date_sheets = []
            for sheet_name in excel_data.sheet_names:
                if sheet_name != '月報表彙整':
                    # 檢查是否為日期格式的工作表（數字開頭）
                    if sheet_name.isdigit() or (len(sheet_name) >= 2 and sheet_name[0].isdigit()):
                        date_sheets.append(sheet_name)
            
            date_sheets.sort()  # 按照名稱排序
            print(f"🗓️  找到日期工作表: {date_sheets}")
            
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
                        
                    print(f"   {sheet_name}: 業績 {performance_value if pd.notna(performance_value) else 0:,.0f}, 消耗 {consumption_value if pd.notna(consumption_value) else 0:,.0f}")
                    
                except Exception as e:
                    print(f"⚠️  讀取工作表 '{sheet_name}' 時發生錯誤: {e}")
                    continue
            
            print(f"\n💰 業績總額: {total_performance:,.0f} 元")
            print(f"🛍️  消耗總額: {total_consumption:,.0f} 元")
            
            return df, total_performance, total_consumption, date_sheets
            
        except Exception as e:
            print(f"❌ 讀取Excel文件時發生錯誤: {e}")
            return None, 0, 0, []
    
    def count_mask_sales(self, excel_file, date_sheets):
        """統計各淨膚師的水光面膜銷售數量"""
        mask_sales = {}  # {淨膚師編號: 銷售數量}
        
        print("\n🎭 正在統計水光面膜銷售...")
        
        for sheet_name in date_sheets:
            try:
                sheet_df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
                
                # 檢查F:H列（細項）是否包含"水光面膜"
                for index, row in sheet_df.iterrows():
                    # 檢查F、G、H列
                    for col in [5, 6, 7]:  # F=5, G=6, H=7 (0-indexed)
                        if col < sheet_df.shape[1]:
                            cell_value = sheet_df.iloc[index, col]
                            if pd.notna(cell_value) and "水光面膜" in str(cell_value):
                                # 找到水光面膜，檢查N列的淨膚師編號
                                if 13 < sheet_df.shape[1]:  # N列是第14列 (0-indexed: 13)
                                    therapist_id = sheet_df.iloc[index, 13]  # N列
                                    if pd.notna(therapist_id):
                                        therapist_key = str(therapist_id).strip()
                                        if therapist_key not in mask_sales:
                                            mask_sales[therapist_key] = 0
                                        mask_sales[therapist_key] += 1
                                        print(f"   {sheet_name}: 淨膚師{therapist_key} +1 水光面膜")
                                        break  # 避免同一行重複計算
                
            except Exception as e:
                print(f"⚠️  統計工作表 '{sheet_name}' 水光面膜時發生錯誤: {e}")
                continue
        
        print(f"\n🎭 水光面膜統計結果: {mask_sales}")
        return mask_sales

    def calculate_person_count_bonus(self, person_count):
        """計算個人人次激勵獎金
        110人以上才有獎金，獎金從第111人開始計算
        111-132人：每人100元
        133人以上：每人200元
        舉例：134人 = (111-132) 22人×100元 + (133-134) 2人×200元 = 2200 + 400 = 2600元
        """
        if person_count < 110:
            return 0
        
        bonus = 0
        
        # 111-132人，每人100元
        if person_count >= 110:
            tier1_start = 111
            tier1_end = min(person_count, 132)
            if tier1_end >= tier1_start:
                tier1_count = tier1_end - tier1_start + 1
                bonus += tier1_count * 100
        
        # 133人以上，每人200元
        if person_count > 132:
            tier2_count = person_count - 132
            bonus += tier2_count * 200
        
        return bonus
    
    def calculate_charge_target_bonus(self, personal_performance, mask_count):
        """計算充值目標達成獎"""
        bonus = 0
        
        # 檢查業績達標
        if personal_performance >= 250000:
            bonus += 2000
            if personal_performance >= 300000:
                bonus += 5000
        
        # 面膜銷售額外獎金（最高7組）
        mask_bonus = min(mask_count, self.seasonal_bonus_rules['mask_sales_max']) * 1000
        
        # 總獎金最高7000元
        total_bonus = min(bonus + mask_bonus, 7000)
        
        return total_bonus, bonus, mask_bonus

    def preview_employee_data(self, df):
        """預覽員工數據"""
        print("\n👥 員工數據預覽 (A12-A15):")
        print("-" * 70)
        
        for i, row in enumerate([12, 13, 14, 15], 1):
            try:
                name = df.iloc[row-1, 0]  # A行
                personal_performance = df.iloc[row-1, 1]  # B行
                person_count = df.iloc[row-1, 3]  # D行
                skill_bonus = df.iloc[row-1, 22]  # W行
                
                personal_performance = personal_performance if pd.notna(personal_performance) else 0
                person_count = person_count if pd.notna(person_count) else 0
                skill_bonus = skill_bonus if pd.notna(skill_bonus) else 0
                
                print(f"行號 {row}: {name}")
                print(f"  個人業績: {personal_performance:,.0f} 元, 人次: {person_count:.0f}, 手技獎金: {skill_bonus:,.0f} 元")
            except Exception as e:
                print(f"行號 {row}: 讀取錯誤 - {e}")
        
        print("-" * 70)
    
    def get_employee_data(self, df, employee_rows):
        """獲取員工數據"""
        employees = []
        
        for row in employee_rows:
            try:
                # 獲取員工姓名 (A行)
                name = df.iloc[row-1, 0]  # 轉換為0-indexed
                
                # 獲取手計供獎累計 (W行)
                skill_bonus_total = df.iloc[row-1, 22]  # W列是第23列 (0-indexed: 22)
                
                # 獲取個人業績 (B行)
                personal_performance = df.iloc[row-1, 1]  # B列是第2列 (0-indexed: 1)
                
                # 獲取人次總數 (D行)
                person_count = df.iloc[row-1, 3]  # D列是第4列 (0-indexed: 3)
                
                employees.append({
                    'name': name,
                    'skill_bonus_total': skill_bonus_total if pd.notna(skill_bonus_total) else 0,
                    'personal_performance': personal_performance if pd.notna(personal_performance) else 0,
                    'person_count': person_count if pd.notna(person_count) else 0,
                    'row': row
                })
                
            except Exception as e:
                print(f"❌ 獲取第{row}行員工數據時發生錯誤: {e}")
                
        return employees

    def calculate_seasonal_bonus(self, employees, mask_sales):
        """計算季獎金 - 目前只計算人次激勵獎金"""
        print("\n🎉 正在計算季獎金（人次激勵）...")
        
        for employee in employees:
            # 人次激勵獎金
            person_count_bonus = self.calculate_person_count_bonus(employee['person_count'])
            
            # 將季獎金資訊添加到員工資料
            employee['person_count_bonus'] = person_count_bonus
            
            print(f"   {employee['name']}: 人次{employee['person_count']:.0f} → 人次激勵獎金{person_count_bonus:,}元")
            
            # 顯示詳細計算過程
            if person_count_bonus > 0:
                if employee['person_count'] > 132:
                    tier1_count = 132 - 111 + 1  # 111-132人
                    tier2_count = employee['person_count'] - 132  # 133以上
                    print(f"      詳細: 111-132人({tier1_count}人×100元) + 133-{employee['person_count']:.0f}人({tier2_count}人×200元)")
                elif employee['person_count'] >= 110:
                    tier1_count = employee['person_count'] - 111 + 1  # 111到person_count
                    print(f"      詳細: 111-{employee['person_count']:.0f}人({tier1_count:.0f}人×100元)")
        
        return employees

    def calculate_team_bonus(self, num_formal_staff, total_performance, total_consumption):
        """計算團獎"""
        if num_formal_staff not in self.team_bonus_rules:
            print(f"❌ 沒有{num_formal_staff}位正式淨膚師的團獎規則")
            return 0
        
        required_performance, required_consumption_rate, bonus_amount = self.team_bonus_rules[num_formal_staff]
        
        print(f"\n🎯 團獎檢查 ({num_formal_staff}位正式淨膚師):")
        print(f"   業績要求: {required_performance:,} 元")
        print(f"   實際業績: {total_performance:,.0f} 元")
        
        # 檢查是否達到業績要求
        if total_performance < required_performance:
            print(f"❌ 業績未達標: 差額 {required_performance - total_performance:,.0f} 元")
            return 0
        
        # 檢查消耗比例
        if total_performance > 0:
            consumption_rate = total_consumption / total_performance
            print(f"   消耗比例要求: {required_consumption_rate*100}%")
            print(f"   實際消耗比例: {consumption_rate*100:.1f}%")
            
            if consumption_rate < required_consumption_rate:
                print("❌ 消耗比例未達標")
                return 0
        
        print(f"✅ 達到團獎條件！每位正式淨膚師可獲得 {bonus_amount:,} 元團獎")
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
            
            # 季獎金 - 只有正式淨膚師才有
            person_count_bonus = employee.get('person_count_bonus', 0) if is_formal_staff else 0
            
            # 計算總薪水
            total_salary = base + meal + overtime + skill_bonus + team_bonus + person_count_bonus
            
            result = {
                'name': employee['name'],
                'base_salary': base,
                'meal_allowance': meal,
                'overtime_pay': overtime,
                'skill_bonus': skill_bonus,
                'team_bonus': team_bonus,
                'person_count_bonus': person_count_bonus,
                'total_salary': total_salary,
                'is_formal_staff': is_formal_staff
            }
            
            results.append(result)
        
        return results
    
    def print_results(self, results, total_performance, total_consumption):
        """輸出結果"""
        print("\n" + "="*70)
        print("🏆 淨膚寶薪水計算結果（含人次激勵獎金）")
        print("="*70)
        
        print(f"\n💰 當月業績總額: {total_performance:,.0f} 元")
        print(f"🛍️  當月消耗總額: {total_consumption:,.0f} 元")
        if total_performance > 0:
            consumption_rate = (total_consumption / total_performance) * 100
            print(f"📊 消耗比例: {consumption_rate:.1f}%")
        
        print("\n" + "="*70)
        print("👥 員工薪資明細")
        print("="*70)
        
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
            print(f"   人次激勵獎金: {result['person_count_bonus']:,} 元")
            print("   ─────────────────────────────")
            print(f"   💰 總薪水: {result['total_salary']:,} 元")
            
            total_all_salary += result['total_salary']
        
        print("\n" + "="*70)
        print(f"💵 薪資總計: {total_all_salary:,} 元")
        print("="*70)

def main():
    print("🏢 淨膚寶薪水計算小程式 - 自動化版本（含季獎金）")
    print("="*60)
    
    calculator = AutoSalaryCalculator()
    
    # 獲取Excel文件路徑
    excel_file = calculator.get_excel_file_path()
    if not excel_file:
        print("❌ 程式結束")
        return
    
    # 讀取Excel數據
    df, total_performance, total_consumption, date_sheets = calculator.read_excel_data(excel_file)
    if df is None:
        print("❌ 無法讀取Excel文件，程式結束")
        return
    
    # 統計水光面膜銷售（暫時不使用）
    # mask_sales = calculator.count_mask_sales(excel_file, date_sheets)
    mask_sales = {}  # 空字典，後續擴充其他季獎金時使用
    
    # 預覽員工數據
    calculator.preview_employee_data(df)
    
    # 獲取正式淨膚師人數
    try:
        num_formal_staff = int(input("\n請輸入正式淨膚師人數 (2-6): "))
        if num_formal_staff < 2 or num_formal_staff > 6:
            print("❌ 正式淨膚師人數必須在2-6之間")
            return
    except ValueError:
        print("❌ 請輸入有效的數字")
        return
    
    # 獲取正式淨膚師的行位置
    formal_staff_positions = []
    print(f"\n請輸入{num_formal_staff}位正式淨膚師在Excel中的行號 (參考上方預覽):")
    for i in range(num_formal_staff):
        try:
            row = int(input(f"第{i+1}位正式淨膚師的行號: "))
            if row not in [12, 13, 14, 15]:
                print("⚠️  警告: 行號不在預期範圍內 (12-15)")
            formal_staff_positions.append(row)
        except ValueError:
            print("❌ 請輸入有效的行號")
            return
    
    # 固定讀取A12-A15的員工數據
    employee_rows = [12, 13, 14, 15]  # A12到A15
    employees = calculator.get_employee_data(df, employee_rows)
    
    if not employees:
        print("❌ 無法獲取員工數據")
        return
    
    # 計算季獎金
    employees = calculator.calculate_seasonal_bonus(employees, mask_sales)
    
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
