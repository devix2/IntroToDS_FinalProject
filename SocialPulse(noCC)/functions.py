"""
    Questa doveva essere una libreria di funzioni
    Alla fine abbiam fatto quasi tutto dentro a make_dataset.py

"""


def appforth(df, line):
    """
    Function that adds a line at the top of a dataframe
    """
    df.loc[-1]=line
    df.index = df.index + 1  # shifting index
    df = df.sort_index()  # sorting by index
    return df