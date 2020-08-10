from ADR.Components.Points.TPR import TPR
import numpy.testing as npt
import pytest


def test_TPR():
    tpr_call = TPR({"x": 3, "y": 1, "z": 2})

    npt.assert_almost_equal(tpr_call.x, 3)
    npt.assert_almost_equal(tpr_call.y, 1)
    npt.assert_almost_equal(tpr_call.z, 2)
