from django.db import models
from datetime import datetime

# Create your models here.


# id = models.AutoField(primary_key=True)

class Mitarbeiter(models.Model):
    url = models.URLField()
    nickname = models.CharField('nickname', max_length=75)
    pwd = models.CharField('pwd', max_length=100)
    vorname = models.CharField('vorname', max_length=100)
    nachname = models.CharField('nachname', max_length=100)
    ANREDE=(
        ('K', 'Keine Auswahl'),
        ('F', 'Frau'),
        ('H', 'Herr'),
    )
    anrede = models.CharField('anrede', default='K', max_length=1, choices=ANREDE)
    titel = models.CharField('titel', null=True, max_length=100)
    position = models.CharField('position', max_length=100)
    telefon = models.CharField('telefon', null=True, max_length=25)
    fax = models.CharField('fax', null=True, max_length=100)
    mobile = models.CharField('mobile', null=True, max_length=100)
    email = models.CharField('email', null=True, max_length=100)

class Kunden(models.Model):
    firma = models.CharField('firma', max_length=100)
    strasse = models.CharField('strasse', null=True, max_length=100)
    plzort = models.CharField('plzort', null=True, max_length=100)
    telefon = models.CharField('telefon', null=True, max_length=100)
    fax = models.CharField('fax', null=True, max_length=100)
    webseite = models.CharField('webseite', null=True, max_length=100)

class Ansprechpartner(models.Model):
    kunden = models.ForeignKey(Kunden)
    vorname = models.CharField('vorname', max_length=100)
    nachname = models.CharField('nachname', max_length=100)
    ANREDE=(
        ('K', 'Keine Auswahl'),
        ('F', 'Frau'),
        ('H', 'Herr'),
    )
    anrede = models.CharField('anrede', default='K', max_length=1, choices=ANREDE)
    titel = models.CharField('titel', null=True, max_length=100)
    position = models.CharField('position', max_length=100)
    telefon = models.CharField('telefon', null=True, max_length=25)
    fax = models.CharField('fax', null=True, max_length=100)
    mobile = models.CharField('mobile', null=True,  max_length=100)
    email = models.CharField('email', null=True, max_length=100)

class Termine(models.Model):
    mitarbeiter = models.ManyToManyField(Mitarbeiter, through='TeilnehmerInt')           #many to many Field
    ansprechpartner = models.ManyToManyField(Ansprechpartner, through='TeilnehmerExt')   # many to many Field
    datum = models.DateTimeField('datum', default=datetime.now())
    titel = models.CharField('titel', max_length=100)
    ort = models.CharField('ort', max_length=100)

class TeilnehmerExt(models.Model):
    ansprechpartner = models.ForeignKey(Ansprechpartner)
    termine = models.ForeignKey(Termine)
    status = models.IntegerField('status', default=0)

class TeilnehmerInt(models.Model):
    mitarbeiter = models.ForeignKey(Mitarbeiter)
    termine = models.ForeignKey(Termine)
    leiter = models.BooleanField('leiter', default=False)
    status = models.IntegerField('status', default=0)

class Notizen(models.Model):
    ansprechpartner = models.ForeignKey(Ansprechpartner)
    mitarbeiter = models.ForeignKey(Mitarbeiter)
    gespraechsart = models.IntegerField('gespraechsart', default=0)
    notiztext = models.CharField('nituztext', max_length=200)