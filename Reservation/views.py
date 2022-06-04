from contextlib import redirect_stderr
import email
from multiprocessing import context
from webbrowser import Opera
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login as auth_login,logout
from datetime import *


from .models import * 

from django.http import HttpResponseRedirect

   ##---------------###debut du view partie admin ou agent -------###############--------------
def home(request):
    return render (request,'Reservation/Tabledebord.html ')

def client(request):
    return render(request, 'Reservation/Client.html')

def salle(request):
    return render(request,'Reservation/Salle.html')

def reservation_salle(request):
    return render (request, 'Reservation/Reservation_salle.html')

def table(request):
    return render(request, 'Reservation/Table.html')    

def reservation_table(request):
    return render(request, 'Reservation/Reservation_Table.html')
def voitureclient(request):
    return 
def afficher_client(request):
    client = Client.objects.all()
    return render(request, 'Reservation/Client.html',{'client' : client})
##-----------------------------------fin view partie admin ou agent -----------------------------------## 


#########################d  debut view pour partie client   #---------------------------#############
def client_home(request):
    return render(request, 'Reservation/TabledebordClient.html')


def ajout_reservation_table_client(request):
    return render(request,'Reservation/Ajout_reservation_table_Client.html' )


def ajout_reservation_salle_client(request):
    return render(request, 'Reservation/Ajout_reservation_salle_Client.html')

def reservation_client(request):
    return render(request, 'Reservation/Ajout_Reservation.html')

# Create your views here.
