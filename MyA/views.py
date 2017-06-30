"""
Filename: views.py
Description: All view definition and their logic
"""
from calendar import *
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from MyA.forms import *
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from MyA.admin import EmployeeResource, CustomerResource, ContactResource, NoteResource
from datetime import datetime


def dashboard(request):
    """
    Renders a dashboard page with a list of notes and events of the current user
    """
    # get the employee model of the current user
    employee = Employee.objects.get(user=request.user.id)

    # get the notes of the current user
    try:
        my_notes = Note.objects.filter(employee=employee)
    except ObjectDoesNotExist:
        my_notes = []

    # get the future events of the current user
    try:
        my_events = Event.objects.filter(memberint__employee_id=employee.id).exclude(date__lt=datetime.today())
    except ObjectDoesNotExist:
        my_events = []

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
        if not (request.user.is_superuser or user == request.user):
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
            # we need to set the relationsship between the user and the employee manually
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

            if is_profile:
                messages.success(request, u'Profil gespeichert')
                return HttpResponseRedirect(reverse('profile'))
            else:
                messages.success(request, u'Mitarbeiter gespeichert')
                return HttpResponseRedirect(reverse('list_employees'))
        else:
            messages.error(request, u'Daten konnten nicht gespeichert werden')
            pass
    else:
        employee_form = EmployeeForm(instance=employee)
        # the form for a new user and an existing user differs (password field)
        if is_edit:
            user_form = UserEditForm(instance=user)
        else:
            user_form = UserCreationForm(instance=user)

    return render(request, 'detail.html', {'page_title': page_title, 'forms': [user_form, employee_form]})


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
    employee = Employee.objects.get(user=request.user.id)

    # use the detail_employee view with the is_profile flag set
    return detail_employee(request, pk=employee.id, is_profile=True)


# ======================================================== #
# Superuser - View
# ======================================================== #

# only the superuser is allowed for this view
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
            messages.success(request, 'Das Passwort wurde geändert')
        else:
            messages.error(request, 'Fehler')
    else:
        form = SetPasswordForm(user)
    return render(request, 'detail.html', {'page_title': page_title, 'forms': [form]})


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
            messages.success(request, 'Das Passwort wurde geändert')
        else:
            messages.error(request, 'Fehler')
    else:
        form = PasswordChangeForm(user=user)
    return render(request, 'detail.html', {'page_title': page_title, 'forms': [form]})


@user_passes_test(lambda u: u.is_superuser)
def toggle_employee_active(request, pk=None):
    """
    Deactivates/activates a user  depending on the current status
    ADMIN ONLY: This view can only be used by the superuser
    """
    if pk is None:
        messages.error(request, u'Mitarbeiter konnten nicht aktiviert/deaktiviert werden')
    else:
        employee = get_object_or_404(Employee, id=pk)
        user = employee.user
        if user.is_active:
            user.is_active = False
            user.save()
            messages.success(request, u'Mitarbeiter erfolgreich deaktiviert')
        else:
            user.is_active = True
            user.save()
            messages.success(request, u'Mitarbeiter erfolgreich aktiviert')
    return HttpResponseRedirect(reverse('list_employees'))


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
        # Validity check
        if form.is_valid():
            form.save()
            messages.success(request, u'Daten erfolgreich geändert')
            return HttpResponseRedirect(reverse('list_customers'))
        else:
            # error message
            messages.error(request, u'Daten konnten nicht gespeichert werden')
            pass
    else:
        # form first call
        form = CustomerForm(instance=customer)
    return render(request, 'detail.html', {'page_title': page_title, 'forms': [form]})


def delete_customer(request, pk=None, status=None):
    """
    Deletes a customer.
    """
    if pk is None:
        messages.error(request, u'Daten konnten nicht gelöscht werden')
    else:
        if status == '2':

            customer = get_object_or_404(Customer, id=pk)
            # check if customer has no contacts
            nocontact = 0
            for c in Contact.objects.raw('SELECT * FROM mya_contact where customer_id='+pk):
                nocontact = 1
            if nocontact == 0:
                customer.delete()
                messages.success(request, u'Daten erfolgreich gelöscht')
            else:
                if customer.status == 0:
                    # Customer has contact so he can only be disabled
                    customer.status = 1
                    Contact.objects.select_related().filter(customer=customer.id).update(status=1)
                    customer.save()
                    messages.success(request, u'Daten erfolgreich de-/aktiviert')
                else:
                    messages.error(request, u'Daten konnten nicht gelöscht werden')
        else:
            customer = get_object_or_404(Customer, id=pk)

            if customer.status == 0:
                customer.status = 1
                Contact.objects.select_related().filter(customer=customer.id).update(status=1)
            elif customer.status == 1:
                customer.status = 0
                Contact.objects.select_related().filter(customer=customer.id).update(status=0)
            customer.save()
            messages.success(request, u'Daten erfolgreich de-/aktiviert')
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
    contacts = Contact.objects.all().filter(customer_id=fk)
    # show the company in the title - select from customer
    customers = Customer.objects.filter(id=fk)
    for c in customers:
        customername = " - " + c.company
    page_title = "Ansprechpartner" + customername

    # paraameter selcted customer for the list_contact.html using by call view new contact
    return render(request, 'list_contact.html', {'page_title': page_title, 'contacts': contacts,
                                                 'selected_customer_id': fk})


# create a new contact or edit a contact
# parameters for create and edit selected customer (foreign key)
#            for edit primary key of the contact
def details_contact(request, pk=None, fk=None):
    # show the company in the title - select from customer
    customers = Customer.objects.filter(id=fk)
    for c in customers:
        customername = " - " + c.company
    # set page-title for a nwe contact or for edit contact
    if pk is None:
        # new contact
        contact = Contact()
        page_title = "Ansprechpartner anlegen" + customername
    else:
        # edit contact
        contact = get_object_or_404(Contact, id=pk)
        page_title = "Ansprechpartner ändern" + customername

    if request.method == 'POST':

        # form sent off
        # parameter of the form selcted customer (fk) per initial
        form = ContactForm(request.POST, instance=contact, initial={'customer': fk})

        # Validity check
        if form.is_valid():
            form = form.save(commit=False)
            # set customer-id
            form.customer_id = fk
            form.save()
            messages.success(request, u'Daten erfolgreich geändert')
            # parameter to filter to the selected customer (fk) per args
            return HttpResponseRedirect(reverse('list_contacts', args=[fk]))

        else:
            # error message
            messages.error(request, u'Daten konnten nicht gespeichert werden')
            pass
    else:
        # form first call
        # parameter of the form selcted customer (fk) per initial
        form = ContactForm(instance=contact,  initial={'customer': fk})
    return render(request, 'detail.html', {'page_title': page_title, 'forms': [form]})


def delete_contact(request, pk=None, fk=None, status=None):
    """
    Deletes a contact for a customer (fk)
    """
    if pk is None:
        messages.error(request, u'Daten konnten nicht gelöscht werden')
    else:
        if status == '2':
            contact = get_object_or_404(Contact, id=pk)
            # check if contact has no notes and no events / memberext
            no_notes_and_events = 0
            for n in Note.objects.raw('SELECT * FROM mya_note where contact_id=' + pk):
                no_notes_and_events = 1
            for e in MemberExt.objects.raw('SELECT * FROM mya_memberext where contact_id=' + pk):
                no_notes_and_events = 1
            if no_notes_and_events == 0:
                contact.delete()
                messages.success(request, u'Daten erfolgreich gelöscht')
            else:
                # check if customer active
                customer = Customer.objects.filter(id=contact.customer_id).first()
                if customer.status == 0 and contact.status == 0:
                    # contact has relaticns to a child-table so it can only be disabled
                    contact.status = 1
                    contact.save()
                    messages.success(request, u'Daten erfolgreich de-/aktiviert')
                else:
                    messages.error(request, u'Daten konnten nicht gelöscht werden')
        else:
            contact = get_object_or_404(Contact, id=pk)
            # check if customer active
            customer = Customer.objects.filter(id=contact.customer_id).first()
            if customer.status == 0:
                if contact.status == 0:
                    contact.status = 1
                elif contact.status == 1:
                    contact.status = 0
                contact.save()
                messages.success(request, u'Daten erfolgreich de-/aktiviert')
            else:
                messages.error(request,
                               u'Anspechpartner konnten nicht de-/aktiviert werden, da der Kunde deaktiviert ist! ')
    # paramter to filter to the selected customer (fk) per args
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

        if selemployee == '' and selcustomer == '' and selcontact == '':
            # no filter
            notes = Note.objects.all()
        elif selcustomer != '' and selcontact == '':
            # filter by customer - no contact
            if selemployee == '':
                notes = Note.objects.raw(
                'SELECT * FROM mya_note WHERE contact_id IN (SELECT id FROM mya_contact WHERE customer_id=' + selcustomer + ')')

            elif selemployee != '':
                # filter employee and customer
                notes = Note.objects.raw('SELECT * FROM mya_note WHERE employee_id = ' + selemployee +
                                         ' AND contact_id IN (SELECT id FROM mya_contact WHERE customer_id=' + selcustomer + ')')
                # show employee in filtertext
                for e in Employee.objects.filter(id=int(selemployee)):
                    if filtertext == '':
                        filtertext = 'Filter nach: ' + e.firstname + ' ' + e.lastname
                    else:
                        filtertext += ', ' + e.firstname + ' ' + e.lastname
            # show customer in filtertext
            for c in Customer.objects.filter(id=int(selcustomer)):
                if filtertext == '':
                    filtertext = 'Filter nach: ' + c.company
                else:
                    filtertext += ', ' + c.company
        else:

            if selemployee != '' and selcontact != '':
                # filter employee and contact
                notes = Note.objects.filter(employee_id=int(selemployee), contact_id=int(selcontact))
                # show employee in filtertext
                for e in Employee.objects.filter(id=int(selemployee)):
                    if filtertext == '':
                        filtertext = 'Filter nach: ' + e.firstname + ' ' + e.lastname
                    else:
                        filtertext += ', ' + e.firstname + ' ' + e.lastname
                # show contact in filtertext
                for co in Contact.objects.filter(id=int(selcontact)):
                    if filtertext == '':
                        filtertext = 'Filter nach: ' + co.firstname + ' ' + co.lastname
                    else:
                        filtertext += ', ' + + co.firstname + ' ' + co.lastname
            elif selemployee != '' and selcontact == '':
                # filter employee
                notes = Note.objects.filter(employee_id=int(selemployee))
                # show employee in filtertext
                for e in Employee.objects.filter(id=int(selemployee)):
                    if filtertext == '':
                        filtertext = 'Filter nach: ' + e.firstname + ' ' + e.lastname
                    else:
                        filtertext += ', ' + e.firstname + ' ' + e.lastname
            elif selemployee == '' and selcontact != '':
                # filter contact
                notes = Note.objects.filter(contact_id=int(selcontact))
                # show contact in filtertext
                for co in Contact.objects.filter(id=int(selcontact)):
                    if filtertext == '':
                        filtertext = 'Filter nach: ' + co.firstname + ' ' + co.lastname
                    else:
                        filtertext += ', ' + + co.firstname + ' ' + co.lastname
    else:
        # first call
        notes = Note.objects.all()

    form = FilterNoteForm()
    # Contact list for use in javascript for the dynamic list
    mylist = Contact.objects.all()
    return render(request, 'list_note.html', {'page_title': 'Notizen', 'notes': notes, 'forms': [form], 'mylist': mylist, 'page_filtertext':filtertext})


def detail_note(request, pk=None):
    """
    Creates/edits a note.
    """
    if pk is None:
        note = Note()
        page_title = "Notiz anlegen"
    else:
        note = get_object_or_404(Note, id=pk)
        page_title = "Notiz ändern"

    if request.method == 'POST':

        # form sent off
        form = NoteForm(request.POST, instance=note)
        # Validity check
        if form.is_valid():
            form = form.save(commit=False)
            # set contact from the Select-Contact-Field - value form the request
            form.contact_id = request.POST.get('selcontact')
            form.save()
            messages.success(request, u'Daten erfolgreich geändert')
            return HttpResponseRedirect(reverse('list_notes'))
        else:
            # error message
            messages.error(request, u'Daten konnten nicht gespeichert werden')
            pass

    else:

        if pk is None:
            # form first call - to insert a new note
            form = NoteForm(instance=note)
        else:
            # form first call with a pk - to edit a note
            # transfer the customer_id and the contact_id for the unbound selection fields
            form = NoteForm(instance=note,  mycustomer=note.contact.customer_id, mycontact=note.contact_id)

    # Contact list for use in javascript for the dynamic list
    mylist = Contact.objects.all()
    return render(request, 'detail_note.html', {'page_title': page_title, 'forms': [form], 'mylist': mylist})


def delete_note(request, pk=None):
    """
    Deletes a note.
    """
    if pk is None:
        messages.error(request, u'Daten konnten nicht gelöscht werden')
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
    Returns the name of the day
    """
    return datetime(1900, 1, day_number).strftime("%A")


def named_month(month_number):
    """
    Returns the name of the month
    """
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
                   # 'event_today': event_today
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

        # Validity check
        if form.is_valid():
            form.save()
            messages.success(request, u'Daten erfolgreich geändert')
            return HttpResponseRedirect(reverse('calendar'))
        else:
            # error message
            messages.error(request, u'Daten konnten nicht gespeichert werden')
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
        messages.error(request, u'Daten konnten nicht gelöscht werden')
    else:
        delevent = get_object_or_404(Event, id=pk)
        delevent.delete()

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

    events = get_object_or_404(Event, id=pk)

    if request.method == 'POST':
        if request.POST.get('submit') == 'addEvent':
            # form sent off
            form = EventForm(request.POST, instance=events)

            # Validity check
            if form.is_valid():
                form.save()
                messages.success(request, u'Daten erfolgreich geändert')
                # return HttpResponseRedirect(reverse('calendar'))

            else:
                # error message
                messages.error(request, u'Daten konnten nicht gespeichert werden')
                pass
        elif request.POST.get('submit') == 'addInt':
            selemployee = request.POST.get('selemployee')
            if pk is None:
                # error message
                messages.error(request, u'Event muss gespeichert werden')
                pass
            elif selemployee == '':
                # error message
                messages.error(request, u'Mitarbeiter muss ausgewählt werden')
                pass
            else:
                if request.POST.get('leader') == 'on':
                    leader = True
                else:
                    leader = False
                memberint = MemberInt(employee_id=int(selemployee), leader=leader, event_id=pk)
                memberint.save()
        elif request.POST.get('submit') == 'addExt':
            selcontact = request.POST.get('selcontact')
            if pk is None:
                # error message
                messages.error(request, u'Event muss gespeichert werden')
                pass
            elif selcontact == '':
                # error message
                messages.error(request, u'Ansprechpartner muss ausgewählt werden')
                pass
            else:
                memberext = MemberExt(contact_id=int(selcontact), event_id=pk)
                memberext.save()

    page_title = "Termin ändern"
    form = EventForm(instance=events, initial={'date': act_date})
    memberints = MemberInt.objects.all().filter(event_id=pk)
    memberexts = MemberExt.objects.all().filter(event_id=pk)
    form_int = EventAddMembersInt()
    form_ext = EventAddMembersExt()
    return render(request, 'detail_event.html', {'page_title': page_title, 'forms': form,
                                                 'memberints': memberints,
                                                 'memberexts': memberexts,
                                                 'formsL': form_int, 'formsR': form_ext})


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
    event = Event.objects.all().filter(id=event_id)
    act_date = event[0].date.strftime('%d.%m.%Y')
    # use for from
    events = get_object_or_404(Event, id=event_id)

    page_title = "Termin ändern"
    form = EventForm(instance=events, initial={'date': act_date})
    memberints = MemberInt.objects.all().filter(event_id=pk)
    memberexts = MemberExt.objects.all().filter(event_id=pk)
    form_int = EventAddMembersInt()
    form_ext = EventAddMembersExt()
    return render(request, 'detail_event.html', {'page_title': page_title, 'forms': form,
                                                 'memberints': memberints,
                                                 'memberexts': memberexts,
                                                 'formsL': form_int, 'formsR': form_ext})


def delete_event_member_external(request, pk=None):
    """
    Remove external members (contacts of cusomters) from an event
    """
    if pk is None:
        return HttpResponseRedirect(reverse('calendar'))

    member_ext = get_object_or_404(MemberExt, id=pk)
    event_id = member_ext.event_id
    member_ext.delete()
    # use for select act_date
    event = Event.objects.all().filter(id=event_id)
    act_date = event[0].date.strftime('%d.%m.%Y')
    # use for from
    events = get_object_or_404(Event, id=event_id)

    page_title = "Termin ändern"
    form = EventForm(instance=events, initial={'date': act_date})
    memberints = MemberInt.objects.all().filter(event_id=pk)
    memberexts = MemberExt.objects.all().filter(event_id=pk)
    form_int = EventAddMembersInt()
    form_ext = EventAddMembersExt()
    return render(request, 'detail_event.html', {'page_title': page_title, 'forms': form,
                                                 'memberints': memberints,
                                                 'memberexts': memberexts,
                                                 'formsL': form_int, 'formsR': form_ext})
