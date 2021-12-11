from django.db import models
from django.utils.text import slugify
from django.db.models.signals import  pre_save


# Create your models here.
class Product(models.Model):
    title= models.CharField(max_length=100)
    price= models.DecimalField(max_digits=10,decimal_places=0, default=0.0)
    description=models.TextField()
    image = models.ImageField(upload_to='product/',null=False,blank=False)
    tiempo=models.DecimalField(max_digits=10,decimal_places=2, default=0.0)
    created_at=models.DateTimeField(auto_now_add=True)
    slug=models.SlugField(max_length=200, null=False, blank=False, unique=True)


    def __str__(self):
        return self.title

def new_slug(sender,instance,*args,**kwargs):
        instance.slug= slugify(instance.title)
    
pre_save.connect(new_slug, sender=Product)