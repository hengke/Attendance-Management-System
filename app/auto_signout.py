import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from datetime import datetime, timedelta, time

import django
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()

from app.models import Signingin, Employee


def auto_signout(hh):
    # from app.models import Signingin
    all_Signingin = Signingin.objects.filter(end_time=None)
    cur_datetime = datetime.now()
    # cur_datetime = datetime(2019, 8, 6, hh, 10, 0)
    for item in all_Signingin:
        if cur_datetime.time() > time(23, 00, 0):
            item.end_time = datetime.strptime(cur_datetime.strftime('%Y-%m-%d') + ' 23:00:00', '%Y-%m-%d %H:%M:%S')
        elif cur_datetime.time() > time(18, 00, 0):
            item.end_time = datetime.strptime(cur_datetime.strftime('%Y-%m-%d') + ' 17:30:00', '%Y-%m-%d %H:%M:%S')
        elif cur_datetime.time() > time(12, 00, 0):
            item.end_time = datetime.strptime(cur_datetime.strftime('%Y-%m-%d') + ' 11:30:00', '%Y-%m-%d %H:%M:%S')
        elif cur_datetime.time() > time(5, 00, 0):
            item.end_time = datetime.strptime(cur_datetime.strftime('%Y-%m-%d') + ' 5:00:00', '%Y-%m-%d %H:%M:%S')
        else:
            item.end_time = datetime.strptime(cur_datetime.strftime('%Y-%m-%d') + ' 2:00:00', '%Y-%m-%d %H:%M:%S')
        item.is_auto_signout = True
        duration = round((item.end_time - item.start_time).seconds / 3600, 1)
        item.duration = duration
        item.save()
        print('DateTime:', cur_datetime, 'id:', item.id)


def test_auto_signout():
    # from app.models import Signingin
    emp = Employee.objects.get(user__username='zhhk')
    # Signingin.objects.create(employee=emp, start_time=datetime(2019, 8, 6, 2, 55, 0))
    ii = [23, 18, 12, 5, 2]
    for i in ii:
        Signingin.objects.create(employee=emp, start_time=datetime(2019, 8, 6, 2, 55, 0))
        auto_signout(i)

if __name__ == "__main__":
    # HolidayArrangements()
    test_auto_signout()
    print('Done!')