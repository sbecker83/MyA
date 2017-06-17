#TODO File Description
"""
File Description
"""
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from MyA.forms import *
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,SetPasswordForm

# Create your views here.

# Index - View
def homesite(request):
    return render(request, 'index.html', {'page_title': 'Startseite'})


# Employee - View
# only the superuser is allowed for this view
@user_passes_test(lambda u: u.is_superuser)
def get_employees(request):
    employees = Employee.objects.all()
    return render(request, 'employee/employee.html', {'page_title': 'Mitarbeiter', 'employees': employees})


def edit_profile(request):
    # get the current employee from the current user id
    employee = Employee.objects.get(user=request.user.id)
    # use the view for creating and editing employees but for the current user id
    return details_employee(request, pk=employee.id)

# Create new Employee - View
def details_employee(request, pk=None):
    is_edit = False
    if pk==None:
        # a new user is will be created
        user = User()
        employee = Employee()
        page_title = "Mitarbeiter anlegen"
    else:
        # an existing user will be edited
        is_edit = True
        employee = get_object_or_404(Employee, id=pk)
        user = employee.user
        # check if the current user has permission to edit this employee/user
        if not (request.user.is_superuser or user == request.user ):
            raise PermissionDenied
        page_title = "Mitarbeiter editieren"
    if request.method == 'POST':
        # the form for a new user and an existing user differs (password field)
        if is_edit:
            user_form = UserEditForm(request.POST, instance=user)
        else:
            user_form = UserCreationForm(request.POST, instance=user)

        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid() and user_form.is_valid():
            user = user_form.save()
            # we need to set the relationsship between the user and the employee manually
            employee = form.save(commit=False)
            employee.user = user
            employee.save()

            messages.success(request, u'Mitarbeiter angelegt')
            return HttpResponseRedirect(reversed('mitarbeiter'))
        else:
            messages.error(request, u'Daten konnten nicht gespeichert werden')
            pass
    else:
        form = EmployeeForm(instance=employee)
        # the form for a new user and an existing user differs (password field)
        if is_edit:
            user_form = UserEditForm(instance=user)
        else:
            user_form = UserCreationForm(instance=user)

    return render(request, 'employee/newEmployee.html', {'page_title': page_title, 'user_form': user_form, 'form': form})


# only the superuser is allowed for this view
@user_passes_test(lambda u: u.is_superuser)
def set_password(request, pk):
    user = get_object_or_404(User, id=pk)
    page_title = "Passwort für User " + user.username + " ändern"
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Das Passwort wurde geändert')
        else:
            messages.error(request, 'Fehler')
    else:
        form = SetPasswordForm(user)
    return render(request, 'employee/password.html', {'page_title': page_title, 'form': form})

def change_password(request,pk=None):
    user = request.user
    page_title = "Eigenes Passwort ändern"
    if request.method == 'POST':
        form = PasswordChangeForm(user,request.POST)
        if form.is_valid():
            user = form.save()
            # we need to update the session after a password change
            update_session_auth_hash(request,user)
            messages.success(request,'Das Passwort wurde geändert')
        else:
            messages.error(request,'Fehler')
    else:
        form = PasswordChangeForm(instance=user)
    return render(request, 'employee/password.html', {'page_title': page_title, 'form': form})

# Calendar - View
def calendar(request):
    return render(request, 'calendar/calendar.html', {'page_title': 'Terminkalender'})

# Customer - View
def get_customer(request):
    customers = Customer.objects.all()
    return render(request, 'customer/customer.html', {'page_title': 'Kunden', 'customers':customers})

# create a new customer or edit a customer
def details_customer(request, pk=None):
    if pk==None:
        customer = Customer ()
        page_title="Kunden anlegen"
    else:
        customer = get_object_or_404(Customer, id=pk)
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
    return render(request, 'details.html', {'page_title': page_title, 'form':form})

# delete a customer
def delete_customer(request, pk=None):
    if pk==None:
        messages.error (request, u'Daten konnten nicht gelöscht werden')
    else:
        customer = get_object_or_404(Customer, id=pk)
        # check if customer has no contacts
        nocontact= 0
        for c in Contact.objects.raw ('SELECT * FROM mya_contacts where customer_id='+pk):
            nocontact = 1
        if nocontact==0 :
            customer.delete()
            messages.success (request, u'Daten erfoglreich gelöscht')
        else:
            messages.error (request, u'Daten konnten nicht gelöscht werden')
    return HttpResponseRedirect (reverse ('kundenliste'))

# Contact - View
def get_contact(request):
    contacts = Contact.objects.all()
    return render(request, 'contact/contact.html', {'page_title': 'Ansprechpartner', 'contacts':contacts})

# create a new contact or edit a contact
def details_contact(request, pk=None):
    if pk==None:
        contact = Contact ()
        page_title="Ansprechpartner anlegen"
    else:
        contact = get_object_or_404(Contact, id=pk)
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
    return render(request, 'details.html', {'page_title': page_title, 'form':form})

# delete a contact
def delete_contact(request, pk=None):
    if pk==None:
        messages.error (request, u'Daten konnten nicht gelöscht werden')
    else:
        contact = get_object_or_404 (Contact, id=pk)
        # check if contact has no notes and no events / memberext
        no_notes_and_events= 0
        for n in Note.objects.raw ('SELECT * FROM mya_notes where contact_id='+pk):
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
    notes = Note.objects.all()
    return render(request, 'note/note.html', {'page_title': 'Notizen', 'notes':notes})

# create a new note or edit a note
def details_note(request, pk=None):
    if pk==None:
        note = Note ()
        page_title="Notiz anlegen"
    else:
        note = get_object_or_404(Note, id=pk)
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
    return render(request, 'details.html', {'page_title': page_title, 'form':form})

# delete a customer
def delete_note(request, pk=None):
    if pk==None:
        messages.error (request, u'Daten konnten nicht gelöscht werden')
    else:
        note = get_object_or_404 (Note, id=pk)
        note.delete()

    return HttpResponseRedirect (reverse ('notizliste'))
