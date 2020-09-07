from adr.helper_functions import transform, rotate, translate
from vec import Vector2
import math
import numpy.testing as npt


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
