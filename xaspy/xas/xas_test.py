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
    y = np.ones_like(x)
    step(x, y, 5)
