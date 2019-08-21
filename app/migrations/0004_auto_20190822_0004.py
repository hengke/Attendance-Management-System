# Generated by Django 2.2.3 on 2019-08-22 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20190821_2334'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendance',
            options={'verbose_name': '考勤记录', 'verbose_name_plural': '考勤记录'},
        ),
        migrations.AlterModelOptions(
            name='holidayarrangements',
            options={'ordering': ['date'], 'verbose_name': '节假日及调休表', 'verbose_name_plural': '节假日及调休表'},
        ),
        migrations.AlterModelOptions(
            name='holidayname',
            options={'verbose_name': '节假日名称', 'verbose_name_plural': '节假日名称'},
        ),
        migrations.AlterModelOptions(
            name='leave',
            options={'ordering': ['ask_time'], 'verbose_name': '请假记录', 'verbose_name_plural': '请假记录'},
        ),
        migrations.AlterModelOptions(
            name='leavetype',
            options={'verbose_name': '休假类别', 'verbose_name_plural': '休假类别'},
        ),
        migrations.AlterModelOptions(
            name='notice',
            options={'verbose_name': '公告表', 'verbose_name_plural': '公告表'},
        ),
        migrations.AlterModelOptions(
            name='signingin',
            options={'verbose_name': '签到表', 'verbose_name_plural': '签到表'},
        ),
        migrations.AlterModelOptions(
            name='usertype',
            options={'verbose_name': '用户类型', 'verbose_name_plural': '用户类型'},
        ),
        migrations.AlterModelOptions(
            name='worktime',
            options={'verbose_name': '工作时间制度', 'verbose_name_plural': '工作时间制度'},
        ),
    ]
