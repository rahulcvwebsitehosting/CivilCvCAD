# SPDX-License-Identifier: LGPL-2.1-or-later

if (PROJECT_NAME)
    set(IS_SUB_PROJECT TRUE)
endif()

if (NOT IS_SUB_PROJECT)
    project(CivilCvCAD_widgets)
    cmake_minimum_required(VERSION 3.2.0)

    set(CMAKE_INCLUDE_CURRENT_DIR ON)
    set(CMAKE_AUTOMOC ON)

    find_package(Qt${CIVILCVCAD_QT_MAJOR_VERSION} COMPONENTS Core Designer Widgets REQUIRED)
endif()

include_directories(
    SYSTEM
    ${Qt${CIVILCVCAD_QT_MAJOR_VERSION}Core_INCLUDE_DIRS}
    ${Qt${CIVILCVCAD_QT_MAJOR_VERSION}Widgets_INCLUDE_DIRS}
    ${Qt${CIVILCVCAD_QT_MAJOR_VERSION}Designer_INCLUDE_DIRS}
)

add_library(CivilCvCAD_widgets SHARED
    customwidgets.cpp
    customwidgets.h
    plugin.cpp
    plugin.h
)

set(CivilCvCAD_widgets_LIBS
    ${Qt${CIVILCVCAD_QT_MAJOR_VERSION}Widgets_LIBRARIES}
    ${Qt${CIVILCVCAD_QT_MAJOR_VERSION}Designer_LIBRARIES}
)

if(MSVC)
    list(APPEND CivilCvCAD_widgets_LIBS
        debug msvcrtd.lib
        debug msvcprtd.lib
        optimized msvcrt.lib
        optimized msvcprt.lib
    )

    #Universal C runtime introduced in VS 2015 (cl version 19)
    if (NOT (CMAKE_CXX_COMPILER_VERSION VERSION_LESS "19"))
        list(APPEND CivilCvCAD_widgets_LIBS
            debug vcruntimed.lib
            debug ucrtd.lib
            debug concrtd.lib
            optimized vcruntime.lib
            optimized ucrt.lib
            optimized concrt.lib
        )
    endif()
endif()

target_link_libraries(CivilCvCAD_widgets PRIVATE ${CivilCvCAD_widgets_LIBS})
target_compile_options(CivilCvCAD_widgets PRIVATE ${COMPILE_OPTIONS})


# Get the install location of a plugin to determine the path to designer plguins
get_target_property(QMAKE_EXECUTABLE Qt${CIVILCVCAD_QT_MAJOR_VERSION}::qmake LOCATION)
execute_process(COMMAND ${QMAKE_EXECUTABLE} "-query" "QT_INSTALL_PLUGINS" RESULT_VARIABLE return_code OUTPUT_VARIABLE DEFAULT_QT_PLUGINS_DIR OUTPUT_STRIP_TRAILING_WHITESPACE)
set(DESIGNER_PLUGIN_LOCATION ${DEFAULT_QT_PLUGINS_DIR}/designer CACHE PATH "Path where the plugin will be installed to")

if (NOT IS_SUB_PROJECT)
    message(STATUS "Plugin will be installed to: ${DESIGNER_PLUGIN_LOCATION}")
else()
    set (libCivilCvCAD_widgets "${CMAKE_SHARED_LIBRARY_PREFIX}CivilCvCAD_widgets${CMAKE_SHARED_LIBRARY_SUFFIX}" PARENT_SCOPE)
endif()


INSTALL(TARGETS CivilCvCAD_widgets
    RUNTIME DESTINATION ${DESIGNER_PLUGIN_LOCATION}
    LIBRARY DESTINATION ${DESIGNER_PLUGIN_LOCATION}
)
