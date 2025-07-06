# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

block_cipher = None

# 獲取當前目錄
current_dir = Path.cwd()

a = Analysis(
    ['standalone_main.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=[
        ('auto_salary_calculator.py', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'xlrd',
        'numpy',
        'pandas._libs.tslibs.timedeltas',
        'pandas._libs.tslibs.np_datetime',
        'pandas._libs.tslibs.nattype',
        'pandas._libs.properties',
        'pandas._libs.testing',
        'pandas._libs.tslibs.offsets',
        'pandas._libs.tslibs.parsing',
        'pandas._libs.tslibs.period',
        'pandas._libs.tslibs.timestamps',
        'pandas._libs.parsers',
        'pandas._libs.writers',
        'pandas.io.formats.format',
        'pandas.io.common',
        'pandas.io.excel._base',
        'openpyxl.chart',
        'openpyxl.styles',
        'openpyxl.worksheet',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='淨膚寶薪資計算程式',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
