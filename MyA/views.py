from django.shortcuts import render
from django.http import HttpResponse
from MyA.models import Mitarbeiter

# Create your views here.


def get_staff(request):

    mitarbeiters = Mitarbeiter.objects.all()

    return render(request, 'staff.html', {'page_titel': 'Mitarbeiter', 'mitarbeiters':mitarbeiters})