from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
    

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='menu/', blank=True, null=True)
    description = models.TextField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Reservation(models.Model):
        name = models.CharField(max_length=100)
        phone = models.CharField(max_length=15)
        email = models.EmailField()
        date = models.DateField()
        time = models.TimeField()
        guests = models.IntegerField()

        def __str__(self):
            return self.name
             