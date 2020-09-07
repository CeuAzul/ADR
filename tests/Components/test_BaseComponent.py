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