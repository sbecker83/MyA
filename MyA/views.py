"""
Filename: views.py
Description: All view definition and their logic
"""
import locale
from calendar import *
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from MyA.forms import *
from MyA.admin import EmployeeResource, CustomerResource, ContactResource, NoteResource
from datetime import datetime


# ======================================================== #
# Dashboard - View
# ======================================================== #

def dashboard(request):
    """
    Renders a dashboard page with a list of notes and events of the current user
    """
    # get the employee model of the current user
    employee = Employee.objects.get(user=request.user.id)

    # get the notes of the current user
    my_notes = Note.objects.filter(employee=employee)

    # get the future events of the current user
    my_events = Event.objects.filter(memberint__employee_id=employee.id).exclude(date__lt=datetime.today())

    # add a custom field "status" for the events of the current user
    for my_event in my_events:
        member_int = MemberInt.objects.get(event=my_event, employee=employee)
        my_event.status = member_int.status

    return render(request, 'dashboard.html', {'page_title': 'Dashboard',
                                              'employee_name': employee.get_fullname(),
                                              'my_notes': my_notes,
                                              'my_events': my_events})


# ======================================================== #
# Employee - View
# ======================================================== #

@user_passes_test(lambda u: u.is_superuser)
def list_employees(request):
    """
    Renders a list with all employees.
    ADMIN ONLY: This view can only be used by the superuser
    """
    employees = Employee.objects.all()

    return render(request, 'list_employee.html', {'page_title': 'Mitarbeiter', 'employees': employees})


def detail_employee(request, pk=None, is_profile=False):
    """
    Creates/edits an employee.
    The employee model will be directly linked to the django auth user.
    It may also be used with the profile of an user (hence the is_profile variable), the only difference is
    the redirect after an edit.
    """
    # if an existing employee is edited, this variable will be set to True
    is_edit = False

    if pk is None:
        # a new user/employee is will be created as no primary key if given
        user = User()
        employee = Employee()
        page_title = "Mitarbeiter anlegen"
    else:
        # an existing user will be edited
        is_edit = True
        employee = get_object_or_404(Employee, id=pk)
        user = employee.user
        # check if the current user has permission to edit this employee/user
        if not(request.user.is_superuser or user == request.user):
            raise PermissionDenied
        # set page title
        page_title = "Bearbeiten: {}".format(employee.get_fullname())

    if request.method == 'POST':
        # the form for a new user and an existing user differs (password field)
        if is_edit:
            user_form = UserEditForm(request.POST, instance=user)
        else:
            user_form = UserCreationForm(request.POST, instance=user)

        employee_form = EmployeeForm(request.POST, instance=employee)
        if employee_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            # we need to set the relationship between the user and the employee manually
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

            if is_profile:
                messages.success(request, u'Profil gespeichert!')
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                messages.success(request, u'Mitarbeiter gespeichert!')
                return HttpResponseRedirect(reverse('list_employees'))
        else:
            messages.error(request, u'Daten konnten nicht gespeichert werden!')
            pass
    else:
        employee_form = EmployeeForm(instance=employee)
        # the form for a new user and an existing user differs (password field)
        if is_edit:
            user_form = UserEditForm(instance=user)
        else:
            user_form = UserCreationForm(instance=user)

    return render(request, 'detail.html', {'page_title': page_title, 'forms': [user_form, employee_form]})


@user_passes_test(lambda u: u.is_superuser)
def toggle_employee_active(request, pk=None):
    """
    Deactivates/activates a user  depending on the current status
    ADMIN ONLY: This view can only be used by the superuser
    """
    if pk is None:
        messages.error(request, u'Mitarbeiter konnten nicht aktiviert/deaktiviert werden!')
    else:
        employee = get_object_or_404(Employee, id=pk)
        user = employee.user
        if user.is_active:
            user.is_active = False
            user.save()
            messages.success(request, u'Mitarbeiter erfolgreich deaktiviert!')
        else:
            user.is_active = True
            user.save()
            messages.success(request, u'Mitarbeiter erfolgreich aktiviert!')

    return HttpResponseRedirect(reverse('list_employees'))


@user_passes_test(lambda u: u.is_superuser)
def set_password(request, pk):
    """
    Sets the password for a user WITHOUT entering the old password
    ADMIN ONLY: This view can only be used by the superuser
    """
    user = get_object_or_404(User, id=pk)
    page_title = "Passwort für User " + user.username + " ändern"
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Das Passwort wurde geändert!')
            return HttpResponseRedirect(reverse('edit_employee', args=[pk]))
        else:
            messages.error(request, 'Fehler!')
    else:
        form = SetPasswordForm(user)

    return render(request, 'detail.html', {'page_title': page_title, 'forms': [form]})


def export_employees(request):
    """
    Exports the list of employees to an Excel document
    """
    dataset = EmployeeResource().export()
    filename = 'employees.xls'

    # set the response as a downloadable excel file
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    # set the file name
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    return response


# ======================================================== #
# Profile - View
# ======================================================== #

def edit_profile(request):
    """
    Uses the detail_employee view but with the is_profile variable set, so the details_employee view can handle
    profile specifics
    """
    # get the current employee from the current user id
    employee = get_object_or_404(Employee, user=request.user.id)

    # use the detail_employee view with the is_profile flag set
    return detail_employee(request, pk=employee.id, is_profile=True)


def change_password(request):
    """
    Changes the password for a user with entering the old password
    """
    user = request.user
    page_title = "Eigenes Passwort ändern"
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            # we need to update the session after a password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Das Passwort wurde geändert!')
            return HttpResponseRedirect(reverse('profile'))
        else:
            messages.error(request, 'Fehler!')
    else:
        form = PasswordChangeForm(user=user)

    return render(request, 'detail.html', {'page_title': page_title, 'forms': [form]})


# ======================================================== #
# Customer - View
# ======================================================== #

def list_customers(request):
    """
    Renders a list with all customers.
    """
    customers = Customer.objects.all

    return render(request, 'list_customer.html', {'page_title': 'Kunden', 'customers': customers})


def detail_customer(request, pk=None):
    """
    Creates/edits a customer.
    """
    if pk is None:
        customer = Customer()
        page_title = "Kunden anlegen"
    else:
        customer = get_object_or_404(Customer, id=pk)
        page_title = "Kunden ändern"

    if request.method == 'POST':
        # form sent off
        form = CustomerForm(request.POST, instance=customer)
        # validity check
        if form.is_valid():
            form.save()
            messages.success(request, u'Daten erfolgreich geändert!')
            return HttpResponseRedirect(reverse('list_customers'))
        else:
            # error message
            messages.error(request, u'Der Kunde konnte nicht gespeichert werden!')
            pass
    else:
        # form first call
        form = CustomerForm(instance=customer)

    return render(request, 'detail.html', {'page_title': page_title, 'forms': [form]})


def delete_customer(request, pk=None, is_delete=None):
    """
    Deletes a customer.
    If a customer can not be deleted (because contacts exist), it will be deactivated for further use.
    """
    if pk is None:
        messages.error(request, u'Der Kunde konnte nicht gelöscht werden!')
    else:
        customer = get_object_or_404(Customer, id=pk)
        if is_delete == "1":
            # trying to delete the customer

            # check if customer has contacts
            has_contacts = Contact.objects.filter(customer_id=pk).exists()
            if not has_contacts:
                customer.delete()
                messages.success(request, u'Der Kunde wurde erfolgreich gelöscht!')
            else:
                if customer.is_active:
                    # Customer has contacts so he can only be disabled
                    customer.is_active = False
                    Contact.objects.select_related().filter(customer=customer.id).update(is_active=False)
                    customer.save()
                    messages.success(request, u'Der Kunde hat zugeordnete Ansprechpartner, deshalb konnte er nicht gelöscht werden! Der Kunde wurde deaktiviert!')
                else:
                    messages.error(request, u'Der Kunde konnte nicht gelöscht werden, weil es noch Ansprechpartner gibt!')
        else:
            # active/deactivate the customer and all its contacts
            if customer.is_active:
                customer.is_active = False
                # update all contacts of the customer as well
                Contact.objects.select_related().filter(customer=customer.id).update(is_active=False)
            else:
                customer.is_active = True
                # update all contacts of the customer as well
                Contact.objects.select_related().filter(customer=customer.id).update(is_active=True)
            customer.save()
            messages.success(request, u'Der Kunde erfolgreich de-/aktiviert!')

    return HttpResponseRedirect(reverse('list_customers'))


def export_customers(request):
    """
    Exports the list of customers to an Excel document
    """
    dataset = CustomerResource().export()
    filename = 'customers.xls'

    # set the response as a downloadable excel file
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    # set the file name
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    return response


# ======================================================== #
# Contact - View
# ======================================================== #

def list_contacts(request, fk=None):
    """
    Renders a list with all contacts of a specific customer (fk).
    """
    contacts = Contact.objects.filter(customer_id=fk)
    # show the customers company name in the title
    customer = get_object_or_404(Customer, id=fk)
    page_title = "Ansprechpartner - {}".format(customer.company)

    return render(request, 'list_contact.html', {'page_title': page_title, 'contacts': contacts,
                                                 'selected_customer_id': fk})


def details_contact(request, pk=None, fk=None):
    """
    Create/edits a contact for a customer
    """
    # show the company in the title - select from customer
    customer = get_object_or_404(Customer, id=fk)

    # set page-title for a new contact or for edit contact
    if pk is None:
        # new contact
        contact = Contact()
        page_title = "Ansprechpartner anlegen - {}".format(customer.company)
    else:
        # edit contact
        contact = get_object_or_404(Contact, id=pk)
        page_title = "Ansprechpartner ändern - {}".format(customer.company)

    if request.method == 'POST':
        # form sent off
        # parameter of the form selected customer (fk) per initial
        form = ContactForm(request.POST, instance=contact, initial={'customer': fk})

        # validity check
        if form.is_valid():
            form = form.save(commit=False)
            # set customer-id
            form.customer_id = fk
            form.save()
            messages.success(request, u'Der Ansprechpartner wurde erfolgreich geändert!')
            # parameter to filter to the selected customer (fk) per args
            return HttpResponseRedirect(reverse('list_contacts', args=[fk]))
        else:
            # error message
            messages.error(request, u'Der Ansprechpartner konnte nicht gespeichert werden!')
            pass
    else:
        # form first call
        # parameter of the form selcted customer (fk) per initial
        form = ContactForm(instance=contact,  initial={'customer': fk})

    return render(request, 'detail.html', {'page_title': page_title, 'forms': [form]})


def delete_contact(request, pk=None, fk=None, is_delete=None):
    """
    Deletes a contact for a customer (fk)
    If a contact can not be deleted (because notes or events exist with this contact), it will be deactivated for
    further use.
    """
    if pk is None:
        messages.error(request, u'Daten konnten nicht gelöscht werden!')
    else:
        if is_delete == "1":
            # trying to delete the customer
            contact = get_object_or_404(Contact, id=pk)
            # check if contact has no notes and no events / memberext
            has_notes = Note.objects.filter(contact_id=contact.id).exists()
            has_member_ext = MemberExt.objects.filter(contact_id=contact.id).exists()
            if not has_notes and not has_member_ext:
                contact.delete()
                messages.success(request, u'Der Ansprechpartner wurde erfolgreich gelöscht!')
            else:
                # check if customer active
                customer = Customer.objects.get(id=contact.customer_id)
                if customer.is_active and contact.is_active:
                    # contact has relations to a child-table so it can only be disabled
                    contact.is_active = False
                    contact.save()
                    messages.success(request, u'Der Ansprechpartner hat zugeordnete Notizen oder Termine, deshalb konnte er nicht gelöscht werden! Er wurde deaktiviert!')
                else:
                    messages.error(request, u'Der Ansprechpartner konnte nicht gelöscht werden, weil es noch zugeordnete Notizen oder Termine!')
        else:
            # active/deactivate the customer and all its contacts
            contact = get_object_or_404(Contact, id=pk)
            # check if customer active
            customer = get_object_or_404(Customer, id=contact.customer_id)

            if customer.is_active:
                if contact.is_active:
                    contact.is_active = False
                    contact.save()
                    messages.success(request, u'Kontakt erfolgreich deaktiviert!')
                elif not contact.is_active:
                    contact.is_active = True
                    contact.save()
                    messages.success(request, u'Kontakt erfolgreich aktiviert!')
            else:
                messages.error(request,
                               u'Anspechpartner konnten nicht de-/aktiviert werden, da der Kunde deaktiviert ist! ')

    # parameter to filter to the selected customer (fk) per args
    return HttpResponseRedirect(reverse('list_contacts', args=[fk]))


def export_contacts(request):
    """
    Exports the list of contacts to an Excel document
    """
    dataset = ContactResource().export()
    filename = 'contacts.xls'

    # set the response as a downloadable excel file
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    # set the file name
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    return response


# ======================================================== #
# Note - View
# ======================================================== #


def list_notes(request):
    """
    Renders a list with notes. Can be filtered.
    """
    filtertext = ''
    if request.method == 'POST':
        selemployee = request.POST.get('selemployee')
        selcustomer = request.POST.get('selcustomer')
        selcontact = request.POST.get('selcontact')

        # check if employee filter is set and get the corresponding employee object
        if selemployee != '':
            has_employee_filter = True
            employee = get_object_or_404(Employee, id=selemployee)
        else:
            has_employee_filter = False

        # check if customer filter is set and get the corresponding customer object
        if selcustomer != '':
            has_customer_filter = True
            customer = get_object_or_404(Customer, id=selcustomer)
        else:
            has_customer_filter = False

        # check if contact filter is set and get the corresponding contact object
        if selcontact != '':
            has_contact_filter = True
            contact = get_object_or_404(Contact, id=selcontact)
        else:
            has_contact_filter = False

        # no filter selected:
        if not has_employee_filter and not has_customer_filter and not has_contact_filter:
            notes = Note.objects.all()
        else:
            # at least one filter is set
            filtertext = "Filter nach: "

            # employee filter:
            if has_employee_filter and not has_customer_filter and not has_contact_filter:
                notes = Note.objects.filter(employee_id=selemployee)
                filtertext += employee.get_fullname()

            # customer filter:
            elif not has_employee_filter and has_customer_filter and not has_contact_filter:
                notes = Note.objects.filter(contact__customer_id=selcustomer)
                filtertext += customer.company

            # contact (or customer and contact combined) filter:
            elif (not has_employee_filter and not has_customer_filter and has_contact_filter)\
                    or (not has_employee_filter and has_customer_filter and has_contact_filter):
                notes = Note.objects.filter(contact_id=selcontact)
                filtertext += contact.get_fullname()

            # employee and customer filter:
            elif has_employee_filter and has_customer_filter and not has_contact_filter:
                notes = Note.objects.filter(contact__customer_id=selcustomer, employee_id=selemployee)
                filtertext += employee.get_fullname() + ", " + customer.company

            # employee and contact filter:
            elif has_employee_filter and not has_customer_filter and has_contact_filter:
                notes = Note.objects.filter(contact_id=selcontact).filter(employee_id=selemployee)
                filtertext += employee.get_fullname() + ", " + contact.get_fullname()

    else:
        # first call
        notes = Note.objects.all()

    form = FilterNoteForm()
    # Contact list for use in javascript for the dynamic list
    mylist = Contact.objects.all()

    return render(request, 'list_note.html',
                  {'page_title': 'Notizen',
                   'notes': notes,
                   'forms': [form],
                   'mylist': mylist,
                   'page_filtertext': filtertext})


def detail_note(request, pk=None):
    """
    Creates/edits a note.
    """
    # current employee
    employee = get_object_or_404(Employee, user=request.user.id)
    if pk is None:
        note = Note()
        page_title = "Notiz anlegen"
    else:
        note = get_object_or_404(Note, id=pk)
        page_title = "Notiz ändern"

    if request.method == 'POST':
        # form sent off
        form = NoteForm(request.POST, instance=note)
        # validity check
        if form.is_valid():
            form = form.save(commit=False)
            # set employee with current employee
            form.employee_id = employee.id
            # set contact from the Select-Contact-Field - value form the request
            form.contact_id = request.POST.get('selcontact')
            form.save()
            messages.success(request, u'Die Notiz wurde erfolgreich geändert!')
            return HttpResponseRedirect(reverse('list_notes'))
        else:
            # error message
            messages.error(request, u'Die Notiz konnte nicht gespeichert werden!')
            pass
    else:
        if pk is None:
            # form first call - to insert a new note
            # tranfer current employee
            form = NoteForm(instance=note, myemployee=employee.id,)
        else:
            # form first call with a pk - to edit a note
            # transfer the customer_id and the contact_id for the unbound selection fields
            form = NoteForm(instance=note, myemployee=employee.id,  mycustomer=note.contact.customer_id, mycontact=note.contact_id)

    # Contact list for use in javascript for the dynamic list
    mylist = Contact.objects.all()

    return render(request, 'detail_note.html', {'page_title': page_title, 'forms': [form], 'mylist': mylist})


def delete_note(request, pk=None):
    """
    Deletes a note.
    """
    if pk is None:
        messages.error(request, u'Die Notiz konnte nicht gelöscht werden!')
    else:
        note = get_object_or_404(Note, id=pk)
        note.delete()

    return HttpResponseRedirect(reverse('list_notes'))


def export_notes(request):
    """
    Exports the list of notes to an Excel document
    """
    dataset = NoteResource().export()
    filename = 'notes.xls'

    # set the response as a downloadable excel file
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    # set the file name
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    return response


# ======================================================== #
# Calendar - View
# ======================================================== #

def named_day(day_number):
    """
    Returns the name of the day in german
    """
    locale.setlocale(locale.LC_ALL, 'deu_deu')
    return datetime(1900, 1, day_number).strftime("%A")


def named_month(month_number):
    """
    Returns the name of the month
    """
    # set name of month in german, only for Windows OS
    locale.setlocale(locale.LC_ALL, 'deu_deu')
    return datetime(1900, month_number, 1).strftime("%B")


def get_calendar(request, year=None, month=None):
    """
    Renders the calendar
    """
    if year is not None and month is not None:
        act_year = int(year)
        act_month = int(month)
    else:
        act_year = datetime.now().year
        act_month = datetime.now().month

    # all events of model Event
    all_events = Event.objects.all()

    # all days of month, output: eg. for month March (3, 31)
    all_month_day = monthcalendar(act_year, act_month)

    # Calculate values for the calender controls. (Januar = 1)
    previous_year = act_year
    previous_month = act_month - 1
    if previous_month == 0:
        previous_year = act_year - 1
        previous_month = 12
    next_year = act_year
    next_month = act_month + 1
    if next_month == 13:
        next_year = act_year + 1
        next_month = 1
    year_after_this = act_year + 1
    year_befor_this = act_year - 1

    return render(request, 'calendar.html',
                  {'page_title': 'Terminkalender',
                   'calendar': all_month_day,
                   'month': act_month,
                   'month_name': named_month(act_month),
                   'year': act_year,
                   'previous_month': previous_month,
                   'previous_month_name': named_month(previous_month),
                   'previous_year': previous_year,
                   'next_month': next_month,
                   'next_month_name': named_month(next_month),
                   'next_year': next_year,
                   'year_before_this': year_befor_this,
                   'year_after_this': year_after_this,
                   'all_events': all_events
                   })


def detail_event(request, pk=None, year=None, month=None, day=None):
    """
    Creates/edits an event
    """
    act_year = int(year)
    act_month = int(month)
    act_day = int(day)

    act_date = datetime(act_year, act_month, act_day).__format__('%d.%m.%Y')
    if pk is None:
        events = Event()
        page_title = "Neuen Termin anlegen"
    else:
        events = get_object_or_404(Event, id=pk)
        page_title = "Termin ändern"

    if request.method == 'POST':
        # form sent off
        form = EventForm(request.POST, instance=events)

        # validity check
        if form.is_valid():
            event = form.save()
            messages.success(request, u'Daten erfolgreich geändert')
            return HttpResponseRedirect(reverse('edit_event', args=[act_year, act_month, act_day, event.id]))
        else:
            # error message
            messages.error(request, u'Daten konnten nicht gespeichert werden!')
            pass
    else:
        # form first call
        form = EventForm(instance=events, initial={'date': act_date})

    return render(request, 'detail.html', {'page_title': page_title, 'forms': [form]})


# delete an event in calendar View
def delete_event(request, pk=None):
    """
    Deletes an event
    """
    if pk is None:
        messages.error(request, u'Daten konnten nicht gelöscht werden!')
    else:
        del_event = get_object_or_404(Event, id=pk)
        del_event.delete()

    return HttpResponseRedirect(reverse('calendar'))


def detail_event_members(request, pk=None, year=None, month=None, day=None):
    """
    Assign event members to a member
    """
    if pk is None:
        # error back to calendar
        return HttpResponseRedirect(reverse('calendar'))
    act_year = int(year)
    act_month = int(month)
    act_day = int(day)

    act_date = datetime(act_year, act_month, act_day).__format__('%d.%m.%Y')

    event = get_object_or_404(Event, id=pk)

    if request.method == 'POST':
        if request.POST.get('submit') == 'addEvent':
            # form sent off
            form = EventForm(request.POST, instance=event)

            # validity check
            if form.is_valid():
                form.save()
                messages.success(request, u'Daten erfolgreich geändert!')
            else:
                # error message
                messages.error(request, u'Daten konnten nicht gespeichert werden!')
                pass
        elif request.POST.get('submit') == 'addInt':
            selemployee = request.POST.get('selemployee')
            if pk is None:
                # error message
                messages.error(request, u'Event muss gespeichert werden!')
                pass
            elif selemployee == '':
                # error message
                messages.error(request, u'Mitarbeiter muss ausgewählt werden!')
                pass
            else:
                if request.POST.get('leader') == 'on':
                    leader = True
                    # the leader automatically has the event status: accepted
                    status = 1
                else:
                    leader = False
                    # the leader automatically has the event status: invited
                    status = 0

                if not MemberInt.objects.filter(event_id=pk, leader=True).exists():
                    # add employee only once to the event
                    try:
                        MemberInt.objects.get(employee_id=int(selemployee), event_id=pk)
                    except MemberInt.DoesNotExist:
                        member_int = MemberInt(employee_id=int(selemployee), event_id=pk, leader=leader, status=status)
                        member_int.save()
                else:
                    messages.error(request, u'Es kann nur ein Mitarbeiter Leiter sein!')
                    pass
        elif request.POST.get('submit') == 'addExt':
            selcontact = request.POST.get('selcontact')
            if pk is None:
                # error message
                messages.error(request, u'Event muss gespeichert werden!')
                pass
            elif selcontact == '':
                # error message
                messages.error(request, u'Ansprechpartner muss ausgewählt werden!')
                pass
            else:
                MemberExt.objects.get_or_create(contact_id=int(selcontact), event_id=pk)

    page_title = "Termin ändern"
    form = EventForm(instance=event, initial={'date': act_date})
    member_ints = MemberInt.objects.all().filter(event_id=pk)
    member_exts = MemberExt.objects.all().filter(event_id=pk)
    form_int = EventAddMembersInt()
    form_ext = EventAddMembersExt()
    # Contact list for use in javascript for the dynamic list
    mylist = Contact.objects.all()
    return render(request, 'detail_event.html', {'page_title': page_title, 'forms': form,
                                                 'memberints': member_ints,
                                                 'memberexts': member_exts,
                                                 'formsL': form_int, 'formsR': form_ext, 'mylist': mylist})


def delete_event_member_internal(request, pk=None):
    """
    Remove internal members (employees) from an event
    """
    if pk is None:
        return HttpResponseRedirect(reverse('calendar'))

    member_int = get_object_or_404(MemberInt, id=pk)
    event_id = member_int.event_id
    member_int.delete()

    # use for select act_date
    event = Event.objects.get(id=event_id)
    act_year = event.date.year
    act_month = event.date.month
    act_day = event.date.day
    return HttpResponseRedirect(reverse('edit_event', args=[act_year, act_month, act_day, event_id]))


def delete_event_member_external(request, pk=None):
    """
    Remove external members (contacts of customers) from an event
    """
    if pk is None:
        return HttpResponseRedirect(reverse('calendar'))

    member_ext = get_object_or_404(MemberExt, id=pk)
    event_id = member_ext.event_id
    member_ext.delete()

    # use for select act_date
    event = Event.objects.get(id=event_id)
    act_year = event.date.year
    act_month = event.date.month
    act_day = event.date.day
    return HttpResponseRedirect(reverse('edit_event', args=[act_year, act_month, act_day, event_id]))


def edit_event_member_internal(request, pk=None, status=0):
    """
    edit the status  to o-invited, 1-participate and 2-canceled
    """
    if pk is None:
        messages.error(request, u'Es wurde kein Teilnehmer ausgewählt!')
        pass

    member_int = get_object_or_404(MemberInt, id=pk)
    member_int.status = status
    event_id = member_int.event_id
    member_int.save()
    messages.success(request, u'Teilnahmestatus eingetragen!')

    # use for select act_date
    event = Event.objects.get(id=event_id)
    act_year = event.date.year
    act_month = event.date.month
    act_day = event.date.day
    return HttpResponseRedirect(reverse('edit_event', args=[act_year, act_month, act_day, event_id]))


def edit_event_member_external(request, pk=None, status=0):
    """
    edit the status  to o-invited, 1-participate and 2-canceled
    """
    if pk is None:
        messages.error(request, u'Es wurde kein Teilnehmer ausgewählt!')
        pass

    member_ext = get_object_or_404(MemberExt, id=pk)
    member_ext.status = status
    event_id = member_ext.event_id
    member_ext.save()
    messages.success(request, u'Teilnahmestatus eingetragen!')

    # use for select act_date
    event = Event.objects.get(id=event_id)
    act_year = event.date.year
    act_month = event.date.month
    act_day = event.date.day
    return HttpResponseRedirect(reverse('edit_event', args=[act_year, act_month, act_day, event_id]))
