#TODO File Description
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
        super().__init__(*args, **kwargs)


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
        """
         fields = ('customer', 'gender', 'firstname', 'lastname', 'phone', 'fax', 'mobile', 'email', 'title', 'position')
        labels = {
            'customer': 'Firma',
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

        """
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
        exclude ={'customer'}
"""  widgets = {
            'customer' :  TextInput(attrs={'disabled':'disabled'})
        }
"""



# Form for a note - dynamically Form from model
class NoteForm(ModelForm):
    """
    A form for create or update notes
    """
    class Meta:
        model = Note
        fields = ('date', 'notetext')
        labels = {
            'date': 'Datum / Uhrzeit',
            'notetext': 'Text der Notiz'
        }


# Form with fields to create or update employees
class EventForm(ModelForm):
    """
    A form for create or update employees and update profil of current user
    """
    class Meta:
        model = Event
        fields = ('date', 'title', 'location')
        labels = {
            'date': 'Datum',
            'title': 'Beschreibung',
            'location': 'Ort'
        }
