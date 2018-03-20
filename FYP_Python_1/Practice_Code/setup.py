"""Implementing cx_Freeze to make a tkinter app into an executable"""

import cx_Freeze
import sys
import matplotlib

### This code tries to correct cx_Freeze looking in the wrong directory for mpl-data
import cx_Freeze.hooks  
def hack(finder, module):
    return
cx_Freeze.hooks.load_matplotlib = hack

from cx_Freeze import setup, Executable


base = None

if sys.platform == "win32":
    base = "Win32GUI"

executables = [cx_Freeze.Executable("tkinter_practice_8.py", base=base)]

build_options_dict = {"packages":["tkinter","matplotlib"],
                      "include_files":[(matplotlib.get_data_path(),"mpl-data")],
                      "includes":["numpy.core._methods", "numpy.lib.format"]
                      }
                                       
                        

cx_Freeze.setup(
    name = "SeaofBTC-Client",
    options = {"build_exe":build_options_dict},
    version = "0.01",
    description = "Sea of BTC Trading",
    executables = executables
    )
