# TODO: File Decsription
"""
File Decsription
"""

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

# id = models.AutoField(primary_key=True)

class Employee(models.Model):
    # this connects the employee to the django auth user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField('firstname', max_length=100)
    lastname = models.CharField('lastname', max_length=100)
    GENDER = (
        ('N', 'Keine Auswahl'),
        ('F', 'Frau'),
        ('M', 'Herr'),
    )
    gender = models.CharField('salutation', default='N', max_length=1, choices=GENDER)
    title = models.CharField('title', blank=True, max_length=100)
    position = models.CharField('position', max_length=100)
    phone = models.CharField('phone', blank=True, max_length=25)
    fax = models.CharField('fax', blank=True, max_length=100)
    mobile = models.CharField('mobile', blank=True, max_length=100)
    email = models.CharField('email', blank=True, max_length=100)

    def __str__(self):
        return "{} {} {} {}".format(self.firstname, self.lastname, self.title, self.position)

    @receiver(post_save, sender=User)
    # TODO Nachgucken für Matthias: self wird als fehelnd angemeckert
    def create_employee_for_superuser(sender, instance, created, **kwargs):
        """This signal receiver guarentees a creation of an employee object when the superuser is created"""
        if created and instance.is_superuser:
            employee = Employee()
            employee.firstname = instance.username
            employee.email = instance.email
            employee.position = "Administrator"
            employee.user = instance
            employee.save()


class Customer(models.Model):
    # Check the input of the telephone number - numbers and as a separator / or -
    phoneRegex = RegexValidator(regex=r'^[0-9 -\/]+$', message="Telefonnummern mit / oder -")
    # Check the input of the 5 digit zip code and enter the city
    plzcityRegex = RegexValidator(regex=r'^\d{5} [a-zA-ZäöüÄÖÜ -ß]+$', message="5 stellige PLZ und Stadt")
    company = models.CharField('company', max_length=100)
    street = models.CharField('street', blank=True, max_length=100)
    plzcity = models.CharField('plzcity', validators=[plzcityRegex], blank=True, max_length=100)
    phone = models.CharField('phone', validators=[phoneRegex], blank=True, max_length=100)
    fax = models.CharField('fax', validators=[phoneRegex], blank=True, max_length=100)
    website = models.CharField('website', blank=True, max_length=100)

    def __str__(self):
        return "{}".format(self.company)


class Contact(models.Model):
    # Check the input of the telephone number - numbers and as a separator / or -
    phoneRegex = RegexValidator(regex=r'^[0-9 -\/]+$', message="Telefonnummern mit / oder -")
    customer = models.ForeignKey(Customer)
    firstname = models.CharField('firstname', max_length=100)
    lastname = models.CharField('lastname', max_length=100)
    GENDER = (
        ('N', 'Keine Auswahl'),
        ('F', 'Frau'),
        ('M', 'Herr'),
    )
    gender = models.CharField('gender', default='N', max_length=1, choices=GENDER)
    title = models.CharField('title', blank=True, max_length=100)
    position = models.CharField('position', max_length=100)
    phone = models.CharField('phone', validators=[phoneRegex], blank=True, max_length=25)
    fax = models.CharField('fax', validators=[phoneRegex], blank=True, max_length=100)
    mobile = models.CharField('mobile', blank=True, max_length=100)
    email = models.EmailField('email', blank=True, max_length=100)

    def __str__(self):
        return "{} {} {} {}".format(self.customer, self.firstname, self.lastname, self.position)


class Event(models.Model):
    employee = models.ManyToManyField(Employee, through='MemberInt')       # many to many Field
    contact = models.ManyToManyField(Contact, through='MemberExt')   # many to many Field
    date = models.DateTimeField('date', default=datetime.now().__format__('%d.%m.%Y'))
    # TODO Sandra: Format ändern
    starttime = models.DateTimeField('date', default='00:00')
    endtime = models.DateTimeField('date', default='00:00')
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
    notetext = models.CharField('notetext', max_length=300)
    date = models.DateTimeField('date', default=datetime.now())

    def __str__(self):
        return "{}".format(self.notetext)
