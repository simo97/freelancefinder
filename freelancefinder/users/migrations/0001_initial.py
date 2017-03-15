# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 22:20
from __future__ import unicode_literals

from django.db import migrations

GROUPS = ['Paid', 'Debuggers', 'Administrators']


def load_groups(apps, schema_editor):
    '''Load new groups.'''
    Group = apps.get_model('auth', 'Group')
    for group in GROUPS:
        new_group = Group(name=group)
        new_group.save()


def delete_groups(apps, schema_editor):
    '''Delete these groups.'''
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=GROUPS).delete()


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(load_groups, reverse_code=delete_groups),
    ]
