#TODO: File Decsription
"""
File Decsription
"""

from django.db import models
from datetime import datetime

# Create your models here.

# id = models.AutoField(primary_key=True)

class Staffs(models.Model):
    nickname = models.CharField('nickname', max_length=75)
    pwd = models.CharField('pwd', max_length=100)
    firstname = models.CharField('firstname', max_length=100)
    lastname = models.CharField('lastname', max_length=100)
    GENDER=(
        ('N', 'No Select'),
        ('F', 'Female'),
        ('M', 'Male'),
    )
    gender = models.CharField('salutation', default='N', max_length=1, choices=GENDER)
    title = models.CharField('title', null=True, max_length=100)
    position = models.CharField('position', max_length=100)
    phone = models.CharField('phone', null=True, max_length=25)
    fax = models.CharField('fax', null=True, max_length=100)
    mobile = models.CharField('mobile', null=True, max_length=100)
    email = models.CharField('email', null=True, max_length=100)

    def __str__(self):
        return "{} {} {} {}".format(self.firstname, self.lastname, self.title, self.position)

class Customers(models.Model):
    company = models.CharField('company', max_length=100)
    street = models.CharField('street', null=True, max_length=100)
    plzcity = models.CharField('plzcity', null=True, max_length=100)
    phone = models.CharField('phone', null=True, max_length=100)
    fax = models.CharField('fax', null=True, max_length=100)
    website = models.CharField('website', null=True, max_length=100)

class Contacts(models.Model):
    customer = models.ForeignKey(Customers)
    firstname = models.CharField('firstname', max_length=100)
    lastname = models.CharField('lastname', max_length=100)
    GENDER=(
        ('N', 'No Select'),
        ('F', 'Female'),
        ('M', 'Male'),
    )
    gender = models.CharField('gender', default='N', max_length=1, choices=GENDER)
    title = models.CharField('title', null=True, max_length=100)
    position = models.CharField('position', max_length=100)
    phone = models.CharField('phone', null=True, max_length=25)
    fax = models.CharField('fax', null=True, max_length=100)
    mobile = models.CharField('mobile', null=True,  max_length=100)
    email = models.CharField('email', null=True, max_length=100)

class Events(models.Model):
    staff = models.ManyToManyField(Staffs, through='MemberInt')       # many to many Field
    contact = models.ManyToManyField(Contacts, through='MemberExt')   # many to many Field
    date = models.DateTimeField('date', default=datetime.now())
    title = models.CharField('title', max_length=100)
    location = models.CharField('location', max_length=100)

class MemberExt(models.Model):
    contact = models.ForeignKey(Contacts)
    event = models.ForeignKey(Events)
    status = models.IntegerField('status', default=0)

class MemberInt(models.Model):
    staff = models.ForeignKey(Staffs)
    event = models.ForeignKey(Events)
    leader = models.BooleanField('leader', default=False)
    status = models.IntegerField('status', default=0)

class Notes(models.Model):
    contact = models.ForeignKey(Contacts)
    staff = models.ForeignKey(Staffs)
    calltype = models.IntegerField('calltype', default=0)
    notetext = models.CharField('notetext', max_length=200)