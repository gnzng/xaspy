from xaspy.xas.xas import group
from xaspy.xas.backgrounds import step
import numpy as np
import pytest


@pytest.fixture
def xmcd_141():
    xmcd = group("test", lds=0.7)
    xmcd.energy = np.linspace(0, 1, 5000)
    xmcd.energy_interp = np.linspace(0, 1, 10000)
    xmcd.plus_xas = np.array([1, 2, 3, 4, 5])
    xmcd.minus_xas = np.array([1, 2, 3, 4, 5])
    return xmcd


def test_group_existence(xmcd_141):
    assert xmcd_141 is not None, "group should be existent"


def test_lds_value(xmcd_141):
    assert xmcd_141.lds == 0.7, "should be 0.7"


def test_name(xmcd_141):
    assert xmcd_141.__name__ == "test", "name should be test"


def test_step():
    x = np.linspace(0, 10, 100)
    a = 1.0
    tp = 5.0
    slope = 2.0

    # Test without slope
    result_no_slope = step(a, tp, x)
    assert result_no_slope is not None, "Result should not be None"
    assert len(result_no_slope) == len(x), "Result length should match input length"

    # Test with slope
    result_with_slope = step(a, tp, x, slope=slope)
    assert result_with_slope is not None, "Result should not be None"
    assert len(result_with_slope) == len(x), "Result length should match input length"

    # Test turning point outside range
    with pytest.warns(Warning, match="Turning point \\(tp\\) is outside the range of the energy array."):
        step(a, 15.0, x)

    # Test invalid slope
    with pytest.raises(ValueError, match="slope factor has to be float, e.g. 2.0, 2.3, etc."):
        step(a, tp, x, slope="invalid")
