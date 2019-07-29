from django.db import models
from django.contrib.auth.models import User

from datetime import datetime
from django.utils import timezone


# 工作时间制度
class WorkTime(models.Model):
    name = models.TextField(max_length=20, verbose_name='工作时间制度名称')  # 普通（上午、下午）、朝九晚五、倒班（早班、中班、晚班）
    shift = models.TextField(max_length=20, verbose_name='班次')
    start_time = models.TimeField(null=False, blank=True, verbose_name='开始时间')
    end_time = models.TimeField(null=False, blank=True, verbose_name='结束时间')
    remarks = models.TextField(default='', blank=True, max_length=100, verbose_name='备注')

    def __str__(self):
        return self.name


# 节日名称
class HolidayName(models.Model):
    name = models.TextField(max_length=20, verbose_name='假期名称')
    remarks = models.TextField(default='', blank=True, max_length=100, verbose_name='备注')

    def __str__(self):
        return self.name


# 节日假期及调休表
class HolidayArrangements(models.Model):
    date = models.DateField(null=False, verbose_name='日期')
    name = models.ForeignKey(to='HolidayName', on_delete=models.CASCADE, verbose_name='假期名称')
    is_legal_holidays = models.BooleanField(default=False, verbose_name='是否法定节假日')


# 休假类别
class LeaveType(models.Model):
    name = models.TextField(max_length=20, verbose_name='假别')
    remarks = models.TextField(default='', blank=True, max_length=100, verbose_name='假期名称')

    def __str__(self):
        return self.name


class UserType(models.Model):
    # 用户类型表  字段：用户类型
    caption = models.CharField(max_length=10, verbose_name='用户类型')

    def __str__(self):
        return self.caption


# 员工信息表
class Employee(models.Model):
    GENDER_CHOICES = (
        ('男', '男'),
        ('女', '女'),
        )
    # 创建用户模型，员工编号,密码，部门，姓名,昵称，专业,用户类型,电话，姓名,座右铭,邮件
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.ForeignKey(to='UserType', on_delete=models.CASCADE, verbose_name='用户类型')
    emp_num = models.CharField(max_length=15, primary_key=True, verbose_name='员工编号')
    department = models.ForeignKey('Department', null=True, on_delete=models.CASCADE, verbose_name='部门')

    full_name = models.CharField(max_length=30, null=True, verbose_name='姓名')
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, verbose_name='性别')
    birth_date = models.DateField(null=True, verbose_name='出生日期')
    cell_phone = models.CharField(max_length=11, verbose_name='手机号码')
    work_phone = models.CharField(max_length=20, verbose_name='办公电话')

    def __str__(self):
        # return self.username
        return self.user.username

    def get(self, username):
        return User.objects.get(username)


# 部门信息表
class Department(models.Model):
    name = models.CharField(max_length=20, verbose_name='部门名称')
    parent_dept_id = models.CharField(max_length=64, verbose_name='上级部门编号')

    def __str__(self):
        return self.name


# 请假表
class Leave(models.Model):
    # 请假表 字段：用户，假单编号，假别，请假时间，销假时间，开始时间，结束时间，请假原因，目的地，审批单编号
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, verbose_name='假别', on_delete=models.CASCADE)  # 假别
    ask_time = models.DateField(null=False, blank=True, verbose_name='请假时间')  # 请假时间
    report_back_time = models.DateField(null=True, blank=True, verbose_name='销假时间')  # 销假时间
    start_time = models.DateField(null=False, blank=True, verbose_name='开始时间')  # 开始时间
    end_time = models.DateField(null=False, blank=True, verbose_name='结束时间')  # 结束时间
    reason = models.TextField(default='无', max_length=500, verbose_name='请假原因')   # 请假原因
    destination = models.TextField(null=True, max_length=100, verbose_name='目的地')  # 目的地

    # 例子：2019070811151562555730，datetime.datetime.now().strftime('%Y%m%d%s%f')
    leave_id = models.TextField(max_length=255, verbose_name='假单编号')
    approval_id = models.TextField(max_length=255, verbose_name='审批单编号')

    def __str__(self):
        return self.leave_id

    def _get_leave_days(self):
        if self.report_back_time and self.report_back_time < self.end_time:
            return '%d' % ((self.report_back_time - self.start_time).days + 1)

        return '%d' % ((self.end_time - self.start_time).days + 1)

    class Meta:
        ordering = ['ask_time']

    leave_days = property(_get_leave_days)


# 考勤记录表
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    # cur_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date = models.DateField(default=timezone.now)
    # state=models.BooleanField(default=False)
    is_leave = models.BooleanField(default=False)
    detail = models.TextField(default='', verbose_name='备注')
    leave_count = models.IntegerField(default=0, verbose_name='请假天数')

    def __str__(self):
        return self.employee.user.username


# 签到表
class Signingin(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='签到时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='签退时间')
    duration = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='时长')

    def __str__(self):
        return self.employee.user.username


# 加班记录表
class WorkOvertime(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='签到时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='签退时间')
    duration = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='时长')


# 公告表设计
class Notice(models.Model):
    # 公告表  字段：发布人,发布日期，发布标题，发布内容，发布级别
    author = models.ForeignKey(Employee, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now=True)
    head = models.TextField(max_length=200)
    content = models.TextField(max_length=500)
    level = models.IntegerField(default=0)


# # 考核内容
# # 考核内容表：标题，名称，批阅状态
# class ExamContent(models.Model):
#     title = models.TextField(max_length=200)
#     date = models.DateField(auto_now=True)
#     state = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.title
#
#
# #  考核成绩表设计
# class Exam(models.Model):
#     # 考核成绩表  字段： 用户，考核内容，分数，备注
#     user = models.ForeignKey('Employee', on_delete=models.CASCADE)
#     content = models.ForeignKey(to='ExamContent', on_delete=models.CASCADE)
#     point = models.DecimalField(max_digits=3, decimal_places=0, default=0)
#     detail = models.TextField(max_length=200, default="无")
