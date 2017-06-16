#TODO File Description
"""
 File Decsription:
"""

from django.forms import *
from django.contrib.auth.forms import UserChangeForm
from MyA.models import *

class UserEditForm(UserChangeForm):
    """ A user edit form. This form inherits from UserChangeForm and only changes the fields which are used/shown
    """
    class Meta:
        model = User
        # overwrites the fields of the super class
        fields = {'username','password'}

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

# Form with fields to create or update staff
class StaffForm(ModelForm):
    class Meta:
        model = Staffs
        fields = ('gender', 'firstname', 'lastname', 'phone', 'fax', 'mobile', 'email', 'title', 'position')
        labels = {
            'gender':'Anrede',
            'firstname':'Vorname',
            'lastname':'Nachname',
            'phone':'Telefon',
            'fax': 'Fax',
            'mobile': 'Mobil',
            'email': 'Mail',
            'title': 'Titel',
            'position': 'Position'
        }

# form with fields to show or update staff profile
class StaffProfileForm(ModelForm):
    class Meta:
        model = Staffs
        fields = ('gender', 'firstname', 'lastname', 'phone', 'fax', 'mobile', 'email', 'title', 'position')
        labels = {
            'gender':'Anrede',
            'firstname':'Vorname',
            'lastname':'Nachname',
            'phone':'Telefon',
            'fax': 'Fax',
            'mobile': 'Mobil',
            'email': 'Mail',
            'title': 'Titel',
            'position': 'Position'
        }

# Form for a customer - dynamically Form from model
class CustomerForm(ModelForm):
    class Meta:
        model= Customers
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
    class Meta:
        model= Contacts
        fields = ('customer', 'gender', 'firstname', 'lastname', 'phone', 'fax', 'mobile', 'email', 'title', 'position')
        labels = {
            'customer': 'Firma',
            'gender':'Anrede',
            'firstname':'Vorname',
            'lastname':'Nachname',
            'phone':'Telefon',
            'fax': 'Fax',
            'mobile': 'Mobil',
            'email': 'Mail',
            'title': 'Titel',
            'position': 'Position'
        }
# Form for a note - dynamically Form from model
class NoteForm(ModelForm):
    class Meta:
        model= Notes
        fields = ('calltype', 'notetext' )
        labels = {
            'calltype': 'Type',
            'notetext':'Text der Notiz'
        }