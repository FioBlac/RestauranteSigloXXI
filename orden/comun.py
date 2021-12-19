from enum import  Enum
from django.db import models



class OrdenStatus(models.TextChoices):
    
    CREATED = 'En espera'
    PAYED = 'Pagado'
    COMPLETED = 'Completado'
    CANCELED = 'Cancelado'
    NO = 'No'
    SI = 'Si'
    
choices = [(tag, tag.value) for tag in OrdenStatus]
   