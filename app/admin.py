from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserType, Employee, Department, Holidays, Leave, Notice, Signingin


# Register your models here.

# class EmployeeAdmin(admin.ModelAdmin):
#     # list_display = ['employee'.id, 'employee'.username, 'employee'.password, 'emp_num', 'department']
#     list_display = ['user', 'user_type', 'emp_num', 'department']


class EmployeeInline(admin.TabularInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'

class UserAdmin(UserAdmin):
    inlines = (EmployeeInline,)


class UserTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption']


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent_dept_id']


class HolidaysAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'holidays_name', 'is_legal_holidays']


class LeaveAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'leave_id', 'leave_type', 'ask_time',
                    'report_back_time', 'start_time', 'end_time', 'reason',
                    'destination', 'approval_id']


class SigninginAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'date', 'start_time', 'end_time', 'is_leave', 'duration', 'detail']


class NoticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'head', 'content', 'level']


# class ExamAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'content', 'point', 'detail']
#
#
# class ExamContentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'date', 'state']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserType, UserTypeAdmin)
# admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Holidays, HolidaysAdmin)
# admin.site.register(Signingin, SigninginAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Leave, LeaveAdmin)
# admin.site.register(ExamContent, ExamContentAdmin)
# admin.site.register(Exam, ExamAdmin)

