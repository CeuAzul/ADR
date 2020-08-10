from ADR.Components.Points.CA import CA
import numpy.testing as npt
import pytest


def test_CA():
    ca_call = CA({"x": 3, "surface_x": 1, "z": 2, "surface_z": 1})

    npt.assert_almost_equal(ca_call.abs_x, 4)
    npt.assert_almost_equal(ca_call.abs_z, 3)
