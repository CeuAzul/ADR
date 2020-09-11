import numpy as npt
from vec import Vector2
from adr.World import gravitational_acceleration, Ambient
from adr.Components import BaseComponent, FreeBody, AttachedComponent
import pytest
import math


@pytest.fixture
def base_component():
    base_component = BaseComponent(
        name='component',
        type='generic_component',
        mass=3.4,
    )
    return base_component


@pytest.fixture
def freebody_component():
    freebody_component = FreeBody(
        name='component',
        type='generic_component',
        mass=3.4,
        position_cg=Vector2(-0.7, 0.2),
        pitch_rot_inertia=30.0,
        ambient=Ambient()
    )
    return freebody_component


@pytest.fixture
def attached_component():
    attached_component = AttachedComponent(
        name='attached_component',
        type='generic_attached_component',
        mass=1.4,
        relative_position=Vector2(-0.4, 0.1),
        relative_angle=math.radians(9)
    )
    return attached_component


@pytest.fixture
def payload():
    payload = AttachedComponent(
        name='payload_generic',
        type='payload',
        mass=3.0,
        relative_position=Vector2(-0.6, 0.08),
        relative_angle=math.radians(9)
    )
    return payload

@pytest.fixture
def moment1():
    mag = 25
    ang = math.radians(30)
    moment_point = Vector2(-5,2)
    moment1 = Vector2(r=mag,theta=ang)
    return moment1, moment_point


@pytest.fixture
def force1():
    mag = 10
    ang = math.radians(45)
    force_point = Vector2(-10, 0)
    force1 = Vector2(r=mag, theta=ang)
    return force1, force_point


def test_instantiation(base_component):
    assert(base_component.name == 'component')
    assert(base_component.type == 'generic_component')
    assert(base_component.mass == 3.4)


def test_reset_state(mocker, base_component):
    spy = mocker.spy(base_component, 'reset_children_state')
    base_component.reset_state()
    spy.assert_called_once()


def test_reset_children_state(mocker, base_component):
    child_component_mock = BaseComponent
    child_component_mock.reset_state = mocker.Mock()
    base_component.children = {'mock_component': child_component_mock}
    spy = mocker.spy(child_component_mock, 'reset_state')

    base_component.reset_children_state()
    spy.assert_called_once()


def test_append_child(base_component):
    child_component = BaseComponent("wing1", "wing", 1.1)
    base_component.append_child(child_component)
    assert(base_component.children["wing1"] == child_component)
    assert(base_component.wing1 == child_component)


def test_angle_of_attack(freebody_component, attached_component):
    freebody_component.velocity = Vector2(r=12, theta=math.radians(5))
    attached_component.set_parent(freebody_component)
    npt.testing.assert_almost_equal(
        math.degrees(freebody_component.angle_of_attack), -5.0, decimal=1)
    npt.testing.assert_almost_equal(
        math.degrees(attached_component.angle_of_attack), 4.0, decimal=1)


def test_empty_mass(freebody_component, base_component, attached_component, payload):
    freebody_component.append_child(attached_component)
    base_component.append_child(attached_component)
    base_component.append_child(payload)
    assert(base_component.empty_mass == 4.8)
    assert(freebody_component.empty_mass == 4.8)
    assert(attached_component.empty_mass == 1.4)

def test_total_mass(freebody_component, base_component, attached_component, payload):
    freebody_component.append_child(attached_component)
    base_component.append_child(attached_component)
    base_component.append_child(payload)
    assert base_component.total_mass == 7.8
    assert freebody_component.total_mass == 4.8
    assert attached_component.total_mass == 1.4


def test_moment_from_external_moments(freebody_component, attached_component):
    attached_component.set_parent(freebody_component)
    freebody_component.external_moments['moment1'] = lambda: 10.0
    attached_component.external_moments['moment2'] = lambda: 20.0
    assert(freebody_component.moment_from_external_moments() == 10.0)


def test_force_and_moment_from_external_forces(freebody_component, attached_component):
    def ext_force_function1():
        return Vector2(-0.9, 0.5), Vector2(0.6, 2.0)

    def ext_force_function2():
        return Vector2(1, 1.4), Vector2(-0.5, -0.1)

    freebody_component.angle = math.radians(15)
    attached_component.set_parent(freebody_component)
    freebody_component.external_forces['force1'] = ext_force_function1
    attached_component.external_forces['force2'] = ext_force_function2
    freebody_component.external_forces.pop('weight')
    force, moment = freebody_component.force_and_moment_from_external_forces()
    npt.testing.assert_almost_equal(force.x, -0.9, decimal=3)
    npt.testing.assert_almost_equal(force.y, 0.5, decimal=3)
    npt.testing.assert_almost_equal(moment, 2.1, decimal=3)


def test_force_and_moment_from_children(freebody_component, attached_component):
    def ext_force_function1():
        return Vector2(-0.9, 0.5), Vector2(0.6, 2.0)

    def ext_force_function2():
        return Vector2(1, 1.4), Vector2(-0.5, -0.1)

    attached_component.set_parent(freebody_component)
    freebody_component.external_forces['force1'] = ext_force_function1
    attached_component.external_forces['force2'] = ext_force_function2
    force, moment = freebody_component.force_and_moment_from_children()
    npt.testing.assert_almost_equal(force.x, 0.7686, decimal=3)
    npt.testing.assert_almost_equal(force.y, 1.5391, decimal=3)
    npt.testing.assert_almost_equal(moment, -1.292, decimal=3)


def test_force_and_moment_at_component_origin(freebody_component, attached_component):
    def ext_force_function1():
        return Vector2(-0.9, 0.5), Vector2(0.6, 2.0)

    def ext_force_function2():
        return Vector2(1, 1.4), Vector2(-0.5, -0.1)
    attached_component.set_parent(freebody_component)
    freebody_component.external_forces.pop('weight')
    freebody_component.external_forces['force1'] = ext_force_function1
    freebody_component.external_moments['moment1'] = lambda: 10.0
    attached_component.external_forces['force2'] = ext_force_function2
    attached_component.external_moments['moment2'] = lambda: 20.0
    force, moment = freebody_component.force_and_moment_at_component_origin()
    npt.testing.assert_almost_equal(force.x, -0.131, decimal=3)
    npt.testing.assert_almost_equal(force.y, 2.04, decimal=3)
    npt.testing.assert_almost_equal(moment, 30.807, decimal=3)


def test_nested_components(base_component, attached_component):
    base_component.append_child(attached_component)
    assert(base_component.nested_components["component"] == base_component)
    assert(
        base_component.nested_components["attached_component"] == attached_component)
    assert(
        attached_component.nested_components["attached_component"] == attached_component)
    assert(base_component.nested_components == {
           'component': base_component, 'attached_component': attached_component})
    assert(attached_component.nested_components == {
           'attached_component': attached_component})

def test_add_external_force_function(force1, base_component):
    base_component.add_external_force_function('force1', force1)
    assert(base_component.external_forces['force1'] == force1)
           
def test_add_external_moment_function(moment1, base_component):
    base_component.add_external_force_function('moment1', moment1)
    assert(base_component.external_forces['moment1'] == moment1)
