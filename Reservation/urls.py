from . import views

from django.urls import path

urlpatterns = [
    
    path('',views.client_home, name="client_home"),
    path('home/',views.home,name="home"),
    path('client/',views.client, name="client"),
    path('reservation_salle/',views.reservation_salle, name="reservation_salle"),
    path('reservation_table/',views.reservation_table, name="reservation_table"),
    path('salle/',views.salle,name="salle"),
    path('table/',views.table, name="table"),
    path('ajout_reservation_salle_client/',views.ajout_reservation_salle_client, name="ajout_reservation_salle_client"),
    path('ajout_reservation_table_client/',views.ajout_reservation_table_client, name="ajout_reservation_table_client"),
    path('reservation_client/',views.reservation_client, name="reservation_client"),
    path('afficher_client/',views.afficher_client, name="afficher_client"),
    
    

]

