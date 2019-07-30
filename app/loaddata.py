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


if __name__ == "__main__":
    HolidayArrangements()
    print('Done!')