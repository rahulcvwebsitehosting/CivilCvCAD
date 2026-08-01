# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the CivilCvCAD project.

#--------------------------------------------------------------------------
#   Copyright (c) 2026 Chris Jones github.com/ipatch                      *
#                                                                         *
#   This file is part of the CivilCvCAD CAx development system.              *
#                                                                         *
#   This program is free software; you can redistribute it and/or modify  *
#   it under the terms of the GNU Library General Public License (LGPL)   *
#   as published by the Free Software Foundation; either version 2 of     *
#   the License, or (at your option) any later version.                   *
#   for detail see the LICENCE text file.                                 *
#                                                                         *
#   CivilCvCAD is distributed in the hope that it will be useful,            *
#   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#   GNU Library General Public License for more details.                  *
#                                                                         *
#   You should have received a copy of the GNU Library General Public     *
#   License along with CivilCvCAD; if not, write to the Free Software        *
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#   USA                                                                   *
#                                                                         *
#--------------------------------------------------------------------------

# NOTE: referencing my copy of professional cmake (book) i see the below list of available sanitizers
# 1. AddressSanitizer (ASan) *only supported by Visual Studio
# 2. LeakSanitizer (LSan) *can't be used with (MSan) (TSan)
# 3. MemorySanitizer (MSan)
# 4. ThreadSanitizer (TSan)
# 5. UndefinedBehaviorSanitizer (UBSan) *can be used with all

include(CheckCCompilerFlag)
include(CheckCXXCompilerFlag)

macro(_check_sanitizer_flag flag result)
    set(CMAKE_REQUIRED_LINK_OPTIONS ${flag})
    check_c_compiler_flag(${flag} ${result})
    unset(CMAKE_REQUIRED_LINK_OPTIONS)
    if(NOT ${result})
        message(FATAL_ERROR "Compiler does not support ${flag}")
    endif()
endmacro()

macro(SetupSanitizers)
    if(MSVC)
        if(CIVILCVCAD_USE_SANITIZER_ASAN)
            message(STATUS "Building with AddressSanitizer (ASan)")
            string(REPLACE "/RTC1" "" CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG}")
            string(REPLACE "/RTC1" "" CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")
            add_compile_options(/fsanitize=address /fsanitize-address-use-after-return)
        endif()
    else()
        # Validate incompatible sanitizer combinations
        if(CIVILCVCAD_USE_SANITIZER_ASAN AND (CIVILCVCAD_USE_SANITIZER_MSAN OR CIVILCVCAD_USE_SANITIZER_TSAN))
            message(FATAL_ERROR "ASan cannot be used with MSan or TSan")
        endif()
        # LSan is incompatible with MSan and TSan
        if(CIVILCVCAD_USE_SANITIZER_LSAN AND (CIVILCVCAD_USE_SANITIZER_MSAN OR CIVILCVCAD_USE_SANITIZER_TSAN))
            message(FATAL_ERROR "LSan cannot be used with MSan or TSan")
        endif()
        if(CIVILCVCAD_USE_SANITIZER_TSAN AND CIVILCVCAD_USE_SANITIZER_MSAN)
            message(FATAL_ERROR "TSan and MSan cannot be used together")
        endif()


        # Verify compiler supports requested sanitizers
        if(CIVILCVCAD_USE_SANITIZER_ASAN)
            _check_sanitizer_flag(-fsanitize=address _asan_supported)
        endif()
        if(CIVILCVCAD_USE_SANITIZER_LSAN)
            _check_sanitizer_flag(-fsanitize=leak _lsan_supported)
        endif()
        if(CIVILCVCAD_USE_SANITIZER_MSAN)
            _check_sanitizer_flag(-fsanitize=memory _msan_supported)
        endif()
        if(CIVILCVCAD_USE_SANITIZER_TSAN)
            _check_sanitizer_flag(-fsanitize=thread _tsan_supported)
        endif()
        if(CIVILCVCAD_USE_SANITIZER_UBSAN)
            _check_sanitizer_flag(-fsanitize=undefined _ubsan_supported)
        endif()

        set(_has_sanitizer FALSE)
        if(CIVILCVCAD_USE_SANITIZER_ASAN OR CIVILCVCAD_USE_SANITIZER_LSAN OR CIVILCVCAD_USE_SANITIZER_TSAN
        OR CIVILCVCAD_USE_SANITIZER_UBSAN OR CIVILCVCAD_USE_SANITIZER_MSAN)
            set(_has_sanitizer TRUE)
        endif()


        if(_has_sanitizer)
            if(NOT CMAKE_BUILD_TYPE MATCHES "Debug|RelWithDebInfo")
                message(WARNING "Sanitizers work best with Debug or RelWithDebInfo builds")
            endif()

            set(_sanitizer_flags
                $<$<BOOL:${CIVILCVCAD_USE_SANITIZER_ASAN}>:-fsanitize=address>
                $<$<BOOL:${CIVILCVCAD_USE_SANITIZER_LSAN}>:-fsanitize=leak>
                $<$<BOOL:${CIVILCVCAD_USE_SANITIZER_MSAN}>:-fsanitize=memory>
                $<$<BOOL:${CIVILCVCAD_USE_SANITIZER_TSAN}>:-fsanitize=thread>
                $<$<BOOL:${CIVILCVCAD_USE_SANITIZER_UBSAN}>:-fsanitize=undefined>
            )

            add_compile_options(-fno-omit-frame-pointer ${_sanitizer_flags})
            add_link_options(${_sanitizer_flags})
        endif()
    endif()
endmacro()
