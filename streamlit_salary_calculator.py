#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
淨膚寶薪資計算工具 - Streamlit 網頁版
基於 auto_salary_calculator.py 重新設計
"""

import streamlit as st
import pandas as pd
import io
import os
from auto_salary_calculator import AutoSalaryCalculator

class StreamlitSalaryCalculator(AutoSalaryCalculator):
    """Streamlit 網頁版薪資計算器"""

    def __init__(self):
        super().__init__()

def upload_excel_file():
    """處理 Excel 檔案上傳"""
    st.header("📁 步驟 1: 上傳 Excel 檔案")

    # 初始化 session state
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'excel_data' not in st.session_state:
        st.session_state.excel_data = None
    if 'calculation_results' not in st.session_state:
        st.session_state.calculation_results = None

    uploaded_file = st.file_uploader(
        "選擇淨膚寶月報表 Excel 檔案",
        type=['xlsx', 'xls'],
        help="請上傳包含「月報表彙整」工作表的 Excel 檔案"
    )

    if uploaded_file is not None:
        # 檢查檔案是否變更
        if st.session_state.uploaded_file != uploaded_file.name:
            st.session_state.uploaded_file = uploaded_file.name
            st.session_state.excel_data = None
            st.session_state.calculation_results = None

        # 如果還沒處理過這個檔案，就處理它
        if st.session_state.excel_data is None:
            try:
                with st.spinner("正在讀取 Excel 檔案..."):
                    # 儲存臨時檔案
                    temp_file_path = f"temp_{uploaded_file.name}"
                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # 創建計算器實例並讀取數據
                    calculator = StreamlitSalaryCalculator()

                    # 讀取 Excel 數據
                    df, total_performance, total_consumption, date_sheets = calculator.read_excel_data(temp_file_path)

                    if df is None:
                        st.error("❌ 無法讀取 Excel 檔案，請檢查檔案格式")
                        return False

                    # 計算水光面膜銷售
                    mask_sales = calculator.count_mask_sales(temp_file_path, date_sheets)

                    # 儲存數據到 session state
                    st.session_state.excel_data = {
                        'df': df,
                        'total_performance': total_performance,
                        'total_consumption': total_consumption,
                        'date_sheets': date_sheets,
                        'mask_sales': mask_sales,
                        'temp_file_path': temp_file_path
                    }

                    # 清理臨時檔案
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)

                st.success("✅ Excel 檔案讀取成功！")

            except Exception as e:
                st.error(f"❌ 讀取檔案時發生錯誤: {e}")
                return False

        # 顯示讀取結果
        if st.session_state.excel_data:
            data = st.session_state.excel_data

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 總業績", f"{data['total_performance']:,.0f} 元")
            with col2:
                st.metric("🛍️ 總消耗", f"{data['total_consumption']:,.0f} 元")
            with col3:
                if data['total_performance'] > 0:
                    consumption_rate = (data['total_consumption'] / data['total_performance']) * 100
                    st.metric("📊 消耗比例", f"{consumption_rate:.1f}%")

            # 顯示工作表資訊
            st.write(f"📋 找到的日期工作表: {data['date_sheets']}")

            # 顯示水光面膜銷售統計
            if data['mask_sales']:
                st.write("🎭 水光面膜銷售統計:")
                mask_df = pd.DataFrame(
                    list(data['mask_sales'].items()),
                    columns=['淨膚師編號', '銷售數量']
                )
                st.dataframe(mask_df, use_container_width=True)

            return True

    return False

def get_employee_preview():
    """顯示員工數據預覽"""
    st.header("👥 步驟 2: 員工數據預覽")

    if st.session_state.excel_data is None:
        st.warning("請先上傳 Excel 檔案")
        return None

    df = st.session_state.excel_data['df']
    calculator = StreamlitSalaryCalculator()

    # 獲取動態員工行號
    employee_rows = calculator.get_dynamic_employee_rows(df, start_row=12)

    st.write(f"🔍 自動檢測到 {len(employee_rows)} 位員工（行號: {employee_rows}）")

    # 顯示員工預覽
    preview_data = []
    for row in employee_rows:
        try:
            name = df.iloc[row-1, 0] if row <= df.shape[0] else None
            performance = df.iloc[row-1, 1] if row <= df.shape[0] and df.shape[1] > 1 else 0
            consumption = df.iloc[row-1, 2] if row <= df.shape[0] and df.shape[1] > 2 else 0
            person_count = df.iloc[row-1, 3] if row <= df.shape[0] and df.shape[1] > 3 else 0

            if pd.notna(name):
                preview_data.append({
                    '行號': row,
                    '姓名': name,
                    '個人業績': f"{performance:,.0f}" if pd.notna(performance) else "0",
                    '個人消耗': f"{consumption:,.0f}" if pd.notna(consumption) else "0",
                    '人次': f"{person_count:.0f}" if pd.notna(person_count) else "0"
                })
        except Exception:
            continue

    if preview_data:
        preview_df = pd.DataFrame(preview_data)
        st.dataframe(preview_df, use_container_width=True)
        return employee_rows
    else:
        st.warning("⚠️ 沒有找到有效的員工數據")
        return None

def configure_formal_staff(employee_rows):
    """設定正式淨膚師"""
    st.header("⚙️ 步驟 3: 設定正式淨膚師")

    if not employee_rows:
        st.error("沒有可用的員工數據")
        return None, None

    # 選擇正式淨膚師人數
    num_formal_staff = st.selectbox(
        "正式淨膚師人數",
        options=[2, 3, 4, 5, 6],
        help="根據團獎規則，正式淨膚師人數應在 2-6 之間"
    )

    # 選擇正式淨膚師行號
    st.write(f"請選擇 {num_formal_staff} 位正式淨膚師對應的行號:")

    formal_staff_positions = []
    available_rows = employee_rows.copy()

    for i in range(num_formal_staff):
        row = st.selectbox(
            f"第 {i+1} 位正式淨膚師",
            options=available_rows,
            key=f"formal_staff_{i}",
            help="請選擇對應的員工行號"
        )
        formal_staff_positions.append(row)
        # 從可選項目中移除已選的行號
        if row in available_rows:
            available_rows.remove(row)

    # 檢查是否有重複選擇
    if len(set(formal_staff_positions)) != len(formal_staff_positions):
        st.error("❌ 不能重複選擇同一位員工")
        return None, None

    return num_formal_staff, formal_staff_positions

def calculate_salary():
    """執行薪資計算"""
    st.header("🚀 步驟 4: 開始計算")

    if st.session_state.excel_data is None:
        st.error("請先上傳 Excel 檔案")
        return

    # 獲取員工數據
    employee_rows = get_employee_preview()
    if not employee_rows:
        return

    # 設定正式淨膚師
    config = configure_formal_staff(employee_rows)
    if config[0] is None:
        return

    num_formal_staff, formal_staff_positions = config

    # 計算按鈕
    if st.button("🎯 開始計算薪資", type="primary", use_container_width=True):
        with st.spinner("正在計算薪資..."):
            try:
                calculator = StreamlitSalaryCalculator()
                excel_data = st.session_state.excel_data

                # 獲取員工數據
                employees = calculator.get_employee_data(excel_data['df'], employee_rows)

                if not employees:
                    st.error("❌ 無法獲取員工數據")
                    return

                # 計算季獎金
                employees = calculator.calculate_seasonal_bonus(
                    employees,
                    excel_data['mask_sales'],
                    excel_data['total_consumption']
                )

                # 計算團獎
                team_bonus_per_person = calculator.calculate_team_bonus(
                    num_formal_staff,
                    excel_data['total_performance'],
                    excel_data['total_consumption']
                )

                # 計算薪資
                results = calculator.calculate_salary(
                    employees,
                    team_bonus_per_person,
                    formal_staff_positions
                )

                # 儲存結果
                st.session_state.calculation_results = {
                    'results': results,
                    'total_performance': excel_data['total_performance'],
                    'total_consumption': excel_data['total_consumption'],
                    'team_bonus_per_person': team_bonus_per_person
                }

                st.success("🎉 薪資計算完成！")

            except Exception as e:
                st.error(f"❌ 計算過程中發生錯誤: {e}")

def display_results():
    """顯示計算結果"""
    if st.session_state.calculation_results is None:
        return

    results_data = st.session_state.calculation_results
    results = results_data['results']
    total_performance = results_data['total_performance']
    total_consumption = results_data['total_consumption']

    st.header("🏆 薪資計算結果")

    # 總覽資訊
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 總業績", f"{total_performance:,.0f} 元")
    with col2:
        st.metric("🛍️ 總消耗", f"{total_consumption:,.0f} 元")
    with col3:
        if total_performance > 0:
            consumption_rate = (total_consumption / total_performance) * 100
            st.metric("📊 消耗比例", f"{consumption_rate:.1f}%")

    # 員工薪資明細
    st.subheader("👥 員工薪資明細")

    total_all_salary = 0
    total_all_seasonal_bonus = 0

    # 薪資排序選項
    sort_option = st.selectbox(
        "📊 排序方式",
        ["依姓名排序", "依總薪資排序(高到低)", "依總薪資排序(低到高)"],
        key="salary_sort"
    )

    if sort_option == "依總薪資排序(高到低)":
        results = sorted(results, key=lambda x: x['total_salary'], reverse=True)
    elif sort_option == "依總薪資排序(低到高)":
        results = sorted(results, key=lambda x: x['total_salary'])
    else:
        results = sorted(results, key=lambda x: x['name'])

    for i, result in enumerate(results, 1):
        # 計算薪資組成
        basic_salary = (
            result['base_salary'] + result['meal_allowance'] +
            result['overtime_pay'] + result['skill_bonus'] + result['team_bonus']
        )

        seasonal_bonus_total = (
            result['person_count_bonus'] + result['charge_target_bonus'] +
            result['consumption_bonus'] + result['dual_target_bonus'] +
            result['advanced_course_bonus'] + result['product_sales_bonus'] +
            result['new_customer_rate_bonus']
        )

        # 員工卡片樣式
        with st.container():
            st.markdown("---")

            # 標題行
            title_cols = st.columns([3, 1, 1])
            with title_cols[0]:
                status_emoji = "⭐" if result['is_formal_staff'] else "👤"
                st.markdown(f"### {status_emoji} {result['name']}")
                st.caption(f"{'正式淨膚師' if result['is_formal_staff'] else '一般員工'}")
            with title_cols[1]:
                st.metric("💰 總薪資", f"{result['total_salary']:,.0f}", label_visibility="visible")
            with title_cols[2]:
                st.metric("📊 排名", f"#{i}", label_visibility="visible")

            # 薪資組成卡片
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 💰 基本薪資組成")
                basic_data = {
                    "項目": ["底薪", "伙食費", "加班費", "手技獎金", "團獎"],
                    "金額": [
                        f"{result['base_salary']:,}",
                        f"{result['meal_allowance']:,}",
                        f"{result['overtime_pay']:,.0f}",
                        f"{result['skill_bonus']:,.0f}",
                        f"{result['team_bonus']:,}"
                    ]
                }
                basic_df = pd.DataFrame(basic_data)
                st.dataframe(basic_df, hide_index=True, use_container_width=True)
                st.markdown(f"**小計: {basic_salary:,.0f} 元**")

            with col2:
                st.markdown("#### 🎊 季獎金明細")
                bonus_data = {
                    "項目": ["人次激勵", "充值目標", "個人消耗", "雙達標", "進階課程", "產品銷售", "新客成交率"],
                    "金額": [
                        f"{result['person_count_bonus']:,}",
                        f"{result['charge_target_bonus']:,}",
                        f"{result['consumption_bonus']:,}",
                        f"{result['dual_target_bonus']:,}",
                        f"{result['advanced_course_bonus']:,}",
                        f"{result['product_sales_bonus']:,}",
                        f"{result['new_customer_rate_bonus']:,}"
                    ]
                }
                bonus_df = pd.DataFrame(bonus_data)
                st.dataframe(bonus_df, hide_index=True, use_container_width=True)
                st.markdown(f"**小計: {seasonal_bonus_total:,.0f} 元**")

        total_all_salary += basic_salary
        total_all_seasonal_bonus += seasonal_bonus_total

    # 全店總覽
    st.markdown("---")
    st.markdown("## 📊 全店薪資總覽")

    # 總覽卡片
    with st.container():
        overview_cols = st.columns(4)

        with overview_cols[0]:
            st.metric(
                "💰 基本薪資總計",
                f"{total_all_salary:,.0f} 元",
                help="包含底薪、伙食費、加班費、手技獎金、團獎"
            )

        with overview_cols[1]:
            st.metric(
                "🎊 季獎金總計",
                f"{total_all_seasonal_bonus:,.0f} 元",
                help="包含七項季獎金總和"
            )

        with overview_cols[2]:
            st.metric(
                "💵 全店薪資總額",
                f"{total_all_salary + total_all_seasonal_bonus:,.0f} 元",
                help="基本薪資 + 季獎金"
            )

        with overview_cols[3]:
            avg_salary = (total_all_salary + total_all_seasonal_bonus) / len(results) if results else 0
            st.metric(
                "📈 平均薪資",
                f"{avg_salary:,.0f} 元",
                help="全店平均薪資水準"
            )

    # 薪資分布統計
    if len(results) > 1:
        st.markdown("### 📈 薪資分布統計")

        salaries = [r['total_salary'] for r in results]
        min_salary = min(salaries)
        max_salary = max(salaries)
        median_salary = sorted(salaries)[len(salaries)//2]

        stats_cols = st.columns(4)
        stats_cols[0].metric("最高薪資", f"{max_salary:,.0f} 元")
        stats_cols[1].metric("最低薪資", f"{min_salary:,.0f} 元")
        stats_cols[2].metric("薪資中位數", f"{median_salary:,.0f} 元")
        stats_cols[3].metric("薪資差距", f"{max_salary - min_salary:,.0f} 元")

    # 下載報表
    create_download_report(results, total_performance, total_consumption)

def create_download_report(results, total_performance, total_consumption):
    """建立下載報表"""
    st.subheader("📄 下載報表")

    # 建立 Excel 報表
    output = io.BytesIO()

    # 建立詳細資料
    report_data = []
    for result in results:
        basic_salary = (
            result['base_salary'] + result['meal_allowance'] +
            result['overtime_pay'] + result['skill_bonus'] + result['team_bonus']
        )
        seasonal_bonus_total = (
            result['person_count_bonus'] + result['charge_target_bonus'] +
            result['consumption_bonus'] + result['dual_target_bonus'] +
            result['advanced_course_bonus'] + result['product_sales_bonus'] +
            result['new_customer_rate_bonus']
        )

        report_data.append({
            '員工姓名': result['name'],
            '身份': '正式淨膚師' if result['is_formal_staff'] else '一般員工',
            '底薪': result['base_salary'],
            '伙食費': result['meal_allowance'],
            '加班費': result['overtime_pay'],
            '手技獎金': result['skill_bonus'],
            '團獎': result['team_bonus'],
            '基本薪資小計': basic_salary,
            '人次激勵獎金': result['person_count_bonus'],
            '充值目標達成獎': result['charge_target_bonus'],
            '個人消耗獎勵': result['consumption_bonus'],
            '消耗充值雙達標獎': result['dual_target_bonus'],
            '進階課程工獎': result['advanced_course_bonus'],
            '產品銷售供獎': result['product_sales_bonus'],
            '新客成交率70%獎金': result['new_customer_rate_bonus'],
            '季獎金小計': seasonal_bonus_total,
            '總薪資': result['total_salary']
        })

    # 建立 DataFrame 並寫入 Excel
    report_df = pd.DataFrame(report_data)

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        report_df.to_excel(writer, sheet_name='薪資明細', index=False)

        # 建立總覽表
        summary_data = {
            '項目': ['業績總額', '消耗總額', '消耗比例', '基本薪資總計', '季獎金總計', '全店薪資總額'],
            '金額/比例': [
                f"{total_performance:,.0f} 元",
                f"{total_consumption:,.0f} 元",
                f"{(total_consumption/total_performance)*100:.1f}%" if total_performance > 0 else "0%",
                f"{sum([r['base_salary']+r['meal_allowance']+r['overtime_pay']+r['skill_bonus']+r['team_bonus'] for r in results]):,.0f} 元",
                f"{sum([r['person_count_bonus']+r['charge_target_bonus']+r['consumption_bonus']+r['dual_target_bonus']+r['advanced_course_bonus']+r['product_sales_bonus']+r['new_customer_rate_bonus'] for r in results]):,.0f} 元",
                f"{sum([r['total_salary'] for r in results]):,.0f} 元"
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='總覽', index=False)

    # 下載按鈕
    st.download_button(
        label="📥 下載 Excel 薪資報表",
        data=output.getvalue(),
        file_name=f"淨膚寶薪資計算報表_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def main():
    """主程式"""
    # 頁面配置
    st.set_page_config(
        page_title="淨膚寶薪資計算系統",
        page_icon="💰",
        layout="wide"
    )

    # 主標題
    st.title("💰 淨膚寶薪資計算系統")
    st.write("基於 auto_salary_calculator.py 的網頁版薪資計算工具")

    # 側邊欄
    with st.sidebar:
        st.title("🏢 操作指南")
        st.write("1. 📁 上傳 Excel 檔案")
        st.write("2. 👥 確認員工數據")
        st.write("3. ⚙️ 設定正式淨膚師")
        st.write("4. 🚀 執行計算")

        if st.button("🔄 重新開始"):
            st.session_state.clear()
            st.rerun()

    # 主要流程
    if upload_excel_file():
        calculate_salary()
        display_results()

if __name__ == "__main__":
    main()