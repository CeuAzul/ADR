import attr
from typing import Dict, Callable
from vec import Vector2
import math

from adr.helper_functions import transform
from adr.Components import BaseComponent


@attr.s(auto_attribs=True)
class AttachedComponent(BaseComponent):
    parent: 'Component' = None
    relative_position: Vector2 = None
    relative_angle: float = None

    # State attributes
    actuation_angle: float = 0.0

    def reset_state(self):
        self.actuation_angle = 0.0
        super().reset_state()

    def set_parent(self, parent) -> None:
        if self.parent is not None:
            raise Exception(f'Component already has a parent: {self.parent}')
        self.parent = parent
        parent.append_child(self)

    @property
    def position(self) -> Vector2:
        return transform(self.relative_position, self.parent.angle, *self.parent.position)

    @property
    def angle(self) -> float:
        return self.parent.angle + self.relative_angle + self.actuation_angle

    @property
    def velocity(self) -> Vector2:
        return self.parent.velocity + None

    @property
    def ambient(self):
        return self.parent.ambient
