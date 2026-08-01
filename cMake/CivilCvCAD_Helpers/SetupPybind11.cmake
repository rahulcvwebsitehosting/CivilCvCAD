macro(SetupPybind11)
# -------------------------------- PyBind11 -----------------------------

    # necessary for flat-mesh feature
    if (CIVILCVCAD_USE_PYBIND11)
        find_package(pybind11 REQUIRED)
    endif()

endmacro(SetupPybind11)
