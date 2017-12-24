''' Date & Time utility functions. '''

import time
from datetime import datetime


def localize_utc_timestamp(utc_datetime):
    ''' Convert timestamp in UTC to local timezone. '''
    now = time.time()
    offset = datetime.fromtimestamp(now) - datetime.utcfromtimestamp(now)
    return utc_datetime + offset
