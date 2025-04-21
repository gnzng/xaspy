import numpy as np
import pandas as pd
import pytest
import os

# imports from xaspy:

from xaspy.xas.polarized import (
    orbital_to_spin_ratio,
    mHYST,
)
from xaspy.xas.xas import group

# HYST tests:

path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]
path_to_file = os.path.join(
    current_directory, "test_files/pd_dataframe_hyst_example1.csv"
)

# Read the DataFrame from the CSV file
df = pd.read_csv(path_to_file)


def test_import_df():
    # nr: 'TrajScan31914-001_0001.txt'
    assert isinstance(df, pd.DataFrame)


hystclass = mHYST(
    df, "Magnet Field", "Energy", "LY", "Clock", ratio="lower/higher", log=True
)


def test_hyst_from_df():
    assert hystclass
    assert isinstance(
        hystclass.average_loops([n for n in range(1, 16)], return_data=True),
        tuple,
    )


def test_raise_value_error_bc_wrong_column_name():
    with pytest.raises(ValueError):
        mHYST(
            df,
            "_non_existent_column",
            "Energy",
            "LY",
            "Clock",
            ratio="lower/higher",
            log=True,
        ).average_loops([n for n in range(1, 16)], return_data=True)


# XMCD tests


testgroup = group()

path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]


xmcd_csv_path = os.path.join(current_directory, "test_files/xmcd_co.csv")

# Read the xmcd data from the CSV file
testgroup.xmcd = pd.read_csv(xmcd_csv_path).to_dict(orient="list")["0"]

testxmcd = testgroup.xmcd


def test_errors():
    #
    # test if errors are right
    #
    with pytest.raises(ValueError):
        orbital_to_spin_ratio(xmcd=testxmcd, orbital="11s")
    with pytest.raises(ValueError):
        orbital_to_spin_ratio(orbital="11s")


def test_orbital_to_spin_ratio():
    #
    # test if orbital_to_spin values yields real values
    #

    # test for xmcd testset:
    assert np.around(0.10483034490920523, 1) == np.around(
        orbital_to_spin_ratio(xmcd=testxmcd, group=None, xp=2750, orbital="3d"),
        1,
    )

    # test for group:
    orbital_to_spin_ratio(xmcd=None, group=testgroup, xp=2750, orbital="3d")
    assert np.around(0.10483034490920523, 1) == np.around(testgroup.lds, 1)
