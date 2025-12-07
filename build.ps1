$ErrorActionPreference = "Stop"

$APP_NAME = "MallAnalyzer"
$ENTRY = "main.py"

$COMMON_OPTS = @(
    "--hidden-import=sklearn.utils._cython_blas"
    "--hidden-import=sklearn.neighbors._quad_tree"
    "--hidden-import=sklearn.neighbors._kd_tree"
    "--hidden-import=sklearn.tree._criterion"
    "--hidden-import=sklearn.tree._splitter"
    "--hidden-import=sklearn.tree._tree"
    "--exclude-module=seaborn"
    "--exclude-module=matplotlib.tests"
    "--exclude-module=tkinter"
    "--exclude-module=pandas.tests"
    "--exclude-module=PyQt5.QtWebEngineWidgets"
    "--exclude-module=PyQt5.QtWebEngineCore"
    "--exclude-module=PyQt5.QtWebEngine"
    "--exclude-module=PyQt5.QtQml"
    "--exclude-module=PyQt5.QtQuick"
    "--exclude-module=bs4"
    "--exclude-module=IPython"
    "--exclude-module=notebook"
    "--exclude-module=zmq"
    "--noconfirm"
    "--clean"
    "--windowed"
    "--noupx"
    "--log-level=INFO"
    "--optimize=2"
)

Write-Host "Building $APP_NAME for Windows..." -ForegroundColor Cyan

$BUILD_MODE = "--onefile"

pyinstaller @COMMON_OPTS $BUILD_MODE --name $APP_NAME $ENTRY

Write-Host "Build completed!" -ForegroundColor Green
