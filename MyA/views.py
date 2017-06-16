#TODO File Description
"""
File Description
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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

# create a new customer or edit a customer
def details_customer(request, pk=None):
    if pk==None:
        customer = Customers ()
        page_title="Kunden anlegen"
    else:
        customer = get_object_or_404(Customers,id=pk)
        page_title = "Kunden ändern"

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
    return render(request, 'details.html', {'page_titel': page_title, 'form':form})

# delete a customer
def delete_customer(request, pk=None):
    if pk==None:
        messages.error (request, u'Daten konnten nicht gelöscht werden')
    else:
        customer = get_object_or_404(Customers,id=pk)
        # check if customer has no contacts
        nocontact= 0
        for c in Contacts.objects.raw ('SELECT * FROM mya_contacts where customer_id='+pk):
            nocontact = 1
        if nocontact==0 :
            customer.delete()
            messages.success (request, u'Daten erfoglreich gelöscht')
        else:
            messages.error (request, u'Daten konnten nicht gelöscht werden')
    return HttpResponseRedirect (reverse ('kundenliste'))

# Contact - View
def get_contact(request):
    contacts = Contacts.objects.all()
    return render(request, 'contact/contact.html', {'page_titel': 'Ansprechpartner', 'contacts':contacts})

# create a new contact or edit a contact
def details_contact(request, pk=None):
    if pk==None:
        contact = Contacts ()
        page_title="Ansprechpartner anlegen"
    else:
        contact = get_object_or_404(Contacts,id=pk)
        page_title = "Ansprechpartner ändern"

    if request.method == 'POST':

        # form sent off
        form = ContactForm (request.POST, instance=contact)
        # Validity check
        if form.is_valid ():
            form.save ()
            messages.success (request, u'Daten erfoglreich geändert')
            return HttpResponseRedirect (reverse ('ansprechpartnerliste'))
        else:
            # error message
            messages.error (request, u'Daten konnten nicht gespeichert werden')
            pass
    else:
        # form first call
        form = ContactForm (instance=contact)
    return render(request, 'details.html', {'page_titel': page_title, 'form':form})

# delete a contact
def delete_contact(request, pk=None):
    if pk==None:
        messages.error (request, u'Daten konnten nicht gelöscht werden')
    else:
        contact = get_object_or_404 (Contacts, id=pk)
        # check if contact has no notes and no events / memberext
        no_notes_and_events= 0
        for n in Notes.objects.raw ('SELECT * FROM mya_notes where contact_id='+pk):
            no_notes_and_events = 1
        for e in MemberExt.objects.raw ('SELECT * FROM mya_memberext where contact_id='+pk):
            no_notes_and_events = 1
        if no_notes_and_events==0 :
            contact.delete()
            messages.success (request, u'Daten erfoglreich gelöscht')
        else:
            messages.error (request, u'Daten konnten nicht gelöscht werden')
    return HttpResponseRedirect (reverse ('ansprechpartnerliste'))

# Note - View
def get_notes(request):
    notes = Notes.objects.all()
    return render(request, 'note/note.html', {'page_titel': 'Notizen', 'notes':notes})

# create a new note or edit a note
def details_note(request, pk=None):
    if pk==None:
        note = Notes ()
        page_title="Notiz anlegen"
    else:
        note = get_object_or_404(Notes,id=pk)
        page_title = "Notiz ändern"

    if request.method == 'POST':

        #form sent off
        form = NoteForm(request.POST,instance=note)
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
        form = NoteForm (instance=note)
    return render(request, 'details.html', {'page_titel': page_title, 'form':form})

# delete a customer
def delete_note(request, pk=None):
    if pk==None:
        messages.error (request, u'Daten konnten nicht gelöscht werden')
    else:
        note = get_object_or_404 (Notes, id=pk)
        note.delete()

    return HttpResponseRedirect (reverse ('notizliste'))
