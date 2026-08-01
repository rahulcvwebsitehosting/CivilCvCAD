# SPDX-License-Identifier: LGPL-2.1-or-later

# this directory is the entry point for namespace modules. Any package
# installed to a directory "civilcvcad" which is in sys.path can be imported
# with "from civilcvcad import package" and is checked for a init_gui.py
# module, which is imported at startup. (CivilCvCADGuiInit.py)

add_subdirectory(civilcvcad)