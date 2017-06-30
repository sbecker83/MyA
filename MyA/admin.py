"""
Filename: admin.py
Description: Handles definitions for the admin site
"""

from django.contrib import admin
from MyA.models import Employee, Customer, Contact, Event, MemberExt, MemberInt, Note
from import_export import resources


# register models
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Contact)
admin.site.register(Event)
admin.site.register(MemberExt)
admin.site.register(MemberInt)
admin.site.register(Note)


# define resource for import/export (see: http://django-import-export.readthedocs.io/en/stable/getting_started.html)
class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee


class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer


class ContactResource(resources.ModelResource):
    class Meta:
        model = Contact
        # the fields are added manually because related fields should be shown
        fields = ('id', 'firstname', 'lastname', 'gender', 'title', 'position', 'phone', 'fax', 'mobile', 'email',
                  'customer__id', 'customer__company',)


class NoteResource(resources.ModelResource):
    class Meta:
        model = Note
        # the fields are added manually because related fields should be shown
        fields = ('id', 'notetext', 'date', 'employee__id', 'employee__firstname', 'employee__lastname', 'contact__id',
                  'contact__firstname', 'contact__lastname')
