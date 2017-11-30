##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2017 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.db import models

from osis_common.models.serializable_model import SerializableModel, SerializableModelAdmin
from internship.models.enums import organization_report_fields


class OrganizationAdmin(SerializableModelAdmin):
    list_display = ('name', 'acronym', 'reference', 'type', 'cohort')
    fieldsets = ((None, {'fields': ('name', 'acronym', 'reference', 'website', 'type', 'cohort')}),)
    search_fields = ['acronym', 'name']


class Organization(SerializableModel):
    name = models.CharField(max_length=255)
    acronym = models.CharField(max_length=15, blank=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    reference = models.CharField(max_length=30, blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True, default="service partner")
    cohort = models.ForeignKey('internship.Cohort', null=False, on_delete=models.CASCADE)
    report_period = models.IntegerField(default=1, blank=True, null=True)
    report_start_date = models.IntegerField(default=2, blank=True, null=True)
    report_end_date = models.IntegerField(default=3, blank=True, null=True)
    report_last_name = models.IntegerField(default=4, blank=True, null=True)
    report_first_name = models.IntegerField(default=5, blank=True, null=True)
    report_gender = models.IntegerField(default=6, blank=True, null=True)
    report_specialty = models.IntegerField(default=7, blank=True, null=True)
    report_birthdate = models.IntegerField(default=8, blank=True, null=True)
    report_email = models.IntegerField(default=9, blank=True, null=True)
    report_noma = models.IntegerField(default=10, blank=True, null=True)
    report_phone = models.IntegerField(default=11, blank=True, null=True)
    report_address = models.IntegerField(default=12, blank=True, null=True)
    report_postal_code = models.IntegerField(default=13, blank=True, null=True)
    report_city = models.IntegerField(default=14, blank=True, null=True)

    def report_sequence(self):
        """ Returns only the report fields that are numered and ordered as numered."""
        sequence = [None, None, None, None, None, None, None,
                    None, None, None, None, None, None, None]
        if self.report_period:
            sequence[self.report_period - 1] = organization_report_fields.PERIOD
        if self.report_start_date:
            sequence[self.report_start_date - 1] = organization_report_fields.START_DATE
        if self.report_end_date:
            sequence[self.report_end_date - 1] = organization_report_fields.END_DATE
        if self.report_last_name:
            sequence[self.report_last_name - 1] = organization_report_fields.LAST_NAME
        if self.report_first_name:
            sequence[self.report_first_name - 1] = organization_report_fields.FIRST_NAME
        if self.report_gender:
            sequence[self.report_gender - 1] = organization_report_fields.GENDER
        if self.report_specialty:
            sequence[self.report_specialty - 1] = organization_report_fields.SPECIALTY
        if self.report_birthdate:
            sequence[self.report_birthdate - 1] = organization_report_fields.BIRTHDATE
        if self.report_email:
            sequence[self.report_email - 1] = organization_report_fields.EMAIL
        if self.report_noma:
            sequence[self.report_noma - 1] = organization_report_fields.NOMA
        if self.report_phone:
            sequence[self.report_phone - 1] = organization_report_fields.PHONE
        if self.report_address:
            sequence[self.report_address - 1] = organization_report_fields.ADDRESS
        if self.report_postal_code:
            sequence[self.report_postal_code - 1] = organization_report_fields.POSTAL_CODE
        if self.report_city:
            sequence[self.report_city - 1] = organization_report_fields.CITY

        return filter(lambda i: i is not None, sequence)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.acronym = self.name[:14]
        super(Organization, self).save(*args, **kwargs)


def search(**kwargs):
    kwargs = {k: v for k, v in kwargs.items() if v}
    queryset = Organization.objects.filter(**kwargs).select_related()
    return queryset


def find_by_id(organization_id):
    return Organization.objects.get(pk=organization_id)
