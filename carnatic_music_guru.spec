# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

data_folders = [('carnatic/config','carnatic/config'),
				('carnatic/Notes','carnatic/Notes'),
				('carnatic/Lib','carnatic/Lib'), 
				('carnatic/model_weights','carnatic/model_weights'), 
				('carnatic/images','carnatic/images'), 
				('carnatic/lang','carnatic/lang'),
				('carnatic/Lessons','carnatic/Lessons'), 
				('carnatic/tmp','carnatic/tmp')]

a = Analysis(
    ['cli.py'],
    pathex=[],
    binaries=[],
    datas=data_folders,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pytest','sqlalchemy','matplotlib','tkinter'],
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
    name='carnatic_music_guru',
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
)
