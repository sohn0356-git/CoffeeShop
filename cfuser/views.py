from django.shortcuts import render
from django.views.generic import ListView

from cfuser.models import Cfuser
# Create your views here.

class UserLV(ListView):
    model = Cfuser
