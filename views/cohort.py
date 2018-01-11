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
import uuid
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from internship.forms.cohort import CohortForm
from internship.models.cohort import Cohort
from internship.models.organization import Organization
from internship.models.internship_speciality import InternshipSpeciality


@login_required()
@permission_required('internship.is_internship_manager', raise_exception=True)
def new(request):
    form = CohortForm(request.POST or None)
    if form.is_valid():
        cohort = form.save()
        _copy_data_if_specified(form, cohort)
        return redirect(reverse('internship'))

    context = {
        'form': form,
        'page_title': _('create_cohort'),
        'form_new': True
    }
    return render(request, 'cohort/cohort_form.html', context)


@login_required()
@permission_required('internship.is_internship_manager', raise_exception=True)
def edit(request, cohort_id):
    cohort = get_object_or_404(Cohort, pk=cohort_id)

    form = CohortForm(data=request.POST or None, instance=cohort)

    if form.is_valid():
        form.save()
        return redirect(reverse('internship'))

    context = {
        'form': form,
        'page_title': _('edit_cohort'),
    }

    return render(request, 'cohort/cohort_form.html', context)


def _copy_data_if_specified(cohort_form, cohort):
    if cohort_form.cleaned_data["copy_organizations_from_cohort"] is not None:
        cohort_id_to_copy_from = int(cohort_form["copy_organizations_from_cohort"].value())
        cohort_to_copy_from = Cohort.objects.get(pk=cohort_id_to_copy_from)
        _copy_organizations(cohort_to_copy_from, cohort)
    if cohort_form.cleaned_data["copy_specialities_from_cohort"] is not None:
        cohort_id_to_copy_from = int(cohort_form["copy_specialities_from_cohort"].value())
        cohort_to_copy_from = Cohort.objects.get(pk=cohort_id_to_copy_from)
        _copy_specialities(cohort_to_copy_from, cohort)


def _copy_organizations(cohort_from, cohort_to):
    organizations = Organization.objects.filter(cohort=cohort_from)
    for organization in organizations:
        new_organization = organization
        new_organization.pk = None
        new_organization.uuid = uuid.uuid4()
        new_organization.cohort = cohort_to
        new_organization.save()


def _copy_specialities(cohort_from, cohort_to):
    specialities = InternshipSpeciality.objects.filter(cohort=cohort_from)
    for speciality in specialities:
        new_speciality = speciality
        new_speciality.pk = None
        new_speciality.uuid = uuid.uuid4()
        new_speciality.cohort = cohort_to
        new_speciality.save()
