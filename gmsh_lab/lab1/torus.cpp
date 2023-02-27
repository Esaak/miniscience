// -----------------------------------------------------------------------------
//
//  Gmsh C++ tutorial 19
//
//  Thrusections, fillets, pipes, mesh size from curvature
//
// -----------------------------------------------------------------------------

// The OpenCASCADE geometry kernel supports several useful features for solid
// modelling.

#include <set>
#include <cmath>
#include <cstdlib>
#include <gmsh.h>

int main(int argc, char **argv)
{
    gmsh::initialize(argc, argv);

    gmsh::model::add("t19");

    gmsh::model::occ::addCircle(0, 0, 0, 1, 1);
    gmsh::model::occ::addWire({1}, 1000);

    gmsh::model::occ::addDisk(1, 0, 0, 0.2, 0.2, 1000);
    gmsh::model::occ::rotate({{2, 1000}}, 0, 0, 0, 1, 0, 0, M_PI / 2);


    gmsh::model::occ::addDisk(1, 0, 0, 0.17, 0.17, 10000);
    gmsh::model::occ::rotate({{2, 10000}}, 0, 0, 0, 1, 0, 0, M_PI / 2);
    std::vector<std::pair<int, int>> ov;
    std::vector<std::vector<std::pair<int, int>>> ovv;
    gmsh::model::occ::cut({{2, 1000}}, {{2, 10000}}, ov, ovv, 3);
    // We extrude the disk along the spline to create a pipe (other sweeping types
    // can be specified; try e.g. "Frenet" instead of "DiscreteTrihedron"):
    std::vector<std::pair<int, int>>out;
    gmsh::model::occ::addPipe({{2, 3}}, 1000,out, "Fixed");
    //gmsh::model::occ::addPipe({{2, 10000}}, 10000,out, "DiscreteTrihedron");

    // We delete the source surface, and increase the number of sub-edges for a
    // nicer display of the geometry:
    gmsh::model::occ::remove({{2, 1000}});
    gmsh::option::setNumber("Geometry.NumSubEdges", 1000);


    gmsh::model::occ::synchronize();

    // We can activate the calculation of mesh element sizes based on curvature
    // (here with a target of 20 elements per 2*Pi radians):
    gmsh::option::setNumber("Mesh.MeshSizeFromCurvature", 20);

    // We can constraint the min and max element sizes to stay within reasonnable
    // values (see `t10.cpp' for more details):
    gmsh::option::setNumber("Mesh.MeshSizeMin", 0.001);
    gmsh::option::setNumber("Mesh.MeshSizeMax", 0.03);

    gmsh::model::mesh::generate(3);
    gmsh::write("t19.msh");

    // Launch the GUI to see the results:
    std::set<std::string> args(argv, argv + argc);
    if(!args.count("-nopopup")) gmsh::fltk::run();

    gmsh::finalize();
    return 0;
}
