# OLD namespace -> moved to beamlines


def raise_error():
    raise ValueError("beam line 6.3.1 functions now in xaspy.beamlines.bl631")


def count_lines(file):
    raise_error()


def SS_indexing():

    raise_error()


def TS_indexing():

    raise_error()


class SigScan:
    # "bl_comp" working at beam line computer with access to all scans
    path = "bl_comp"
    # import using the beam line computer

    def __init__(self, string: str):
        raise_error()


class TrajScan:
    # "bl_comp" working at beam line computer with access to all scans
    path = "bl_comp"
    # import using the beam line computer

    def __init__(self, string: str):
        raise_error()
