# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 14:22
from __future__ import unicode_literals

from django.db import migrations

NEW_SOURCE_CONFIG = {
    'reddit': {'subreddits': ['freelance_forhire', 'forhire', 'python', 'django', 'nsfwforhire', 'sysadminjobs']},
}


def load_config_data(apps, schema_editor):
    '''Load config data for sources.'''
    Source = apps.get_model('remotes', 'Source')
    SourceConfig = apps.get_model('remotes', 'SourceConfig')
    for source_code, data in NEW_SOURCE_CONFIG.items():
        source = Source.objects.filter(code=source_code).first()
        for key, value in data.items():
            source_config = SourceConfig(source=source, config_key=key)
            source_config.config_value = '|'.join(value)
            source_config.save()


def delete_config_data(apps, schema_editor):
    '''Delete data in the config field.'''
    SourceConfig = apps.get_model('remotes', 'SourceConfig')
    SourceConfig.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0003_auto_20170222_1422'),
    ]

    operations = [
        migrations.RunPython(load_config_data, reverse_code=delete_config_data),
    ]
