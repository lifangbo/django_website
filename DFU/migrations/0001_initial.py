# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-08-06 07:29
from __future__ import unicode_literals

from django.db import migrations, models
from ..models import FirmwarePoolInit


def create_constant_tables(apps, schema_editor):
    FirmwarePoolInit()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FirmwarePool',
            fields=[
                ('type', models.CharField(editable=False, max_length=15, primary_key=True, serialize=False)),
                ('version', models.CharField(editable=False, max_length=15)),
                ('size', models.IntegerField(blank=True, editable=False)),
                ('path', models.FilePathField(blank=True, editable=False)),
                ('build_date', models.DateTimeField(blank=True)),
                ('uploaded_date', models.DateTimeField(blank=True)),
                ('download_count', models.IntegerField(blank=True, default=0)),
            ],
        ),

        migrations.RunPython(create_constant_tables),
    ]
