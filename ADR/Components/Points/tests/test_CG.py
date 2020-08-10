from ADR.Components.Points.CG import CG
import numpy.testing as npt
import pytest


def test_CG():
    cg_call = CG({"x": 3, "y": 1, "z": 2})

    npt.assert_almost_equal(cg_call.x, 3)
    npt.assert_almost_equal(cg_call.y, 1)
    npt.assert_almost_equal(cg_call.z, 2)
