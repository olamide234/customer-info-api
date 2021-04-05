from django.db import models

# Create your models here.
class Professions(models.Model): # a model name i.e Professions should be singular i.e Profession
    description = models.CharField(max_length= 64)

class DataSheet(models.Model):
    description= models.CharField(max_length= 64)
    historical_data = models.TextField()

    def __str__(self):
        return self.description

class Customer(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=128)
    profession = models.ManyToManyField(Professions)
    data_sheet = models.OneToOneField(DataSheet, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Document(models.Model):
    PP = 'PP'
    ID = 'ID'
    OT = 'OT'

    DOC_TYPES= [
        (PP, 'Passport'),
        (ID, 'Identity Card'),
        (OT, 'Others')
        ]
    dtype = models.CharField(choices=DOC_TYPES, max_length= 2)
    doc_number = models.CharField(max_length=64)
    documents = models.ForeignKey(Customer, on_delete = models.CASCADE)

    def __str__(self):
        return self.doc_number

