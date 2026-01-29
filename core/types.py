'''
This module contains common data structures and math functions usable across the renderer
'''

import taichi as ti

# ---------------------------------------------------
# Constants
# ---------------------------------------------------

EPSILON = 0.0001 #Threshold for ray marching
MAX_STEPS = 1000 #Maximum number of steps for ray marching
MAX_DISTANCE = 1000.0 #Maximum distance for ray marching
NORMAL_EPSILON = 0.001 #Epsilon for normal calculation

BACKGROUND_TOP = ti.Vector([0.6, 0.8, 1.0]) #Sky color
BACKGROUND_BOTTOM = ti.Vector([1.0, 1.0, 1.0]) #Ground color

# ---------------------------------------------------
# Common Vector Math Functions
# ---------------------------------------------------

@ti.func
def clamp(x: float, min_val: float, max_val: float) -> float:
    "Clamp a value between min_val and max_val"
    return ti.max(min_val, ti.min(x, max_val))


#---------------------------------------------------
# Gamma Correction Functions
#---------------------------------------------------

@ti.func
def gamma_correct(color: ti.math.vec3) -> ti.math.vec3: #type: ignore
    "Apply gamma correction to a color"
    return ti.math.vec3(
        ti.pow(clamp(color.x, 0.0, 1.0), 1/2.2), 
        ti.pow(clamp(color.y, 0.0, 1.0), 1/2.2), 
        ti.pow(clamp(color.z, 0.0, 1.0), 1/2.2)
        )

@ti.func
def inverse_gamma_correct(color: ti.math.vec3) -> ti.math.vec3: #type: ignore
    "Apply inverse gamma correction to a color"
    return ti.math.vec3(
        ti.pow(clamp(color.x, 0.0, 1.0), 2.2), 
        ti.pow(clamp(color.y, 0.0, 1.0), 2.2), 
        ti.pow(clamp(color.z, 0.0, 1.0), 2.2)
        )

