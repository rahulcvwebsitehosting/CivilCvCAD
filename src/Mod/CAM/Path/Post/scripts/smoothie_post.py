# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2017 sliptonic <shopinthewoods@gmail.com>               *
# *                                                                         *
# *   This file is part of the CivilCvCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   CivilCvCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Lesser General Public License for more details.                   *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with CivilCvCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

import os
import sys
from typing import Any, Dict, Optional

from Path.Post.Processor import PostProcessor

import Path
import CivilCvCAD

translate = CivilCvCAD.Qt.translate

DEBUG = False
if DEBUG:
    Path.Log.setLevel(Path.Log.Level.DEBUG, Path.Log.thisModule())
    Path.Log.trackModule(Path.Log.thisModule())
else:
    Path.Log.setLevel(Path.Log.Level.INFO, Path.Log.thisModule())

#
# Define some types that are used throughout this file.
#
Values = Dict[str, Any]

POST_TYPE = "machine"


class Smoothie(PostProcessor):
    """
    The SmoothieBoard post processor class.

    This postprocessor outputs G-code suitable for SmoothieBoard controllers.
        Network upload is disabled in this offline-only distribution.
    """

    def __init__(
        self,
        job,
        tooltip=translate("CAM", "Refactored SmoothieBoard post processor"),
        tooltipargs=[],
        units="Metric",
    ) -> None:
        super().__init__(
            job=job,
            tooltip=tooltip,
            tooltipargs=tooltipargs,
            units=units,
        )
        Path.Log.debug("Refactored SmoothieBoard post processor initialized.")
        self.ip_addr: Optional[str] = None
        self.verbose: bool = False

    def init_values(self, values: Values) -> None:
        """Initialize values that are used throughout the postprocessor."""
        #
        super().init_values(values)
        #
        # Set any values here that need to override the default values set
        # in the parent routine.
        #
        # The order of parameters.
        # SmoothieBoard doesn't want K properties on XY plane (like LinuxCNC).
        #
        values["PARAMETER_ORDER"] = [
            "X",
            "Y",
            "Z",
            "A",
            "B",
            "I",
            "J",
            "F",
            "S",
            "T",
            "Q",
            "R",
            "L",
        ]
        #
        # Used in the argparser code as the "name" of the postprocessor program.
        #
        values["MACHINE_NAME"] = "SmoothieBoard"
        #
        # Any commands in this value will be output as the last commands
        # in the G-code file.
        #
        values["POSTAMBLE"] = """M05
G17 G90
M2"""
        values["POSTPROCESSOR_FILE_NAME"] = __name__
        #
        # Any commands in this value will be output after the header and
        # safety block at the beginning of the G-code file.
        #
        values["PREAMBLE"] = """G17 G90"""

    def init_arguments(self, values, argument_defaults, arguments_visible):
        """Initialize local-file postprocessing arguments."""
        return super().init_arguments(values, argument_defaults, arguments_visible)

    def process_arguments(self):
        """Process local-file postprocessing arguments."""
        return super().process_arguments()

    def export(self):
        """Export G-code to a local file."""
        return super().export()

    def remote_post(self, gcode_sections):
        """Reject SmoothieBoard network upload in offline-only builds."""
        CivilCvCAD.Console.PrintError("Network posting is disabled in offline-only CivilCvCAD.\n")
        return
        # Check if remote posting is enabled and IP address is specified
        if self.values.get("REMOTE_POST", False) and self.ip_addr:
            # Combine all G-code sections
            gcode = ""
            for section_name, section_gcode in gcode_sections:
                if section_gcode:
                    gcode += section_gcode

            # Get the output filename from the job
            filename = self._job.PostProcessorOutputFile
            if not filename or filename == "-":
                filename = "output.nc"

            self._send_to_smoothie(self.ip_addr, gcode, filename)

    def _send_to_smoothie(self, ip: str, gcode: str, fname: str) -> None:
        """
        Disabled legacy remote-posting entry point.

        Args:
            ip: IP address of the SmoothieBoard
            gcode: G-code string to send
            fname: Filename to use on the SmoothieBoard SD card
        """
        CivilCvCAD.Console.PrintError("Network posting is disabled in offline-only CivilCvCAD.\n")
        return

        fname = os.path.basename(fname)
        CivilCvCAD.Console.PrintMessage(f"Sending to SmoothieBoard: {fname}\n")

        gcode = gcode.rstrip()
        filesize = len(gcode)

        try:
            # Make connection to SmoothieBoard SFTP server (port 115)
            s = None
            s.settimeout(4.0)
            s.connect((ip, 115))
            tn = s.makefile(mode="rw")

            # Read startup prompt
            ln = tn.readline()
            if not ln.startswith("+"):
                CivilCvCAD.Console.PrintError(f"Failed to connect with SFTP: {ln}\n")
                return

            if self.verbose:
                print("RSP: " + ln.strip())

            # Issue initial store command
            tn.write(f"STOR OLD /sd/{fname}\n")
            tn.flush()

            ln = tn.readline()
            if not ln.startswith("+"):
                CivilCvCAD.Console.PrintError(f"Failed to create file: {ln}\n")
                return

            if self.verbose:
                print("RSP: " + ln.strip())

            # Send size of file
            tn.write(f"SIZE {filesize}\n")
            tn.flush()

            ln = tn.readline()
            if not ln.startswith("+"):
                CivilCvCAD.Console.PrintError(f"Failed: {ln}\n")
                return

            if self.verbose:
                print("RSP: " + ln.strip())

            # Now send file
            cnt = 0
            for line in gcode.splitlines(True):
                tn.write(line)
                if self.verbose:
                    cnt += len(line)
                    print("SND: " + line.strip())
                    print(f"{cnt}/{filesize}\r", end="")

            tn.flush()

            ln = tn.readline()
            if not ln.startswith("+"):
                CivilCvCAD.Console.PrintError(f"Failed to save file: {ln}\n")
                return

            if self.verbose:
                print("RSP: " + ln.strip())

            # Exit
            tn.write("DONE\n")
            tn.flush()
            tn.close()

            CivilCvCAD.Console.PrintMessage("Upload complete\n")

        except TimeoutError:
            CivilCvCAD.Console.PrintError(f"Connection timeout while connecting to {ip}:115\n")
        except ConnectionRefusedError:
            CivilCvCAD.Console.PrintError(
                f"Connection refused by {ip}:115. Is the SmoothieBoard running?\n"
            )
        except Exception as e:
            CivilCvCAD.Console.PrintError(f"Error sending to SmoothieBoard: {str(e)}\n")

    @property
    def tooltip(self):
        tooltip: str = """
        This is a postprocessor file for the CAM workbench.
        It is used to take a pseudo-gcode fragment from a CAM object
        and output 'real' GCode suitable for a SmoothieBoard controller.

        This offline-only postprocessor writes G-code to local files.
        """
        return tooltip
