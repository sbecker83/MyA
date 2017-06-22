#TODO: File Decsription
"""
File Decsription
"""

# register models

from django.contrib import admin
from MyA.models import Employee, Customer, Contact, Event, MemberExt, MemberInt, Note
from import_export import resources

admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Contact)
admin.site.register(Event)
admin.site.register(MemberExt)
admin.site.register(MemberInt)
admin.site.register(Note)



class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee

class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer

class ContactResource(resources.ModelResource):
    class Meta:
        model = Contact
        # the fields are added manually because the company name of the customer relationship should be shown instead of the id
        fields = ('id', 'firstname', 'lastname', 'gender', 'title', 'position', 'phone', 'fax', 'mobile', 'email', 'customer__id', 'customer__company',)

class NoteResource(resources.ModelResource):
    class Meta:
        model = Note