# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller: icono opcional en ``assets/icon.ico`` (misma convención que gen-dni-esp).

Mantener alineada la versión con ``APP_VERSION`` en ``src/config.py``.

Ejecutar: python -m PyInstaller GenCardNumb.spec
"""
import os

_root = os.path.dirname(os.path.abspath(SPEC))
_assets_ico = os.path.join(_root, "assets", "icon.ico")
_assets_png = os.path.join(_root, "assets", "icon.png")

_exe_icon = os.path.abspath(_assets_ico) if os.path.isfile(_assets_ico) else None

_datas = []
if os.path.isfile(_assets_ico):
    _datas.append((os.path.abspath(_assets_ico), "assets"))
if os.path.isfile(_assets_png):
    _datas.append((os.path.abspath(_assets_png), "assets"))

a = Analysis(
    ["src\\main.py"],
    pathex=[_root],
    binaries=[],
    datas=_datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="GenCardNumb",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=_exe_icon,
)
