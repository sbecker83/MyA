"""
Beschreibung zum Inhalt der Dabei
"""

from django.shortcuts import render
from django.http import HttpResponse
from MyA.models import Mitarbeiter

# Create your views here.

# Mitarbeiter - Hauptseite
def get_staff(request):
    mitarbeiters = Mitarbeiter.objects.all()
    return render(request, 'staff/staff.html', {'page_titel': 'Mitarbeiter', 'mitarbeiters':mitarbeiters})

# Neue Mitarbeiter Anlegen
def new_staff(request):
    return render(request, 'staff/newStaff.html',  {'page_titel': 'Neue Mitarbeiter anlegen'})


