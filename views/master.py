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
from django import shortcuts
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required

from reference.models import country
from internship.models import master_allocation, internship_master, internship_speciality, organization, cohort
from internship.forms.master import MasterForm


@login_required
@permission_required('internship.is_internship_manager', raise_exception=True)
def masters(request, cohort_id):
    current_cohort = shortcuts.get_object_or_404(cohort.Cohort, pk=cohort_id)
    filter_specialty = int(request.GET.get('specialty', 0))
    filter_hospital = int(request.GET.get('hospital', 0))

    allocations = master_allocation.search(current_cohort, filter_specialty, filter_hospital)
    if not filter_specialty and not filter_hospital:
        unallocated_masters = master_allocation.find_unallocated_masters()

    specialties = internship_speciality.find_by_cohort(current_cohort)
    hospitals = organization.find_by_cohort(current_cohort)

    return shortcuts.render(request, "masters.html", locals())


@login_required
@permission_required('internship.is_internship_manager', raise_exception=True)
def master(request, cohort_id, master_id):
    current_cohort = shortcuts.get_object_or_404(cohort.Cohort, pk=cohort_id)
    allocated_master = internship_master.get_by_id(master_id)
    allocations = master_allocation.find_by_master(allocated_master)
    return shortcuts.render(request, "master.html", locals())


@login_required
@permission_required('internship.is_internship_manager', raise_exception=True)
def master_form(request, cohort_id, master_id=None):
    current_cohort = shortcuts.get_object_or_404(cohort.Cohort, pk=cohort_id)
    if master_id:
        allocated_master = internship_master.get_by_id(master_id)
        allocations = master_allocation.find_by_master(allocated_master)
        doctor_selected = 'selected' if allocated_master.civility == 'DOCTOR' else ''
        professor_selected = 'selected' if allocated_master.civility == 'PROFESSOR' else ''
        female_selected = 'selected' if allocated_master.gender == 'F' else ''
        male_selected = 'selected' if allocated_master.gender == 'M' else ''
        generalist_selected = 'selected' if allocated_master.type_mastery == 'GENERALIST' else ''
        specialist_selected = 'selected' if allocated_master.type_mastery == 'SPECIALIST' else ''

    countries = country.find_all()
    specialties = internship_speciality.find_by_cohort(current_cohort)
    hospitals = organization.find_by_cohort(current_cohort)
    return shortcuts.render(request, "master_form.html", locals())


@login_required
@permission_required('internship.is_internship_manager', raise_exception=True)
def master_save(request, cohort_id):
    current_cohort = shortcuts.get_object_or_404(cohort.Cohort, pk=cohort_id)
    allocated_master = internship_master.get_by_id(request.POST.get("id")) if request.POST.get("id") else None

    form = MasterForm(request.POST, instance=allocated_master)
    errors = []
    hospital = ""
    if form.is_valid():
        form.save()
        master_allocation.clean_allocations(allocated_master)
        allocations = _build_allocations(request, allocated_master)
        _save_allocations(allocations)
        hospital = _extract_hospital_id(allocations)
    else:
        errors.append(form.errors)

    if errors:
        return HttpResponseRedirect(reverse("master_edit", args=[current_cohort.id]))

    return HttpResponseRedirect("{}?hospital={}".format(reverse("internships_masters", args=[current_cohort.id]),
                                                        hospital))


@login_required
@permission_required('internship.is_internship_manager', raise_exception=True)
def master_remove(request, cohort_id):
    return None


def _build_allocations(request, allocated_master):
    hospitals = []
    if 'hospital' in request.POST:
        hospitals = request.POST.getlist('hospital')
        hospitals = list(filter(lambda x: x is not "", hospitals))

    specialties = []
    if 'specialty' in request.POST:
        specialties = request.POST.getlist('specialty')
        specialties = list(filter(lambda x: x is not "", specialties))

    allocations = []
    for i, a_hospital in enumerate(hospitals):
        hospital = organization.find_by_id(a_hospital)
        specialty = internship_speciality.find_by_id(specialties[i])
        allocation = master_allocation.MasterAllocation(master=allocated_master,
                                                        organization=hospital,
                                                        specialty=specialty)
        allocations.append(allocation)

    return allocations


def _save_allocations(allocations):
    for allocation in allocations:
        allocation.save()


def _extract_hospital_id(allocations):
    if allocations:
        return allocations[0].organization.id
    else:
        return 0
