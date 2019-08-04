import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")


import django
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()


def HolidayArrangements():
    from app.models import HolidayName
    from app.models import HolidayArrangements

    print('Django %s' % django.get_version())

    all_HolidayName = HolidayName.objects.all()
    print(all_HolidayName)
    f = open('../sampledata/HolidayArrangements.txt')
    all_lines = f.readlines()
    f.close()

    for line in all_lines:
        strs = line.rstrip('\n').split(',')
        my_HolidayName = HolidayName.objects.get(name=strs[1])
        h = HolidayArrangements()
        h.date = strs[0].replace('/','-')
        h.name = my_HolidayName
        if strs[2] == '1':
            h.is_legal_holiday = True
        else:
            h.is_legal_holiday = False
        h.save()
    print(HolidayArrangements.objects.all())


def MakeEveryDayArrangements(year):
    from app.models import HolidayArrangements
    from datetime import datetime, timedelta

    from app.models import EveryDayArrangements
    all_HolidayArrangements = HolidayArrangements.objects.all()
    myday = datetime(year - 1, 12, 28)
    for i in range(1, 369):
        myday = myday + timedelta(days=1)
        try:
            h = EveryDayArrangements.objects.get(date=myday)
        except EveryDayArrangements.DoesNotExist:
            h = EveryDayArrangements()

        h.date = myday
        h.is_workday = False
        h.weekday = myday.weekday() + 1
        if h.weekday in range(1, 6):
            h.is_workday = True
        h.save()
    print(myday)
    for item in all_HolidayArrangements:
        try:
            d = EveryDayArrangements.objects.get(date=item.date)
            d.is_legal_holiday = item.is_legal_holiday
            d.remarks = str(item.name)
            if str(item.name) == '上班':
                d.is_workday = True
            else:
                d.is_workday = False
                d.is_holiday = True
                d.holiday_name = str(item.name)
            d.save()
        except EveryDayArrangements.DoesNotExist:
            pass


if __name__ == "__main__":
    # HolidayArrangements()
    MakeEveryDayArrangements(2019)
    print('Done!')