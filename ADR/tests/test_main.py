from ADR.main import adr_analyser
import numpy.testing as npt


def test_adr_analyser():
    npt.assert_almost_equal(adr_analyser(plot=False), 193.749, decimal=3)
