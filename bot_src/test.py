from sre_compile import isstring
from edge import look_edges_db


print(isstring(look_edges_db('Co')))
print(isstring(look_edges_db('Co','K')))
print(isstring(look_edges_db('Co','L3')))
print(isstring(look_edges_db('Co','L')))
#print(isstring(look_edges_db('Co','P')))
#print(iserr(look_edges_db('magnetesindcool')))