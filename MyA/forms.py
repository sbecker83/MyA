# TODO File Description
"""
 File Decsription:
"""
from django.forms import *
from django.contrib.auth.forms import UserChangeForm
from MyA.models import *


class UserEditForm(UserChangeForm):
    """
    A user edit form. This form inherits from UserChangeForm and only changes the fields which are used/shown
    """
    class Meta:
        model = User
        # overwrites the fields of the super class
        fields = {'username', 'password'}

    def __init__(self, *args, **kwargs):
        # TODO Syntax geändert: UserEditForm und self eingefügt => für Matthias
        super(UserEditForm, self).__init__(*args, **kwargs)


# Form with fields to create or update employees
class EmployeeForm(ModelForm):
    """
    A form for create or update employees and update profil of current user
    """
    class Meta:
        model = Employee
        fields = ('gender', 'firstname', 'lastname', 'phone', 'fax', 'mobile', 'email', 'title', 'position')
        labels = {
            'gender': 'Anrede',
            'firstname': 'Vorname',
            'lastname': 'Nachname',
            'phone': 'Telefon',
            'fax': 'Fax',
            'mobile': 'Mobil',
            'email': 'Mail',
            'title': 'Titel',
            'position': 'Position'
        }


# Form for a customer - dynamically Form from model
class CustomerForm(ModelForm):
    """
    A form for create or update customers
    """
    class Meta:
        model = Customer
        fields = ('company', 'street', 'plzcity', 'phone', 'fax', 'website')
        labels = {
            'company': 'Firma',
            'street': 'Strasse / Nr.',
            'plzcity': 'PLZ / Ort',
            'phone': 'Telefon',
            'fax': 'Fax',
            'website': 'Webseite'
        }


# Form for a contac - dynamically Form from model
class ContactForm(ModelForm):
    """
    A form for create or update contacts
    """

    class Meta:
        model = Contact

        fields = ('gender', 'firstname', 'lastname', 'phone', 'fax', 'mobile', 'email', 'title', 'position')
        labels = {
            'gender': 'Anrede',
            'firstname': 'Vorname',
            'lastname': 'Nachname',
            'phone': 'Telefon',
            'fax': 'Fax',
            'mobile': 'Mobil',
            'email': 'Mail',
            'title': 'Titel',
            'position': 'Position'
        }
        exclude = {'customer'}


# Form for a note - dynamically Form from model
class NoteForm(ModelForm):
    """
    A form for create or update notes
    With two fields for selecting customer/company and the respective contact
    """

    selcustomer = ModelChoiceField(queryset=Customer.objects.all(), label='Firma',
                                   widget=Select(attrs={"onChange": 'mySelect()'}))
    selcontact = ModelChoiceField(queryset=Contact.objects.all(), label='Ansprecchpartner')

    class Meta:
        model = Note
        fields = ('selcustomer', 'selcontact', 'employee', 'date', 'notetext')
        labels = {
            'employee': 'Mitarbeiter',
            'date': 'Datum / Uhrzeit',
            'notetext': 'Text der Notiz'
        }

    def __init__(self,  *args, **kwargs):
        # Initialize the two unbound fields and assign the values ​​when editing notes
        # Transfer by parameter in the views.py
        mycustomer = kwargs.pop('mycustomer', None)
        mycontact = kwargs.pop('mycontact', None)
        super(NoteForm, self).__init__(*args, **kwargs)
        if mycustomer != None:
            self.fields['selcustomer'].initial = mycustomer
            # filter the contactlist
            self.fields['selcontact'].queryset = Contact.objects.filter(customer=mycustomer)
            self.fields['selcontact'].initial = mycontact


# Form with fields to create or update employees
class EventForm(ModelForm):
    """
    A form for create or update employees and update profil of current user
    """
    my_starttime = CharField(label='Startzeit')
    my_endtime = CharField(label='Endzeit')

    class Meta:
        model = Event
        fields = ('date', 'title', 'my_starttime', 'my_endtime', 'location')
        labels = {
            'date': 'Datum',
            'title': 'Beschreibung',
            'location': 'Ort'
        }


    """
    def clean_starttime(self):
        str_date = str(self.date) + ' ' + str(self.starttime)
        starttime = datetime.strptime(str_date, '%d.%m.%Y HH:mm').date()
        return starttime

    def clean(self):
        super(ModelForm, self).clean()
        str_date = str(self.cleaned_data['date']) + ' ' + str(self.cleaned_data['starttime'])
        self.cleaned_data['starttime'] = datetime.strptime(str_date, '%d.%m.%Y HH:mm').date()
        return self.cleaned_data
    """