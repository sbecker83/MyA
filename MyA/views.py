"""
Beschreibung zum Inhalt der Dabei
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from MyA.models import *
from MyA.forms import *


# Create your views here.

# Mitarbeiter - Hauptseite
def homesite(request):
    return render(request, 'index.html', {'page_titel': 'Startseite'})


# Mitarbeiter - Hauptseite
def get_staff(request):
    mitarbeiter = Staffs.objects.all()
    return render(request, 'staff/staff.html', {'page_titel': 'Mitarbeiter', 'staffs': mitarbeiter})


# Neue Mitarbeiter Anlegen
def new_Staff(request):
    if request.method == 'POST':
        # Formular wurde abgeschickt
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u'Mitarbeiter angelegt')
            return HttpResponseRedirect(reversed('staff'))
        else:
            messages.error(request, u'Daten konnten nicht gespeichert werden')
            pass
    else:
        form = StaffForm()

    return render(request, 'staff/newStaff.html', {'page_titel': 'Neue Mitarbeiter anlegen', 'form': form})


# Neue Mitarbeiter Anlegen
def myProfile(request):

    if request.method == 'POST':
        # Formular wurde abgeschickt
        form = StaffProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u'Daten erfoglreich geändert')
            return HttpResponseRedirect(reversed('profile'))
        else:
            messages.error(request, u'Daten konnten nicht gespeichert werden')
            pass
    else:
        form = StaffProfileForm()

    return render(request, 'profile.html', {'page_titel': 'Mein Profil',  'form': form})
