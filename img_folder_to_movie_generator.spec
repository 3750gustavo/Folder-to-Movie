# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['img folder to movie generator.py'],
    pathex=[
        '.',
        './translations',
        './package_manager.py'],
    binaries=[],
    datas=[
        ('translations/*', 'translations'),  # Include all files from the translations folder
        ('package_manager.py', '.')  # Include package_manager.py in the root of the executable
    ],
    hiddenimports=[],
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
    name='img_folder_to_movie_generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)