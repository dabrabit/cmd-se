from datetime import datetime
from dateutil.relativedelta import relativedelta

dt0 = datetime(year=2012, month=11, day=26)
dt1 = datetime(year=2015, month=12, day=31)

while dt0 <= dt1:
    print(dt0.month)