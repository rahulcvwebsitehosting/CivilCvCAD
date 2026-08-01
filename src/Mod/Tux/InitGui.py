# SPDX-License-Identifier: LGPL-2.1-or-later

# Tux module for CivilCvCAD
# Copyright (C) 2017  triplus @ FreeCAD
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

"""Tux module for CivilCvCAD."""

p = CivilCvCAD.ParamGet("User parameter:Tux")


# Navigation indicator
if p.GetGroup("NavigationIndicator").GetBool("Enabled", 1):
    import NavigationIndicatorGui
else:
    pass


# Persistent toolbars
if p.GetGroup("PersistentToolbars").GetBool("Enabled", 1):
    import PersistentToolbarsGui
else:
    pass

# Temporary - for CivilCvCAD v1.0
# Detect a possible clash between the built-in BIM WB in v1.0
# and the BIM addon. Resolve this by renaming the BIM add-on path
try:
    import Arch_rc

    # we could import Arch_rc, nothing to be done, either we are
    # running built-in BIM without the addon, or the addon without built-in BIM
except:
    # Arch_rc not importable: We have both the BIM addon and the built-in BIM
    from pathlib import Path
    import CivilCvCAD

    bim_modpath = Path(CivilCvCAD.getUserAppDataDir(), "Mod", "BIM")
    try:
        bim_modpath.rename(bim_modpath.with_name("BIM021"))
    except FileNotFoundError:
        pass
    else:
        CivilCvCAD.Console.PrintWarning(
            "BIM addon path has been renamed to BIM021 to avoid conflicts with the builtin BIM workbench. Please restart CivilCvCAD\n"
        )
