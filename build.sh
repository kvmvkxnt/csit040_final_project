#!/usr/bin/env bash

set -e
set -o pipefail

APP_NAME="MallAnalyzer"
ENTRY="main.py"

# PyInstaller options common to all platforms
COMMON_OPTS="--hidden-import=sklearn.utils._cython_blas \
--hidden-import=sklearn.neighbors._quad_tree \
--hidden-import=sklearn.neighbors._kd_tree \
--hidden-import=sklearn.tree._criterion \
--hidden-import=sklearn.tree._splitter \
--hidden-import=sklearn.tree._tree \
--exclude-module=seaborn \
--exclude-module=matplotlib.tests \
--exclude-module=tkinter \
--exclude-module=pandas.tests \
--exclude-module=PyQt5.QtWebEngineWidgets \
--exclude-module=PyQt5.QtWebEngineCore \
--exclude-module=PyQt5.QtWebEngine \
--exclude-module=PyQt5.QtQml \
--exclude-module=PyQt5.QtQuick \
--exclude-module=bs4 \
--exclude-module=IPython \
--exclude-module=notebook \
--exclude-module=zmq \
--noconfirm \
--clean \
--windowed \
--noupx \
--log-level=INFO \
--optimize=2"

# Detect OS
OS_TYPE="$(uname -s | tr '[:upper:]' '[:lower:]')"
echo "Detected OS: $OS_TYPE"

case "$OS_TYPE" in
darwin*)
  echo "Building for macOS (.app, --onedir)"
  pyinstaller $COMMON_OPTS --onedir --name "$APP_NAME" "$ENTRY"
  ;;
linux* | mingw* | cygwin* | msys*)
  echo "Building for Linux/Windows (--onefile)"
  pyinstaller $COMMON_OPTS --onefile --name "$APP_NAME" "$ENTRY"
  ;;
*)
  echo "Unsupported OS: $OS_TYPE"
  exit 1
  ;;
esac

echo "Build completed!"
