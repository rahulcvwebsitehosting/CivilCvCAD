# ADAPTED FOR CIVILCVCAD FROM VTK'S vtkQt.cmake
# ORIGINAL VTK COPYRIGHT NOTICE FOLLOWS (BSD 3-CLAUSE)
#
# /*=========================================================================
#
#   Program:   Visualization Toolkit
#   Module:    Copyright.txt
#
# Copyright (c) 1993-2015 Ken Martin, Will Schroeder, Bill Lorensen
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  * Neither name of Ken Martin, Will Schroeder, or Bill Lorensen nor the names
#    of any contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHORS OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# =========================================================================*/


# CIVILCVCAD_QT_VERSION is used to choose between Qt5 and Qt6.

# If it is set to Auto(default), CivilCvCAD finds and uses the
# version installed on the system. If both versions are
# found, Qt6 is preferred.

# The output variable is CIVILCVCAD_QT_MAJOR_VERSION, which will be either 5 or 6

macro(ChooseQtVersion)
  set(civilcvcad_supported_qt_versions "Auto" 5 6)

  # The following `if` check can be removed once CMake 3.21 is required and
  # the policy CMP0126 is set to NEW.
  if (NOT DEFINED CIVILCVCAD_QT_VERSION)
    set(CIVILCVCAD_QT_VERSION "Auto" CACHE
      STRING "Expected Qt major version. Valid values are Auto, 5, 6.")
    set_property(CACHE CIVILCVCAD_QT_VERSION PROPERTY STRINGS "${civilcvcad_supported_qt_versions}")
  endif()

  if(CIVILCVCAD_LIBPACK_USE)
    find_file(CIVILCVCAD_LIBPACK_CHECKFILE_VERSION NAMES CIVILCVCAD_LIBPACK_VERSION PATHS ${CIVILCVCAD_LIBPACK_DIR} NO_DEFAULT_PATH)
    if(CIVILCVCAD_LIBPACK_CHECKFILE_VERSION)
      file(READ ${CIVILCVCAD_LIBPACK_CHECKFILE_VERSION} CIVILCVCAD_LIBPACK_VERSION)
      message(STATUS "LibPack: read version file and got ${CIVILCVCAD_LIBPACK_VERSION}")
      if(CIVILCVCAD_LIBPACK_VERSION VERSION_GREATER_EQUAL "3.0.0")
        message(STATUS "Using Qt6 directory from LibPack in ${CIVILCVCAD_LIBPACK_DIR}/lib/cmake/Qt6")
        set(Qt6_DIR ${CIVILCVCAD_LIBPACK_DIR}/lib/cmake/Qt6)
        set(CIVILCVCAD_QT_VERSION 6)
      else()
        message(ERROR ": Unrecognized LibPack version ${CIVILCVCAD_LIBPACK_CHECKFILE_VERSION}")
      endif()
    else()
      if (NOT Qt5_DIR OR Qt5_DIR STREQUAL "Qt5_DIR-NOTFOUND")
        message(STATUS "Using Qt5 directory from LibPack in ${CIVILCVCAD_LIBPACK_DIR}/lib/cmake/Qt5")
        set(Qt5_DIR ${CIVILCVCAD_LIBPACK_DIR}/lib/cmake/Qt5)
      endif()
    endif()
  endif()

  if (NOT CIVILCVCAD_QT_VERSION STREQUAL "Auto")
    if (NOT CIVILCVCAD_QT_VERSION IN_LIST civilcvcad_supported_qt_versions)
      message(FATAL_ERROR
        "Supported Qt versions are \"${civilcvcad_supported_qt_versions}\". But "
        "CIVILCVCAD_QT_VERSION is set to ${CIVILCVCAD_QT_VERSION}.")
    endif ()
    set(_CIVILCVCAD_QT_VERSION "${CIVILCVCAD_QT_VERSION}")
  else ()
    find_package(Qt6 QUIET COMPONENTS Core)
    set(_CIVILCVCAD_QT_VERSION 6)
    if (NOT Qt6_FOUND)
      find_package(Qt5 QUIET COMPONENTS Core)
      if (NOT Qt5_FOUND)
        message(FATAL_ERROR
          "Could not find a valid Qt installation. Consider setting Qt5_DIR or Qt6_DIR (as needed).")
      endif ()
      set(_CIVILCVCAD_QT_VERSION 5)
    endif ()
  endif ()
  set(CIVILCVCAD_QT_MAJOR_VERSION "${_CIVILCVCAD_QT_VERSION}" CACHE INTERNAL
    "Major version number for the Qt installation used.")
  message(STATUS  "Compiling with Qt ${CIVILCVCAD_QT_MAJOR_VERSION}")
endmacro()
