# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-24 17:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calaccess_processed', '0041_form460schedulecsummary_form460schedulecsummaryversion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='form460schedulecsummary',
            options={'verbose_name': 'Form 460 (Campaign Disclosure) Schedule C summary', 'verbose_name_plural': 'Form 460 (Campaign Disclosure) Schedule C summaries'},
        ),
        migrations.AlterModelOptions(
            name='form460schedulecsummaryversion',
            options={'verbose_name': 'Form 460 (Campaign Disclosure) Schedule C summary version'},
        ),
    ]
