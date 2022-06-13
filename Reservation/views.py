from ast import Or
from contextlib import redirect_stderr
import email
from multiprocessing import context
from webbrowser import Opera
from xmlrpc.client import boolean
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login as auth_login,logout
from datetime import *
from django.db.models import Count
from django.shortcuts import render

import Reservation


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

def ajout_table(request):
    if request.method=="POST":   
        numero = request.POST['numero']
        type = request.POST['type']
        iddd = request.POST['idd']
        salle = Salle.objects.get(id=iddd)
        c = Table.objects.create(numero=numero, type=type, salle=salle )
        c.save()
        return redirect("/table")
    salles = Salle.objects.all()
    return render(request, 'Reservation/ajout_table.html',{'salles' : salles})

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
        r.save() 
        idd = r.id
        return render(request, 'Reservation/impression_table.html',{'idd': idd})  
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
        idd = r.id;
        return render (request, 'Reservation/impression_salle.html', {'idd': idd}) 
    salles = Salle.objects.all()
    return render(request, 'Reservation/Ajout_reservation_salle_Client.html',{'salles':salles})

def reservation_client(request):
    return render(request, 'Reservation/Ajout_Reservation.html')

def vos_reservation(request):
    
    return render(request, 'Reservation/Vos_reservation.html')
def vos_reservation_salle(request):
    
    return render(request, 'Reservation/Vos_reservation_salle.html')
def vos_reservation_table(request):
    
    return render(request, 'Reservation/Vos_reservation_table.html')

def cherche_reservation_client(request):
     if request.method == "POST":
           tel = request.POST['tel']
           reservation = {}
          
           try:
                client = Client.objects.get(tel=tel)  
                print(client.nom) 
                print(client.prenom)
               
                if Reservation_salle.objects.get(client=client) and Reservation_table.objects.get(client=client): 
                    
                    table = Reservation_table.objects.get(client=client)
                    print(table.table.numero)
                    print(table.table.salle.numero)
                    date = Reservation_table.objects.get(client=client)
                    print(date.date_reservation)
                    salle = Reservation_salle.objects.get(client=client)
                    print(salle.salle.numero)
                    date_s = Reservation_salle.objects.get(client=client)
                    print(date_s.date_reservation)
                    idd = salle.id
                    reservation = {'tel' : tel,
                                'client' : client,
                                'table' : table,                             
                                'date' : date,
                                'salle' : salle,                             
                                'date_s' : date_s,
                                'idd' : idd,
                                'msg' : 1 }
                     
                    return render(request, 'Reservation/cherche_reservation_client.html',reservation)
            
           except:
               reservation = {'msg' : "ne existe pas"}
               return render(request, 'Reservation/cherche_reservation_client.html',reservation)
                
           
                
     return render(request, 'Reservation/cherche_reservation_client.html')

def cherche_reservation_client_table(request):
    
     if request.method == "POST":
           tel = request.POST['tel']
           reservation = {}
          
           try:
                client = Client.objects.get(tel=tel)  
                print(client.nom) 
                print(client.prenom)
               
                if Reservation_table.objects.get(client=client) : 

                    table = Reservation_table.objects.get(client=client)
                    
                    print(table.table.numero)
                    print(table.table.salle.numero)
                    date = Reservation_table.objects.get(client=client)
                    print(date.date_reservation)
                   
                    
                    reservation = {'tel' : tel,
                                'client' : client,
                                'table' : table,                             
                                'date' : date,
                                'msg' : 1}
                     
                    return render(request, 'Reservation/cherche_reservation_client_table.html',reservation)
            
           except:
                  reservation = {'msg' : "ne existe pas"}
                  return render(request, 'Reservation/cherche_reservation_client_table.html',reservation)
    
    
     return render(request, 'Reservation/cherche_reservation_client_table.html')           


def cherche_reservation_client_salle(request):
    
     if request.method == "POST":
           tel = request.POST['tel']
           reservation = {}
          
           try:
                client = Client.objects.get(tel=tel)  
                print(client.nom) 
                print(client.prenom)
               
                if Reservation_salle.objects.get(client=client) : 

                    salle = Reservation_salle.objects.get(client=client)
                    
                    print(salle.salle.numero)
                    date = Reservation_salle.objects.get(client=client)
                    print(date.date_reservation)
                   
                    
                    reservation = {'tel' : tel,
                                'client' : client,
                                'salle' : salle,                             
                                'date' : date,
                                'msg' : 1}
                     
                    return render(request, 'Reservation/cherche_reservation_client_salle.html',reservation)
            
           except:
                  reservation = {'msg' : "ne existe pas"}
                  return render(request, 'Reservation/cherche_reservation_client_salle.html',reservation)
    
    
     return render(request, 'Reservation/cherche_reservation_client_salle.html')           




def Billet(request):
 
    return render (request, 'Reservation/Billet.html')

def Billet_salle(request,myid):
    billet = Reservation_salle.objects.get(id = myid)
    date = datetime.now 
    return render (request, 'Reservation/Billet_salle.html',{'billet':billet,'date':date})

def Billet_table(request,myid):
    billet = Reservation_table.objects.get(id = myid)
    date = datetime.now 
    return render (request, 'Reservation/Billet_table.html',{'billet':billet,'date':date})


def impression_table(request):
    
    return render (request, 'Reservation/impression_table.html')

def impression_salle(request):
    
    return render (request, 'Reservation/impression_salle.html')

def Vos_reserv(request):
    return render(request, 'Reservation/Vos_reser.html')

def login(request):
    if request.method == "POST":
        user = request.POST['username']
        passs = request.POST['password']
        user = authenticate(username=user, password=passs)
        if user is not None:
            if user.is_superuser:
                
                return redirect("/home")
        else:   
            msg = "Les données sont  erronés,ressayer"
            return render(request, "Reservation/Login.html", {"msg":msg})
    
    return render (request, 'Reservation/Login.html')