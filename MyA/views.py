"""
Beschreibung zum Inhalt der Dabei
"""

from django.shortcuts import render
from django.http import HttpResponse
from MyA.models import Staffs

# Create your views here.

# Mitarbeiter - Hauptseite
def homesite(request):
    return render(request, 'index.html', {'page_titel': 'Startseite'})

# Mitarbeiter - Hauptseite
def get_staff(request):
    mitarbeiter = Staffs.objects.all()
    return render(request, 'staff/staff.html', {'page_titel': 'Mitarbeiter', 'staffs':mitarbeiter})

# Neue Mitarbeiter Anlegen
def new_staff(request):
    return render(request, 'staff/newStaff.html',  {'page_titel': 'Neue Mitarbeiter anlegen'})

# Neue Mitarbeiter Anlegen
def myProfile(request):
    return render(request, 'profile.html',  {'page_titel': 'Mein Profil'})
