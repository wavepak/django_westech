import os, time
from datetime import datetime as DT

# Time zone setup
os.environ['TZ'] = 'US/Pacific'
time.tzset()


# Utility functions and main
def _tstamp():
    """
    formatted time stamp
    """
    ts = time.time()
    # time.strftime('%X %x %Z')
    return '[{:s}]'.format(DT.fromtimestamp(ts).strftime('%m-%d %H:%M:%S'))
