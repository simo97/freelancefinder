# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0011_auto_20170318_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='freelancer',
            name='fingerprint',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='fingerprint',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
