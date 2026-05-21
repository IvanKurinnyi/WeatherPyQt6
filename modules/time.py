import time
from datetime import datetime, timedelta
def find_time(offset_seconds:int):
    
    dt = datetime(*time.gmtime()[:6])
    
    dt_shifted = dt + timedelta(seconds=offset_seconds)
    
    return dt_shifted.strftime('%H:%M')
