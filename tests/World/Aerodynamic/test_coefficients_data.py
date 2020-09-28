import numpy.testing as npt

from adr.World.Aerodynamic.coefficients_data import get_CL, get_CD, get_CM, get_CL_inv, get_CD_inv, get_CM_inv


def test_get_CL():
    npt.assert_almost_equal(get_CL(18), 0)
    npt.assert_almost_equal(get_CL(12), 1.8)
    npt.assert_almost_equal(get_CL(2), 0.8)
    npt.assert_almost_equal(get_CL(0), 0.6)
    npt.assert_almost_equal(get_CL(-2), 0.399, decimal=3)
    npt.assert_almost_equal(get_CL(-12), 0)
    npt.assert_almost_equal(get_CL(-18), 0)


def test_get_CD():
    npt.assert_almost_equal(get_CD(18), 2.1)
    npt.assert_almost_equal(get_CD(12), 0.18)
    npt.assert_almost_equal(get_CD(2), 0.08)
    npt.assert_almost_equal(get_CD(0), 0.06, decimal=3)
    npt.assert_almost_equal(get_CD(-2), 0.04, decimal=3)
    npt.assert_almost_equal(get_CD(-12), 2.1)
    npt.assert_almost_equal(get_CD(-18), 2.1)


def test_get_CM():
    npt.assert_almost_equal(get_CM(18), 0)
    npt.assert_almost_equal(get_CM(12), -0.251, decimal=3)
    npt.assert_almost_equal(get_CM(2), -0.260, decimal=3)
    npt.assert_almost_equal(get_CM(0), -0.232, decimal=3)
    npt.assert_almost_equal(get_CM(-2), -0.195, decimal=3)
    npt.assert_almost_equal(get_CM(-12), 0)
    npt.assert_almost_equal(get_CM(-18), 0)


def test_get_CL_inv():
    npt.assert_almost_equal(get_CL_inv(18), 0)
    npt.assert_almost_equal(get_CL_inv(12), 0)
    npt.assert_almost_equal(get_CL_inv(2), -0.399, decimal=3)
    npt.assert_almost_equal(get_CL_inv(0), -0.6)
    npt.assert_almost_equal(get_CL_inv(-2), -0.8)
    npt.assert_almost_equal(get_CL_inv(-12), -1.8)
    npt.assert_almost_equal(get_CL_inv(-18), 0)


def test_get_CD_inv():
    npt.assert_almost_equal(get_CD_inv(18), 2.1)
    npt.assert_almost_equal(get_CD_inv(12), 2.1)
    npt.assert_almost_equal(get_CD_inv(2), 0.04, decimal=3)
    npt.assert_almost_equal(get_CD_inv(0), 0.06, decimal=3)
    npt.assert_almost_equal(get_CD_inv(-2), 0.08)
    npt.assert_almost_equal(get_CD_inv(-12), 0.18)
    npt.assert_almost_equal(get_CD_inv(-18), 2.1)


def test_get_CM_inv():
    npt.assert_almost_equal(get_CM_inv(18), 0)
    npt.assert_almost_equal(get_CM_inv(12), 0)
    npt.assert_almost_equal(get_CM_inv(2), 0.195, decimal=3)
    npt.assert_almost_equal(get_CM_inv(0), 0.232, decimal=3)
    npt.assert_almost_equal(get_CM_inv(-2), 0.260, decimal=3)
    npt.assert_almost_equal(get_CM_inv(-12), 0.251, decimal=3)
    npt.assert_almost_equal(get_CM_inv(-18), 0)
