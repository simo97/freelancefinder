# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-17 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0007_auto_20170430_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='harvest_type',
            field=models.CharField(choices=[('rss_feed', 'rss_feed'), ('custom', 'custom')], default='custom', max_length=20),
        ),
    ]
