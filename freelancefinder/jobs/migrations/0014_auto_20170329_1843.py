# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0013_auto_20170329_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancer',
            name='fingerprint',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='job',
            name='fingerprint',
            field=models.CharField(max_length=255),
        ),
    ]
