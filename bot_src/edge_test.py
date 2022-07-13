from edge import look_edges_db
import pytest


def test_if_str_is_returned():
    assert isinstance(look_edges_db('Co'),str)
    assert isinstance(look_edges_db('Co','K'),str)
    assert isinstance(look_edges_db('Co','L3'),str)
    assert isinstance(look_edges_db('Co','L'),str)

def test_raises_error():
    with pytest.raises(ValueError):
        look_edges_db('magnetesindcool')

