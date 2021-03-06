# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 14:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('remotes', '0002_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='SourceConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config_key', models.CharField(max_length=32)),
                ('config_value', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='sourceconfig',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='config', to='remotes.Source'),
        ),
        migrations.AlterUniqueTogether(
            name='sourceconfig',
            unique_together=set([('source', 'config_key')]),
        ),
    ]
