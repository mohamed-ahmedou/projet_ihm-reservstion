from . import views

from django.urls import path

urlpatterns = [
    
    path('',views.client_home, name="client_home"),
    path('home/',views.home,name="home"),
    path('client/',views.client, name="client"),
    path('reservation/',views.reservation, name="reservation"),
    path('reservation_salle/',views.reservation_salle, name="reservation_salle"),
    path('reservation_table/',views.reservation_table, name="reservation_table"),
    path('salle/',views.salle,name="salle"),
    path('table/',views.table, name="table"),
    path('ajout_reservation_salle_client/',views.ajout_reservation_salle_client, name="ajout_reservation_salle_client"),
    path('ajout_reservation_table_client/',views.ajout_reservation_table_client, name="ajout_reservation_table_client"),
    path('reservation_client/',views.reservation_client, name="reservation_client"),
    path('vos_reservation/',views.vos_reservation, name="vos_reservation"),
    path('vos_reservation_salle/',views.vos_reservation_salle, name="vos_reservation_salle"),
    path('vos_reservation_table/',views.vos_reservation_table, name="vos_reservation_table"),
    path('cherche_reservation_client/',views.cherche_reservation_client, name="cherche_reservation_client"),
    path('ajout_salle/',views.ajout_salle, name="ajout_salle"),
    path('ajout_table/',views.ajout_table, name="ajout_table"),
    path('Billet/', views.Billet, name="Billet"),
    path('Billet_salle/<int:myid>/', views.Billet_salle, name="Billet_salle"),
    path('Billet_table/<int:myid>/', views.Billet_table, name="Billet_table"),
    path('Billet_salle_table/<int:myid>/', views.Billet_salle_table, name="Billet_salle_table"),
    path('impression_table/',views.impression_table, name="impression_table"),
    path('impression_salle/',views.impression_salle, name="impression_salle"),
    path('login/', views.login, name="login"),
    path('cherche_reservation_client_table/', views.cherche_reservation_client_table, name="cherche_reservation_client_table"),
    path('cherche_reservation_client_salle/', views.cherche_reservation_client_salle, name="cherche_reservation_client_salle"),
    path('Vos_reserv/', views.Vos_reserv, name="Vos_reserv"),
    path('rechercher_table/', views.rechercher_table, name="rechercher_table"),
    path('rechercher_client/', views.rechercher_client, name="rechercher_client"), 
    path('rechercher_salle/', views.rechercher_salle, name="rechercher_salle"), 
    path('ajout_client/', views.ajout_client, name="ajout_client"),
    path('ajout_reservation_salle/', views.ajout_reservation_salle, name="ajout_reservation_salle"),
    path('ajout_reservation_table/', views.ajout_reservation_table, name="ajout_reservation_table"),
    path('impression_salle_admin/<int:myid>/',views.impression_salle_admin, name="impression_salle_admin"),
    path('impression_table_admin/',views.impression_table_admin, name="impression_table_admin"),
    path('rechercher_reservation_salle/',views.rechercher_reservation_salle, name="rechercher_reservation_salle"),
    path('rechercher_reservation_table/',views.rechercher_reservation_table, name="rechercher_reservation_table"),
    path('modifier_salle/<int:myid>/', views.modifier_salle, name="modifier_salle"),
    path('supprimer_salle/<int:myid>/', views.supprimer_salle, name="supprimer_salle"),
    path('modifier_client/<int:myid>/', views.modifier_client, name="modifier_client"),
    path('supprimer_client/<int:myid>/', views.supprimer_client, name="supprimer_client"),
    path('modifier_table/<int:iddd>/', views.modifier_table, name="modifier_table"),
    path('supprimer_table/<int:myid>/', views.supprimer_table, name="supprimer_table"),
    path('supprimer_reservation_salle/<int:myid>/', views.supprimer_reservation_salle, name="supprimer_reservation_salle"),
    path('supprimer_reservation_table/<int:myid>/', views.supprimer_reservation_table, name="supprimer_reservation_table"),
    path('contactez_nous/',views.contactez_nous, name="contactez_nous"),
    
    
   
    
]

