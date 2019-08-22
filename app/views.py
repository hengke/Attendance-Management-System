from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .forms import loginForm
from django.contrib.auth import authenticate, login
from .api import check_cookie, DecimalEncoder, is_login
from .models import UserType, Employee, Structure, Notice, Leave, HolidayArrangements, Signingin, \
    WorkTime, LeaveType, EveryDayArrangements
# django自带加密解密库
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Q, Avg, Sum, Max, Min, Count
import json
import datetime


# Create your views here.

# 检查是否登录的装饰器
# def check_login(func):
#     def inner(request,*args,**kwargs):
#         (flag, rank) = check_cookie(request)
#         if flag:
#             func(request,*args,**kwargs)
#         else:
#             return render(request, 'page-login.html', {'error_msg': ''})
#
#     return inner

# 首页
def index(request):
    return redirect('/login/')
    # (flag, rank) = check_cookie(request)
    # print('flag', flag)
    #
    # if flag:
    #     return render(request, 'check.html',locals())
    #
    # return render(request, 'page-login.html', {'error_msg': ''})


# 登录页面
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # print("login:", user)
        if user is not None:
            if user.is_active:
                try:
                    # 尝试获取此用户名对应的员工，有则跳到签到页面，没有则跳转到员工信息编辑页面
                    emp = Employee.objects.get(user=user)
                except Employee.DoesNotExist:
                    return render(request, 'edit_emp_info.html', locals())
                else:
                    response = redirect('/check/')
                    response.set_cookie('qwer', username, 3600)
                    response.set_cookie('asdf', password, 3600)
                    return response
            else:
                return render(request, 'page-login.html', {'error_msg': '账户未激活！请联系管理员！'})
        else:
            return render(request, 'page-login.html', {'error_msg': '账号或密码错误请重新输入'})
    else:
        (flag, rank) = check_cookie(request)
        if flag:
            return redirect('/check/')
        return render(request, 'page-login.html', {'error_msg': ''})


def check(request):
    (flag, rank) = check_cookie(request)

    if flag:  # flag为True时，rank为user

        try:
            emp = Employee.objects.get(user=rank)
        except Employee.DoesNotExist:
            emp = None
            return render(request, 'edit_emp_info.html', locals())

        cur_datetime = datetime.datetime.now()
        # 推迟签到，提前签退时间各10分钟
        h = cur_datetime.hour
        m = cur_datetime.minute
        if (h == 8 and m <= 10) or (h == 13 and (30 <= m or m <= 40)):
            cur_datetime = cur_datetime + datetime.timedelta(minutes=-10)
        if (h == 11 and (20 <= m or m <= 30)) or (h == 17 and (30 <= m or m <= 40)):
            cur_datetime = cur_datetime + datetime.timedelta(minutes=10)
        # test = False
        # if test is True:
        #     cur_datetime = datetime.datetime(2019, 4, 8, 7, 10, 0)

        cur_date = cur_datetime.date()
        cur_time = cur_datetime.time()

        try:
            cur_day = EveryDayArrangements.objects.get(date=cur_date)
        except EveryDayArrangements.DoesNotExist:
            return render(request, 'page-login.html',
                          {'error_msg': "EveryDayArrangements: Cann't find " + str(cur_date)})
        # print('cur_day:' + str(cur_day.date))

        try:
            worktime = WorkTime.objects.filter(name='普通')
        except EveryDayArrangements.DoesNotExist:
            return render(request, 'page-login.html', {'error_msg': "WorkTime: Cann't find " + '普通'})

        # print('cur_time:' + str(cur_time))
        # 判断是否是工作时间内，
        if cur_day.is_workday:
            if cur_time > worktime[0].start_time and cur_time < worktime[0].end_time:
                is_worktime = True
            elif cur_time > worktime[1].start_time and cur_time < worktime[1].end_time:
                is_worktime = True
            else:
                is_worktime = False
        else:
            is_worktime = False
        # print('is_worktime:' + str(is_worktime))
        # 判断员工是否休假中
        try:
            leave_list = Leave.objects.filter(employee=emp, report_back_time__isnull=True)
        except Leave.DoesNotExist:
            pass
        else:
            if len(leave_list) == 0:
                is_in_leaving = False
            else:
                is_in_leaving = True

        # print('is_in_leaving:' + str(is_in_leaving))

        if request.method == 'POST':
            sign_flag = request.POST.get('sign')
            if sign_flag == 'True':  # 签到，创建记录
                sign = Signingin(employee=emp, start_time=cur_datetime)
                # print(sign.__dict__)
                if is_in_leaving:
                    sign.is_holiday = True
                    sign.remarks = '休假中加班'
                elif not is_worktime:
                    # 加班，包括夜班
                    if cur_day.is_legal_holiday:
                        sign.is_legal_holiday = True
                    if cur_day.is_holiday:
                        sign.is_holiday = True
                    if cur_time > datetime.time(19, 0, 0) or cur_time < datetime.time(5, 0, 0):
                        sign.is_night = True
                else:
                    sign.is_come_late = True
                # print(sign.__dict__)
                sign.save()
            elif sign_flag == 'False':  # 签退，更新签退时间和时长
                is_left_early = False
                if is_worktime:
                    is_left_early = True
                cur_attendent = Signingin.objects.filter(employee=emp, end_time=None)
                # 计算时长
                duration = round((cur_datetime - cur_attendent.last().start_time).seconds / 3600, 1)
                cur_attendent.update(end_time=cur_datetime, duration=duration, is_left_early=is_left_early)
            return HttpResponse(request, '操作成功')
        else:  # 非POST请求，查询是否有未签退记录，有显示签退
            try:
                pre_atts = Signingin.objects.filter(employee=emp, end_time=None)
            except Signingin.DoesNotExist:
                pass
            else:
                if len(pre_atts) == 0:
                    sign_flag = True
                else:
                    sign_flag = False
            att_list = Signingin.objects.filter(start_time__gt=(cur_date + datetime.timedelta(days=-10)),
                                                employee=emp).order_by('-id')
            return render(request, 'check.html', locals())
    else:
        return render(request, 'page-login.html', {'error_msg': '您未登录，请登录！'})


# 编辑员工信息
@is_login
def edit_emp_info(request):
    (flag, rank) = check_cookie(request)
    # print('check：flag', flag)
    # print('check：rank', rank)
    user = rank
    if flag:
        emp = Employee.objects.get(user=user)
        print(emp.birth_date)
        # 所有用户类型列表
        user_type_list = UserType.objects.all()
        # 所有的部门
        dept_list = Structure.objects.all()

        if request.method == 'POST':
            # department = Structure.objects.get(title=request.POST.get('department'))
            # user_type = UserType.objects.get(caption=request.POST.get('user_type'))
            full_name = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            work_phone = request.POST.get('work_phone')
            cell_phone = request.POST.get('cell_phone')
            email = request.POST.get('email')

            user.email = email
            emp.full_name = full_name
            # emp.department = department
            # emp.user_type = user_type
            emp.gender = gender
            emp.birth_date = birth_date
            emp.work_phone = work_phone
            emp.cell_phone = cell_phone

            user.save()
            emp.save()
            # return render(request, 'show_emp_info.html', locals())

        return render(request, 'edit_emp_info.html', locals())
    else:
        return render(request, 'page-login.html', {'error_msg': '您未登录，请登录！'})


# 编辑加班原因
def edit_sign_reason(request):
    (flag, rank) = check_cookie(request)
    if flag:
        if request.method == 'POST':
            sign_id = request.POST.get('sign_id')
            worktime_reason = request.POST.get('worktime-reason')
            print(sign_id)
            print(worktime_reason)
            sign = Signingin.objects.get(id=sign_id)
            sign.reason = worktime_reason
            sign.save()
            reason_save_flag = True
            return render(request, 'check.html', locals())
        return render(request, 'check.html', locals())
    else:
        return render(request, 'page-login.html', {'error_msg': '您未登录，请登录！'})


# 请假申请
@is_login
def leave_ask(request):
    (flag, rank) = check_cookie(request)
    # user = User.objects.get(username=username)
    if flag:
        emp = Employee.objects.get(user=rank)
        leave_list = Leave.objects.filter(employee=emp)
        leave_type_list = LeaveType.objects.all()

        if request.method == 'POST':
            leavetype = request.POST.get('leaveType')
            leave_type = LeaveType.objects.get(name=leavetype)
            startdate = request.POST.get('startdate')
            starttime = request.POST.get('starttime')
            endtime = request.POST.get('endtime')
            enddate = request.POST.get('enddate')
            destination = request.POST.get('destination')
            reason = request.POST.get('reason')
            if startdate == '':
                startdate = datetime.datetime.now().strftime('%Y-%m-%d')

            if enddate == '':
                enddate = startdate

            if starttime == '':
                starttime = '00:00:00'
            else:
                starttime = starttime + ':00'

            if endtime == '':
                endtime = '00:00:00'
            else:
                endtime = endtime + ':00'
            str11 = startdate + ' ' + starttime
            str22 = enddate + ' ' + endtime
            startdatetime = datetime.datetime.strptime(str11, '%Y-%m-%d %H:%M:%S')
            enddatetime = datetime.datetime.strptime(str22, '%Y-%m-%d %H:%M:%S')
            ask_time = datetime.datetime.now()
            leave_id = datetime.datetime.now().strftime('%Y%m%d%s%f')
            approval_id = datetime.datetime.now().strftime('%Y%m%d%s%f')

            Leave.objects.create(employee=emp, leave_id=leave_id, leave_type=leave_type, ask_time=ask_time,
                                 start_time=startdatetime, end_time=enddatetime, reason=reason, destination=destination,
                                 approval_id=approval_id)
            # return render(request, 'leavequery.html', locals())

        return render(request, 'leaveask.html', locals())
    else:
        return render(request, 'page-login.html', {'error_msg': '您未登录，请登录！'})


# 请假查询
@is_login
def leave_query(request):
    (flag, rank) = check_cookie(request)
    if flag:
        emp = Employee.objects.get(user=rank)

        if request.method == 'POST':
            leave_id = request.POST.get('leave_id')
            print('leave_report_back:leave_id:leave_id', leave_id)
            leave = Leave.objects.get(employee=emp, leave_id=leave_id)
            leave.report_back_time = datetime.datetime.now()
            leave.save()
            return render(request, 'leave_report_back_success.html', locals())

        leave_list = Leave.objects.filter(employee=emp)
        return render(request, 'leavequery.html', locals())
    else:
        return render(request, 'page-login.html', {'error_msg': '您未登录，请登录！'})


# 假别设置
# @is_login
# def set_leave_type(request):
#     leave_type_list = LeaveType.objects.all()
#     if request.method == 'POST':
#         pass
#     return render(request, 'set_leave_type.html', locals())


# 注销登录
def logout(request):
    req = redirect('/login/')
    req.delete_cookie('asdf')
    req.delete_cookie('qwer')
    return req


# 注册页面
@csrf_exempt
def register(request):
    if request.method == 'POST':
        if request.is_ajax():

            emp_num = request.POST.get('emp_num')
            username = request.POST.get('username')
            if Employee.objects.filter(emp_num=emp_num) or User.objects.filter(username=username):
                ret = {'valid': False}
            else:
                ret = {'valid': True}

            return HttpResponse(json.dumps(ret))

    else:
        return render(request, 'register.html')


# 注册验证
def register_verify(request):
    if request.method == 'POST':
        print('register_verify:验证成功')
        username = request.POST.get('username')
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        emp_num = request.POST.get('emp_num')
        cell_phone = request.POST.get('cell_phone')

        user = User.objects.create_user(username, email, pwd)
        # user.is_superuser = False
        user.save()

        emp = Employee.objects.create(user=user, emp_num=emp_num, user_type_id=2, cell_phone=cell_phone)
        emp.save()
        return HttpResponse('OK')


# 签到统计
@is_login
def total(request):
    (flag, user) = check_cookie(request)

    nowdate = datetime.datetime.now()
    weekDay = datetime.datetime.weekday(nowdate)
    firstDay = nowdate - datetime.timedelta(days=weekDay)
    lastDay = nowdate + datetime.timedelta(days=6 - weekDay)

    if flag:
        if request.method == 'POST':
            # print(firstDay,lastDay)
            # info_list=Signingin.objects.filter(date__gte=firstDay,date__lte=lastDay) \
            #   .values('employee','emp__username','emp__cid__name') \
            #   .annotate(total_time=Sum('duration'),leave_count=Sum('is_leave')).order_by()

            info_list = Signingin.objects.filter(date__gte=firstDay, date__lte=lastDay) \
                .values('employee', 'emp__username', 'emp__cid__name', 'leave_count') \
                .annotate(total_time=Sum('duration')).order_by()
            info_list = json.dumps(list(info_list), cls=DecimalEncoder)

            return HttpResponse(info_list)
        else:
            # print(firstDay,lastDay)
            leave_list = Leave.objects.filter().values('user', 'start_time', 'end_time')
            # print(leave_list)
            info_list = Signingin.objects.filter(date__gte=firstDay, date__lte=lastDay) \
                .values('employee', 'emp__username', 'emp__cid__name', 'leave_count') \
                .annotate(total_time=Sum('duration')).order_by()

            # info_list=Signingin.objects.filter(date__gte=firstDay,date__lte=lastDay).values('employee','emp__username','emp__cid__name')\
            #     .annotate(total_time=Sum('duration'),leave_count=Sum('is_leave'))\
            #     .extra(
            #     select={'starttime':"select start_time from app_leave where %s BETWEEN start_time AND end_time"},
            #     select_params=[nowdate]
            # )\
            #     .order_by()

            # info_list=json.dumps(list(info_list),cls=DecimalEncoder)
            print(info_list)

            return render(request, 'total.html', locals())
    else:
        return render(request, 'page-login.html', {'error_msg': ''})

# # 部门管理
# def department_manage(request):
#     (flag, rank) = check_cookie(request)
#     print('departmentManage:flag', flag)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             class_list = Structure.objects.all()
#
#             return render(request, 'department_manage.html', {'class_list': class_list})
#         else:
#             return render(request, 'department_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})
#
#
# # 编辑部门
# @csrf_exempt
# def edit_department(request):
#     (flag, rank) = check_cookie(request)
#     print('flag', flag)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             if request.method == 'POST':
#                 pre_edit_id = request.POST.get('edit_id')
#                 class_name = request.POST.get('edit_department_name')
#                 temp_flag = Structure.objects.filter(name=class_name)
#                 print('pre_edit_id1', pre_edit_id)
#                 pre_obj = Structure.objects.get(id=pre_edit_id)
#                 if not temp_flag and class_name:
#                     pre_obj.name = class_name
#                     pre_obj.save()
#                 return HttpResponse('部门修改成功')
#             class_list = Structure.objects.all()
#             return render(request, 'departmentManage.html', {'class_list': class_list})
#             # return HttpResponse('编辑部门')
#         else:
#             return render(request, 'department_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})
#
#
# # 添加部门
# @csrf_exempt
# def add_department(request):
#     # print('进来了')
#     if request.method == 'POST':
#         # print('这是post')
#         add_department_name = request.POST.get('add_department_name')
#         flag = Structure.objects.filter(name=add_department_name)
#         if flag:
#             pass
#             # print('已有数据，不处理')
#         else:
#             if add_department_name:
#                 Structure.objects.create(name=add_department_name).save()
#
#         return HttpResponse('添加部门成功')
#
#
# # 删除部门
# def delete_department(request):
#     (flag, rank) = check_cookie(request)
#     print('flag', flag)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             # class_list=Structure.objects.all()
#             delete_id = request.GET.get('delete_id')
#             Structure.objects.filter(id=delete_id).delete()
#             return redirect('/departmentManage/')
#         else:
#             return render(request, 'department_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})
#
#
# # 成员管理
# def member_manage(request):
#     (flag, rank) = check_cookie(request)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             member_list = Employee.objects.all()
#
#             return render(request, 'member_manage.html', {'member_list': member_list})
#         else:
#             return render(request, 'member_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})
#
#
# # 删除成员
# def delete_member(request):
#     (flag, rank) = check_cookie(request)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             delete_sno = request.GET.get('delete_sno')
#             Employee.objects.get(emp_num=delete_sno).delete()
#             member_list = Employee.objects.all()
#             return render(request, 'member_manage.html', {'member_list': member_list})
#         else:
#             return render(request, 'member_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})
#
#
# #   编辑成员
# def edit_member(request):
#     (flag, rank) = check_cookie(request)
#     if flag:
#         if rank.user_type.caption == 'admin':
#
#             if request.method == 'POST':
#                 emp_num = request.POST.get('emp_num')
#                 username = request.POST.get('username')
#                 email = request.POST.get('email')
#                 age = request.POST.get('age')
#                 if age:
#                     age = int(age)
#                 else:
#                     age = 0
#
#                 gender = int(request.POST.get('gender'))
#                 cls = Structure.objects.get(name=request.POST.get('cls'))
#                 nickname = request.POST.get('nickname')
#                 usertype = UserType.objects.get(caption=request.POST.get('user_type'))
#                 phone = request.POST.get('phone')
#                 motto = request.POST.get('motto')
#                 edit_obj = Employee.objects.filter(emp_num=emp_num)
#                 edit_obj.update(emp_num=emp_num, username=username, email=email, cid=cls, nickname=nickname,
#                                 user_type=usertype, motto=motto,
#                                 gender=gender, phone=phone,
#                                 age=age
#                                 )
#                 member_list = Employee.objects.all()
#
#                 return redirect('/memberManage/', {'member_list': member_list})
#             else:
#                 edit_member_id = request.GET.get('edit_sno')
#                 # 所有用户类型列表
#                 emp_type_list = UserType.objects.all()
#                 # 所有的部门
#                 cls_list = Structure.objects.all()
#                 # 所有的专业
#                 major_list = MajorInfo.objects.all()
#                 # 当前编辑的用户对象
#                 edit_emp_obj = Employee.objects.get(emp_num=edit_member_id)
#                 return render(request, 'edit_member.html', locals())
#         else:
#             return render(request, 'member_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})
#
#
# # 公告墙展示
# @is_login
# def notice(request):
#     info_list = Notice.objects.all().order_by('-post_date')
#     return render(request, 'notice.html', locals())
#
#
# # 公告墙发布
# @is_login
# def noticeManage(request):
#     (flag, user) = check_cookie(request)
#     if user.user_type.caption == 'admin':
#         if request.method == 'POST':
#             title = request.POST.get('title')
#             content = request.POST.get('content')
#             level = request.POST.get('selectLevel')
#             Notice.objects.create(head=title, content=content, level=level, author=user)
#             return render(request, 'notice_manage.html')
#         else:
#             return render(request, 'notice_manage.html')
#     else:
#         return render(request, 'notice_manage_denied.html')
#
#
# # 考核记录
# @is_login
# def exam(request):
#     exam_list=ExamContent.objects.all()
#     exam_id=request.GET.get('exam_id')
#     if exam_id:
#         user_list=Exam.objects.filter(content_id=exam_id).all()
#     return render(request, 'exam.html',locals())
#
#
# # 考核管理
# @is_login
# def exam_manage(request):
#     (flag, user) = check_cookie(request)
#     if user.user_type.caption == 'admin':
#         if request.method == 'POST':
#             title = request.POST.get('title')
#
#             if title:
#                 ExamContent.objects.create(title=title)
#             else:
#                 count = Employee.objects.all().count()
#                 content_id = request.POST.get('exam_id')
#                 for i in range(count):
#                     point=request.POST.get('point{}'.format(i))
#
#                     empID=request.POST.get('emp{}'.format(i))
#                     detail = request.POST.get('detail{}'.format(i))
#                     Exam.objects.create(point=point,content_id=content_id,user_id=empID,detail=detail)
#                 # print(request.body)
#                 ExamContent.objects.filter(id=content_id).update(state=True)
#         check_list = ExamContent.objects.filter(state=False)
#         user_list = Employee.objects.all()
#         return render(request, 'exam_manage.html', locals())
#     else:
#         return render(request, 'exam_manage_denied.html')
#
#
# # 专业管理
# def majorManage(request):
#     (flag, rank) = check_cookie(request)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             major_list = MajorInfo.objects.all()
#
#             return render(request, 'major_manage.html', {'major_list': major_list})
#         else:
#             return render(request, 'major_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})
#
#
# # 添加专业
# @csrf_exempt
# def add_major(request):
#     (flag, rank) = check_cookie(request)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             major_list = MajorInfo.objects.all()
#             if request.method == 'POST':
#
#                 add_major_name = request.POST.get('add_major_name')
#                 print(add_major_name)
#                 if not MajorInfo.objects.filter(name=add_major_name):
#                     new_major = MajorInfo.objects.create(name=add_major_name)
#                 return HttpResponse('专业添加成功')
#
#             return render(request, 'major_manage.html', {'major_list': major_list})
#         else:
#             return render(request, 'major_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})
#
#
# # 删除专业
# def delete_major(request):
#     (flag, rank) = check_cookie(request)
#     if flag:
#         if rank.user_type.caption == 'admin':
#
#             delete_major_id = request.GET.get('delete_id')
#             MajorInfo.objects.get(id=delete_major_id).delete()
#             major_list = MajorInfo.objects.all()
#             return render(request, 'major_manage.html', {'major_list': major_list})
#         else:
#             return render(request, 'major_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})
#
#
# # 编辑专业
# @csrf_exempt
# def edit_major(request):
#     (flag, rank) = check_cookie(request)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             major_list = MajorInfo.objects.all()
#             edit_major_id = request.POST.get('edit_major_id')
#             edit_major_name = request.POST.get('edit_major_name')
#             print(edit_major_id)
#             print(edit_major_name)
#             if not MajorInfo.objects.filter(name=edit_major_name):
#                 change_obj = MajorInfo.objects.get(id=edit_major_id)
#                 change_obj.name = edit_major_name
#                 change_obj.save()
#             return HttpResponse('专业修改成功')
#
#         else:
#             return render(request, 'major_manage_denied.html')
#     else:
#         return render(request, 'page-login.html', {'error_msg': ''})
