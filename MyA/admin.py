#TODO: File Decsription
"""
File Decsription
"""

# register models

from django.contrib import admin
from MyA.models import Employee, Customer, Contact, Event, MemberExt, MemberInt, Note


admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Contact)
admin.site.register(Event)
admin.site.register(MemberExt)
admin.site.register(MemberInt)
admin.site.register(Note)
