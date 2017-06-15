#TODO File Description
"""
File Description
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse
from MyA.forms import *


# Create your views here.

# Index - View
def homesite(request):
    return render(request, 'index.html', {'page_titel': 'Startseite'})


# Staff - View
def get_staff(request):
    mitarbeiter = Staffs.objects.all()
    return render(request, 'staff/staff.html', {'page_titel': 'Mitarbeiter', 'staffs': mitarbeiter})


# Create new Staff - View
def new_Staff(request):
    if request.method == 'POST':
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


# Staff Profile - View
def myProfile(request):
    if request.method == 'POST':
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

# Calendar - View
def calendar(request):
    return render(request, 'calendar/calendar.html', {'page_titel': 'Terminkalender'})

# Customer - View
def get_customer(request):
    customers = Customers.objects.all()
    return render(request, 'customer/customer.html', {'page_titel': 'Kunden', 'customers':customers})

# Create new Customer
def new_customer(request):
    customer = Customers ()
    if request.method == 'POST':

        #form sent off
        form = CustomerForm(request.POST,instance=customer)
        #Validity check
        if form.is_valid():
            form.save()
            messages.success (request, u'Daten erfoglreich geändert')
            return HttpResponseRedirect(reverse('kundenliste'))
        else:
            # error message
            messages.error (request, u'Daten konnten nicht gespeichert werden')
            pass
    else:
        # form first call
        form = CustomerForm (instance=customer)
    return render(request, 'customer/newcustomer.html', {'page_titel': 'Kunden', 'form':form})
