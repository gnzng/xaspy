from sre_compile import isstring
from sys import exc_info
from edge import look_edges_db
import pytest


assert isstring(look_edges_db('Co'))
assert isstring(look_edges_db('Co','K'))
assert isstring(look_edges_db('Co','L3'))
assert isstring(look_edges_db('Co','L'))

with pytest.raises(ValueError) as exc_info:
    look_edges_db('magnetesindcool')
    