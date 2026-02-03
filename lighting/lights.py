from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple

class FallOffType(Enum):
    NONE = "none"
    LINEAR = "linear"
    QUADRATIC = "quadratic"

@dataclass
class PointLight:
    """
    PointLight class to represent a point light source.

    Takes the following arguments:
        1. position
        2. color
        3. intensity
        4. falloff_type
    """
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    intensity: float = 1.0
    falloff_type: FallOffType = FallOffType.NONE

    def get_position_tuple(self) -> Tuple[float, float, float]:
        return self.position
    
    def get_color_tuple(self) -> Tuple[float, float, float]:
        return self.color
    
@dataclass
class AmbientLight:
    """
    AmbientLight class to represent an ambient light source.

    Takes the following arguments:
        1. color
        2. intensity
    """
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    intensity: float = 0.1

    def get_color_tuple(self) -> Tuple[float, float, float]:
        return self.color
    
@dataclass
class DirectionalLight:
    """
    DirectionalLight class to represent a directional light source.

    Takes the following arguments:
        1. direction
        2. color
        3. intensity
    """
    direction: Tuple[float, float, float] = (0.0, -1.0, 0.0)
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    intensity: float = 1.0

    def get_direction_tuple(self) -> Tuple[float, float, float]:
        dx = self.direction[0]
        dy = self.direction[1]  
        dz = self.direction[2]
        length = (dx**2 + dy**2 + dz**2) ** 0.5
        if length == 0:
            return (0.0, 1.0, 0.0)
        self.direction = (dx / length, dy / length, dz / length)
        return self.direction
    
    def get_color_tuple(self) -> Tuple[float, float, float]:
        return self.color