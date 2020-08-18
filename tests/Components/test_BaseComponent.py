from adr.Components import BaseComponent
import pytest
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
