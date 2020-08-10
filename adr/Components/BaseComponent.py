import attr
from typing import Dict, Callable
from vec import Vector2
import math

from adr.helper_functions import transform
from adr.World.constants import gravitational_acceleration


@attr.s(auto_attribs=True)
class BaseComponent:
    name: str = None
    type: str = None
    mass: float = None
    children: Dict['str', 'Component'] = attr.Factory(dict)
    external_forces: Dict['str', Callable] = attr.Factory(dict)
    external_moments: Dict['str', Callable] = attr.Factory(dict)

    def append_child(self, child) -> None:
        self.children[child.name] = child
        setattr(self, child.name, child)

    def reset_state(self) -> None:
        self.reset_children_state()

    def reset_children_state(self) -> None:
        for component in self.children.values():
            component.reset_state()

    def add_external_force_function(self, name, function):
        self.external_forces[name] = function

    def add_external_moment_function(self, name, function):
        self.external_moments[name] = function

    def force_and_moment_at_component_origin(self):
        force = Vector2(0, 0)
        moment = 0.0

        _force, _moment = self.force_and_moment_from_external_forces()
        force += _force
        moment += _moment

        _moment = self.moment_from_external_moments()
        moment += _moment

        _force, _moment = self.force_and_moment_from_children()
        force += _force
        moment += _moment

        return force, moment

    def force_and_moment_from_external_forces(self):
        force = Vector2(0.00001, 0)
        moment = 0.0
        for force_function in self.external_forces.values():
            _force, _application_point = force_function()
            force += _force
            moment += _application_point.cross(_force)
        return force, moment

    def moment_from_external_moments(self):
        moment = 0.0
        for moment_function in self.external_moments.values():
            moment += moment_function()
        return moment

    def force_and_moment_from_children(self):
        force = Vector2(0, 0)
        moment = 0.0

        for component in self.children.values():
            _force, _moment = component.force_and_moment_at_component_origin()
            force += _force.rotated(component.relative_angle)
            moment += _moment
            moment += component.relative_position.cross(_force)
        return force, moment

    @property
    def nested_components(self):
        nested_components = {}
        nested_components[self.name] = self
        for component_name, component in self.children.items():
            nested_components[component_name] = component
            nested_components = {**nested_components,
                                 **component.nested_components}
        return nested_components

    @property
    def angle_of_attack(self) -> float:
        return self.angle - self.velocity.theta

    @property
    def total_mass(self):
        mass = 0
        components = self.nested_components
        for component in components.values():
            mass += component.mass
        return mass

    @property
    def empty_mass(self):
        mass = 0
        components = self.nested_components
        for component in components.values():
            if component.type != 'payload':
                mass += component.mass
        return mass
