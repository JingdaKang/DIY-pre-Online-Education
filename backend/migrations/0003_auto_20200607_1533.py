# Generated by Django 2.2 on 2020-06-07 07:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20200607_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 7, 15, 33, 44, 929100), verbose_name='消息发送时间'),
        ),
    ]
