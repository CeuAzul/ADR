from adr.Components import BaseComponent
import pytest


@pytest.fixture
def base_component():
    base_component = BaseComponent(
        name='component',
        type='generic_component',
        mass=3.4,
    )
    return base_component


def test_instantiation(base_component):
    assert(base_component.name == 'component')
    assert(base_component.type == 'generic_component')
    assert(base_component.mass == 3.4)


def test_append_child(base_component):
    child_component = BaseComponent("wing1", "wing", 1.1)
    base_component.append_child(child_component)
    assert(base_component.children["wing1"] == child_component)
    assert(base_component.wing1 == child_component)
