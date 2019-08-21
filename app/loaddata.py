import os
from datetime import datetime, timedelta
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()

from app.models import HolidayName, HolidayArrangements, EveryDayArrangements, LeaveType, UserType
from app.models import WorkTime


def LoadWorkTime():
    print('Start load UserType data into database from ../sampledata/WorkTime.txt')
    f = open('../sampledata/WorkTime.txt')
    all_lines = f.readlines()
    f.close()
    for i in range(1, len(all_lines)):
        strs = all_lines[i].rstrip('\n').split(',')
        h = WorkTime()
        h.name = strs[0]
        h.shift = strs[1]
        h.start_time = strs[2]
        h.end_time = strs[3]
        h.remarks = strs[4]
        h.save()
    print(WorkTime.objects.all())


def LoadUserType():
    print('Start load UserType data into database from ../sampledata/UserType.txt')
    f = open('../sampledata/UserType.txt')
    all_lines = f.readlines()
    f.close()
    for i in range(1, len(all_lines)):
        str = all_lines[i].rstrip('\n')
        h = UserType()
        h.caption = str
        h.save()
    print(UserType.objects.all())


def LoadLeaveType():
    print('Start load LeaveType data into database from ../sampledata/LeaveType.txt')
    f = open('../sampledata/LeaveType.txt')
    all_lines = f.readlines()
    f.close()
    for i in range(1, len(all_lines)):
        str = all_lines[i].rstrip('\n')
        h = LeaveType()
        h.name = str
        h.save()
    print(LeaveType.objects.all())


def LoadHolidayName():
    print('Start load HolidayName data into database from ../sampledata/HolidayName.txt')
    f = open('../sampledata/HolidayName.txt')
    all_lines = f.readlines()
    f.close()
    for i in range(1, len(all_lines)):
        strs = all_lines[i].rstrip('\n').split(',')
        h = HolidayName()
        h.name = strs[0]
        if len(strs) > 1:
            h.remarks = strs[1]
        h.save()
    print(HolidayName.objects.all())


def LoadHolidayArrangements():
    print('Start load HolidayArrangements data into database from ../sampledata/HolidayArrangements.txt')
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
    print('Start make EveryDayArrangements data')
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
    LoadWorkTime()
    # LoadUserType()
    # LoadLeaveType()
    # LoadHolidayName()
    # LoadHolidayArrangements()
    # MakeEveryDayArrangements(2019)
    print('Done!')