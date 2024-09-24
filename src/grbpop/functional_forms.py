import numpy as np
import scipy as sp


def Schechter_log(logL, logLbreak, slope):
    """
        Returns the unnormalized Schechter function
        Expects Lum arguments to be in log scale
    """
    x = 10.**(logL - logLbreak)
    Sch = x**(1.-slope) * np.exp(-x)
    return Sch


def BPL_lum(logL, logLbreak, slopeL, slopeH):
    """
        Returns the unnormalized broken power law function
        Expects Lum arguments to be in log scale
    """
    x = 10.**(logL - logLbreak)
    BPL_func = np.where(x <= 1, x**(1.-slopeL), x**(1.-slopeH))
    return BPL_func


def SH03(z, a=2.37, b=1.8, zm=2, nu=0.178, IMF_norm=0.007422):
    """
        Springel-Hernquist+03 functional form for the cosmic SFR.
        Default are given the values of Vangioni+15.
        Returns an event rate in units of yr-1 Mpc-3
        Note : nu is in units of Msun/yr/Mpc3 and IMF_norm in units of Msun-1
    """
    shape = a * np.exp(b*(z-zm)) / ((a-b) + b*np.exp(a*(z-zm)))
    norm = IMF_norm * nu
    return norm*shape


def HB06(z, z1=0.97, z2=4.48, a=3.44, b=-0.26, c=-7.8, norm=0.0197, IMF_norm=0.007422):
    """
        Hopkins & Beacom 2006
    """
    shape = np.where(z <= z1, (1.+z)**a, (1.+z)**b * (1.+z1)**(a-b))
    shape = np.where(z >= z2, (1.+z)**c * (1.+z2)**(b-c) * (1.+z1)**(a-b), shape)
    return norm * shape


def BExp(z, a=1.1, b=-0.57, zm=1.9, SFR_norm=0.02744, IMF_norm=0.007422, nGRB0=None):
    """
        GRB rate as parametrized by a broken exponential function.
        Default values are chosen as best fit from SFR of Vangioni+15
        If you leave the default SFR_norm and IMF_norm, the result
        will be in units of core-collapses yr-1 Mpc-3.
        IMF_norm is in units of M_sun-1 and converts the CSFRD (in
        units of M_sun yr-1 Mpc-3) to a core-collapse rate density (in
        units of yr-1 Mpc-3).
        SFR_norm is adjusted on the functional form of Springel-Hernquist
        (SH) with the parameter values of Vangioni+15.
    """
    shape = np.where(z <= zm, np.exp(a*z), np.exp(b*z) * np.exp((a-b)*zm))
    if nGRB0 is None:
        norm = IMF_norm * SFR_norm
    else:
        norm = nGRB0
    return norm*shape


def S12(z, Zth=None, n_dens=None):
    """
        Redshift distribution for LGRB assuming they obey a metallicity
        threshold of Zth.
        Note: Zth is actually the fraction Zth/Zsun
    """
    shape = Li08(z)
    if n_dens is not None:
        shape = shape * (1.+z)**n_dens
    if Zth is not None:
        shape = shape * sp.special.gammainc(0.84, Zth**2 * 10**(0.3*z))

    return shape


def Li08(z, a=0.0157, b=0.118, c=3.23, d=4.66, IMF_norm=0.007422):
    """
        Li+08 star formation rate density, normalized to an event rate assuming Salpeter IMF.
        Returns an event rate in units of yr-1 Mpc-3
    """
    return IMF_norm * (a + b*z)/(1 + (z/c)**d)


def BPL_z(z, a=2.07, b=-1.36, zm=3.11, nGRB0=1.3e-9, eta0=1, av_jet_ang=1):
    """
        Returns the LGRB comoving event rate
        The default values are from Wanderman & Piran 2010
        The norm is given by them as well:
        converted to units of yr-1 Mpc-3 (carefull this is the LGRB rate
        not the core-collapse rate, you need to divide by the
        efficiency eta0 and the average opening angle fraction.)
    """
    shape = np.where(z <= zm, (1.+z)**a, (1.+z)**b * (1.+zm)**(a-b))
    norm = nGRB0/(eta0*av_jet_ang)
    return norm*shape


def MD14(z, a=0.015, b=2.7, c=2.9, d=5.6, IMF_norm=0.007422):
    """
        The Star Formation Rate Density from Madau & Dickinson 2014,
        converted to a core-collapse rate assuming Salpeter IMF.
        Returns an CC comoving event rate density in units of
        [yr-1 Mpc-3]
    """
    shape = (1.+z)**b / (1. + ((1.+z)/c)**d)
    norm = IMF_norm*a
    return norm*shape


def Rob15(z, a=0.01376, b=3.26, c=2.59, d=5.68,
    a_err=0.001, b_err=0.21, c_err=0.14, d_err=0.19,
    IMF_norm=0.007422):
    """
        The Star Formation Rate Density from Robertson et al. 2015,
        converted to a core-collapse rate assuming Salpeter IMF.
        Returns an CC comoving event rate density in units of
        [yr-1 Mpc-3]
    """
    shape = (1.+z)**b / (1. + ((1.+z)/c)**d)
    norm = IMF_norm*a
    return norm*shape


def qD06(z, SFR, mod='A', IMF_norm=0.0122):
    """
        LGRB rate of Daigne+06.
        Returns an LGRB comoving event rate density in units of
        [yr-1 Mpc-3]
        Default values for [SFR1, SFR2, SFR3] are:
        a = [0.320, 0.196, 0.175]
        b = [3.30, 4.0, 3.67]
        c = [3.52, 4.0, 3.48]
        d = [23.6, 14.6, 12.6]
        k = [3e-6, 2.5e-6, 8e-7]
    """
    a_s = [0.320, 0.196, 0.175]
    b_s = [3.30, 4.0, 3.67]
    c_s = [3.52, 4.0, 3.48]
    d_s = [23.6, 14.6, 12.6]
    if mod == 'LN':
        k_s = [2.5e-6, 2e-6, 6.3e-7]
    elif mod == 'A':
        k_s = [4e-6, 3.2e-6, 1.2e-6]
    else:
        raise ValueError('mod must be A or LN')

    if SFR not in [1,2,3]:
        raise ValueError('SFR must be an int equal to 1, 2, or 3.')

    shape = a_s[SFR-1]*np.exp(b_s[SFR-1]*z) / (d_s[SFR-1] + np.exp(c_s[SFR-1]*z))
    norm = k_s[SFR-1] * IMF_norm
    return norm*shape


def D06(z, a, b, c, d, IMF_norm=0.0122):
    """
        Core-collapse rate of Daigne+06.
        Returns an core-collapse comoving event rate density in units of
        [yr-1 Mpc-3]
        Default values for [SFR1, SFR2, SFR3] are:
        a = [0.320, 0.196, 0.175]
        b = [3.30, 4.0, 3.67]
        c = [3.52, 4.0, 3.48]
        d = [23.6, 14.6, 12.6]
        k = [3e-6, 2.5e-6, 8e-7]
    """

    shape = a*np.exp(b*z) / (d + np.exp(c*z))
    norm = IMF_norm
    return norm*shape
