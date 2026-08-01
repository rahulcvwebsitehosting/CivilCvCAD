macro(InitializeCivilCvCADBuildOptions)
    # ==============================================================================
    # =================   All the options for the build process    =================
    # ==============================================================================

    option(BUILD_FORCE_DIRECTORY "The build directory must be different to the source directory." OFF)
    option(BUILD_GUI "Build CivilCvCAD Gui. Otherwise you have only the command line and the Python import module." ON)
    option(CIVILCVCAD_USE_EXTERNAL_ZIPIOS "Use system installed zipios++ instead of the bundled." OFF)
    option(CIVILCVCAD_USE_EXTERNAL_SMESH "Use system installed smesh instead of the bundled." OFF)
    option(CIVILCVCAD_USE_EXTERNAL_KDL "Use system installed orocos-kdl instead of the bundled." OFF)
    option(CIVILCVCAD_USE_EXTERNAL_ONDSELSOLVER "Use system installed OndselSolver instead of git submodule." OFF)
    option(CIVILCVCAD_USE_EXTERNAL_E57FORMAT "Use system installed libE57Format instead of the bundled." OFF)
    option(CIVILCVCAD_USE_EXTERNAL_PYCXX "Use system installed PyCXX, located using pkgconfig" OFF)
    option(CIVILCVCAD_USE_EXTERNAL_CLIPPER2 "Use system installed Clipper2" OFF)
    option(CIVILCVCAD_USE_EXTERNAL_KDTREE "Use system installed libkdtree++" OFF)
    option(CIVILCVCAD_USE_EXTERNAL_JSON "Use system installed nlohmann_json" OFF)
    option(CIVILCVCAD_USE_EXTERNAL_COIN_PIVY "Use system installed Coin and Pivy instead of the bundled versions." OFF)
    option(CIVILCVCAD_USE_FREETYPE "Builds the features using FreeType libs" ON)
    option(CIVILCVCAD_CHECK_PIVY "Check for pivy version using Python at build time" ON)
    option(CIVILCVCAD_PARALLEL_COMPILE_JOBS "Compilation jobs pool size to fit memory limitations.")
    option(CIVILCVCAD_PARALLEL_LINK_JOBS "Linkage jobs pool size to fit memory limitations.")
    option(BUILD_WITH_CONDA "Set ON if you build CivilCvCAD with conda" OFF)
    option(BUILD_DYNAMIC_LINK_PYTHON "If OFF extension-modules do not link against python-libraries" ON)
    option(BUILD_TRACY_FRAME_PROFILER "If ON then enables support for the Tracy frame profiler" OFF)

    option(INSTALL_TO_SITEPACKAGES "If ON the civilcvcad root namespace (python) is installed into python's site-packages" ON)
    option(INSTALL_PREFER_SYMLINKS "If ON then fc_copy_sources macro will create symlinks instead of copying files" OFF)
    option(OCCT_CMAKE_FALLBACK "disable usage of occt-config files" OFF)
    option(CIVILCVCAD_USE_QT_DIALOGS "Use Qt's dialogs instead of the native one." OFF)

    # == Win32 is default behaviour use the LibPack copied in Source tree ==========
    if(MSVC)
        option(CIVILCVCAD_RELEASE_PDB "Create PDB files for Release version." ON)
        option(CIVILCVCAD_RELEASE_SEH "Enable Structured Exception Handling for Release version." ON)
        option(CIVILCVCAD_LIBPACK_USE "Use the Windows LibPack to build CivilCvCAD (MSVC only)." ON)
        option(CIVILCVCAD_USE_PCH "Activate precompiled headers where it's used." ON)

        if (DEFINED ENV{CIVILCVCAD_LIBPACK_DIR})
            set(CIVILCVCAD_LIBPACK_DIR $ENV{CIVILCVCAD_LIBPACK_DIR} CACHE PATH  "Directory of the CivilCvCAD LibPack")
            message(STATUS "Found libpack env variable: ${CIVILCVCAD_LIBPACK_DIR}")
        else()
            set(CIVILCVCAD_LIBPACK_DIR ${CMAKE_SOURCE_DIR} CACHE PATH  "Directory of the CivilCvCAD LibPack")
        endif()

        set(LIBPACK_FOUND OFF)
        if (CIVILCVCAD_LIBPACK_USE)
            if (NOT CIVILCVCAD_LIBPACK_DIR)
                message(WARNING "CIVILCVCAD_LIBPACK_USE is ON, but CIVILCVCAD_LIBPACK_DIR is not set. Turning CIVILCVCAD_LIBPACK_USE OFF.")
                set(CIVILCVCAD_LIBPACK_USE OFF)
            else()
                # Check to see if this LibPack's mode matches our build mode -- on Windows, full-blown Debug mode is an
                # all-or-nothing operation. If you have debug libraries, you MUST compile in debug, and if you don't
                # have debug libraries, you must NOT compile in debug.
                set(NONDEBUG_CHECKFILE "${CIVILCVCAD_LIBPACK_DIR}/plugins/imageformats/qsvg.dll")
                set(DEBUG_CHECKFILE "${CIVILCVCAD_LIBPACK_DIR}/plugins/imageformats/qsvgd.dll")
                get_property(_is_multi_config GLOBAL PROPERTY GENERATOR_IS_MULTI_CONFIG)
                if (_is_multi_config)
                    # For multi-config generators (Visual Studio, Ninja Multi-Config) we check to see which version of
                    # the LibPack was specified (Debug or Non-Debug) and then restrict CMAKE_CONFIGURATION_TYPES so the
                    # IDE only offers configurations that would actually work with the given LibPack.
                    if (EXISTS "${NONDEBUG_CHECKFILE}" AND EXISTS "${DEBUG_CHECKFILE}")
                        message(WARNING "The specified LibPack:\n  ${CIVILCVCAD_LIBPACK_DIR}\ncontains both release and debug libraries: that often causes problems.\nTrying to continue...")
                        set(LIBPACK_FOUND ON)
                    elseif(EXISTS "${NONDEBUG_CHECKFILE}")
                        message(STATUS "NOTE: The specified LibPack was not compiled in Debug mode, so CivilCvCAD cannot be either.")
                        set(CMAKE_CONFIGURATION_TYPES "Release;RelWithDebInfo;MinSizeRel" CACHE STRING "Configurations supported by the selected LibPack" FORCE)
                        set(LIBPACK_FOUND ON)
                    elseif(EXISTS "${DEBUG_CHECKFILE}")
                        message(STATUS "NOTE: The specified LibPack was compiled in Debug mode, so CivilCvCAD must be as well.")
                        set(CMAKE_CONFIGURATION_TYPES "Debug" CACHE STRING "Configurations supported by the selected LibPack" FORCE)
                        set(LIBPACK_FOUND ON)
                    else()
                        message(NOTICE "LibPack not found in ${CIVILCVCAD_LIBPACK_DIR}\nSet CIVILCVCAD_LIBPACK_DIR to the LibPack directory.")
                        message(FATAL_ERROR "Visit: https://github.com/CivilCvCAD/CivilCvCAD-Libpack/releases/ for Windows LibPack downloads.")
                    endif()
                else()
                    if (EXISTS "${NONDEBUG_CHECKFILE}" AND EXISTS "${DEBUG_CHECKFILE}")
                        message(WARNING "The specified LibPack:\n  ${CIVILCVCAD_LIBPACK_DIR}\ncontains both release and debug libraries: that often causes problems.\nTrying to continue...")
                        set(LIBPACK_FOUND ON)
                    elseif(CMAKE_BUILD_TYPE STREQUAL "Debug" AND EXISTS "${NONDEBUG_CHECKFILE}")
                        message(FATAL_ERROR "The specified LibPack:\n  ${CIVILCVCAD_LIBPACK_DIR}\nwas not built for Debug mode and cannot be used for this type of build")
                    elseif(NOT CMAKE_BUILD_TYPE STREQUAL "Debug" AND EXISTS "${DEBUG_CHECKFILE}")
                        message(FATAL_ERROR "This specified LibPack:\n  ${CIVILCVCAD_LIBPACK_DIR}\nwas built for Debug mode and cannot be used in ${CMAKE_BUILD_TYPE}")
                    elseif(NOT EXISTS "${NONDEBUG_CHECKFILE}" AND NOT EXISTS "${DEBUG_CHECKFILE}")
                        message(NOTICE "LibPack not found in ${CIVILCVCAD_LIBPACK_DIR}\nSet CIVILCVCAD_LIBPACK_DIR to the LibPack directory.")
                        message(FATAL_ERROR "Visit: https://github.com/CivilCvCAD/CivilCvCAD-Libpack/releases/ for Windows LibPack downloads.")
                    else()
                        set(LIBPACK_FOUND ON)
                    endif()
                endif()
            endif()
        endif()

        if (LIBPACK_FOUND)
            set(COPY_LIBPACK_BIN_TO_BUILD OFF)
            # Create install commands for dependencies for INSTALL target in CivilCvCAD solution
            option(CIVILCVCAD_INSTALL_DEPEND_DIRS "Create install dependency commands for the INSTALL target found
                in the CivilCvCAD solution." ON)
            # Copy libpack smaller dependency folders to build folder per user request - if non-existent at destination
            if ((NOT CMAKE_BUILD_TYPE STREQUAL "Debug" AND NOT EXISTS ${CMAKE_BINARY_DIR}/bin/imageformats/qsvg.dll) OR
                (CMAKE_BUILD_TYPE STREQUAL "Debug" AND NOT EXISTS ${CMAKE_BINARY_DIR}/bin/imageformats/qsvgd.dll))
                option(CIVILCVCAD_COPY_DEPEND_DIRS_TO_BUILD "Copy smaller LibPack dependency directories to build directory." OFF)
            endif()
            # Copy libpack 'bin' directory contents to build 'bin' per user request - only IF NOT EXISTS already
            if (NOT EXISTS ${CMAKE_BINARY_DIR}/bin/DLLs)
                set(COPY_LIBPACK_BIN_TO_BUILD ON )
                option(CIVILCVCAD_COPY_LIBPACK_BIN_TO_BUILD "Copy larger LibPack dependency 'bin' folder to the build directory." OFF)
                # Copy only the minimum number of files to get a working application
                option(CIVILCVCAD_COPY_PLUGINS_BIN_TO_BUILD "Copy plugins to the build directory." OFF)
            endif()
        endif()
    elseif(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_COMPILER_IS_CLANGXX)
        option(CIVILCVCAD_WARN_ERROR "Make all warnings into errors. " OFF)
    else(MSVC)
        option(CIVILCVCAD_LIBPACK_USE "Use the LibPack to build CivilCvCAD (MSVC only)." OFF)
        set(CIVILCVCAD_LIBPACK_DIR ""  CACHE PATH  "Directory of the CivilCvCAD LibPack")
    endif(MSVC)

    ChooseQtVersion()

    option(BUILD_DESIGNER_PLUGIN "Build and install the designer plugin" OFF)

    if(APPLE)
        option(CIVILCVCAD_CREATE_MAC_APP "Create app bundle on install" OFF)

        if(CIVILCVCAD_CREATE_MAC_APP)
            install(
                DIRECTORY ${CMAKE_SOURCE_DIR}/src/MacAppBundle/CivilCvCAD.app/
                DESTINATION ${CMAKE_INSTALL_PREFIX}/${PROJECT_NAME}.app
            )

            # It should be safe to assume we've got sed on OSX...
            install(CODE "
                execute_process(COMMAND
                    sed -i \"\" -e s/VERSION_STRING_FROM_CMAKE/${PACKAGE_VERSION}/
                    -e s/NAME_STRING_FROM_CMAKE/${PROJECT_NAME}/
                    ${CMAKE_INSTALL_PREFIX}/${PROJECT_NAME}.app/Contents/Info.plist)
                   ")

            set(CMAKE_INSTALL_PREFIX
                ${CMAKE_INSTALL_PREFIX}/${PROJECT_NAME}.app/Contents)
            set(CMAKE_INSTALL_LIBDIR ${CMAKE_INSTALL_PREFIX}/lib )
        endif(CIVILCVCAD_CREATE_MAC_APP)
        set(CMAKE_MACOSX_RPATH TRUE )
    endif(APPLE)

    option(BUILD_FEM "Build the CivilCvCAD FEM module" ON)
    option(BUILD_TEMPLATE "Build the CivilCvCAD template module which is only for testing purposes" OFF)
    # CivilCvCAD is an offline-only distribution. Keep network-backed modules
    # out of every build, including builds configured from an existing cache.
    option(BUILD_ADDONMGR "Build the CivilCvCAD addon manager module" OFF)
    option(BUILD_BIM "Build the CivilCvCAD BIM module" ON)
    option(BUILD_DRAFT "Build the CivilCvCAD draft module" ON)
    option(BUILD_HELP "Build the CivilCvCAD help module" ON)
    option(BUILD_IMPORT "Build the CivilCvCAD import module" ON)
    option(BUILD_INSPECTION "Build the CivilCvCAD inspection module" ON)
    option(BUILD_JTREADER "Build the CivilCvCAD jt reader module" OFF)
    option(BUILD_MATERIAL "Build the CivilCvCAD material module" ON)
    option(BUILD_MATERIAL_EXTERNAL "Build the CivilCvCAD material external interface module" OFF)
    option(BUILD_MESH "Build the CivilCvCAD mesh module" ON)
    option(BUILD_MESH_PART "Build the CivilCvCAD mesh part module" ON)
    option(BUILD_FLAT_MESH "Build the CivilCvCAD flat mesh module" ON)
    option(BUILD_OPENSCAD "Build the CivilCvCAD openscad module" ON)
    option(BUILD_PART "Build the CivilCvCAD part module" ON)
    option(BUILD_PART_DESIGN "Build the CivilCvCAD part design module" ON)
    option(BUILD_CAM "Build the CivilCvCAD CAM module" ON)
    option(BUILD_ASSEMBLY "Build the CivilCvCAD Assembly module" ON)
    option(BUILD_PLOT "Build the CivilCvCAD plot module" ON)
    option(BUILD_POINTS "Build the CivilCvCAD points module" ON)
    option(BUILD_REVERSEENGINEERING "Build the CivilCvCAD reverse engineering module" ON)
    option(BUILD_ROBOT "Build the CivilCvCAD robot module" ON)
    option(BUILD_SHOW "Build the CivilCvCAD Show module (helper module for visibility automation)" ON)
    option(BUILD_SKETCHER "Build the CivilCvCAD sketcher module" ON)
    option(BUILD_SPREADSHEET "Build the CivilCvCAD spreadsheet module" ON)
    option(BUILD_START "Build the CivilCvCAD start module" ON)
    option(BUILD_TEST "Build the CivilCvCAD test module" ON)
    option(BUILD_MEASURE "Build the CivilCvCAD Measure module" ON)
    option(BUILD_TECHDRAW "Build the CivilCvCAD Technical Drawing module" ON)
    option(BUILD_TUX "Build the CivilCvCAD Tux module" ON)
    option(BUILD_WEB "Build the CivilCvCAD Web module" OFF)
    option(BUILD_SURFACE "Build the CivilCvCAD surface module" ON)
    option(BUILD_VR "Build the CivilCvCAD Oculus Rift support (need Oculus SDK 4.x or higher)" OFF)
    option(ENABLE_DEVELOPER_TESTS "Build the CivilCvCAD unit tests suit" ON)

    set(BUILD_ADDONMGR OFF CACHE BOOL
        "Disabled permanently: CivilCvCAD is offline-only" FORCE)
    set(BUILD_WEB OFF CACHE BOOL
        "Disabled permanently: CivilCvCAD is offline-only" FORCE)

    if(MSVC OR APPLE)
        set(CIVILCVCAD_3DCONNEXION_SUPPORT "NavLib" CACHE STRING "Select version of the 3Dconnexion device integration")
        set_property(CACHE CIVILCVCAD_3DCONNEXION_SUPPORT PROPERTY STRINGS "None" "NavLib" "Legacy" "Both")
    else(MSVC OR APPLE)
        option(CIVILCVCAD_USE_3DCONNEXION_LEGACY "Enable support for 3Dconnexion devices." ON)
    endif(MSVC OR APPLE)

    if(CIVILCVCAD_3DCONNEXION_SUPPORT STREQUAL "NavLib")
        set(CIVILCVCAD_USE_3DCONNEXION_NAVLIB ON)
    elseif(CIVILCVCAD_3DCONNEXION_SUPPORT STREQUAL "Both")
        set(CIVILCVCAD_USE_3DCONNEXION_NAVLIB ON)
        set(CIVILCVCAD_USE_3DCONNEXION_LEGACY ON)
    elseif(CIVILCVCAD_3DCONNEXION_SUPPORT STREQUAL "Legacy")
        set(CIVILCVCAD_USE_3DCONNEXION_LEGACY ON)
    elseif(CIVILCVCAD_3DCONNEXION_SUPPORT STREQUAL "None")
        set(CIVILCVCAD_USE_3DCONNEXION_NAVLIB OFF)
        set(CIVILCVCAD_USE_3DCONNEXION_LEGACY OFF)
    endif()

    if(APPLE AND CIVILCVCAD_USE_3DCONNEXION_LEGACY)
        find_library(3DCONNEXIONCLIENT_FRAMEWORK 3DconnexionClient)
        if(NOT (IS_DIRECTORY ${3DCONNEXIONCLIENT_FRAMEWORK}))
            set(CIVILCVCAD_USE_3DCONNEXION_LEGACY OFF)
        endif()
    endif()

    if(MSVC)
        option(BUILD_FEM_NETGEN "Build the CivilCvCAD FEM module with the NETGEN mesher" ON)
        option(CIVILCVCAD_USE_PCL "Build the features that use PCL libs" OFF)
    endif(MSVC)
    if(NOT MSVC)
        option(BUILD_FEM_NETGEN "Build the CivilCvCAD FEM module with the NETGEN mesher" OFF)
        option(CIVILCVCAD_USE_PCL "Build the features that use PCL libs" OFF)
    endif(NOT MSVC)

    if(BUILD_FEM OR BUILD_MESH_PART)
        set(CIVILCVCAD_USE_SMESH ON)
        if(CIVILCVCAD_USE_EXTERNAL_SMESH)
            set(BUILD_SMESH OFF)
        else()
            set(BUILD_SMESH ON)
        endif()
    else()
        set(CIVILCVCAD_USE_SMESH OFF)
        set(BUILD_SMESH OFF)
    endif()

    if (BUILD_CAM OR BUILD_FLAT_MESH)
        set(CIVILCVCAD_USE_PYBIND11 ON)
    endif()

    # force build directory to be different to source directory
    if (BUILD_FORCE_DIRECTORY)
        if(${CMAKE_SOURCE_DIR} STREQUAL ${CMAKE_BINARY_DIR})
            message(FATAL_ERROR "The build directory (${CMAKE_BINARY_DIR}) must be different to the source directory (${CMAKE_SOURCE_DIR}).\n"
                                "Please choose another build directory! Or disable the option BUILD_FORCE_DIRECTORY.")
        endif()
    endif()

    if(CIVILCVCAD_PARALLEL_COMPILE_JOBS)
        if(CMAKE_GENERATOR MATCHES "Ninja")
            set_property(GLOBAL APPEND PROPERTY JOB_POOLS compile_job_pool=${CIVILCVCAD_PARALLEL_COMPILE_JOBS})
            set(CMAKE_JOB_POOL_COMPILE compile_job_pool)
        else()
            message(WARNING "Job pooling is only available with Ninja generators.")
        endif()
    endif()

    if(CIVILCVCAD_PARALLEL_LINK_JOBS)
        if(CMAKE_GENERATOR MATCHES "Ninja")
            set_property(GLOBAL APPEND PROPERTY JOB_POOLS link_job_pool=${CIVILCVCAD_PARALLEL_LINK_JOBS})
            set(CMAKE_JOB_POOL_LINK link_job_pool)
        else()
            message(WARNING "Job pooling is only available with Ninja generators.")
        endif()
    endif()
endmacro(InitializeCivilCvCADBuildOptions)
