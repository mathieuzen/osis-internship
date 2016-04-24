##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2016 Université catholique de Louvain (http://www.uclouvain.be)
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
from django.conf.urls import url

from internship.views import home, internship, master, period, place, student, student_resume

urlpatterns = [
    # S'il vous plaît, organiser les urls par ordre alphabétique.
    url(r'^$', home.internships_home, name='internships_home'),
    url(r'^internships', internship.internships, name='internships'),
    url(r'^internships_masters/$', master.interships_masters, name='interships_masters'),
    url(r'^periods/$', period.internships_periods, name='internships_periods'),
    url(r'^places/$', place.internships_places, name='internships_places'),
    url(r'^students/$', student.internships_students, name='internships_students'),
    url(r'^students/resume/$', student_resume.internships_student_resume, name='internships_student_resume'),
    url(r'^students/search$', student_resume.internships_student_search, name='internships_student_search'),
    url(r'^students/([0-9]+)/resume/$', student_resume.internships_student_read, name='internships_student_read'),
]