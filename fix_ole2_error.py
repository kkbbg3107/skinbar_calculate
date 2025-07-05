#!/usr/bin/env python3
"""
修正薪資計算程式中的 Excel 讀取問題
專門處理 OLE2 compound document 錯誤
"""

import pandas as pd
import os
from pathlib import Path

class ExcelFileHandler:
    """處理各種 Excel 檔案問題的類別"""
    
    def __init__(self):
        self.supported_engines = {
            '.xlsx': 'openpyxl',
            '.xls': 'xlrd'
        }
    
    def safe_read_excel(self, file_path, **kwargs):
        """安全讀取 Excel 檔案，處理各種錯誤"""
        file_path = str(file_path)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"檔案不存在: {file_path}")
        
        file_ext = Path(file_path).suffix.lower()
        
        # 方法1: 使用推薦的引擎
        if file_ext in self.supported_engines:
            engine = self.supported_engines[file_ext]
            try:
                return pd.read_excel(file_path, engine=engine, **kwargs)
            except Exception as e:
                print(f"⚠️  使用 {engine} 引擎失敗: {e}")
        
        # 方法2: 嘗試自動偵測
        try:
            return pd.read_excel(file_path, **kwargs)
        except Exception as auto_error:
            print(f"⚠️  自動偵測失敗: {auto_error}")
            
            # 方法3: 如果是 OLE2 錯誤，可能是檔案格式問題
            if "OLE2" in str(auto_error) or "compound document" in str(auto_error):
                print("🔧 偵測到 OLE2 錯誤，嘗試修復...")
                
                # 檢查檔案大小
                file_size = os.path.getsize(file_path)
                if file_size == 0:
                    raise ValueError("檔案大小為 0，可能是空檔案或下載不完整")
                
                # 嘗試強制使用不同引擎
                engines_to_try = ['openpyxl', 'xlrd']
                for engine in engines_to_try:
                    try:
                        print(f"   嘗試使用 {engine} 引擎...")
                        return pd.read_excel(file_path, engine=engine, **kwargs)
                    except Exception as engine_error:
                        print(f"   {engine} 引擎失敗: {engine_error}")
                
                # 如果都失敗，提供修復建議
                self._suggest_file_fix(file_path)
                raise Exception(f"無法讀取 Excel 檔案: {file_path}")
            else:
                raise auto_error
    
    def _suggest_file_fix(self, file_path):
        """提供檔案修復建議"""
        print("\n💡 建議修復步驟:")
        print("1. 在 Microsoft Excel 中開啟檔案")
        print("2. 點選「檔案」→「另存新檔」")
        print("3. 選擇「Excel 活頁簿 (*.xlsx)」格式")
        print("4. 儲存為新檔案")
        print("5. 使用新檔案執行程式")
        
        new_path = str(file_path).replace('.xls', '.xlsx')
        if new_path != file_path:
            print(f"\n建議的新檔案名稱: {new_path}")

def update_salary_calculator():
    """更新薪資計算程式以使用安全的 Excel 讀取"""
    print("🔧 更新薪資計算程式的 Excel 讀取功能...")
    
    # 這裡我們可以修改主程式使用安全的讀取方法
    handler_code = '''
# 在 auto_salary_calculator.py 中加入安全的 Excel 讀取
from pathlib import Path
import pandas as pd
import os

class SafeExcelReader:
    """安全的 Excel 讀取器"""
    
    @staticmethod
    def safe_read_excel(file_path, **kwargs):
        """安全讀取 Excel 檔案"""
        file_path = str(file_path)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"檔案不存在: {file_path}")
        
        file_ext = Path(file_path).suffix.lower()
        
        # 根據副檔名選擇引擎
        if file_ext == '.xlsx':
            try:
                return pd.read_excel(file_path, engine='openpyxl', **kwargs)
            except Exception:
                pass
        elif file_ext == '.xls':
            try:
                return pd.read_excel(file_path, engine='xlrd', **kwargs)
            except Exception:
                pass
        
        # 最後嘗試自動偵測
        return pd.read_excel(file_path, **kwargs)
'''
    
    print("建議在薪資計算程式中加入上述安全讀取功能")
    return handler_code

if __name__ == "__main__":
    # 測試安全讀取功能
    handler = ExcelFileHandler()
    
    test_path = "/Users/ben_kuo/skinbar_report/skinbar202506.xlsx"
    print(f"🧪 測試安全讀取: {test_path}")
    
    try:
        # 嘗試讀取檔案的工作表資訊
        xl_file = pd.ExcelFile(test_path)
        print(f"✅ 成功讀取，工作表: {xl_file.sheet_names[:5]}")
    except Exception as e:
        print(f"❌ 讀取失敗: {e}")
        
        # 嘗試使用安全讀取方法
        try:
            data = handler.safe_read_excel(test_path, sheet_name=None, nrows=1)
            print(f"✅ 安全讀取成功，找到 {len(data)} 個工作表")
        except Exception as safe_error:
            print(f"❌ 安全讀取也失敗: {safe_error}")
    
    # 提供程式碼更新建議
    update_code = update_salary_calculator()
    print("\n" + "="*60)
    print("建議的程式碼更新:")
    print(update_code)
