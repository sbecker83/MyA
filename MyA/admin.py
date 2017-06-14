"""
prepopulated_fields:
Das Attribut prepopulated_fields hilft in der Admin-Applikation dabei, dass Feld slug bei der Eingabe automatisch zu füllen. In diesem Fall mit dem Attribut name des Models.
"""

# Models beim Admin regisitrieren

from django.contrib import admin
from MyA.models import Staffs, Customers, Contacts, Events, MemberExt, MemberInt, Notes


admin.site.register(Staffs)
admin.site.register(Customers)
admin.site.register(Contacts)
admin.site.register(Events)
admin.site.register(MemberExt)
admin.site.register(MemberInt)
admin.site.register(Notes)
