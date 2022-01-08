import pandas as pd

from .short import LibraryShortener


def read_bookings_csv(csv_path: str, short_path: str) -> pd.DataFrame:
    """Read bookings csv into dataframe and convert columns to correct type."""

    df = pd.read_csv(csv_path, sep=';', index_col=0)

    df.index = pd.to_datetime(df.index, unit='s')
    df.index = df.index.tz_localize('GMT').tz_convert('Europe/Berlin')
    df.period_start = pd.to_timedelta(df.period_start.str.cat([':00'] * len(df)))
    df.period_end = pd.to_timedelta(df.period_end.str.cat([':00'] * len(df)))
    df.day = pd.to_datetime(df.day)
    df.bookable = df.bookable == 1

    # Offset of timestamp and booking day. This should range from -1 day to 6 hours.
    df['offset'] = (df.index.tz_localize(None) - df.day).dt.floor('T')

    shortener = LibraryShortener(short_path)
    df.library = df.library.apply(shortener.get_name)

    return df
