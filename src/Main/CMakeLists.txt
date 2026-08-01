# SPDX-License-Identifier: LGPL-2.1-or-later

configure_file(civilcvcad.rc.cmake ${CMAKE_CURRENT_BINARY_DIR}/civilcvcad.rc)
configure_file(civilcvcadCmd.rc.cmake ${CMAKE_CURRENT_BINARY_DIR}/civilcvcadCmd.rc)
file(COPY icon.ico DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

######################## CivilCvCADMain ########################
if(BUILD_GUI)

    SET(CivilCvCAD_SRCS
        ${CMAKE_CURRENT_BINARY_DIR}/civilcvcad.rc
        icon.ico
        MainGui.cpp
    )

    SET(CivilCvCAD_LIBS
        CivilCvCADGui
    )

    if(NOT BUILD_DYNAMIC_LINK_PYTHON)
        # executables have to be linked against python libraries,
        # because extension modules are not.
        list(APPEND CivilCvCAD_LIBS
            ${Python3_LIBRARIES}
        )
    endif(NOT BUILD_DYNAMIC_LINK_PYTHON)

    add_executable(CivilCvCADMain WIN32 ${CivilCvCAD_SRCS})
    target_link_libraries(CivilCvCADMain ${CivilCvCAD_LIBS})
    if(BUILD_TEST)
        add_dependencies(CivilCvCADMain TestSources)
        add_dependencies(CivilCvCADMain TestGuiSources)
    endif()
    if (CIVILCVCAD_WARN_ERROR)
        target_compile_warn_error(CivilCvCADMain)
    endif()

    SET_BIN_DIR(CivilCvCADMain CivilCvCAD)

    if(WIN32)
        INSTALL(TARGETS CivilCvCADMain
            RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
            LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        )
    elseif(APPLE AND NOT BUILD_WITH_CONDA)
        INSTALL(TARGETS CivilCvCADMain
        RUNTIME DESTINATION MacOS
            LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        )
    else()
        INSTALL(TARGETS CivilCvCADMain
            RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        )
    endif()
endif(BUILD_GUI)
######################## CivilCvCADMainCmd ########################

SET(CivilCvCADMainCmd_SRCS
    ${CMAKE_CURRENT_BINARY_DIR}/civilcvcadCmd.rc
    icon.ico
    MainCmd.cpp
)

add_executable(CivilCvCADMainCmd ${CivilCvCADMainCmd_SRCS})
if(BUILD_TEST)
    add_dependencies(CivilCvCADMainCmd TestSources)
endif()

SET(CivilCvCADMainCmd_LIBS
    CivilCvCADApp
    ${QtCore_LIBRARIES}
    ${QtXml_LIBRARIES}
)

if(NOT BUILD_DYNAMIC_LINK_PYTHON)
    # executables have to be linked against python libraries,
    # because extension modules are not.
    list(APPEND CivilCvCADMainCmd_LIBS
        ${Python3_LIBRARIES}
    )
endif(NOT BUILD_DYNAMIC_LINK_PYTHON)

target_link_libraries(CivilCvCADMainCmd
    ${CivilCvCADMainCmd_LIBS}
)
if (CIVILCVCAD_WARN_ERROR)
    target_compile_warn_error(CivilCvCADMainCmd)
endif()

SET_BIN_DIR(CivilCvCADMainCmd CivilCvCADCmd)

if(WIN32)
    INSTALL(TARGETS CivilCvCADMainCmd
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )
elseif(APPLE AND NOT BUILD_WITH_CONDA)
    INSTALL(TARGETS CivilCvCADMainCmd
        RUNTIME DESTINATION MacOS
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )
else()
    INSTALL(TARGETS CivilCvCADMainCmd
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    )
endif()

######################## CivilCvCADMainPy ########################

SET(CivilCvCADMainPy_SRCS
    MainPy.cpp
)

add_library(CivilCvCADMainPy SHARED ${CivilCvCADMainPy_SRCS})

target_link_libraries(CivilCvCADMainPy CivilCvCADApp)
if (CIVILCVCAD_WARN_ERROR)
    target_compile_warn_error(CivilCvCADMainPy)
endif()

SET_BIN_DIR(CivilCvCADMainPy CivilCvCAD)
SET_PYTHON_PREFIX_SUFFIX(CivilCvCADMainPy)

if(WIN32)
    INSTALL(TARGETS CivilCvCADMainPy
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )
else(WIN32)
    INSTALL(TARGETS CivilCvCADMainPy
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )
endif(WIN32)

######################## CivilCvCADGuiPy ########################
if(BUILD_GUI)

    SET(CivilCvCADGuiPy_SRCS
        CivilCvCADGuiPy.cpp
    )

    add_library(CivilCvCADGuiPy SHARED ${CivilCvCADGuiPy_SRCS})

    target_link_libraries(CivilCvCADGuiPy CivilCvCADGui)
    if (CIVILCVCAD_WARN_ERROR)
        target_compile_warn_error(CivilCvCADGuiPy)
    endif()

    SET_BIN_DIR(CivilCvCADGuiPy CivilCvCADGui)
    SET_PYTHON_PREFIX_SUFFIX(CivilCvCADGuiPy)
    if(WIN32)
        # Name clash with target "CivilCvCADGui"
        # Must be called "CivilCvCADGuiPy_d" and "CivilCvCADGuiPy" to work so override default
        set_target_properties(CivilCvCADGuiPy PROPERTIES PDB_NAME_DEBUG "CivilCvCADGuiPy_d")
        set_target_properties(CivilCvCADGuiPy PROPERTIES PDB_NAME_RELEASE "CivilCvCADGuiPy")
    endif(WIN32)

    if(WIN32)
        INSTALL(TARGETS CivilCvCADGuiPy
            RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
            LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        )
    else(WIN32)
        INSTALL(TARGETS CivilCvCADGuiPy
            LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        )
    endif(WIN32)
endif(BUILD_GUI)
