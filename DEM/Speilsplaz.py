
import pytz
from datetime import datetime, timedelta


def get_month_dates():
    ist_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    today = ist_date.today()
    today = str(today).split(' ')[0]
    startdate = str(today).split('-')
    MonthStartDate = str(startdate[0]) + '-' + str(startdate[1]) + '-01'
    return (today, MonthStartDate)



print(get_month_dates())