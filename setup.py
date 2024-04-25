import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name = "ITAwer_Defense",
    options = {'build_exe': {'packages':['pygame'],
                             'include_files': ['assets']}},
    executables = executables
)