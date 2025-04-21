import os
import pytest
from xaspy.beamlines.bl631 import TrajScan
from xaspy.beamlines.bl631 import HYST_scanpair, XMCD_scanpair

path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]
path_to_file = os.path.join(current_directory, "test_files")


def test_imports():
    TrajScan.path = path_to_file
    assert len(TrajScan("31914-001_0001").df) == 12224
    assert len(TrajScan("31914-001_0001").header) == 10
    assert TrajScan("31914-001_0001").scantype == "Magnetic Field"


def test_scn_maker():
    HYST_scanpair()
    XMCD_scanpair(1.9, [735, 800])


def test_warnings():
    # Test if warnings are raised for incorrect edge energy ordering
    with pytest.warns(UserWarning, match="Scan is running backwards in energy."):
        XMCD_scanpair(1.9, [735, 734])

    # Test if warnings are raised for duplicate edge energies
    with pytest.warns(UserWarning, match="Same point for start and stop energy."):
        XMCD_scanpair(1.9, [735, 735])


def test_legacy_imports_raises_errors():
    from xaspy.readin.bl631 import (
        count_lines,
        SS_indexing,
        TS_indexing,
        SigScan,
        TrajScan,
    )

    # Test if the legacy functions raise an error
    with pytest.raises(
        ValueError, match="beam line 6.3.1 functions now in xaspy.beamlines.bl631"
    ):
        count_lines("test.txt")
    with pytest.raises(
        ValueError, match="beam line 6.3.1 functions now in xaspy.beamlines.bl631"
    ):
        SS_indexing()
    with pytest.raises(
        ValueError, match="beam line 6.3.1 functions now in xaspy.beamlines.bl631"
    ):
        TS_indexing()
    with pytest.raises(
        ValueError, match="beam line 6.3.1 functions now in xaspy.beamlines.bl631"
    ):
        SigScan("test")
    with pytest.raises(
        ValueError, match="beam line 6.3.1 functions now in xaspy.beamlines.bl631"
    ):
        TrajScan("test")
