from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.contrib import auth

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/pelis/tarea7/vista_crud')
