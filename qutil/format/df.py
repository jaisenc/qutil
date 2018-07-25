import re
import pandas as pd

# Dataframe cleaning
from qutil.format.number import fmtl, fmtn, fmtpx


def clean_column_names(df, inplace=True):
    clean_cols = df.columns.str.lower().str.replace(' ', '_')
    clean_cols = [re.sub(r'\W+', '', x) for x in clean_cols]
    clean_cols = [re.sub('__', '_', x) for x in clean_cols]
    df.columns = clean_cols
    return None


def proper_column_names(df, inplace=False, for_display=True):
    """
    Clean column names

    :param df: DataFrame
    :param inplace:
    :return:
    """
    if not inplace:
        df = df.copy()
    clean_cols = df.columns.str.replace(' ', '_')
    clean_cols = [re.sub(r'\W+', '', x) for x in clean_cols]
    clean_cols = [re.sub('__', '_', x) for x in clean_cols]
    clean_cols = [x.title() for x in clean_cols if not (x.isupper())]
    if for_display:
        clean_cols = [x.replace('_', ' ') for x in clean_cols]
    df.columns = clean_cols
    if not inplace:
        return df


def cols_to_datetime(df, keys):
    if isinstance(keys, list):
        for key in keys:
            df[key] = pd.to_datetime(df[key])
    elif keys == 'index':
        df.index = pd.to_datetime(df.index)
    else:
        df[keys] = pd.to_datetime(df[keys])


def color_negative_red_positive_green(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, green otherwise.
    """
    color = 'red' if val < 0 else 'green'
    return 'color: %s; text-align: right;' % color


def render(df, infer_objects=True, idx_fmtl=None, idx_fmth=None, idx_colour=None, idx_fmtpx=None,
           pct_dec=1, num_dec=2):
    """
    Render the DataFrame in style

    :param df: DataFrame
    :param infer_objects:
    :param idx_fmtl:
    :param idx_fmth:
    :param idx_colour: green or red
    :param idx_fmtpx: price
    :param pct_dec: percentage decimal
    :param num_dec: number decimal
    :return:
    """
    if infer_objects:
        df = df.convert_objects(convert_dates=True, convert_numeric=True, copy=True)
    st = df.style
    if idx_fmtl:
        st = st.format(fmtl, subset=idx_fmtl)
    if idx_fmth:
        st = st.format(fmtn, decimal=0, subset=idx_fmth)
    if idx_fmtpx:
        st = st.format(fmtpx, subset=idx_fmtpx)
    if idx_colour:
        st = st.apply(color_negative_red_positive_green(), subset=idx_colour)
    return st


def is_unique_values(df: pd.DataFrame, cols: list) -> dict:
    """
    Check if the columns have unique values
    :param df: DataFrame
    :param cols: list of str
    :return: dict
    """
    out = dict()
    for col in cols:
        if col in df.columns:
            out[col] = df[col].unique().shape[0] == df[col].shape[0]
        else:
            raise ValueError('{} is not a valid column name in the dataframe'.format(col))
    return out
