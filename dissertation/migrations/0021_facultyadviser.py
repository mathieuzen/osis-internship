# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-12 20:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0045_auto_20160512_0917'),
        ('dissertation', '0020_auto_20160512_2233'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacultyAdviser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dissertation.Adviser')),
                ('structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Structure')),
            ],
        ),
    ]
