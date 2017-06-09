"""
prepopulated_fields:
Das Attribut prepopulated_fields hilft in der Admin-Applikation dabei, dass Feld slug bei der Eingabe automatisch zu füllen. In diesem Fall mit dem Attribut name des Models.
"""

# Models beim Admin regisitrieren

from django.contrib import admin
from MyA.models import Mitarbeiter, Kunden, Ansprechpartner, Termine, TeilnehmerExt, TeilnehmerInt, Notizen


admin.site.register(Mitarbeiter)
admin.site.register(Kunden)
admin.site.register(Ansprechpartner)
admin.site.register(Termine)
admin.site.register(TeilnehmerExt)
admin.site.register(TeilnehmerInt)
admin.site.register(Notizen)
