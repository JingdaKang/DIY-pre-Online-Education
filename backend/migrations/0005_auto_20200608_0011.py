# Generated by Django 2.2 on 2020-06-07 16:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20200607_1550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='credit',
        ),
        migrations.RemoveField(
            model_name='course',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='course',
            name='tname',
        ),
        migrations.RemoveField(
            model_name='course',
            name='type',
        ),
        migrations.RemoveField(
            model_name='course',
            name='year',
        ),
        migrations.AddField(
            model_name='course',
            name='status',
            field=models.IntegerField(default=1, verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='course',
            name='stime',
            field=models.DateField(null=True, verbose_name='开始日期'),
        ),
        migrations.AddField(
            model_name='course',
            name='time',
            field=models.IntegerField(default=0, verbose_name='课时'),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 8, 0, 11, 5, 574757), verbose_name='消息发送时间'),
        ),
    ]
