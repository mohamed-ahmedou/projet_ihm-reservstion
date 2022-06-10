from contextlib import redirect_stderr
import email
from multiprocessing import context
from webbrowser import Opera
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login as auth_login,logout
from datetime import *
from django.db.models import Count
from django.shortcuts import render


from .models import * 

from django.http import HttpResponseRedirect

   ##---------------###debut du view partie admin ou agent -------###############--------------
def home(request):
    client = Client.objects.all()
    table = Table.objects.all()
    salle = Salle.objects.all()
    resrevation_table = Reservation_table.objects.all()
    resrevation_salle = Reservation_salle.objects.all()
    nb_client = Client.objects.all().count()
    nb_table = Table.objects.all().count()
    nb_salle = Salle.objects.all().count()
    nb_reservation_table = Reservation_table.objects.all().count()
    nb_reservation_salle = Reservation_salle.objects.all().count()
    nb_table_non_reserver = nb_table - nb_reservation_table
    nb_salle_non_reserver = nb_salle - nb_reservation_salle
    totale_reservations = nb_reservation_table + nb_reservation_salle
    context = {'client' : client,
               'table': table,
               'salle': salle,
               'resrevation_table' : resrevation_table,
               'resrevation_salle' : resrevation_salle,
               'nb_client' : nb_client,
               'nb_table' : nb_table,
               'nb_salle' : nb_salle,
               'nb_reservation_table' : nb_reservation_table,
               'nb_reservation_salle' : nb_reservation_salle,
               'totale_reservations':totale_reservations,
               'nb_table_non_reserver':nb_table_non_reserver,
               'nb_salle_non_reserver' : nb_salle_non_reserver}
    return render (request,'Reservation/Tabledebord.html ',context)

def client(request):
    client = Client.objects.all()
    return render(request, 'Reservation/Client.html',{'client':client})


def salle(request):
    salle = Salle.objects.all
    return render(request, 'Reservation/Salle.html', {'salle':salle}) 

def ajout_salle(request):
    if request.method=="POST":   
        numero = request.POST['numero']
        type = request.POST['type']
        c = Salle.objects.create(numero=numero, type = type )
        c.save()
        return redirect("/salle")
    
    return render(request, 'Reservation/ajout_salle.html')


def reservation_salle(request):
    return render (request, 'Reservation/Reservation_salle.html')

def table(request):
    table = Table.objects.all()
    return render(request, 'Reservation/Table.html', {'table':table})    

def reservation_table(request):
    return render(request, 'Reservation/Reservation_Table.html')



##-----------------------------------fin view partie admin ou agent -----------------------------------## 


#########################d  debut view pour partie client   #---------------------------#############
def client_home(request):
    return render(request, 'Reservation/TabledebordClient.html')


def ajout_reservation_table_client(request):
    if request.method=="POST":   
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        tel = request.POST['tel']
        email = request.POST['email']
        iddd = request.POST['idd']
        date_reservation = request.POST['date_reservation']
        table = Table.objects.get(id=iddd)
     
        client = Client.objects.create(nom=nom, prenom=prenom, tel=tel, email=email)
        r = Reservation_table.objects.create(client = client, table=table, date_reservation = date_reservation )
        
        client.save()
        table.disponiblité = False
        table.save()
        r.save()
        
        return redirect("/ajout_reservation_table_client")  
    tables = Table.objects.all()
    return render(request,'Reservation/Ajout_reservation_table_Client.html',{'tables' : tables} )


def ajout_reservation_salle_client(request):
    if request.method=="POST":   
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        tel = request.POST['tel']
        email = request.POST['email']
        iddd = request.POST['idd']
        date_reservation = request.POST['date_reservation']
        salle = Salle.objects.get(id=iddd)
        client = Client.objects.create(nom=nom, prenom=prenom, tel=tel, email=email)
        r = Reservation_salle.objects.create(client = client, salle=salle, date_reservation = date_reservation)
        client.save()
        r.save()
        
        return redirect("/ajout_reservation_salle_client")  
    salles = Salle.objects.all()
    return render(request, 'Reservation/Ajout_reservation_salle_Client.html',{'salles':salles})

def reservation_client(request):
    return render(request, 'Reservation/Ajout_Reservation.html')

def vos_reservation(request):
    
    return render(request, 'Reservation/Vos_reservation.html')

def cherche_reservation_client(request):
     if request.method == "POST":
           tel = request.POST['tel']
           res = {}
           try:
                client = Client.objects.get(tel=tel)  
                print(client.nom) 
                print(client.prenom)
                
                salle = Reservation_salle.objects.filter(client=client).count()
                print(salle.numero)
                print(table.numero)
                nb_res_salle = salle.count()
                
                table = Reservation_table.objects.filter(client=client).count()
                print(table.numero)
                print(table.salle.numero)
                nb_res_table=table.count()
                
                nb_total_reservation = nb_res_salle + nb_res_table
               
                reservation = {'tel' : tel,
                                'client' : client,
                                'salle' : salle,
                                'nb_res_salle': nb_res_salle,
                                'table' : table,
                                'nb_res_table' : nb_res_table,
                                'nb_total_reservation' : nb_total_reservation,
                                'msg' : 1}
                return render(request, 'Reservation/cherche_reservation_client.html',reservation)
           except:
               res = {'msg' : "ne existe pas",
                                }
               return render(request, 'Reservation/cherche_reservation_client.html',res)
                
           
                
     return render(request, 'Reservation/cherche_reservation_client.html')
# Create your views here.

