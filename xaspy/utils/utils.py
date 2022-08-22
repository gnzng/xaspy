import numpy as np
import pandas as pd


class get_scan_metadata:
    def __init__(self, file):
        if "TrajScan" in file:
            t1 = pd.read_csv(file, skiprows=9, sep="\t", engine="python")
            self.df = t1
            # print the values:
            self.energy(t1)
            self.field(t1)
            self.temperature(t1)
            self.sample_position(t1)

    def energy(self, df):
        """
        get properties of energy steps
        """
        df = df
        arr = np.array(df["Energy"])

        # check if HYST oder XMCD, XMCD field is const
        # HYST field changing check for first 10 datapoints
        step = []
        for n in range(10):
            step.append(np.around(arr[n + 1], 1) - np.around(arr[n], 1))
        step_mean = np.around(np.mean(step), 1)
        step_std = np.around(np.std(step), 1)

        if (step_mean == 0) and (step_std == 0):
            unique_ene = np.unique(np.around(arr, 1))
            meas_type = f"HYST at points {unique_ene}eV"

        elif (step_mean != 0) and (step_std == 0):
            meas_type = f"energy scan with step size {step_mean}eV"

        else:
            meas_type = "unknown measurement type"

        arr_min, arr_max = np.around(np.min(arr), 1), np.around(np.max(arr), 1)
        print(f"{arr_min}eV and {arr_max}eV {meas_type}")

    def field(self, df):
        """
        get properties of magnetic field
        """
        df = df
        arr = np.array(df["Magnet Field"])

        # check if HYST oder XMCD, XMCD field is const
        # HYST field changing check for first 10 datapoints
        step = []
        for n in range(10):
            step.append(np.around(arr[n + 1], 3) - np.around(arr[n], 3))
        step_mean = np.around(np.mean(step), 3)
        step_std = np.around(np.std(step), 3)

        if (step_mean == 0) and (step_std == 0):
            meas_type = "static field(s)"

        elif (step_mean != 0) and (step_std == 0):
            meas_type = f"HYST with step size {step_mean}T"
        else:
            meas_type = "unknown measurement type"

        arr_min, arr_max = np.min(arr), np.max(arr)
        print(f"min: {arr_min}T | max: {arr_max}T {meas_type}")

    def temperature(self, df):
        """
        get properties of temperature sensor Temp B
        """
        df = df
        arr = np.array(df["Temp B"])

        temp = np.around(np.mean(arr), 1)
        print(f"measurement temperature {temp}K")

    def sample_position(self, df):
        """
        get x,y,z coordinates for sample determination, and angle
        """
        df = df

        list_pos = []
        for n in ["X", "Y", "Z", "Theta"]:
            arr_mean = np.mean(np.array(df[n]))
            list_pos.append(np.around(arr_mean, 1))
        print("sample position at [X,Y,Z,Theta]")
        print(list_pos)


def toggle(**kws):
    """
    removed in version 0.2.1:
        toggles cell in Jupyter notebook;
        makes button with label 'a'
    """
    return print("this has been removed in version 0.2.1")


def showspeccom(a):
    """
    a = SPEC file
    returns list with commands/comments #C and #S
    """
    clst = []
    with open(a, "r") as f:
        for line in f:
            if "#C" in line:
                clst.append(line.replace("\n", ""))
            if "#S" in line:
                clst.append(line.replace("\n", ""))
    return clst
