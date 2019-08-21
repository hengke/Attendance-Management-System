from .models import Employee, Structure, UserType
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from functools import wraps
from django.shortcuts import render
import json
import decimal


def check_cookie(request):
    d = request.COOKIES.keys()
    # print("check_cookie:keys", d)
    if "qwer" in d and "asdf" in d:
        username = request.COOKIES['qwer']
        password = request.COOKIES['asdf']
        # print("check_cookie:username", username)
        # print("check_cookie:password", password)
        # select_user = Employee.objects.filter(employee__username=username).filter(employee__password=password)
        # select_user = User.objects.filter(username=username).filter(password=password)
        # if len(select_user) == 0:
        #     return (False, -1)
        # else:
        #     return (True, select_user[0])
        user = authenticate(username=username, password=password)
        if user is None:
            return (False, -1)
        else:
            return (True, user)
    else:
        return (False, -1)


def is_login(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        (flag, rank) = check_cookie(request)
        if flag:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'page-login.html', {'error_msg': ''})
    return inner


def check_login(username, password):
    # select_user = User.objects.filter(username=username).filter(password=password)
    # select_user = Employee.objects.filter(employee__username=username).filter(employee__password=password)
    # print("API:check_login:",select_user)
    # if len(select_user) == 0:
    #     return False
    # else:
    #     return True

    user = authenticate(username=username, password=password)
    # print("API:check_login:", user)
    if user is not None:
        # if user.is_active:
        #     return True
        return True
    else:
        return False

# def get_all_major():
#     return MajorInfo.objects.all()


def get_all_department():
    return Structure.objects.all()


def get_all_type():
    return UserType.objects.all()


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder,self).default(obj)