from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .forms import loginForm
from django.contrib.auth import authenticate, login
from .api import check_cookie, DecimalEncoder, is_login
from .models import UserType, Employee, Department, Notice, Leave, HolidayArrangements, Signingin, LeaveType
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
    return redirect('/check/')
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
                    response = redirect('/index/')
                    response.set_cookie('qwer', username, 3600)
                    response.set_cookie('asdf', password, 3600)
                    return response
                except Employee.DoesNotExist:
                    return render(request, 'edit_emp_info.html', locals())
            else:
                return render(request, 'page-login.html', {'error_msg': '账户未激活！请联系管理员！'})
        else:
            return render(request, 'page-login.html', {'error_msg': '账号或密码错误请重新输入'})
    else:
        (flag, rank) = check_cookie(request)
        if flag:
            return redirect('/index/')
        return render(request, 'page-login.html', {'error_msg': ''})


def check(request):
    (flag, rank) = check_cookie(request)
    # get cur_day cur_time
    # if cur_day is workday:
    #     is_workday = True
    # else:
    #     is_workday = False
    #
    # if cur_day is legal_holiday:
    #     is_legal_holidays = True
    # else:
    #     is_legal_holidays = False
    #
    # if cur_time is worktime:
    #     is_worktime = True
    # else:
    #     is_worktime = False
    #
    # if 员工在休假中:
    #     is_in_leaving = True
    # else:
    #     is_in_leaving = False

    if flag:  # flag为True时，rank为user
        #
        # if workday and worktime:
        #     if not is_in_leaving:
        #         签到
        #     else:
        #         提示正在休假中，显示当前休假详情
        #         询问是否加班，还是提前销假
        #         加班：
        #             签到，并创建加班记录，填写加班内容，备注休假中途加班
        #         提前销假：
        #             跳转到销假页面
        # else if is_legal_holidays:
        #     签到，并创建加班记录，填写加班内容，备注节日加班
        # else:
        #     签到，并创建加班记录，填写加班内容，备注普通加班
        try:
            emp = Employee.objects.get(user=rank)
        except Employee.DoesNotExist:
            emp = None
            return render(request, 'edit_emp_info.html', locals())

        if request.method == 'POST':
            sign_flag = request.POST.get('sign')
            # print('check:sign_flag', type(sign_flag), sign_flag)
            if sign_flag == 'True':  # 签到，创建记录
                Signingin.objects.create(employee=emp, start_time=datetime.datetime.now())
            elif sign_flag == 'False':  # 签退，更新签退时间和时长
                cur_attendent = Signingin.objects.filter(employee=emp, end_time=None)
                tmp_time = datetime.datetime.now()
                duration = round((tmp_time - cur_attendent.last().start_time).seconds / 3600, 1)

                cur_attendent.update(end_time=tmp_time, duration=duration)
            return HttpResponse(request, '操作成功')
        else:
            # 查询上一个签到的状态
            pre_att = Signingin.objects.filter(employee=emp).order_by('start_time').last()
            # print('check:pre_att', pre_att)
            if pre_att:
                # 如果当前时间距上次签到时间超过六小时，并且上次签退时间等于签到时间
                if (datetime.datetime.now() - pre_att.start_time.replace(
                        tzinfo=None)).seconds / 3600 > 6 and pre_att.end_time == None:
                    pre_att.delete()
                    sign_flag = True

                elif (datetime.datetime.now() - pre_att.start_time.replace(
                        tzinfo=None)).seconds / 3600 < 6 and pre_att.end_time == None:
                    sign_flag = False
                else:
                    sign_flag = True
            else:
                sign_flag = True
            att_list = Signingin.objects.all().order_by('-id')
            return render(request, 'check.html', locals())
    else:
        return render(request, 'page-login.html', {'error_msg': ''})


# 编辑员工信息
def edit_emp_info(request):
    (flag, rank) = check_cookie(request)
    # print('check：flag', flag)
    # print('check：rank', rank)
    user = rank
    emp = Employee.objects.get(user=user)
    # 所有用户类型列表
    user_type_list = UserType.objects.all()
    # 所有的部门
    dept_list = Department.objects.all()

    if request.method == 'POST':
        user = User.objects.get(username=request.POST.get('username'))
        emp_num = request.POST.get('emp_num')
        department = Department.objects.get(name=request.POST.get('department'))
        user_type = UserType.objects.get(caption=request.POST.get('user_type'))
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        work_phone = request.POST.get('work_phone')
        cell_phone = request.POST.get('cell_phone')
        email = request.POST.get('email')
        user.email = email

        try:
            emp = Employee.objects.get(user=user)
            emp.emp_num = emp_num
            emp.full_name = full_name
            emp.department = department
            emp.user_type = user_type
            emp.gender = gender
            emp.birth_date = birth_date
            emp.work_phone = work_phone
            emp.cell_phone = cell_phone
        except Employee.DoesNotExist:
            emp = Employee.objects.create(user=user, emp_num=emp_num, full_name=full_name, department=department,
                                          gender=gender, birth_date=birth_date, work_phone=work_phone,
                                          user_type=user_type, cell_phone=cell_phone)

        emp.save()
        return render(request, 'show_emp_info.html', locals())

    return render(request, 'edit_emp_info.html', locals())


# 请假申请
@is_login
def leave_ask(request):
    (flag, user) = check_cookie(request)
    # user = User.objects.get(username=username)
    emp = Employee.objects.get(user=user)
    leave_list = Leave.objects.filter(employee=emp)
    leave_type_list = LeaveType.objects.all()

    if request.method == 'POST':
        leavetype = request.POST.get('leaveType')
        leave_type = LeaveType.objects.get(name=leavetype)
        starttime = request.POST.get('starttime')
        endtime = request.POST.get('endtime')
        destination = request.POST.get('destination')
        reason = request.POST.get('reason')

        ask_time = datetime.datetime.now()
        leave_id = datetime.datetime.now().strftime('%Y%m%d%s%f')
        approval_id = datetime.datetime.now().strftime('%Y%m%d%s%f')

        Leave.objects.create(employee=emp, leave_id=leave_id, leave_type=leave_type, ask_time=ask_time, start_time=starttime,
                             end_time=endtime, reason=reason, destination=destination, approval_id=approval_id)
        return render(request, 'leavequery.html', locals())

    return render(request, 'leaveask.html', locals())


# 销假管理
@is_login
def leave_report_back(request):
    (flag, user) = check_cookie(request)
    emp = Employee.objects.get(user=user)

    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        leave = Leave.objects.get(leave_id=leave_id)
        leave.report_back_time = datetime.datetime.now()
        leave.save()
    leave_list = Leave.objects.filter(employee=emp)
    return render(request, 'leavequery.html', locals())


# 请假查询
@is_login
def leave_query(request):
    (flag, user) = check_cookie(request)
    emp = Employee.objects.get(user=user)
    leave_list = Leave.objects.filter(employee=emp)
    return render(request, 'leavequery.html', locals())


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
        print('验证成功')
        username = request.POST.get('username')
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        user = User.objects.create_user(username, email, pwd)
        # user.is_superuser = False

        user.save()

        emp_num = request.POST.get('emp_num')
        emp = Employee.objects.create(user=user, emp_num=emp_num, user_type_id=2)

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

    # if flag:
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
    # else:
    #     return render(request, 'page-login.html', {'error_msg': ''})


# # 部门管理
# def department_manage(request):
#     (flag, rank) = check_cookie(request)
#     print('departmentManage:flag', flag)
#     if flag:
#         if rank.user_type.caption == 'admin':
#             class_list = Department.objects.all()
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
#                 temp_flag = Department.objects.filter(name=class_name)
#                 print('pre_edit_id1', pre_edit_id)
#                 pre_obj = Department.objects.get(id=pre_edit_id)
#                 if not temp_flag and class_name:
#                     pre_obj.name = class_name
#                     pre_obj.save()
#                 return HttpResponse('部门修改成功')
#             class_list = Department.objects.all()
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
#         flag = Department.objects.filter(name=add_department_name)
#         if flag:
#             pass
#             # print('已有数据，不处理')
#         else:
#             if add_department_name:
#                 Department.objects.create(name=add_department_name).save()
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
#             # class_list=Department.objects.all()
#             delete_id = request.GET.get('delete_id')
#             Department.objects.filter(id=delete_id).delete()
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
#                 cls = Department.objects.get(name=request.POST.get('cls'))
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
#                 cls_list = Department.objects.all()
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
