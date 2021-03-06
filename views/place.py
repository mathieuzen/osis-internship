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
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from internship import models
from internship.forms.organization_form import OrganizationForm
from internship.utils.exporting import organization_affectation_master
from internship.utils.exporting import organization_affectation_hospital
from internship.views.internship import get_all_specialities, set_tabs_name
from reference.models import country


@login_required
@permission_required('internship.is_internship_manager', raise_exception=True)
def internships_places(request, cohort_id):
    cohort = get_object_or_404(models.cohort.Cohort, pk=cohort_id)
    organizations = models.organization.Organization.objects.filter(cohort=cohort).order_by('reference')

    context = {
        'section': 'internship',
        'all_organizations': organizations,
        'cohort': cohort,
    }
    return render(request, "places.html", context)


@login_required
@permission_required('internship.is_internship_manager', raise_exception=True)
def place_save(request, cohort_id, organization_id):
    cohort = get_object_or_404(models.cohort.Cohort, pk=cohort_id)

    if organization_id:
        organization = models.organization.get_by_id(organization_id)
    else:
        models.organization.Organization.objects.filter(reference=request.POST.get('reference')).delete()
        organization = models.organization.Organization()

    organization.cohort = cohort

    form = OrganizationForm(data=request.POST, instance=organization)
    if form.is_valid():
        form.save()

    countries = country.find_all()

    return render(request, "place_form.html", locals())


@login_required
@permission_required('internship.is_internship_manager', raise_exception=True)
def place_remove(request, cohort_id, organization_id):
    cohort = get_object_or_404(models.cohort.Cohort, pk=cohort_id)
    organization = models.organization.get_by_id(organization_id)
    organization.delete()
    return internships_places(request, cohort_id)


@login_required
@permission_required('internship.is_internship_manager', raise_exception=True)
def organization_new(request, cohort_id):
    return place_save(request, cohort_id, None)


@login_required
@permission_required('internship.is_internship_manager', raise_exception=True)
def organization_edit(request, cohort_id, organization_id):
    cohort = get_object_or_404(models.cohort.Cohort, pk=cohort_id)
    organization = models.organization.get_by_id(organization_id)
    countries = country.find_all()
    return render(request, "place_form.html", locals())


@login_required
@permission_required('internship.is_internship_manager', raise_exception=True)
def organization_create(request, cohort_id):
    cohort = get_object_or_404(models.cohort.Cohort, pk=cohort_id)
    countries = country.find_all()
    return render(request, "place_form.html", locals())


@login_required
@permission_required('internship.is_internship_manager', raise_exception=True)
def student_choice(request, cohort_id, organization_id):
    cohort = get_object_or_404(models.cohort.Cohort, pk=cohort_id)
    organization = get_object_or_404(models.organization.Organization, pk=organization_id)
    organization_choice = models.internship_choice.search(organization=organization)

    all_offers = models.internship_offer.search(organization=organization, cohort=cohort)
    all_speciality = models.internship_speciality.find_all(cohort)
    set_tabs_name(all_speciality)
    for al in all_offers:
        number_first_choice = len(models.internship_choice.search(organization=al.organization,
                                                                  speciality=al.speciality,
                                                                  choice=1))
        number_all_choice = len(models.internship_choice.search(organization=al.organization,
                                                                speciality=al.speciality))
        al.number_first_choice = number_first_choice
        al.number_all_choice = number_all_choice

    context = {
        'organization': organization,
        'organization_choice': organization_choice,
        'offers': all_offers,
        'specialities': all_speciality,
        'cohort': cohort,
    }
    return render(request, "place_detail.html", context)


@login_required
@permission_required('internship.is_internship_manager', raise_exception=True)
def student_affectation(request, cohort_id, organization_id):
    cohort = get_object_or_404(models.cohort.Cohort, pk=cohort_id)
    organization = get_object_or_404(models.organization.Organization, pk=organization_id)

    affectations = models.internship_student_affectation_stat.search(organization=organization).order_by("student__person__last_name", "student__person__first_name")

    for a in affectations:
        a.email = ""
        a.adress = ""
        a.phone_mobile = ""
        internship_student_information= models.internship_student_information.search(person=a.student.person,
                                                                                     cohort=cohort)
        if internship_student_information:
            informations = internship_student_information.first()
            a.email = informations.email
            a.adress = informations.location + " " + informations.postal_code + " " + informations.city
            a.phone_mobile = informations.phone_mobile
    periods = models.period.search(cohort=cohort)

    internships = models.internship_offer.search(organization = organization, cohort=cohort)
    all_speciality = get_all_specialities(internships)
    all_speciality = models.internship_speciality.set_speciality_unique(all_speciality)
    set_tabs_name(all_speciality)
    context = {
        'organization': organization,
        'affectations': affectations,
        'specialities': all_speciality,
        'periods': periods,
        'cohort': cohort,
    }
    return render(request, "place_detail_affectation.html", context)


@login_required
@permission_required('internship.is_internship_manager', raise_exception=True)
def export_organisation_affectation_master(request, cohort_id, organization_id):
    cohort = get_object_or_404(models.cohort.Cohort, pk=cohort_id)
    organization = models.organization.get_by_id(organization_id)
    internships = models.internship_offer.search(organization=organization)
    specialities = list({offer.speciality for offer in internships})
    specialities = sorted(specialities, key=lambda spec: spec.name)
    affections_by_specialities = [(internship_speciality,
                                   list(models.internship_student_affectation_stat.search(organization=organization,
                                                                                          speciality=internship_speciality)))
                                  for internship_speciality in specialities]
    for speciality, affectations in affections_by_specialities:
        for affectation in affectations:
            affectation.email = ""
            affectation.adress = ""
            affectation.phone_mobile = ""
            affectation.master = ""
            internship_student_information = models.internship_student_information.search(person=affectation.student.person)
            internship_offer = models.internship_offer.search(organization=affectation.organization,
                                                              speciality=affectation.speciality)
            if internship_student_information:
                informations = internship_student_information.first()
                affectation.email = informations.email
                affectation.adress = informations.location + " " + informations.postal_code + " " + informations.city
                affectation.phone_mobile = informations.phone_mobile
            if internship_offer:
                offer = internship_offer.first()
                affectation.master = offer.master
    return _export_xls_master(cohort, organization, affections_by_specialities)


@login_required
@permission_required('internship.is_internship_manager', raise_exception=True)
def export_hospital_affectation(request, cohort_id, organization_id):
    cohort = get_object_or_404(models.cohort.Cohort, pk=cohort_id)
    organization = models.organization.get_by_id(organization_id)
    return _export_xls_hospital(cohort, organization)


def _export_xls_master(cohort, organization, affections_by_specialities):
    if not affections_by_specialities:
        redirect_url = reverse('place_detail_student_affectation', kwargs={
            'cohort_id': cohort.id,
            'organization_id': organization.id,
        })
        return HttpResponseRedirect(redirect_url)
    else:
        virtual_workbook = organization_affectation_master.export_master_xls(cohort, organization,
                                                                             affections_by_specialities)
        return _export_xls(organization, virtual_workbook)


def _export_xls_hospital(cohort, organization):
    virtual_workbook = organization_affectation_hospital.export_hospital_xls(cohort, organization)
    return _export_xls(organization, virtual_workbook)


def _export_xls(organization, virtual_workbook):
    response = HttpResponse(virtual_workbook,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    file_name_parts = organization.name.strip().replace(' ', '_')
    file_name = "affectation_{}_{}.xlsx".format(str(organization.reference), file_name_parts)
    response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
    return response
