import numpy as np


def fmtp(number, decimals=2):
    """
    Formatting helper - percent: 0.52 -> 52.00%
    """
    if np.isnan(number):
        return '-'
    return format(number, '.{}%'.format(decimals))


def fmtpn(number, decimals=2):
    """
    Formatting helper - percent no % sign: 0.523 -> 52.30
    """
    if np.isnan(number):
        return '-'
    return format(number * 100, '.{}f'.format(decimals))


def fmtph(number, decimals=2):
    """
    Formatting helper - percent no % sign: 52.30 -> 52.30%
    """
    if np.isnan(number):
        return '-'
    return format(number / 100, '.{}%'.format(decimals))


def fmtn(number, decimals=2):
    """
    Formatting helper - float
    """
    if np.isnan(number):
        return '-'
    return format(number, '.{}f'.format(decimals))


def fmti(number):
    """
    Formatting helper - int
    :param number:
    :return:
    """
    if np.isnan(number):
        return '-'
    return format(number, '.0f')


def fmtth(x, decimal=0):
    if np.isnan(x):
        return '-'
    return '{0:.{1}f}'.format(x, decimal)


def fmtpx(x):
    return fmtth(x, decimal=2)


def fmtl(x):
    """
    Formatting helper - large number

    :param x:
    :return:
    """
    if np.isnan(x):
        return '-'
    elif abs(x) >= 1000000000:
        return '{:,.0f} Bln'.format(x / 1000000000)
    elif abs(x) >= 1000000:
        return '{:,.0f} Mln'.format(x / 1000000)
    elif abs(x) >= 1000:
        return '{:,.0f} k'.format(x / 1000)
    else:
        return '{:,.0f}'.format(x)
