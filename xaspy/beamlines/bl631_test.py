import os
import pytest
from bl631 import TrajScan
from bl631 import HYST_scanpair, XMCD_scanpair


path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]
path_to_file = os.path.join(current_directory, "../test_files")


def test_imports():
    TrajScan.path = path_to_file
    TrajScan("31914-001_0001").df
    TrajScan("31914-001_0001").header
    assert TrajScan("31914-001_0001").scantype == "Magnetic Field"


def test_scn_maker():
    HYST_scanpair()
    XMCD_scanpair(1.9, [735, 800])
    pass


def test_warnings():
    # Test if warnings are raised for incorrect edge energy ordering
    with pytest.warns(UserWarning, match="Scan is running backwards in energy."):
        XMCD_scanpair(1.9, [735, 734])

    # Test if warnings are raised for duplicate edge energies
    with pytest.warns(UserWarning, match="Same point for start and stop energy."):
        XMCD_scanpair(1.9, [735, 735])
