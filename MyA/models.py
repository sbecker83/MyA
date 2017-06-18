#TODO: File Decsription
"""
File Decsription
"""

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

# id = models.AutoField(primary_key=True)

class Employee(models.Model):
    # this connects the employee to the django auth user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #nickname = models.CharField('nickname', max_length=75)
    #pwd = models.CharField('pwd', max_length=100)
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


class Customer(models.Model):
    company = models.CharField('company', max_length=100)
    street = models.CharField('street', null=True, max_length=100)
    plzcity = models.CharField('plzcity', null=True, max_length=100)
    phone = models.CharField('phone', null=True, max_length=100)
    fax = models.CharField('fax', null=True, max_length=100)
    website = models.CharField('website', null=True, max_length=100)

    def __str__(self):
        return "{}".format(self.company)


class Contact(models.Model):
    customer = models.ForeignKey(Customer)
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
    
    def __str__(self):
        return "{} {} {} {}".format(self.company, self.firstname, self.lastname, self.position)


class Event(models.Model):
    employee = models.ManyToManyField(Employee, through='MemberInt')       # many to many Field
    contact = models.ManyToManyField(Contact, through='MemberExt')   # many to many Field
    date = models.DateTimeField('date', default=datetime.now())
    title = models.CharField('title', max_length=100)
    location = models.CharField('location', max_length=100)


class MemberExt(models.Model):
    contact = models.ForeignKey(Contact)
    event = models.ForeignKey(Event)
    status = models.IntegerField('status', default=0)


class MemberInt(models.Model):
    employee = models.ForeignKey(Employee)
    event = models.ForeignKey(Event)
    leader = models.BooleanField('leader', default=False)
    status = models.IntegerField('status', default=0)


class Note(models.Model):
    contact = models.ForeignKey(Contact)
    employee = models.ForeignKey(Employee)
    calltype = models.IntegerField('calltype', default=0)
    notetext = models.CharField('notetext', max_length=200)