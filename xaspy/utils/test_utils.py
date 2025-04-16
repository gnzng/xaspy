import pytest
import numpy as np
from utils.utils import cumtrapz


def test_cumtrapz_basic():
    """Test basic functionality of cumtrapz with constant signal."""
    signal = np.ones(5)
    result = cumtrapz(signal)
    expected = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    np.testing.assert_allclose(result, expected)


def test_cumtrapz_with_energy():
    """Test cumtrapz with custom energy values."""
    signal = np.array([0, 1, 2, 3, 4])
    energy = np.array([0, 1, 3, 5, 6])
    result = cumtrapz(signal, energy)
    expected = np.array([0.0, 0.5, 3.5, 8.5, 12.0])
    np.testing.assert_allclose(result, expected)


def test_cumtrapz_linear():
    """Test cumtrapz with linearly increasing signal."""
    signal = np.array([0, 1, 2, 3, 4])
    result = cumtrapz(signal)
    expected = np.array([0.0, 0.5, 2.0, 4.5, 8.0])
    np.testing.assert_allclose(result, expected)


def test_cumtrapz_empty():
    """Test cumtrapz with empty array."""
    signal = np.array([])
    with pytest.raises(ValueError):
        cumtrapz(signal)


def test_cumtrapz_single_value():
    """Test cumtrapz with a single value."""
    signal = np.array([5.0])
    result = cumtrapz(signal)
    expected = np.array([0.0])
    np.testing.assert_allclose(result, expected)


def test_cumtrapz_dtype():
    """Test that output preserves input dtype."""
    signal = np.ones(5)
    result = cumtrapz(signal)
    assert isinstance(result, np.ndarray)


def test_cumtrapz_not_increasing_at_the_end():
    """Test cumtrapz with a non-increasing signal at the end."""
    signal = np.array([1, 2, 3, 2, 1, 0.0, 0.0, 0.0])
    result = cumtrapz(signal)
    expected = np.array([0.0, 1.5, 4.0, 6.5, 8.0, 8.5, 8.5, 8.5])
    np.testing.assert_allclose(result, expected)
