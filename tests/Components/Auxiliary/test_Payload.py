import pytest
import math
from vec import Vector2

from adr.Components.Auxiliary import Payload


@pytest.fixture
def main_payload():
    main_payload = Payload(
        name='main_payload',
        mass=9.2,
        relative_position=Vector2(-0.2, 0),
        relative_angle=math.radians(0)
    )
    return main_payload


def test_instantiation(main_payload):
    assert(main_payload.type == 'payload')
