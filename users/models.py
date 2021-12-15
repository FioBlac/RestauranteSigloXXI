from django.db import models
from orden.comun import OrdenStatus
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
# Create your models here.


class Cliente(User):
    class Meta:
        proxy = True

    def get_products(self):
        return []

class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    biografia = models.TextField()
