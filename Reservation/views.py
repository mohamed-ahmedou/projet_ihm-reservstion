from ast import Or
from contextlib import redirect_stderr
import email
from genericpath import exists
from multiprocessing import context
from urllib.request import Request
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

def ajout_client(request):
    if request.method=="POST":   
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        tel = request.POST['tel']
        c = Client.objects.create(nom=nom, prenom = prenom, email=email, tel=tel )
        c.save()
        return redirect("/client")
    
    return render(request, 'Reservation/Ajout_client.html')

def table(request):
    table = Table.objects.all()
    return render(request, 'Reservation/Table.html', {'table':table}) 

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
    reserv_salle = Reservation_salle.objects.all()
    return render (request, 'Reservation/Reservation_salle.html',{'reserv_salle' : reserv_salle})


 

def reservation_table(request):
    reserv_table = Reservation_table.objects.all()
    return render(request, 'Reservation/Reservation_Table.html',{'reserv_table' : reserv_table})

def ajout_reservation_table(request):
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
        return render(request, 'Reservation/impression_table_admin.html',{'idd': idd}) 
           
    tables = Table.objects.all()
    return render(request,'Reservation/Ajout_reservation_table.html',{'tables' : tables} )


def ajout_reservation_salle(request):
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
        idd = r.id 
        nom = Reservation_salle.objects.all()
        return render (request, 'Reservation/impression_salle_admin.html', {'idd': idd}) 
    salles = Salle.objects.all()
    return render(request, 'Reservation/Ajout_reservation_salle.html',{'salles':salles})

def impression_table_admin(request):
    
    return render (request, 'Reservation/impression_table_admin.html')

def impression_salle_admin(request,myid):
    reservation = Reservation_salle.object.get(id=myid)
    t = Reservation_salle.object.all()
    return render (request, 'Reservation/impression_salle_admin.html',{'reservation' : reservation},{'t':t})

def rechercher_reservation_salle(request):
    if request.method=="POST":
        tel = request.POST['tel']     
        try:
            
           client = Client.objects.get(tel=tel)
           
           salle = Reservation_salle.objects.get(client=client)
           print(salle.salle.numero)
           date_s = Reservation_salle.objects.get(client=client)
           print(date_s.date_reservation)
           cl = Reservation_salle.objects.get(client=client)
           print(cl.client.nom)
           idd = salle.id
           reservation = {'tel' : tel,
                        'client' : client,
                        'tel' : tel,                             
                        'salle' : salle,                             
                        'date_s' : date_s,
                        'idd' : idd }
           
           return render (request , 'Reservation/Rechercher_reservation_salle.html',reservation )
          
        except:
            return render (request , 'Reservation/Rechercher_reservation_salle.html', {})
    else:    
        return render (request , 'Reservation/Rechercher_reservation_salle.html', {})
    
def rechercher_reservation_table(request):
    if request.method=="POST":
        tel = request.POST['tel']     
        try:
            
           client = Client.objects.get(tel=tel)
           
           table = Reservation_table.objects.get(client=client)
           print(table.table.numero)
           date_s = Reservation_table.objects.get(client=client)
           print(date_s.date_reservation)
           cl = Reservation_table.objects.get(client=client)
           print(cl.client.nom)
           idd = table.id
           reservation = {'tel' : tel,
                        'client' : client,
                        'tel' : tel,                             
                        'table' : table,                             
                        'date_s' : date_s,
                        'cl' : 'cl',
                        'idd' : idd }
           
           return render (request , 'Reservation/Rechercher_reservation_table.html',reservation )
          
        except:
            return render (request , 'Reservation/Rechercher_reservation_table.html', {})
    else:    
        return render (request , 'Reservation/Rechercher_reservation_table.html', {})
    
def rechercher_table(request):
    if request.method=="POST":
        numero = request.POST['numero']  
        try:
            re = Table.objects.get(numero = numero)
            print(re.numero)
            context ={'numero' : numero,
                     're' : re}
            return render(request, 'Reservation/Rechercher_table.html',context)
        except:
           return render(request, 'Reservation/Rechercher_table.html',{})
    else: 
        return render(request, 'Reservation/Rechercher_table.html',{})

def rechercher_client(request):
    if request.method=="POST":
        tel = request.POST['tel']  
        try:
            re = Client.objects.get(tel = tel)
            print(re.nom)
            context ={'tel' : tel,
                     're' : re}
            return render(request, 'Reservation/Rechercher_client.html',context)
        except:
           return render(request, 'Reservation/Rechercher_client.html',{})
    else: 
        return render(request, 'Reservation/Rechercher_client.html',{})
    
def rechercher_salle(request):
    if request.method=="POST":
        numero = request.POST['numero']  
        try:
            re = Salle.objects.get(numero = numero)
            print(re.numero)
            context ={'numero' : numero,
                     're' : re}
            return render(request, 'Reservation/Rechercher_salle.html',context)
        except:
           return render(request, 'Reservation/Rechercher_salle.html',{})
    else: 
        return render(request, 'Reservation/Rechercher_salle.html',{})
    
def modifier_salle(request, myid):
    v = Salle.objects.get(id=myid)
    if request.method=="POST":   
        v.numero = request.POST['numero']
        v.type = request.POST['type']
        v.save()
        return redirect("/salle")  
    return render(request, 'Reservation/Modifier_salle.html', {'v': v})

def supprimer_salle(request, myid):
    salle = Salle.objects.filter(id=myid)
    salle.delete()
    return redirect("/salle")  

def modifier_client(request, myid):
    cl = Client.objects.get(id=myid)
    if request.method=="POST":   
        cl.nom = request.POST['nom']
        cl.prenom = request.POST['prenom']
        cl.email = request.POST['email']
        cl.tel = request.POST['tel']
        cl.save()
        return redirect("/client")  
    return render(request, 'Reservation/Modifier_client.html', {'cl': cl})

def supprimer_client(request, myid):
    client = Client.objects.filter(id=myid)
    client.delete()
    return redirect("/client") 

def modifier_table(request, iddd):
    t = Table.objects.get(id=iddd)
    if request.method=="POST":   
       t.numero = request.POST['numero']
       t.type = request.POST['type']
       idddd = request.POST['iddd']
       salle = Salle.objects.get(id=idddd)
       t.salle = salle
       t.save()
       return redirect("/table") 
    s =Salle.objects.all()
    return render(request, 'Reservation/Modifier_table.html', {'t': t},{'s' : s})

def supprimer_table(request, myid):
    table = Table.objects.filter(id=myid)
    table.delete()
    return redirect("/table") 

def supprimer_reservation_salle(request, myid):
    res = Reservation_salle.objects.filter(id=myid)
    res.delete()
    return redirect("/reservation_salle")
  
def supprimer_reservation_table(request, myid):
    res = Reservation_table.objects.filter(id=myid)
    res.delete()
    return redirect("/reservation_table")  

def reservation(request):
    
    return render( request, 'Reservation/Reservation.html')

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
        try:
            
           table = Table.objects.get(id=iddd)
        
           if date_reservation  != Reservation_table.date_reservation :
              client = Client.objects.create(nom=nom, prenom=prenom, tel=tel, email=email)
              r = Reservation_table.objects.create(client = client, table=table, date_reservation = date_reservation )
              client.save()
              r.save() 
              idd = r.id
              return render(request, 'Reservation/impression_table.html',{'idd': idd}) 
           else:
              return render(request, 'Reservation/Salle.html')  
        except:
            res = {'msg' : 1}
            return render(request, 'Reservation/Salle.html',{'res' : res})  
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
               
                if Reservation_table.objects.get(client=client) and Reservation_salle.objects.get(client=client): 
                    
                    table = Reservation_table.objects.get(client=client)
                    print(table.table.numero)
                    print(table.table.salle.numero)
                    date = Reservation_table.objects.get(client=client)
                    print(date.date_reservation)
                    salle = Reservation_salle.objects.get(client=client)
                    print(salle.salle.numero)
                    date_s = Reservation_salle.objects.get(client=client)
                    print(date_s.date_reservation)
                    
                    idd = Reservation_table.objects.get(client=client) 
                    iddd = (idd.id) 
                    id_s = Reservation_salle.objects.get(client=client) 
                    id_sa = (id_s.id)
                    
                    
                    reservation = {'tel' : tel,
                                'client' : client,
                                'table' : table,                             
                                'date' : date,
                                'salle' : salle,                             
                                'date_s' : date_s,
                                'idd' : idd,
                                'iddd' : iddd,
                                 'id_s' : id_s,
                                'id_sa' : id_sa,
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
                    idd = Reservation_table.objects.get(client=client)
                    iddd = idd.id
                    reservation = {'tel' : tel,
                                'client' : client,
                                'table' : table,                             
                                'date' : date,
                                'iddd' : iddd,
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
                    idd = Reservation_salle.objects.get(client=client)
                    iddd = (idd.id)
                    
                    reservation = {'tel' : tel,
                                'client' : client,
                                'salle' : salle,                             
                                'date' : date,
                                'idd' : idd,
                                'iddd' : iddd,
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

def Billet_salle_table(request,myid):
    try:
       if Reservation_salle.objects.get(id=myid) :
          billet_salle = Reservation_salle.objects.get(id=myid)
          print(billet_salle.client.nom)
          print(billet_salle.client.prenom)
          print(billet_salle.salle.numero)
          date = datetime.now 
        
          context = {'billet_salle' : billet_salle,
                     'date' : date
                    }
          return render (request, 'Reservation/Billet_salle_table.html',context)
       return render (request, 'Reservation/Billet_salle_table.html',context)
    
    except:
        return render (request, 'Reservation/Billet_salle_table.html',{})
        
def impression_table(request):
    
    return render (request, 'Reservation/impression_table.html')

def impression_salle(request):
    
    return render (request, 'Reservation/impression_salle.html')

def Vos_reserv(request):
    return render(request, 'Reservation/Vos_reser.html')


def contactez_nous(request):
    return render(request, 'Reservation/Contactez_nous.html')

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