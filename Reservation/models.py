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
    SALLE_TYPE = (
        ('VIP', 'vip'),
        ('NORMAL', 'Normal')
    )
    numero = models.IntegerField()
    type = models.CharField(max_length=50, choices=SALLE_TYPE)
    
    
    def __str__(self):
      return f"le numero de salle est :{self.numero}  et le type : {self.type}"
    

class Table(models.Model):
    TABLE_TYPE = (
        ('VIP', 'vip'),
        ('NORMAL', 'Normal')
    )
    numero = models.IntegerField()
    type = models.CharField(max_length=50, choices=TABLE_TYPE)
    salle = models.ForeignKey(Salle, null=True, on_delete=models.CASCADE)
    disponiblité = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.numero} {self.type}"
    
class Reservation_table(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    table = models.ForeignKey(Table,  on_delete=models.CASCADE)
    date_reservation = models.DateTimeField()
    disponiblité = models.BooleanField(default=True)
    
    def __str__(self):
       return f"{self.client.nom} {self.client.prenom} a reserver la table numero {self.table.numero} dans la salle numero {self.table.salle.numero}, date de reservation: {self.date_reservation}"
  
class Reservation_salle(models.Model):
    client = models.ForeignKey(Client,  on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    date_reservation = models.DateTimeField()
    
    def __str__(self):
            return f"{self.client.nom} {self.client.prenom} a reserver la salle numero {self.salle.numero}, date de reservation: {self.date_reservation}"
    
      