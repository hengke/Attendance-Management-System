from django import forms
from .models import Employee


class loginForm(forms.Form):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=Employee
        field=('emp_num')
