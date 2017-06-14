#TODO: File Decsription
"""
File Decsription
"""

# register models

from django.contrib import admin
from MyA.models import Staffs, Customers, Contacts, Events, MemberExt, MemberInt, Notes


admin.site.register(Staffs)
admin.site.register(Customers)
admin.site.register(Contacts)
admin.site.register(Events)
admin.site.register(MemberExt)
admin.site.register(MemberInt)
admin.site.register(Notes)
