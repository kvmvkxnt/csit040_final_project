# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['sklearn.utils._cython_blas', 'sklearn.utils._cython_blas', 'sklearn.neighbors._quad_tree', 'sklearn.neighbors._kd_tree', 'sklearn.tree._criterion', 'sklearn.tree._splitter', 'sklearn.tree._tree'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["seaborn", "matplotlib.tests", "tkinter", "pandas.tests", "PyQt5.QtWebEngineWidgets","PyQt5.QtWebEngineCore", "PyQt5.QtWebEngine", "PyQt5.QtQml", "PyQt5.QtQuick", "bs4", "IPython", "notebook", "zmq"],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    exclude_binaries=True,
    name='MallAnalyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='MallAnalyzer',
)
app = BUNDLE(
    coll,
    name='MallAnalyzer.app',
    icon=None,
    bundle_identifier=None,
)
