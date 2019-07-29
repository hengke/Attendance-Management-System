from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserType, Employee, Department, Leave, Notice, Signingin
from .models import WorkTime, HolidayName, HolidayArrangements, LeaveType, WorkOvertime


# Register your models here.

class WorkTimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'shift', 'start_time', 'end_time', 'remarks']


class HolidayNameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'remarks']


class HolidayArrangementsAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'name', 'is_legal_holidays']


class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'remarks']


class UserTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption']


# class EmployeeAdmin(admin.ModelAdmin):
#     # list_display = ['employee'.id, 'employee'.username, 'employee'.password, 'emp_num', 'department']
#     list_display = ['user', 'user_type', 'emp_num', 'department']


class EmployeeInline(admin.TabularInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'


class UserAdmin(UserAdmin):
    inlines = (EmployeeInline,)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent_dept_id']


class LeaveAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'leave_id', 'leave_type', 'ask_time',
                    'report_back_time', 'start_time', 'end_time', 'reason',
                    'destination', 'approval_id']


# class SigninginAdmin(admin.ModelAdmin):
#     list_display = ['id', 'employee', 'date', 'start_time', 'end_time', 'is_leave', 'duration', 'detail']


class NoticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'head', 'content', 'level']


class WorkOvertimeAdmin(admin.ModelAdmin):
    list_display = ['employee', 'start_time', 'end_time', 'duration']
 

# class ExamAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'content', 'point', 'detail']
#
#
# class ExamContentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'date', 'state']

admin.site.register(WorkTime, WorkTimeAdmin)
admin.site.register(HolidayName, HolidayNameAdmin)
admin.site.register(HolidayArrangements, HolidayArrangementsAdmin)
admin.site.register(LeaveType, LeaveTypeAdmin)
admin.site.register(UserType, UserTypeAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.register(Employee, EmployeeAdmin)

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Leave, LeaveAdmin)
# admin.site.register(Signingin, SigninginAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(WorkOvertime, WorkOvertimeAdmin)
# admin.site.register(ExamContent, ExamContentAdmin)
# admin.site.register(Exam, ExamAdmin)

