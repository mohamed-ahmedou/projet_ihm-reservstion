from unicodedata import category
from django.db import models

# Create your models here.

class Client(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    tel = models.IntegerField()
    
    
    def __str__(self):
        return self.nom

class Salle(models.Model):
    categorie = models.CharField(max_length=50)
    
    def __str__(self):
        return self.categorie

class Table(models.Model):
    categorie = models.CharField(max_length=50)
    salle = models.ForeignKey(Salle, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.categorie
    
class Reservation_table(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    table = models.ForeignKey(Table, null=True, on_delete=models.SET_NULL)
    date_reservation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.table
  
class Reservation_salle(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    salle = models.ForeignKey(Salle, null=True, on_delete=models.SET_NULL)
    date_reservation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
            return self.salle
    
      