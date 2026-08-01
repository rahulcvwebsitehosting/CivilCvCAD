macro(SetupJSON)

    if(CIVILCVCAD_USE_EXTERNAL_JSON)
        find_package(nlohmann_json REQUIRED)
    else(CIVILCVCAD_USE_EXTERNAL_JSON)
        set(nlohmann_json_INCLUDE_DIRS ${CMAKE_SOURCE_DIR}/src/3rdParty/json/single_include)
    endif(CIVILCVCAD_USE_EXTERNAL_JSON)

endmacro(SetupJSON)
