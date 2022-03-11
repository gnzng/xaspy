from ._version import __name__, __date__, __version__,__authors__

class info():
    """
    simple class for printing package info all at once
    """
    def __init__(self):
        print( __name__)
        print(__date__) 
        print(__version__)
        print(__authors__)