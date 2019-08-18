import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from datetime import datetime, time

import django
if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()

from app.models import Signingin, Employee


# 每天2:01、5:01、12:01、18:01、23:01自动运行签退程序
def auto_signout(cur_datetime):
    all_NotSignout = Signingin.objects.filter(end_time=None)
    for item in all_NotSignout:
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
        print(cur_datetime.isoformat(), ' id:', item.id, 'emp:', item.employee, 'StartTime:', item.start_time,
              ' EndTime:', item.end_time)
        cur_datetime = datetime.now()


def test_auto_signout():
    emp = Employee.objects.get(user__username='zhhk')
    # Signingin.objects.create(employee=emp, start_time=datetime(2019, 8, 6, 2, 55, 0))
    Signingin.objects.create(employee=emp, start_time=datetime(2019, 8, 6, 23, 5, 0))
    cur_datetime = datetime.strptime('2019-8-6 2:01:00', '%Y-%m-%d %H:%M:%S')
    auto_signout(cur_datetime)
    ii = [23, 18, 12, 5, 2]
    for i in ii:
        Signingin.objects.create(employee=emp, start_time=datetime(2019, 8, 6, int(i - 2), 5, 0))
        cur_datetime = datetime.strptime('2019-8-6 ' + str(i) + ':01:00', '%Y-%m-%d %H:%M:%S')
        auto_signout(cur_datetime)


if __name__ == "__main__":
    # HolidayArrangements()
    test_auto_signout()
    # auto_signout(datetime.now())
    print('Done!')