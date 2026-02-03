import taichi as ti
import numpy as np
from dataclasses import dataclass, field
from typing import Tuple
import math 


@dataclass
class Camera:
    """
    Camera class to generate rays. 

    Takes the following arguments:
        1. position
        2. look_at
        3. up
        4. fov
    """
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    look_at: Tuple[float, float, float] = (0.0, 0.0, -1.0)
    up: Tuple[float, float, float] = (0.0, 1.0, 0.0)
    fov: float = 45.0  # Field of view in degrees

    _forward: np.ndarray = field(default=None, repr=False)
    _up: np.ndarray = field(default=None, repr=False)
    _right: np.ndarray = field(default=None, repr=False)

    def _compute_basis(self):
        pos = np.array(self.position, dtype=np.float32)
        target = np.array(self.look_at, dtype=np.float32)
        up = np.array(self.up, dtype=np.float32)

        self._forward = target - pos
        self._forward /= np.linalg.norm(self._forward)

        self._right = np.cross(self._forward, up)
        self._right /= np.linalg.norm(self._right)

        self._up = np.cross(self._right, self._forward)
        self._up /= np.linalg.norm(self._up)

    
    def generate_rays(self, width: int, height: int):
        """
        Docstring for generate_rays
        
        :param self: Description
        :param width: Description
        :type width: int
        :param height: Description
        :type height: int
        """
        aspect_ratio = width / height
        fov_rad = math.radians(self.fov)
        half_height = math.tan(fov_rad / 2)
        half_width = aspect_ratio * half_height

        rays = ti.Vector.field(3, dtype=ti.f32, shape=(width, height))

        forward = self._forward.to_list()
        up = self._up.to_list()
        right = self._right.to_list()

        @ti.kernel
        def compute_rays(rays: ti.template(), #type: ignore
                         width: int, height: int, half_width: float, half_height: float,
                         forward_x: float, forward_y: float, forward_z: float,
                         right_x: float, right_y: float, right_z: float,
                         up_x: float, up_y: float, up_z: float
                         ):
            for i, j in ti.ndrange(width, height):
                u = (2 * ((i + 0.5) / width) - 1) * half_width
                v = (1 - 2 * ((j + 0.5) / height)) * half_height

                direction = (self._forward + u * self._right + v * self._up)
                direction /= ti.sqrt(direction.dot(direction))

                rays[i, j] = direction

        compute_rays(rays, width=width, height=height, half_width=half_width, half_height=half_height,
                     forward_x=forward[0], forward_y=forward[1], forward_z=forward[2],
                     up_x=up[0], up_y=up[1], up_z=up[2],
                     right_x=right[0], right_y=right[1], right_z=right[2])
        
        return rays
    
    def get_position_vec3(self) -> ti.math.vec3:
        """
        Returns the camera position as a Taichi vector.
        """
        return ti.math.vec3(self.position[0], self.position[1], self.position[2])
    