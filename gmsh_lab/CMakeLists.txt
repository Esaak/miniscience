cmake_minimum_required(VERSION 3.24)
project(LABS)

set(CMAKE_CXX_STANDARD 11)

add_library(gmsh SHARED IMPORTED)
set_target_properties(gmsh PROPERTIES
        IMPORTED_LOCATION "/home/ilya/science_prog_lab/gmsh-4.11.1-Linux64-sdk/lib/libgmsh.so"
        INTERFACE_INCLUDE_DIRECTORIES "/home/ilya/science_prog_lab/gmsh-4.11.1-Linux64-sdk/include/"
        )
set(GMSH_LIBRARY gmsh)

# Укажем библиотеки для линковки

add_executable(LAB1 ./lab1/1.cpp)
target_link_libraries(LAB1 ${GMSH_LIBRARY})


add_executable(LAB2 ./lab1/2.cpp)
target_link_libraries(LAB2 ${GMSH_LIBRARY})