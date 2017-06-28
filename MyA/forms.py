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
    required_css_class = 'required'

    class Meta:
        model = User
        # overwrites the fields of the super class
        fields = {'username', 'password'}

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)


# Form with fields to create or update employees
class EmployeeForm(ModelForm):
    """
    A form for create or update employees and update profil of current user
    """
    required_css_class = 'required'

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
    required_css_class = 'required'

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
    required_css_class = 'required'

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
    required_css_class = 'required'

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
        widgets = {'date': DateTimeInput(attrs={'id': 'datetimepicker'})}

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


class FilterNoteForm(Form):
    """
    A form for filter notes
    """
    required_css_class = 'required'

    selemployee = ModelChoiceField(label='Mitarbeiter', queryset=Employee.objects.all(), required=False)
    selcustomer = ModelChoiceField(queryset=Customer.objects.all(), label='Firma',
                                    widget=Select(attrs={"onChange": 'mySelect()'}), required=False)
    selcontact = ModelChoiceField(queryset=Contact.objects.all(), label='Ansprecchpartner', required=False)


# Form with fields to create or update employees
class EventForm(ModelForm):
    """
    A form for create or update events
    """
    required_css_class = 'required'

    class Meta:
        model = Event
        fields = ('date', 'title', 'starttime', 'endtime', 'location')
        labels = {
            'date': 'Datum',
            'starttime': 'Startzeit',
            'endtime': 'Endzeit',
            'title': 'Beschreibung',
            'location': 'Ort'
        }
        widgets = {'starttime': DateTimeInput(attrs={'id': 'datetimepicker-start'}),
                   'endtime': DateTimeInput(attrs={'id': 'datetimepicker-end'})}

