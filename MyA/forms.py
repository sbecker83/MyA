#TODO File Description
"""
 File Decsription:
"""

from django.forms import *
from MyA.models import *

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

# form with fields to shwow staff profile
class StaffProfileForm(ModelForm):
    class Meta:
        model = Staffs
        fields = ('gender', 'firstname', 'lastname', 'nickname', 'pwd', 'phone', 'fax', 'mobile', 'email', 'title', 'position')
        labels = {
            'gender':'Anrede',
            'firstname':'Vorname',
            'lastname':'Nachname',
            'nickname':'Nickname',
            'pwd':'Passwort',
            'phone':'Telefon',
            'fax': 'Fax',
            'mobile': 'Mobil',
            'email': 'Mail',
            'title': 'Titel',
            'position': 'Position'
        }