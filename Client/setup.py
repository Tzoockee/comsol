from distutils.core import setup
import py2exe
import sys
sys.path.append("..\\Shared\\")

setup(
    options = {
        "py2exe": {
            "dll_excludes": ["MSVCP90.dll"],
            'includes': 'decimal'
        }
    },
    windows=['client_ui.py'])