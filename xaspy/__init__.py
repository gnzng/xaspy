from ._version import __name__, __date__, __version__, __authors__


class info:
    """
    simple class for printing package info all at once
    """

    def __init__(self):
        print("name:", "\t", __name__)
        print("updated:", "\t", __date__)
        print("version:", "\t", __version__)
        print("authors:", "\t", __authors__)
