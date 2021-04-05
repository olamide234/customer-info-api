from django.shortcuts import render
from .models import Customer, Professions, DataSheet, Document
from rest_framework import viewsets
from .serializer import CustomerSerializer, ProfessionsSerializer, DataSheetSerializer, DocumentSerializer

# Create your views here.
# ViewSets define the view behavior.
class CustomerViewSet(viewsets.ModelViewSet):
    #queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    #to override the method get_queryset
    def get_queryset(self):
        active_customer = Customer.objects.filter(active=True)
        return active_customer

class ProfessionsViewSet(viewsets.ModelViewSet):
    queryset = Professions.objects.all()
    serializer_class = ProfessionsSerializer

class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
