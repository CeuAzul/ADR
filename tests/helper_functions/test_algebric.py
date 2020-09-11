from adr.helper_functions import transform, rotate, translate, \
    component_vector_in_absolute_frame, component_vector_coords_in_absolute_frame
from vec import Vector2
import math
import numpy.testing as npt
from adr.Components import BaseComponent


def test_rotate():
    v1 = Vector2(0.7, 0.1)
    v1_rot_90 = rotate(v1, math.radians(90))
    v1_rot_n90 = rotate(v1, math.radians(-90))
    v1_rot_n135 = rotate(v1, math.radians(-135))
    npt.assert_almost_equal(v1_rot_90.x, -0.1)
    npt.assert_almost_equal(v1_rot_90.y, 0.7)
    npt.assert_almost_equal(v1_rot_n90.x, 0.1)
    npt.assert_almost_equal(v1_rot_n90.y, -0.7)
    npt.assert_almost_equal(v1_rot_n135.x, -0.424, decimal=3)
    npt.assert_almost_equal(v1_rot_n135.y, -0.565, decimal=3)

    v2 = Vector2(-1.4, 0.6)
    v2_rot_90 = rotate(v2, math.radians(90))
    v2_rot_n90 = rotate(v2, math.radians(-90))
    v2_rot_n135 = rotate(v2, math.radians(-135))
    npt.assert_almost_equal(v2_rot_90.x, -0.6)
    npt.assert_almost_equal(v2_rot_90.y, -1.4)
    npt.assert_almost_equal(v2_rot_n90.x, 0.6)
    npt.assert_almost_equal(v2_rot_n90.y, 1.4)
    npt.assert_almost_equal(v2_rot_n135.x, 1.414, decimal=3)
    npt.assert_almost_equal(v2_rot_n135.y, 0.565, decimal=3)


def test_translate():
    v1 = Vector2(-1.4, 0.6)
    v1_trans1 = translate(v1, 0.3, 0.6)
    v1_trans2 = translate(v1, -0.3, -0.6)
    npt.assert_almost_equal(v1_trans1.x, -1.1)
    npt.assert_almost_equal(v1_trans1.y, 1.2)
    npt.assert_almost_equal(v1_trans2.x, -1.7)
    npt.assert_almost_equal(v1_trans2.y, 0.0)


def test_transform():
    v1 = Vector2(0.7, 0.1)
    v1_trans1 = transform(v1, math.radians(90), -0.2, 0.5)
    v1_trans2 = transform(v1, math.radians(-90), -0.2, 0.5)
    npt.assert_almost_equal(v1_trans1.x, -0.3)
    npt.assert_almost_equal(v1_trans1.y, 1.2)
    npt.assert_almost_equal(v1_trans2.x, -0.1)
    npt.assert_almost_equal(v1_trans2.y, -0.2)


def test_component_vector_in_absolute_frame(mocker):
    component = mocker.Mock()
    component.position = Vector2(1.4, 0.6)
    component.angle = math.radians(24)
    vector = Vector2(-0.4, 0.1)
    new_vector = component_vector_in_absolute_frame(vector, component)
    npt.assert_almost_equal(new_vector.x, 0.994, decimal=3)
    npt.assert_almost_equal(new_vector.y, 0.53, decimal=3)


def test_component_vector_coords_in_absolute_frame(mocker):
    component = mocker.Mock()
    component.position = Vector2(1.4, 0.6)
    component.angle = math.radians(25)
    vector_origin = Vector2(-0.4, 0.1)
    vector = Vector2(0, 0.5)
    x0, y0, x, y = component_vector_coords_in_absolute_frame(
        vector_origin, vector, component)
    npt.assert_almost_equal(x0, 0.994, decimal=3)
    npt.assert_almost_equal(y0, 0.521, decimal=3)
    npt.assert_almost_equal(x, 0.784, decimal=3)
    npt.assert_almost_equal(y, 0.975, decimal=3)
