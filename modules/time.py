import time
from datetime import datetime, timedelta
def find_time(offset_seconds:int):
    
    dt = datetime(*time.gmtime()[:6])
    
    # Применяем смещение
    dt_shifted = dt + timedelta(seconds=offset_seconds)
    
    # Возвращаем строку в формате HH:MM
    return dt_shifted.strftime('%H:%M')
