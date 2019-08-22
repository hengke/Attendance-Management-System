from datetime import datetime, timedelta
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import sys
print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend([sys.path[0]])

import django
print('Django %s' % django.get_version())
if 'setup' in dir(django):
    django.setup()

from app.models import HolidayName, HolidayArrangements, EveryDayArrangements, LeaveType, UserType
from app.models import WorkTime, Structure, Employee


def LoadStructure():
    print('Start load Structure data into database from ./sampledata/Structure.txt')
    f = open('./sampledata/Structure.txt')
    all_lines = f.readlines()
    f.close()
    for i in range(1, len(all_lines)):
        strs = all_lines[i].rstrip('\n').split(',')
        h = Structure()
        if strs[0] == '公司' or strs[0] == 'firm':
            h.type = 'firm'
        else:
            h.type = 'department'

        h.title = strs[1]
        try:
            parent = Structure.objects.get(title=strs[2])
        except Structure.DoesNotExist:
            pass
        else:
            h.parent = parent

        h.save()
    print(Structure.objects.all())
    print('Done!\n')


def LoadEmployee():
    print('Start load Employee data into database from ./sampledata/Employee.csv')
    f = open('./sampledata/Employee.csv')
    all_lines = f.readlines()
    f.close()
    for i in range(1, len(all_lines)):
        strs = all_lines[i].rstrip('\n').split(',')
        h = Employee()
        h.full_name = strs[0]
        h.department = strs[0]
        h.user = strs[0]
        h.user_type = strs[0]
        h.post = strs[0]
        h.superior = strs[0]  # 上级主管

        h.title = strs[1]
        try:
            parent = Employee.objects.get(title=strs[2])
        except Employee.DoesNotExist:
            pass
        else:
            h.parent = parent

        h.save()
    print(Employee.objects.all())
    print('Done!\n')


def LoadWorkTime():
    print('Start load UserType data into database from ./sampledata/WorkTime.txt')
    f = open('./sampledata/WorkTime.txt')
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
    print('Done!\n')


def LoadUserType():
    print('Start load UserType data into database from ./sampledata/UserType.txt')
    f = open('./sampledata/UserType.txt')
    all_lines = f.readlines()
    f.close()
    for i in range(1, len(all_lines)):
        str = all_lines[i].rstrip('\n')
        h = UserType()
        h.caption = str
        h.save()
    print(UserType.objects.all())
    print('Done!\n')


def LoadLeaveType():
    print('Start load LeaveType data into database from ./sampledata/LeaveType.txt')
    f = open('./sampledata/LeaveType.txt')
    all_lines = f.readlines()
    f.close()
    for i in range(1, len(all_lines)):
        str = all_lines[i].rstrip('\n')
        h = LeaveType()
        h.name = str
        h.save()
    print(LeaveType.objects.all())
    print('Done!\n')


def LoadHolidayName():
    print('Start load HolidayName data into database from ./sampledata/HolidayName.txt')
    f = open('./sampledata/HolidayName.txt')
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
    print('Done!\n')


def LoadHolidayArrangements():
    print('Start load HolidayArrangements data into database from ./sampledata/HolidayArrangements.txt')
    all_HolidayName = HolidayName.objects.all()
    print(all_HolidayName)
    f = open('./sampledata/HolidayArrangements.txt')
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
    print('Done!\n')


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
    print('Done!\n')


if __name__ == "__main__":
    LoadStructure()
    # LoadWorkTime()
    # LoadUserType()
    # LoadLeaveType()
    # LoadHolidayName()
    # LoadHolidayArrangements()
    # MakeEveryDayArrangements(2019)
