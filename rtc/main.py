from machine import Pin, I2C
from ds3231 import DS3231

i2c = I2C(id=0, sda=Pin(20), scl=Pin(21), )

ds = DS3231(i2c)

def set_date():
    year = 2024 # Can be yyyy or yy format
    month = 7
    mday = 28
    hour = 19 # 24 hour format only
    minute = 38
    second = 00 # Optional
    weekday = 7 # Optional

    datetime = (year, month, mday, hour, minute, second, weekday)
    ds.datetime(datetime)

# rtc = RTC()
# rtc.datetime(ds.datetime)
print(ds.datetime())
