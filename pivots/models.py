from django.db import models

# Create your models here.
class Professions(models.Model): # a model name i.e Professions should be singular i.e Profession
    description = models.CharField(max_length= 64)

    def __str__(self):
        return self.description

class DataSheet(models.Model):
    description= models.CharField(max_length= 64)
    historical_data = models.TextField()

    def __str__(self):
        return self.description

class Customer(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=128)
    profession = models.ManyToManyField(Professions)
    data_sheet = models.OneToOneField(DataSheet, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=True)

    @property
    def status_message(self):
        if self.active:
            return 'Customer active'
        else:
            return 'Customer inactive'

    def no_of_professions(self):
        return self.profession.all().count()

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
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)

    def __str__(self):
        return self.doc_number

