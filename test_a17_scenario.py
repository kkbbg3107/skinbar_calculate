#!/usr/bin/env python3
"""
測試A17員工情況
"""

import pandas as pd

def test_a17_scenario():
    """測試員工到A17的情況"""
    print("🧪 測試員工到A17的情況")
    print("=" * 40)
    
    # 情況1: 員工到A17，B18為0
    print("情況1: 員工A12-A17，B18為0")
    test_data_1 = {
        'A': [None] * 11 + ['員工1', '員工2', '員工3', '員工4', '員工5', '員工6', None],  # A12-A17有員工
        'B': [None] * 11 + [250000, 180000, 320000, 150000, 200000, 280000, 0],      # B18為0
    }
    
    # 填充到X列
    for col in ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']:
        test_data_1[col] = [None] * 18
    
    df1 = pd.DataFrame(test_data_1)
    test_dynamic_detection(df1, "A12-A17員工，B18為0")
    
    print("\n" + "-" * 40)
    
    # 情況2: 員工到A17，B17已經是0（這種情況會有問題）
    print("情況2: 員工A12-A16，B17為0")
    test_data_2 = {
        'A': [None] * 11 + ['員工1', '員工2', '員工3', '員工4', '員工5', None, None],  # A12-A16有員工
        'B': [None] * 11 + [250000, 180000, 320000, 150000, 200000, 0, None],      # B17為0
    }
    
    for col in ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']:
        test_data_2[col] = [None] * 18
    
    df2 = pd.DataFrame(test_data_2)
    test_dynamic_detection(df2, "A12-A16員工，B17為0")
    
    print("\n" + "-" * 40)
    
    # 情況3: 特殊情況 - A17有員工但B17不是0（可能是業績為空）
    print("情況3: A17有員工但B17為空值")
    test_data_3 = {
        'A': [None] * 11 + ['員工1', '員工2', '員工3', '員工4', '員工5', '員工6', None],  # A12-A17有員工
        'B': [None] * 11 + [250000, 180000, 320000, 150000, 200000, None, 0],      # B17為空，B18為0
    }
    
    for col in ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']:
        test_data_3[col] = [None] * 18
    
    df3 = pd.DataFrame(test_data_3)
    test_dynamic_detection(df3, "A17有員工但B17為空值")

def test_dynamic_detection(df, description):
    """測試動態檢測邏輯"""
    print(f"\n🔍 測試: {description}")
    
    # 顯示測試數據
    for row in range(12, 19):
        try:
            a_val = df.iloc[row-1, 0] if row <= df.shape[0] else "超出範圍"
            b_val = df.iloc[row-1, 1] if row <= df.shape[0] and df.shape[1] > 1 else "超出範圍"
            
            a_display = str(a_val) if pd.notna(a_val) else "空值"
            
            if pd.notna(b_val):
                if isinstance(b_val, (int, float)):
                    b_display = f"{b_val:,.0f}" if b_val != 0 else "0"
                else:
                    b_display = str(b_val)
            else:
                b_display = "空值"
            
            print(f"  第{row}行: A={a_display:8s} B={b_display}")
        except Exception:
            print(f"  第{row}行: 讀取錯誤")
    
    # 模擬動態檢測邏輯
    employee_rows = []
    row = 12
    
    print("\n🎯 動態檢測過程:")
    while row <= df.shape[0]:
        try:
            b_value = df.iloc[row-1, 1]
            
            if pd.isna(b_value) or b_value == 0:
                print(f"  第{row}行: B列為 {b_value}，停止搜尋")
                break
            
            a_value = df.iloc[row-1, 0]
            if pd.notna(a_value) and str(a_value).strip():
                employee_rows.append(row)
                print(f"  第{row}行: ✅ {a_value} (業績: {b_value})")
            else:
                print(f"  第{row}行: ⚠️ A列無姓名，跳過")
            
            row += 1
            
        except IndexError:
            print(f"  第{row}行: 超出資料範圍")
            break
        except Exception as e:
            print(f"  第{row}行: 錯誤 - {e}")
            break
    
    print(f"結果: {employee_rows}")

if __name__ == "__main__":
    test_a17_scenario()
