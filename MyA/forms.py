"""
Filename: forms.py
Description: Handles all forms
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
        # overwrites the shown fields of the super class
        fields = {'username', 'password'}

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)


class EmployeeForm(ModelForm):
    """
    A form for creating or updating employees and update profile of current user
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


class CustomerForm(ModelForm):
    """
    A form for creating or updating customers
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


class ContactForm(ModelForm):
    """
    A form for creating or updating contacts
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


class NoteForm(ModelForm):
    """
    A form for creating or updating notes
    With two fields for selecting customer/company and the respective contact
    """
    required_css_class = 'required'
    selemployee= ModelChoiceField(label='Mitarbeiter', queryset=Employee.objects.filter(user__is_active=True), required=False,disabled=True)
    selcustomer = ModelChoiceField(queryset=Customer.objects.filter(is_active=True), label='Firma',
                                   widget=Select(attrs={"onChange": 'mySelect()'}),required=False)
    selcontact = ModelChoiceField(queryset=Contact.objects.filter(is_active=True), label='Ansprechpartner')

    class Meta:
        model = Note
        fields = ('selcustomer', 'selcontact','selemployee', 'date', 'notetext')
        labels = {
            'date': 'Datum / Uhrzeit',
            'notetext': 'Text der Notiz'
        }
        # set a datetimepicker class which can be used to initialize a datetimepicker via javascript
        widgets = {'date': DateTimeInput(attrs={'class': 'datetimepicker'}),
                   'notetext': Textarea()}

    def __init__(self,  *args, **kwargs):
        # Initialize the two unbound fields and assign the values ​​when editing notes
        # Transfer by parameter in the views.py
        myemployee = kwargs.pop ('myemployee', None)
        mycustomer = kwargs.pop('mycustomer', None)
        mycontact = kwargs.pop('mycontact', None)
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['selemployee'].initial = myemployee
        if mycustomer is not None:
            self.fields['selcustomer'].initial = mycustomer
            # filter the contactlist
            self.fields['selcontact'].queryset = Contact.objects.filter(customer=mycustomer)
            self.fields['selcontact'].initial = mycontact


class FilterNoteForm(Form):
    """
    A form for filtering notes
    """
    required_css_class = 'required'
    selemployee = ModelChoiceField(label='Mitarbeiter', queryset=Employee.objects.all(), required=False)
    selcustomer = ModelChoiceField(queryset=Customer.objects.all(), label='Firma',
                                   widget=Select(attrs={"onChange": 'mySelect()'}), required=False)
    selcontact = ModelChoiceField(queryset=Contact.objects.all(), label='Ansprechpartner', required=False)


class EventForm(ModelForm):
    """
    A form for creating or updating events
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
        # set a timepicker class which can be used to initialize a datetimepicker via javascript
        widgets = {'starttime': TimeInput(attrs={'class': 'timepicker'}),
                   'endtime': TimeInput(attrs={'class': 'timepicker'})}

    def clean(self):
        """
        A custom validation method to forbid a endtime which is earlier than the starttime.
        The error will be rendered on the endtime field
        """
        cleaned_data = super().clean()
        starttime = cleaned_data.get("starttime")
        endtime = cleaned_data.get("endtime")
        if endtime < starttime:
            msg = u"Endzeit muss später sein als die Startzeit"
            self._errors["endtime"] = self.error_class([msg])


class EventAddMembersInt(Form):
    """
    A form for adding an employee to an event
    """
    required_css_class = 'required'
    selemployee = ModelChoiceField(label='Mitarbeiter', queryset=Employee.objects.filter(user__is_active=True), required=False)
    leader = BooleanField(label='Leiter', required=False)


class EventAddMembersExt(Form):
    """
    A form for adding an customer contact to an event
    """
    required_css_class = 'required'
    selcustomer = ModelChoiceField(queryset=Customer.objects.filter(is_active=True), label='Firma',
                                   widget=Select(attrs={"onChange": 'mySelect()'}), required=False)
    selcontact = ModelChoiceField(queryset=Contact.objects.filter(is_active=True), label='Ansprechpartner', required=False)
