# Generated by Django 3.1.7 on 2021-03-08 01:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20210307_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 8, 9, 41, 23, 257097), verbose_name='消息发送时间'),
        ),
    ]
