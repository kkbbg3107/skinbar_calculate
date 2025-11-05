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
        print("📁 請選擇要計算的 Excel 檔案")
        print("💡 提示：可以直接拖拉檔案到終端視窗，或手動輸入完整路徑")
        print()
        
        # 直接要求手動輸入路徑
        while True:
            excel_file = input("Excel檔案路徑: ").strip().strip('"')
            if excel_file.startswith('~'):
                excel_file = str(Path(excel_file).expanduser())
            
            if os.path.exists(excel_file):
                print(f"✅ 檔案確認: {excel_file}")
                return excel_file
            else:
                print(f"❌ 檔案不存在: {excel_file}")
                print("   請檢查路徑是否正確")
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
            
            df = self.safe_read_excel(excel_file, sheet_name='月報表彙整', header=None)
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
                    sheet_df = self.safe_read_excel(excel_file, sheet_name=sheet_name, header=None)
                    
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
                sheet_df = self.safe_read_excel(excel_file, sheet_name=sheet_name, header=None)
                
                # 檢查 F21:H21 以下的欄位（從第21行開始，0-indexed為20）
                start_row = 20  # F21 對應 index 20
                
                for index in range(start_row, sheet_df.shape[0]):
                    # 檢查F、G、H列
                    for col in [5, 6, 7]:  # F=5, G=6, H=7 (0-indexed)
                        if col < sheet_df.shape[1]:
                            cell_value = sheet_df.iloc[index, col]
                            if pd.notna(cell_value) and "水光面膜3入" in str(cell_value):
                                # 找到水光面膜，檢查同一行N列的淨膚師編號
                                if 13 < sheet_df.shape[1]:  # N列是第14列 (0-indexed: 13)
                                    therapist_id = sheet_df.iloc[index, 13]  # N列
                                    if pd.notna(therapist_id):
                                        therapist_key = str(int(float(therapist_id))).strip()  # 確保是整數格式
                                        if therapist_key not in mask_sales:
                                            mask_sales[therapist_key] = 0
                                        mask_sales[therapist_key] += 1
                                        print(f"   {sheet_name}: 淨膚師{therapist_key} +1 水光面膜3入 (第{index+1}行)")
                                        break  # 避免同一行重複計算
                
            except Exception as e:
                print(f"⚠️  統計工作表 '{sheet_name}' 水光面膜時發生錯誤: {e}")
                continue
        
        print("\n🎭 水光面膜統計結果:")
        for therapist_id, count in mask_sales.items():
            print(f"   淨膚師{therapist_id}: {count}組")
        
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
    
    def calculate_charge_target_bonus(self, personal_performance, therapist_id, mask_sales):
        """計算充值目標達成獎
        條件：同時達成業績門檻 AND 水光面膜銷售7組以上
        - 業績25萬 + 面膜7組 → 2000元
        - 業績30萬 + 面膜7組 → 7000元
        - 面膜不到7組則無獎金
        """
        bonus = 0
        
        # 獲取該淨膚師的水光面膜銷售數量
        mask_count = mask_sales.get(str(therapist_id), 0)
        
        # 先檢查面膜銷售責任額（必須7組以上才能有獎金）
        if mask_count < 7:
            return 0, f"面膜未達責任額: {mask_count}/7組"
        
        # 面膜達標後，檢查業績門檻
        if personal_performance >= 300000:
            bonus = 7000  # 30萬業績 + 7組面膜 = 7000元
            reason = f"業績30萬+面膜{mask_count}組達標"
        elif personal_performance >= 250000:
            bonus = 2000  # 25萬業績 + 7組面膜 = 2000元  
            reason = f"業績25萬+面膜{mask_count}組達標"
        else:
            return 0, f"業績未達25萬門檻: {personal_performance:,.0f}元"
        
        return bonus, reason
    
    def calculate_consumption_bonus(self, personal_consumption, total_consumption):
        """計算個人消耗獎勵季獎金
        消耗達18萬：可抽個人消耗的1.5%
        消耗達20萬：可抽個人消耗的2.5%
        * KOL不計算消耗
        """
        bonus = 0
        reason = ""
        
        if personal_consumption >= 200000:
            # 20萬消耗：個人消耗的2.5%
            bonus = int(personal_consumption * 0.025)
            reason = f"消耗20萬達標，可抽個人消耗{personal_consumption:,.0f}元的2.5%"
        elif personal_consumption >= 180000:
            # 18萬消耗：個人消耗的1.5%
            bonus = int(personal_consumption * 0.015)
            reason = f"消耗18萬達標，可抽個人消耗{personal_consumption:,.0f}元的1.5%"
        else:
            reason = f"消耗未達18萬門檻: {personal_consumption:,.0f}元"
        
        return bonus, reason
    
    def calculate_dual_target_bonus(self, personal_consumption, personal_performance, mask_sales, therapist_id, total_consumption):
        """計算消耗充值雙達標獎
        必須同時達成以下兩個條件：
        1. 充值目標達成獎：業績25萬+ AND 面膜7組+
        2. 個人消耗獎勵：消耗18萬+
        同時達成才能獲得2000元雙達標獎
        """
        bonus = 0
        reason = ""
        
        # 檢查充值目標達成獎條件
        mask_count = mask_sales.get(str(therapist_id), 0)
        charge_bonus, charge_reason = self.calculate_charge_target_bonus(personal_performance, therapist_id, mask_sales)
        
        # 檢查個人消耗獎勵條件
        consumption_bonus, consumption_reason = self.calculate_consumption_bonus(personal_consumption, total_consumption)
        
        # 只有兩個條件都達成才能獲得雙達標獎
        charge_qualified = charge_bonus > 0  # 充值目標達成獎有獎金
        consumption_qualified = consumption_bonus > 0  # 個人消耗獎勵有獎金
        
        if charge_qualified and consumption_qualified:
            bonus = 2000
            reason = "充值目標+個人消耗雙達標"
        else:
            missing = []
            if not charge_qualified:
                if mask_count < 7:
                    missing.append(f"面膜未達7組({mask_count}組)")
                elif personal_performance < 250000:
                    missing.append(f"業績未達25萬({personal_performance:,.0f}元)")
                else:
                    missing.append("充值目標未達成")
            if not consumption_qualified:
                missing.append(f"消耗未達18萬({personal_consumption:,.0f}元)")
            reason = f"未達雙標準: {', '.join(missing)}"
        
        return bonus, reason
    
    def calculate_advanced_course_bonus(self, advanced_course_total):
        """計算進階課程工獎
        類似手技獎金，直接使用V行數據
        """
        return advanced_course_total, "進階課程工獎累計"
    
    def calculate_product_sales_bonus(self, product_sales_total):
        """計算產品銷售供獎
        直接使用X行數據
        """
        return product_sales_total, "產品銷售供獎累計"
    
    def preview_employee_data(self, df):
        """預覽員工數據"""
        print("\n👥 員工數據預覽 (A14-A17):")
        print("-" * 70)
        
        for i, row in enumerate([14, 15, 16, 17], 1):
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
                
                # 獲取個人業績 (B行)
                personal_performance = df.iloc[row-1, 1]  # B列是第2列 (0-indexed: 1)
                
                # 獲取個人消耗 (C行)
                personal_consumption = df.iloc[row-1, 2]  # C列是第3列 (0-indexed: 2)
                
                # 獲取人次總數 (D行)
                person_count = df.iloc[row-1, 3]  # D列是第4列 (0-indexed: 3)
                
                # 獲取新客實際成交率 (I行)
                new_customer_rate = df.iloc[row-1, 8]  # I列是第9列 (0-indexed: 8)
                
                # 獲取進階課程工獎 (V行)
                advanced_course_bonus = df.iloc[row-1, 21]  # V列是第22列 (0-indexed: 21)
                
                # 獲取手計供獎累計 (W行)
                skill_bonus_total = df.iloc[row-1, 22]  # W列是第23列 (0-indexed: 22)
                
                # 獲取產品銷售供獎 (X行)
                product_sales_bonus = df.iloc[row-1, 23]  # X列是第24列 (0-indexed: 23)
                
                employees.append({
                    'name': name,
                    'personal_performance': personal_performance if pd.notna(personal_performance) else 0,
                    'personal_consumption': personal_consumption if pd.notna(personal_consumption) else 0,
                    'person_count': person_count if pd.notna(person_count) else 0,
                    'new_customer_rate': new_customer_rate if pd.notna(new_customer_rate) else 0,
                    'advanced_course_bonus': advanced_course_bonus if pd.notna(advanced_course_bonus) else 0,
                    'skill_bonus_total': skill_bonus_total if pd.notna(skill_bonus_total) else 0,
                    'product_sales_bonus': product_sales_bonus if pd.notna(product_sales_bonus) else 0,
                    'row': row
                })
                
            except Exception as e:
                print(f"❌ 獲取第{row}行員工數據時發生錯誤: {e}")
                
        return employees

    def calculate_seasonal_bonus(self, employees, mask_sales, total_consumption):
        """計算季獎金 - 包含所有六個季獎金細項"""
        print("\n🎉 正在計算季獎金...")
        
        for employee in employees:
            # 根據員工行號推算淨膚師編號 (12->1, 13->2, 14->3, 15->4)
            therapist_id = employee['row'] - 11
            
            # 1. 人次激勵獎金
            person_count_bonus = self.calculate_person_count_bonus(employee['person_count'])
            
            # 2. 充值目標達成獎
            charge_target_bonus, charge_reason = self.calculate_charge_target_bonus(
                employee['personal_performance'], 
                therapist_id, 
                mask_sales
            )
            
            # 3. 個人消耗獎勵季獎金
            consumption_bonus, consumption_reason = self.calculate_consumption_bonus(
                employee['personal_consumption'], 
                total_consumption
            )
            
            # 4. 消耗充值雙達標獎
            dual_target_bonus, dual_reason = self.calculate_dual_target_bonus(
                employee['personal_consumption'], 
                employee['personal_performance'],
                mask_sales,
                therapist_id,
                total_consumption
            )
            
            # 5. 進階課程工獎
            advanced_course_bonus, advanced_reason = self.calculate_advanced_course_bonus(
                employee['advanced_course_bonus']
            )
            
            # 6. 產品銷售供獎
            product_sales_bonus, product_reason = self.calculate_product_sales_bonus(
                employee['product_sales_bonus']
            )
            
            # 7. 新客成交率70%獎金
            new_customer_rate_bonus, new_customer_reason = self.calculate_new_customer_rate_bonus(
                employee['person_count'],
                employee['new_customer_rate']
            )
            
            # 獲取面膜數量用於顯示
            mask_count = mask_sales.get(str(therapist_id), 0)
            
            # 將季獎金資訊添加到員工資料
            employee['person_count_bonus'] = person_count_bonus
            employee['charge_target_bonus'] = charge_target_bonus
            employee['consumption_bonus'] = consumption_bonus
            employee['dual_target_bonus'] = dual_target_bonus
            employee['advanced_course_bonus'] = advanced_course_bonus
            employee['product_sales_bonus'] = product_sales_bonus
            employee['new_customer_rate_bonus'] = new_customer_rate_bonus
            employee['therapist_id'] = therapist_id
            
            print(f"\n   {employee['name']} (淨膚師{therapist_id}):")
            print(f"      業績: {employee['personal_performance']:,.0f}元, 消耗: {employee['personal_consumption']:,.0f}元")
            print(f"      人次: {employee['person_count']:.0f}, 水光面膜: {mask_count}組, 新客成交率: {employee['new_customer_rate']:.1f}%")
            
            # 顯示各項季獎金
            print(f"      📈 人次激勵獎金: {person_count_bonus:,}元", end="")
            if person_count_bonus > 0:
                if employee['person_count'] > 132:
                    tier1_count = 132 - 111 + 1
                    tier2_count = employee['person_count'] - 132
                    print(f" (111-132人: {tier1_count}×100 + 133-{employee['person_count']:.0f}人: {tier2_count}×200)")
                elif employee['person_count'] >= 110:
                    tier1_count = employee['person_count'] - 111 + 1
                    print(f" (111-{employee['person_count']:.0f}人: {tier1_count:.0f}×100)")
                else:
                    print()
            else:
                print()
            
            # 充值目標達成獎
            status = "✅" if charge_target_bonus > 0 else "❌"
            print(f"      🎯 充值目標達成獎: {charge_target_bonus:,}元 {status} {charge_reason}")
            
            # 個人消耗獎勵季獎金
            status = "✅" if consumption_bonus > 0 else "❌"
            print(f"      💧 個人消耗獎勵: {consumption_bonus:,}元 {status} {consumption_reason}")
            
            # 消耗充值雙達標獎
            status = "✅" if dual_target_bonus > 0 else "❌"
            print(f"      🎪 消耗充值雙達標獎: {dual_target_bonus:,}元 {status} {dual_reason}")
            
            # 進階課程工獎
            print(f"      📚 進階課程工獎: {advanced_course_bonus:,}元 ({advanced_reason})")
            
            # 產品銷售供獎
            print(f"      🛍️  產品銷售供獎: {product_sales_bonus:,}元 ({product_reason})")
            
            # 新客成交率70%獎金
            status = "✅" if new_customer_rate_bonus > 0 else "❌"
            print(f"      🎯 新客成交率70%獎金: {new_customer_rate_bonus:,}元 {status} {new_customer_reason}")
        
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
            
            # 判斷是否為正式淨膚師，決定是否有團獎和季獎金
            is_formal_staff = employee['row'] in formal_staff_positions
            team_bonus = team_bonus_per_person if is_formal_staff else 0
            
            # 季獎金 - 只有正式淨膚師才有
            person_count_bonus = employee.get('person_count_bonus', 0) if is_formal_staff else 0
            charge_target_bonus = employee.get('charge_target_bonus', 0) if is_formal_staff else 0
            consumption_bonus = employee.get('consumption_bonus', 0) if is_formal_staff else 0
            dual_target_bonus = employee.get('dual_target_bonus', 0) if is_formal_staff else 0
            new_customer_rate_bonus = employee.get('new_customer_rate_bonus', 0) if is_formal_staff else 0
            
            # 進階課程工獎和產品銷售供獎（所有員工都有）
            advanced_course_bonus = employee.get('advanced_course_bonus', 0)
            product_sales_bonus = employee.get('product_sales_bonus', 0)
            
            # 計算總薪水
            total_salary = (base + meal + overtime + skill_bonus + team_bonus + 
                          person_count_bonus + charge_target_bonus + consumption_bonus + 
                          dual_target_bonus + advanced_course_bonus + product_sales_bonus + 
                          new_customer_rate_bonus)
            
            result = {
                'name': employee['name'],
                'base_salary': base,
                'meal_allowance': meal,
                'overtime_pay': overtime,
                'skill_bonus': skill_bonus,
                'team_bonus': team_bonus,
                'person_count_bonus': person_count_bonus,
                'charge_target_bonus': charge_target_bonus,
                'consumption_bonus': consumption_bonus,
                'dual_target_bonus': dual_target_bonus,
                'advanced_course_bonus': advanced_course_bonus,
                'product_sales_bonus': product_sales_bonus,
                'new_customer_rate_bonus': new_customer_rate_bonus,
                'total_salary': total_salary,
                'is_formal_staff': is_formal_staff
            }
            
            results.append(result)
        
        return results
    
    def print_results(self, results, total_performance, total_consumption):
        """輸出結果"""
        print("\n" + "="*70)
        print("🏆 淨膚寶薪水計算結果（含季獎金）")
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
        total_all_seasonal_bonus = 0
        
        for i, result in enumerate(results, 1):
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
            print(f"   � 總計: {result['total_salary']:,.0f} 元")
            
            total_all_salary += basic_salary
            total_all_seasonal_bonus += seasonal_bonus_total
        
        print("\n" + "="*70)
        print("📊 全店薪資總覽")
        print("="*70)
        print(f"� 基本薪資總計: {total_all_salary:,.0f} 元 (底薪+伙食費+加班費+手技獎金+團獎)")
        print(f"🎊 季獎金總計: {total_all_seasonal_bonus:,.0f} 元")
        print("─"*70)
        print(f"�💵 全店薪資總額: {total_all_salary + total_all_seasonal_bonus:,.0f} 元")
        print("="*70)

    def calculate_new_customer_rate_bonus(self, person_count, new_customer_rate):
        """計算新客成交率70%獎金
        條件：客人數量達132人 + 新客實際成交率70%
        獎金：4000元（需人工檢查出勤狀況）
        """
        bonus = 0
        reason = ""
        
        # 檢查人次是否達132人
        person_count_ok = person_count >= 132
        
        # 檢查新客成交率是否達70%（0.7）
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
    
    def safe_read_excel(self, file_path, **kwargs):
        """安全讀取 Excel 檔案，處理 OLE2 compound document 錯誤"""
        try:
            file_path = str(file_path)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"檔案不存在: {file_path}")
            
            file_ext = Path(file_path).suffix.lower()
            
            # 根據副檔名選擇適當的引擎
            if file_ext == '.xlsx':
                try:
                    return pd.read_excel(file_path, engine='openpyxl', **kwargs)
                except Exception as e:
                    print(f"⚠️  openpyxl 引擎失敗: {e}")
            elif file_ext == '.xls':
                try:
                    return pd.read_excel(file_path, engine='xlrd', **kwargs)
                except Exception as e:
                    print(f"⚠️  xlrd 引擎失敗: {e}")
            
            # 嘗試自動偵測引擎
            try:
                return pd.read_excel(file_path, **kwargs)
            except Exception as auto_error:
                if "OLE2" in str(auto_error) or "compound document" in str(auto_error):
                    print("🔧 偵測到 OLE2 錯誤，嘗試修復...")
                    print("💡 建議解決方案:")
                    print("1. 在 Excel 中開啟檔案，另存為 .xlsx 格式")
                    print("2. 檢查檔案是否完整下載")
                    print("3. 確認檔案沒有被其他程序佔用")
                    raise Exception(f"Excel 檔案格式錯誤 (OLE2): {auto_error}")
                else:
                    raise auto_error
                    
        except Exception as e:
            print(f"❌ 讀取Excel文件時發生錯誤: {e}")
            raise

    def get_dynamic_employee_rows(self, df, start_row=14):
        """動態獲取員工行號，從指定行開始，連續遇到多個空行才停止

        改進的邏輯：
        - 跳過表頭行（B行為文字）
        - 連續遇到2個B行為0的行才停止（更容錯）
        - 只收集姓名不為純數字的員工行
        """
        employee_rows = []
        row = start_row
        consecutive_zeros = 0  # 連續遇到0的次數

        print(f"🔍 動態搜尋員工數據（從第{start_row}行開始）...")

        # 增加最大搜尋範圍，避免無限循環
        max_row = min(df.shape[0], start_row + 20)  # 最多搜尋20行

        while row <= max_row:
            try:
                # 檢查B行的值（個人業績）
                b_value = df.iloc[row-1, 1] if df.shape[1] > 1 else None

                # 檢查A行是否有員工姓名
                a_value = df.iloc[row-1, 0] if df.shape[0] >= row else None

                print(f"   第{row}行檢查: A='{a_value}' B='{b_value}'")

                # 檢查B行是否為數字
                try:
                    b_numeric = float(b_value) if pd.notna(b_value) else 0
                except (ValueError, TypeError):
                    # B行為文字（可能是表頭），跳過這行
                    print(f"   第{row}行 B列為文字 '{b_value}'，跳過")
                    row += 1
                    continue

                # 如果B行為0，增加計數器
                if b_numeric == 0:
                    consecutive_zeros += 1
                    print(f"   第{row}行 B列為 0（連續 {consecutive_zeros} 次）")

                    # 連續2個0才停止搜尋
                    if consecutive_zeros >= 2:
                        print(f"   連續遇到 {consecutive_zeros} 個 0，停止搜尋")
                        break
                else:
                    # 重置計數器
                    consecutive_zeros = 0

                # 檢查A行是否有有效的員工姓名
                if pd.notna(a_value) and str(a_value).strip():
                    a_str = str(a_value).strip()

                    # 排除純數字的姓名（如「4」「5」「6」）
                    if a_str.isdigit():
                        print(f"   ⚠️  第{row}行: 姓名為純數字 '{a_str}'，跳過")
                    elif b_numeric > 0:
                        # 有效的員工：姓名不為空、不為純數字、業績>0
                        employee_rows.append(row)
                        print(f"   ✅ 第{row}行: {a_value} (業績: {b_numeric:,.0f})")
                    else:
                        print(f"   第{row}行: {a_value} (業績為0，記錄但可能非正式員工)")

                row += 1

            except IndexError:
                # 超出資料範圍
                print(f"   第{row}行超出資料範圍，停止搜尋")
                break
            except Exception as e:
                print(f"   ❌ 第{row}行讀取錯誤: {e}")
                row += 1
                continue

        print(f"🎯 找到 {len(employee_rows)} 位員工: 行號 {employee_rows}")
        return employee_rows

    def get_manual_employee_rows(self, start_row=12, end_row=17):
        """手動指定員工行號範圍"""
        employee_rows = list(range(start_row, end_row + 1))
        print(f"🔧 手動指定員工範圍: 第{start_row}行到第{end_row}行")
        print(f"   員工行號: {employee_rows}")
        return employee_rows

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
    
    # 統計水光面膜銷售
    mask_sales = calculator.count_mask_sales(excel_file, date_sheets)
    
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
            if row not in [12, 13, 14, 15, 16, 17]:
                print("⚠️  警告: 行號不在預期範圍內 (12-17)")
            formal_staff_positions.append(row)
        except ValueError:
            print("❌ 請輸入有效的行號")
            return
    
    # 選擇員工數據讀取方式
    print("\n📋 員工數據讀取方式:")
    print("1. 自動檢測（根據B行數值判斷）")
    print("2. 手動指定範圍（例如A14到A17）")
    
    detection_choice = input("請選擇 (1/2，直接按Enter使用自動檢測): ").strip()
    
    if detection_choice == "2":
        # 手動指定範圍
        try:
            start_row = int(input("起始行號 (預設14): ") or "12")
            end_row = int(input("結束行號 (預設17): ") or "17")
            employee_rows = calculator.get_manual_employee_rows(start_row, end_row)
        except ValueError:
            print("❌ 輸入錯誤，使用預設範圍 A14-A17")
            employee_rows = calculator.get_manual_employee_rows(12, 17)
    else:
        # 自動檢測（預設）
        employee_rows = calculator.get_dynamic_employee_rows(df, start_row=12)
    
    if not employee_rows:
        print("❌ 沒有找到任何員工數據")
        return
    
    employees = calculator.get_employee_data(df, employee_rows)
    
    if not employees:
        print("❌ 無法獲取員工數據")
        return
    
    # 計算季獎金
    employees = calculator.calculate_seasonal_bonus(employees, mask_sales, total_consumption)
    
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
