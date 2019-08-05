import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from datetime import datetime, timedelta

import django
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()


def auto_signout():
    from app.models import Signingin
    all_Signingin = Signingin.objects.filter(end_time=None)
    cur_datetime = datetime.now()

    for item in all_Signingin:
        if cur_datetime.time() > datetime.time(23, 40, 0):
            item.end_time = datetime.strptime(cur_datetime.strftime('%Y-%m-%d') + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
        elif cur_datetime.time() > datetime.time(17, 30, 0):
            item.end_time = datetime.strptime(cur_datetime.strftime('%Y-%m-%d') + ' 17:30:00', '%Y-%m-%d %H:%M:%S')
        elif cur_datetime.time() > datetime.time(11, 30, 0):
            item.end_time = datetime.strptime(cur_datetime.strftime('%Y-%m-%d') + ' 11:30:00', '%Y-%m-%d %H:%M:%S')
        elif cur_datetime.time() > datetime.time(7, 00, 0):
            item.end_time = datetime.strptime(cur_datetime.strftime('%Y-%m-%d') + ' 7:00:00', '%Y-%m-%d %H:%M:%S')
        item.is_auto_signout = True
        item.save()
        print(item.id)

if __name__ == "__main__":
    # HolidayArrangements()
    auto_signout()
    print('Done!')