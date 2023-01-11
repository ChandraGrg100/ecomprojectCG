from django.shortcuts import render
from .models import *

# Create your views here.

def base():
    views = {}
    views['category'] = Category.objects.all()
    return views


def Home(request):
    views = base()
    return render(request, "index.html", views)
