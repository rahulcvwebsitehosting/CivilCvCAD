# SPDX-License-Identifier: LGPL-2.1-or-later

################################################################################
#                                                                              #
#   © 2026 Billy Huddleston <billy@ivdc.com>                                   #
#                                                                              #
#   CivilCvCAD is free software: you can redistribute it and/or modify            #
#   it under the terms of the GNU Lesser General Public License as             #
#   published by the Free Software Foundation, either version 2.1              #
#   of the License, or (at your option) any later version.                     #
#                                                                              #
#   CivilCvCAD is distributed in the hope that it will be useful,                 #
#   but WITHOUT ANY WARRANTY; without even the implied warranty                #
#   of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                    #
#   See the GNU Lesser General Public License for more details.                #
#                                                                              #
#   You should have received a copy of the GNU Lesser General Public           #
#   License along with CivilCvCAD. If not, see https://www.gnu.org/licenses       #
#                                                                              #
################################################################################

import CivilCvCAD
from typing import Tuple, Mapping
from .base import ToolBitShape


class ToolBitShapeTaperedBallNose(ToolBitShape):
    name: str = "TaperedBallNose"

    @classmethod
    def schema(cls) -> Mapping[str, Tuple[str, str]]:
        return {
            "CuttingEdgeHeight": (
                CivilCvCAD.Qt.translate("ToolBitShape", "Cutting edge height"),
                "App::PropertyLength",
            ),
            "Diameter": (
                CivilCvCAD.Qt.translate("ToolBitShape", "Diameter"),
                "App::PropertyLength",
            ),
            "Flutes": (
                CivilCvCAD.Qt.translate("ToolBitShape", "Flutes"),
                "App::PropertyInteger",
            ),
            "Length": (
                CivilCvCAD.Qt.translate("ToolBitShape", "Overall tool length"),
                "App::PropertyLength",
            ),
            "ShankDiameter": (
                CivilCvCAD.Qt.translate("ToolBitShape", "Shank diameter"),
                "App::PropertyLength",
            ),
            "TaperAngle": (
                CivilCvCAD.Qt.translate("ToolBitShape", "Included Taper angle"),
                "App::PropertyAngle",
            ),
            "TaperDiameter": (
                CivilCvCAD.Qt.translate("ToolBitShape", "Diameter at top of Taper"),
                "App::PropertyLength",
            ),
        }

    @property
    def label(self) -> str:
        return CivilCvCAD.Qt.translate("ToolBitShape", "Tapered Ball Nose")
