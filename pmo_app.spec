# pmo_app.spec  —  PyInstaller build specification for PMO Portfolio Manager
# Run locally:  pyinstaller pmo_app.spec --noconfirm --clean

import sys
import os
from PyInstaller.utils.hooks import (
    collect_data_files,
    collect_submodules,
    collect_dynamic_libs,
)

block_cipher = None
app_root = os.path.abspath(".")

# ── NumPy: must use collect_all to get .pyd C-extensions + DLLs ─────────────
# Plain hiddenimports is NOT enough — PyInstaller misses the compiled .pyd
# files that numpy loads at runtime (numpy.core._multiarray_umath, etc.)
from PyInstaller.utils.hooks import collect_all
numpy_datas,    numpy_binaries,    numpy_hiddens    = collect_all("numpy")
pandas_datas,   pandas_binaries,   pandas_hiddens   = collect_all("pandas")
mpl_datas,      mpl_binaries,      mpl_hiddens      = collect_all("matplotlib")
openpyxl_datas, openpyxl_binaries, openpyxl_hiddens = collect_all("openpyxl")
pyside6_datas,  pyside6_binaries,  pyside6_hiddens  = collect_all("PySide6")

a = Analysis(
    ["main.py"],
    pathex=[app_root],
    binaries=[
        # ── NumPy compiled C-extensions (the #1 cause of the crash) ──────────
        *numpy_binaries,
        *pandas_binaries,
        *mpl_binaries,
        *openpyxl_binaries,
        *pyside6_binaries,
    ],
    datas=[
        # App assets
        ("icons", "icons"),
        # Package data files
        *numpy_datas,
        *pandas_datas,
        *mpl_datas,
        *openpyxl_datas,
        *pyside6_datas,
    ],
    hiddenimports=[
        # ── NumPy internals (critical) ────────────────────────────────────────
        *numpy_hiddens,
        "numpy",
        "numpy.core",
        "numpy.core._multiarray_umath",
        "numpy.core._multiarray_tests",
        "numpy.core.multiarray",
        "numpy.core.numeric",
        "numpy.core._dtype_ctypes",
        "numpy.lib",
        "numpy.lib.stride_tricks",
        "numpy.linalg",
        "numpy.fft",
        "numpy.random",
        "numpy.polynomial",
        # ── Pandas internals ─────────────────────────────────────────────────
        *pandas_hiddens,
        "pandas",
        "pandas._libs",
        "pandas._libs.lib",
        "pandas._libs.tslibs",
        "pandas._libs.tslibs.np_datetime",
        "pandas._libs.tslibs.nattype",
        "pandas._libs.tslibs.timezones",
        "pandas._libs.tslibs.timestamps",
        "pandas._libs.tslibs.offsets",
        "pandas.io.formats.style",
        "pandas.core.arrays.masked",
        "pandas.core.arrays.boolean",
        "pandas.core.arrays.integer",
        "pandas.core.arrays.floating",
        "pandas.io.excel._openpyxl",
        # ── Matplotlib ───────────────────────────────────────────────────────
        *mpl_hiddens,
        "matplotlib.backends.backend_qtagg",
        "matplotlib.backends.backend_agg",
        "matplotlib.backends.backend_pdf",
        "matplotlib.backends.backend_svg",
        "matplotlib.rcsetup",
        "matplotlib._api",
        "matplotlib._fontconfig_pattern",
        "matplotlib._version",
        "matplotlib.docstring",
        "matplotlib.cbook",
        "matplotlib.colors",
        "matplotlib.font_manager",
        "matplotlib.dviread",
        "matplotlib.mathtext",
        "matplotlib.texmanager",
        "matplotlib.tight_layout",
        # ── openpyxl ─────────────────────────────────────────────────────────
        *openpyxl_hiddens,
        "openpyxl",
        "openpyxl.cell._writer",
        "openpyxl.styles",
        "openpyxl.utils",
        # ── PySide6 ──────────────────────────────────────────────────────────
        *pyside6_hiddens,
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "PySide6.QtSvg",
        "PySide6.QtSvgWidgets",
        "PySide6.QtPrintSupport",
        # ── ReportLab (lazy-imported in export_service.py) ────────────────────
        "reportlab",
        "reportlab.lib.pagesizes",
        "reportlab.lib.colors",
        "reportlab.lib.styles",
        "reportlab.lib.units",
        "reportlab.platypus",
        "reportlab.pdfgen",
        "reportlab.pdfgen.canvas",
        # ── App modules ───────────────────────────────────────────────────────
        "app",
        "app.database", "app.database.db_manager",
        "app.models",   "app.models.project_model", "app.models.auth_model",
        "app.services", "app.services.excel_import", "app.services.export_service",
        "app.utils",    "app.utils.theme", "app.utils.widgets",
        "app.ui",
        "app.ui.login_window", "app.ui.login_bg",
        "app.ui.main_window",  "app.ui.dashboard_view",
        "app.ui.project_list_view", "app.ui.project_detail_view",
        "app.ui.kpi_view",     "app.ui.forms",
        "app.ui.account_view", "app.ui.import_view",
        "app.ui.reports_view", "app.ui.rar_tab",
        "app.ui.transport_tab","app.ui.prpo_tab",
        "app.ui.gantt_view",   "app.ui.gantt_planning_view",
        # ── Stdlib sometimes missed ───────────────────────────────────────────
        "sqlite3", "hashlib", "hmac", "math", "pathlib",
        "datetime", "decimal", "fractions", "statistics",
        # unittest is needed by matplotlib.rcsetup internally
        "unittest", "unittest.mock",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Keep the bundle lean — none of these are used by the app
        # NOTE: do NOT exclude unittest/test — matplotlib imports them internally
        "tkinter", "_tkinter",
        "distutils", "setuptools", "pip",
        "IPython", "jupyter", "notebook",
        "scipy",
        "sklearn",
        "wx", "gtk",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PMO_Suite",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    # ── UPX: compress everything EXCEPT DLLs that break when compressed ──────
    upx=True,
    upx_exclude=[
        "vcruntime140.dll",
        "vcruntime140_1.dll",
        "msvcp140.dll",
        "python3*.dll",
        "Qt6*.dll",
        # NumPy DLLs must NOT be UPX-compressed
        "_multiarray_umath*.pyd",
        "numpy*.dll",
    ],
    console=False,                 # no black terminal window on launch
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="icons/pmo_app.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[
        "vcruntime140.dll",
        "vcruntime140_1.dll",
        "msvcp140.dll",
        "python3*.dll",
        "Qt6*.dll",
        "_multiarray_umath*.pyd",
        "numpy*.dll",
    ],
    name="PMO_Suite",
)
