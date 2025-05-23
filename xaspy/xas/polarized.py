#! python

# imports:

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


def XMCD(
    pdat,
    mdat,
    ene,
    det,
    mon,
    log=False,
    xmin=None,
    xmax=None,
    xsize=10000,
    norm="edge_jump",
    eshift=0,
    alpha=0,
) -> tuple:
    """
    xray magnetic circular dichroism function

    Arguments
    ---------

        pdat    = positive list of pandas objects
        mdat    = negative list of pandas objects
        ene     = energy column name of pandas object
        det     = detector column name of pandas object
        mon     = monitor column -> if no monitor wanted, put 'False'
        log     = boolean, use logarithm for transmission experiments
        xmin    = adjust minimum energy
        xmax    = adjust maximum energy
        xsize   = number of points for interpolation default 10000
                  ! be careful: low point density can lead to ValueErrors due
                  ! to rounding numbers,
                  ! set to None, if no interpolation is needed/wanted
        norm    = choose normalization from ['white_line', 'edge_jump',
                  'pre_edge','None']
        eshift  = shift in energy, added to pdat values, default 0
        alpha   = correction factor as suggested by https://doi.org/10.1107/S1600577520009972
                  C. Piamonteze et al. 2020

    Returns
    --------

    energy, plus_xas, minus_xas, averaged_xas, xmcd

    Notes
    --------

    no notes
    """

    t2pdat = pdat
    t2mdat = mdat
    # photon energies:
    pmin = []
    pmax = []
    for n in range(len(t2pdat)):
        pmin.append(np.min(t2pdat[n][ene]))
        pmax.append(np.max(t2pdat[n][ene]))
    mmin = []
    mmax = []
    for n in range(len(t2mdat)):
        mmin.append(np.min(t2mdat[n][ene]))
        mmax.append(np.max(t2mdat[n][ene]))

    # used energy range:
    if xmin is None:
        xmin = np.max(pmin + mmin)
    if xmax is None:
        xmax = np.min(pmax + mmax)

    # energy interpolation range:
    if xsize is None:
        xx = np.array(t2pdat[n][ene])
    else:
        xx = np.linspace(xmin + 0.1, xmax - 0.1, xsize)
    t3pdat = []  # list to addinterpolated
    for n in range(len(t2pdat)):
        v1 = np.array(t2pdat[n][ene])
        if mon is not False:
            v21 = np.array(t2pdat[n][det])
            v22 = np.array(t2pdat[n][mon])
            if log is True:
                v2 = np.log(v22 / v21 - alpha / 2)
            else:
                v2 = v21 / v22 - alpha / 2
        if mon is False:
            v2 = np.array(t2pdat[n][det])
        if xsize is None:
            t3pdat.append(v2)
        else:
            try:
                t3pdat.append(interpolate.interp1d(v1, v2)(xx + float(eshift) / 1000))
            except Exception:
                raise ValueError(
                    "error at plus helicity; check interpolation range "
                    + "eshift to large for interpolation range? "
                    + "max Eshift ca. 100meV."
                )
    t3mdat = []
    for n in range(len(t2mdat)):
        v1 = np.array(t2mdat[n][ene])
        if mon is not False:
            v21 = np.array(t2mdat[n][det])
            v22 = np.array(t2mdat[n][mon])
            if log is True:
                v2 = np.log(v22 / v21 - alpha / 2)
            else:
                v2 = v21 / v22 - alpha / 2
        if mon is False:
            v2 = np.array(t2mdat[n][det])
        if xsize is None:
            t3mdat.append(v2)
        else:
            try:
                t3mdat.append(interpolate.interp1d(v1, v2)(xx))
            except Exception:
                raise ValueError(
                    "error at minus helicity;", "check interpolation range."
                )

    # merging same helicities:
    t4pdat = []  # all from +hel merged
    for k in range(0, len(xx)):
        t4pdat.append(
            np.sum([t3pdat[s][k] for s in range(len(t3pdat))]) / int(len(t3pdat))
        )
    t4mdat = []  # all from -hel merged
    for k in range(0, len(xx)):
        t4mdat.append(
            np.sum([t3mdat[s][k] for s in range(len(t3mdat))]) / int(len(t3mdat))
        )
    t5pdat = np.array(t4pdat)
    t5mdat = np.array(t4mdat)
    pdm = t5pdat / t5mdat  # plus signal divided by minus signal

    # correlation of plus and minus signal via two linear functions:
    corrpre = np.poly1d(
        np.polyfit(xx[: int(len(xx) * 0.1)], pdm[: int(len(xx) * 0.1)], 1)
    )
    corrpost = np.poly1d(
        np.polyfit(
            xx[int(len(xx) - len(xx) * 0.1) :],
            pdm[int(len(xx) - len(xx) * 0.1) :],
            1,
        )
    )
    x1 = xx[2]
    x2 = xx[-2]
    cfy1 = corrpre(x1)  # corr intens. at
    cfy2 = corrpost(x2)

    # correlated signal with pmerged:
    t5mdat = t5mdat * (
        cfy1 - x1 * (cfy1 - cfy2) / (x1 - x2) + xx * (cfy1 - cfy2) / (x1 - x2)
    )
    #####
    xas = (t5pdat + t5mdat) / 2

    # Subtracting backgrounds now:
    linbkg = np.poly1d(
        np.polyfit(xx[: int(len(xx) * 0.1)], xas[: int(len(xx) * 0.1)], 1)
    )(xx)
    xas = xas - linbkg
    pxas = t5pdat - linbkg
    mxas = t5mdat - linbkg

    # normalization:

    norm_opt = ["white_line", "edge_jump", "pre_edge", "None", None]

    # choose factor:

    try:
        if norm == "white_line":
            norm_factor = float(np.max(xas))
        elif norm == "edge_jump":
            last_values = int(len(xx) * 0.05)
            norm_factor = np.mean(xas[:-last_values])

        elif norm == "pre_edge":
            last_values = int(len(xx) * 0.02)
            norm_factor = np.mean(xas[last_values:])

        elif norm in ["None", None]:
            norm_factor = 1.0

    except Exception:
        raise ValueError("normalization not clear, use {}".format(norm_opt))

    xas = np.array(xas) / norm_factor
    pxas = np.array(pxas) / norm_factor
    mxas = np.array(mxas) / norm_factor
    xmcd = np.array(pxas - mxas)

    return xx, pxas, mxas, xas, xmcd


###


# HSYT functions:

# mHYST
#
# new in 0.1.10, developed for many (mHYST) loops in one file:
# added log option in 0.1.13

# added plot together in 0.2.2 and removed typo function,
# automated ene_cut

# version 0.3.0 generalized for more possible magnetic field header names


class mHYST:
    """
    --- class was significantly changed with update 0.3.0 ---
    Arguments
    ---------
        df      = pandas dataframe of multiple Hyst loops
        fld     = field column name of pandas object df
        ene     = energy column name of pandas object df
        det     = detector column name of pandas object
        mon     = monitor column -> if no monitor wanted, put 'False'
        ratio   = either divide higher/lower or lower/higher energy
        log     = neg. logarithm for tranmission experiments, default False
    Returns
    --------
    Nothing, but contains multiple functions:
        - average_loops(), average specific loops
        - plot_separated(onefigure=False), plots all loops separated,
          if onefigure=True,
          it will plot every loop in one figure
    Notes
    --------
    no notes
    """

    def __init__(self, df, fld, ene, det, mon, ratio="higher/lower", log=False):
        import pandas as pd

        header = list(df)
        # CHECKS:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("df is not a pd.DataFrame type")

        for n in [fld, ene, det]:
            if n not in header:
                raise ValueError(
                    "{} is not a column name of the pd.DataFrame".format(n)
                )

        if mon == "False":
            mon = False

        if mon is not False:
            if mon not in header:
                raise ValueError(
                    "{} is not a column name of the pd.DataFrame".format(mon)
                )

        # CHECKS end

        t1 = df
        self.df = df
        self.fld = fld

        # find energy for cutoff:

        min_ene = np.around(np.min(df[ene]), 2)
        max_ene = np.around(np.max(df[ene]), 2)
        ene_cut = np.around((max_ene - min_ene) / 2 + min_ene, 2)

        # save in class:
        self.min_ene = min_ene
        self.max_ene = max_ene

        try:
            # t2 at higher energy -> usually l2 edge, l3 at lower energies:
            # normalizing signal to clock
            t2, t3 = t1[t1[ene] >= ene_cut], t1[t1[ene] <= ene_cut]
            t2 = t2.reset_index()
            t3 = t3.reset_index()
        except Exception:
            raise ValueError("energy cut off failed")

        try:
            if mon is False:
                print("no monitor selected")
                t2["normlzd"] = t2[det]
                t3["normlzd"] = t3[det]
            elif log is True:
                t2["normlzd"] = -np.log(t2[det] / t2[mon])
                t3["normlzd"] = -np.log(t3[det] / t3[mon])
            else:
                t2["normlzd"] = t2[det] / t2[mon]
                t3["normlzd"] = t3[det] / t3[mon]
        except Exception:
            raise ValueError("normalization failed")

        # now use t2 to continue algortithm
        try:
            if ratio == "higher/lower":
                t2["divided"] = t2["normlzd"] / t3["normlzd"]
            elif ratio == "lower/higher":
                t2["divided"] = t3["normlzd"] / t2["normlzd"]
        except Exception:
            raise ValueError("please choose a valid ratio")

        try:
            len_t2 = len(t2)
            self.t2 = t2
            self.slope_ct = self.slope_count(t2, fld).astype(int)
            self.len_per_loop = (len_t2 / self.slope_ct).astype(int)

        except Exception:
            raise ValueError(
                "Could not build Hysteresis loop. Different number of scans? "
            )

    def slope_count(self, df, fld):
        """
        function returns the number of slopes in HYST loops
        """
        df, fld = df, fld
        magfield = np.array(df[fld])
        mag_sign = np.sign(magfield)
        signchange = ((np.roll(mag_sign, 1) - mag_sign) != 0).astype(int)
        return (np.sum(signchange) / 4).astype(int)

    def plot_seperated(self):
        raise SyntaxError("use plot_separated()")

    def plot_separated(self, onefigure=False):
        if onefigure is False:
            for n in range(self.slope_ct):
                plt.figure()
                plt.title("loop {}".format(n))
                plt.plot(
                    self.t2[self.fld][
                        n * self.len_per_loop : (n + 1) * self.len_per_loop
                    ],
                    self.t2["divided"][
                        n * self.len_per_loop : (n + 1) * self.len_per_loop
                    ],
                )
                plt.xlabel("magnetic field [arb. units]")
                plt.ylabel("absorption [arb. units]")
                plt.show()
        elif onefigure is True:
            plt.figure()
            for n in range(self.slope_ct):
                plt.plot(
                    self.t2[self.fld][
                        n * self.len_per_loop : (n + 1) * self.len_per_loop
                    ],
                    self.t2["divided"][
                        n * self.len_per_loop : (n + 1) * self.len_per_loop
                    ],
                    label="{}".format(n),
                )
            plt.xlabel("magnetic field [arb. units]")
            plt.ylabel("absorption [arb. units]")
            plt.legend(title="loop nr.")
            plt.show()
        else:
            raise ValueError("please use onefigure=True/False")

    def average_loops(self, av_list, return_data=False):
        """
        takes number of loops, check before with plot_seperated()
        set return_data to True to get data as tuple(field, signal)
        non plot mode otherwise returns plot of average loops
        """
        self.av_list = av_list
        toaverage = []
        for n in av_list:
            toaverage.append(
                self.t2["divided"][n * self.len_per_loop : (n + 1) * self.len_per_loop]
            )
        averaged = np.mean(toaverage, axis=0)
        self.std = np.std(toaverage, axis=0)
        field = self.t2[self.fld][: self.len_per_loop]

        if return_data is False:
            plt.figure()
            plt.title(f"average loops {*av_list, }")
            plt.plot(field, averaged)
            plt.show()

        elif return_data is True:
            return (np.array(field), np.array(averaged))
        else:
            raise ValueError("return_data mode not clear. use False or True")


def HYST3en(df, fld, ene, det, mon, Epre, Eedg1, Eedg2):
    """
    HYST : edge/pre_edge
    VEKMAG compatible
    df     = takes pandas data frame
    fld    = column name of field values
    ene    = column name of energy values
    det    = column name of detector values
    mon    = column name of monitor
    Epre    = energy of pre edge point
    Eedg1   = energy of edge point 1
    Eedg2   = energy of edge point 2
    """
    df = df
    hyst1 = []
    hyst2 = []
    field1 = []
    for n in np.arange(-6.8, 6.8, 0.1):
        n = np.around(n, 1)
        t1 = df[np.around(df[ene], 1) == Eedg1]
        t1 = t1[np.around(t1[fld], 1) == n]
        t11 = np.mean(t1[det] / t1[mon])
        t2 = df[np.around(df[ene], 1) == Eedg2]
        t2 = t2[np.around(t2[fld], 1) == n]
        t12 = np.mean(t2[det] / t2[mon])
        t1 = df[np.around(df[ene], 1) == Epre]
        t1 = t1[np.around(t1[fld], 1) == n]
        t22 = np.mean(t1[det] / t1[mon])
        hyst1.append(t11 / t22)
        hyst2.append(t12 / t22)
        field1.append(n)
    ############
    return field1, hyst1, hyst2


# sumrules functions
def sumrules_function(xx, xas00, xmcd, px, nh):
    """
    xx = global energy scale
    xas00 = xas - stepfunction
    xmcd = xmcd
    px = point in energy for p value
    nh = number of electron holes"""
    r = np.max(np.cumsum(xas00))
    q = np.max(np.cumsum(xmcd))
    p = np.cumsum(xmcd)[list(np.around(xx, 2)).index(px)]
    # print(np.max(np.cumsum(np.linspace(0,1,steps)))/steps)
    lz = nh * 2 * q / (3 * r)
    sz = nh * (3 * p - 2 * q) / (2 * r)
    return sz, lz


# old sum rule function, please do not use, thanks
def LDS(xx, xmcd, px):
    """
    xx = global energy scale
    xmcd = xmcd
    px = point in energy for p value"""
    q = np.absolute(np.cumsum(xmcd))[-1]
    p = np.absolute(np.cumsum(xmcd)[list(np.around(xx, 2)).index(px)])
    # print(q,p)
    lds = (4 / 3) * q / (3 * p - 2 * q)
    return lds


def orbital_to_spin_ratio(xmcd=None, xp=None, xq=None, group=None, orbital="3d"):
    """
    function for orbital to spin ratio from xmcd without <Tz> term

    Arguments
    ---------

    xmcd    = xmcd spectra as np.array if group is none
    xp,xq   = index of XMCD for dividing (xp) and end of XMCD (xq)
              default values xp = len/2 and xq = last value
    group   = group of a sample
    orbital = probed orbital 3d or 4f

    Returns
    --------

    orbital to spin ratio attached to group if group was provided

    if no group was provided prints orbital to spin ratio

    Notes
    --------

    no notes
    """

    if xmcd is not None:
        xmcd = xmcd

    elif group is not None:
        xmcd = group.xmcd
    else:
        raise ValueError("insert XMCD as group or numpy array")

    if xp is None:
        xp = int(len(xmcd) / 2)

    A = np.cumsum(xmcd[:xp])[-1]
    B = np.cumsum(xmcd[xp:xq])[-1]

    def lds_self_3d(A, B):
        return (2 / 3) * ((A + B) / (A - 2 * B))

    def lds_self_4f(A, B):
        return (A + B) / ((A - (3 / 2) * B))

    if orbital == "3d":
        if group is None:
            return lds_self_3d(A, B)

        if group is not None:
            group.lds = lds_self_3d(A, B)

    elif orbital == "4f":
        if group is None:
            return lds_self_4f(A, B)

        if group is not None:
            group.lds = lds_self_4f(A, B)

    else:
        raise ValueError("choose a valid probed orbital: 3d or 4f")


def Lz(
    xmcd, xas, c=1, l=2, nh=1, tz=None, last_number_xas=1, last_number_xmcd=1
) -> float:
    """
    sum rule taken from:
        Carra, P., Thole, B. T., Altarelli, M., & Wang, X. (1993).
        X-ray circular dichroism and local magnetic fields.
        Phys Rev Lett, 70(5), 694-697.
        doi:10.1103/PhysRevLett.70.694
    xmcd = numpy array of XMCD as in mu_p - mu_m
    xas  = numpy array of step function corrected XAS as in (mu_p + mu_m)/2
    c    = s:0, p:1, d:2, f:3, initial orbital
    l    = s:0, p:1, d:2, f:3, final orbital
    nh   = number of holes
    tz   = can be provided, but will not be used for calculating orbital
           moment
    """
    tz = tz

    factor = (1 / 2) * ((l * (l + 1)) - (c * (c + 1)) + 2) / ((l * (l + 1)))
    # xas is (mu_p + mu_m)/2
    lz = (nh / factor) * (
        np.cumsum(xmcd)[-last_number_xmcd] / (3 * np.cumsum(xas)[-last_number_xas])
    )
    return float(lz)


def Sz(
    xmcd,
    xas,
    c=1,
    l=2,
    nh=1,
    tz=0,
    edge_div=None,
    last_number_xas=1,
    last_number_xmcd=1,
) -> float:
    """
    sum rule taken from:
        Carra, P., Thole, B. T., Altarelli, M., & Wang, X. (1993).
        X-ray circular dichroism and local magnetic fields.
        Phys Rev Lett, 70(5), 694-697.
        doi:10.1103/PhysRevLett.70.694
    xmcd = numpy array of XMCD as in mu_p - mu_m
    xas  = numpy array of step function corrected XAS as in (mu_p + mu_m)/2
    c    = s:0, p:1, d:2, f:3, initial orbital
    l    = s:0, p:1, d:2, f:3, final orbital
    nh   = number of holes
    tz   = magnetic dipole term
    edge_div = if None, middle of spectrum, relative shift to calculated
               middle of spectrum based on index number
    """
    if edge_div is None:
        x_div = int(len(xmcd) / 2)
    else:
        x_div = int(len(xmcd) / 2) + edge_div

    tz_part = (
        (
            l * (l + 1) * (l * (l + 1) + 2 * c * (c + 1) + 4)
            - ((3 * (c - 1) ** 2) * (c + 2) ** 2)
        )
        / (6 * l * c * (l + 1) * nh)
    ) * tz

    spec_part = (
        np.cumsum(xmcd[:x_div])[-1]
        - (((c + 1) / c) * np.cumsum(xmcd[x_div:])[-last_number_xmcd])
    ) / (3 * np.cumsum(xas)[-last_number_xas])

    sz = (spec_part - tz_part) * ((3 * c * nh) / ((l * (l + 1) - 2 - c * (c + 1))))
    return float(sz)


def Lz_cumsum(
    xmcd_cumsum: np.ndarray,
    xas_cumsum: np.ndarray,
    c: int = 1,
    l: int = 2,
    nh: float = 1.0,
    tz=None,
    last_number_xas=1,
    last_number_xmcd=1,
) -> float:
    """
    same as Lz, but using cumsum instead of calculating it in the function
    sum rule taken from:
        Carra, P., Thole, B. T., Altarelli, M., & Wang, X. (1993).
        X-ray circular dichroism and local magnetic fields.
        Phys Rev Lett, 70(5), 694-697.
        doi:10.1103/PhysRevLett.70.694
    xmcd_cumsum = numpy array of XMCD as in mu_p - mu_m
    xas_cumsum  = numpy array of step function corrected XAS as in (mu_p + mu_m)/2
    c    = s:0, p:1, d:2, f:3, initial orbital
    l    = s:0, p:1, d:2, f:3, final orbital
    nh   = number of holes
    tz   = can be provided, but will not be used for calculating orbital
           moment
    """
    tz = tz

    factor = (1 / 2) * ((l * (l + 1)) - (c * (c + 1)) + 2) / ((l * (l + 1)))
    # xas is (mu_p + mu_m)/2
    lz = (nh / factor) * (
        xmcd_cumsum[-last_number_xmcd] / (3 * xas_cumsum[-last_number_xas])
    )
    return float(lz)


def Sz_cumsum(
    xmcd_cumsum: np.ndarray,
    xas_cumsum: np.ndarray,
    c: int = 1,
    l: int = 2,
    nh: float = 1.0,
    tz: float = 0.0,
    edge_div=None,
    last_number_xas=1,
    last_number_xmcd=1,
) -> float:
    """
    same as Sz, but using cumsum instead of calculating it in the function
    sum rule taken from:
        Carra, P., Thole, B. T., Altarelli, M., & Wang, X. (1993).
        X-ray circular dichroism and local magnetic fields.
        Phys Rev Lett, 70(5), 694-697.
        doi:10.1103/PhysRevLett.70.694
    xmcd_cumsum = numpy array of XMCD as in mu_p - mu_m
    xas_cumsum  = numpy array of step function corrected XAS as in (mu_p + mu_m)/2
    c    = s:0, p:1, d:2, f:3, initial orbital
    l    = s:0, p:1, d:2, f:3, final orbital
    nh   = number of holes
    tz   = magnetic dipole term
    edge_div = if None, middle of spectrum, relative shift to calculated
               middle of spectrum based on index number
    """
    if edge_div is None:
        x_div = int(len(xmcd_cumsum) / 2)
    else:
        x_div = int(len(xmcd_cumsum) / 2) + edge_div

    tz_part = (
        (
            l * (l + 1) * (l * (l + 1) + 2 * c * (c + 1) + 4)
            - ((3 * (c - 1) ** 2) * (c + 2) ** 2)
        )
        / (6 * l * c * (l + 1) * nh)
    ) * tz

    spec_part = (
        xmcd_cumsum[:x_div][-1]
        - (
            ((c + 1) / c)
            * ((xmcd_cumsum[x_div:] - xmcd_cumsum[x_div])[-last_number_xmcd])
        )
    ) / (3 * xas_cumsum[-last_number_xas])

    sz = (spec_part - tz_part) * ((3 * c * nh) / ((l * (l + 1) - 2 - c * (c + 1))))
    return float(sz)
