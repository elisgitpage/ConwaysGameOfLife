import cx_Freeze
import os.path

executables = [cx_Freeze.Executable("Basic_Game.py")]

os.environ['TCL_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tcl\\tk8.6"
cx_Freeze.setup(
    name = "Conway's Game of Life",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":[
                               "CGOL_Icon.png",
                           ],
                           },
             },
    executables = executables

)