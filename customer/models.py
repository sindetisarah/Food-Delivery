from django.db import models
from django.db.models.fields import AutoField, DecimalField

# Create your models here.
"""
class for items offered for sales
"""
class MenuItem(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to ='menu_images/')
    price=models.DecimalField(max_digits=5,decimal_places=2)
    category=models.ManyToManyField('Category', related_name='item')

    """
    adding an str method to make it look more better
    
    """
    def __str__(self):
        return self.name
"""
category model
"""
class Category(models.Model):
    name=models.CharField(max_length=100)
    """
    A string method to format it
    """
    def __str__(self):
        return self.name
"""
order model to hold items that have been ordered
"""
class OrderModel(models.Model):
    created_on=models.DateTimeField(auto_now_add=True)
    price=models.DecimalField(max_digits=7,decimal_places=2,default=200)
    items=models.ManyToManyField('MenuItem',related_name='order',blank=True)
    """
    Adding a name, email and address for form confirmation Submission
    """
    name=models.CharField(max_length=30,blank=True)
    email=models.EmailField(max_length=50,blank=True)
    city=models.CharField(max_length=50,blank=True)
    state=models.CharField(max_length=50,blank=True)
    zipCode=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f'Ordered:{self.created_on.strftime("%b %d %I:%M %p")}'
       
       
        
