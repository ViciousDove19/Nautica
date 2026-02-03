#------------------------------------------
# This module contains the most basic blocks that will be used to build complex models.
# All the blocks are signed distance functions (SDFs) for a particular shape.
#------------------------------------------

import taichi as ti

@ti.func
def sdf_sphere(p: ti.math.vec3, center: ti.math.vec3, radius: float) -> float: #type: ignore
    """
    SDF for a sphere function
    """
    return ti.math.length(p - center) - radius


@ti.func
def sdf_plane(p: ti.math.vec3, normal: ti.math.vec3, offset:float) -> float: #type: ignore
    """
    SDF for plane 
    Positive indicates same side as the normal
    """
    return ti.math.dot(p, normal) - offset
