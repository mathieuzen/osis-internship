# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-05 07:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0038_optimize_organization_address_queries'),
    ]

    operations = [
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('length_in_periods', models.IntegerField(default=1)),
                ('cohort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internship.Cohort')),
                ('speciality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='internship.InternshipSpeciality')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
