from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserType, Employee, Structure, Leave, Notice, Signingin
from .models import WorkTime, HolidayName, HolidayArrangements, LeaveType


# Register your models here.

class WorkTimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'shift', 'start_time', 'end_time', 'remarks']
    verbose_name_plural = '工作时间'


class HolidayNameAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'remarks']
    verbose_name_plural = '节假日名称'


class HolidayArrangementsAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'name', 'is_legal_holiday']
    verbose_name_plural = '节假日及调休表'


class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'remarks']
    verbose_name_plural = '休假类别'


class UserTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption']
    verbose_name_plural = '用户类别'


# class EmployeeAdmin(admin.ModelAdmin):
#     # list_display = ['employee'.id, 'employee'.username, 'employee'.password, 'emp_num', 'Structure']
#     list_display = ['user', 'user_type', 'emp_num', 'Structure']


class EmployeeInline(admin.TabularInline):
    model = Employee
    fields = ['user_type', 'emp_num', 'department', 'superior']
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (EmployeeInline,)


class StructureAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'title', 'parent']
    fields = ['id', 'type', 'title', 'parent']


class LeaveAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'leave_id', 'leave_type', 'ask_time',
                    'report_back_time', 'start_time', 'end_time', 'reason',
                    'destination', 'approval_id']
    verbose_name_plural = '休假管理'


# class SigninginAdmin(admin.ModelAdmin):
#     list_display = ['id', 'employee', 'date', 'start_time', 'end_time', 'is_leave', 'duration', 'detail']


class NoticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'head', 'content', 'level']
    verbose_name_plural = '通告管理'


class WorkOvertimeAdmin(admin.ModelAdmin):
    list_display = ['employee', 'start_time', 'end_time', 'duration']
    verbose_name_plural = '加班管理'
 

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

admin.site.register(Structure, StructureAdmin)
admin.site.register(Leave, LeaveAdmin)
# admin.site.register(Signingin, SigninginAdmin)
admin.site.register(Notice, NoticeAdmin)
# admin.site.register(WorkOvertime, WorkOvertimeAdmin)
# admin.site.register(ExamContent, ExamContentAdmin)
# admin.site.register(Exam, ExamAdmin)

