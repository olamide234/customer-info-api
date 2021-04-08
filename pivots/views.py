from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
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

    def list(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        # customers = Customer.objects.filter(id=3)
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        obj = self.get_object()
        serializer = CustomerSerializer(obj)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        customer = Customer.objects.create(
            name = data['name'], address = data['address'], data_sheet_id = data['data_sheet'],
        )
        professions = Professions.objects.get(id = data['profession'])
        customer.profession.add(professions)
        customer.save()
        serializer = CustomerSerializer(customer)
        
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        data = request.data
        customer = self.get_object()
        customer.name = data['name']
        customer.address = data['address']
        customer.data_sheet_id = data['data_sheet']
        
        professions = Professions.objects.get(id = data['profession'])
        for p in customer.profession.all():
            customer.profession.remove(p)
        customer.profession.add(professions)
        customer.save()
        serializer = CustomerSerializer(customer)
        
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.name = request.data.get('name', customer.name)
        customer.address = request.data.get('address', customer.address)
        customer.data_sheet_id = request.data.get('data_sheet', customer.data_sheet_id)
        # data = request.data
        # professions = Professions.objects.get(id = data['profession'])
        # customer.profession = request.data.get(professions, customer.profession)

        customer.save()
        serializer = CustomerSerializer(customer)
        
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.delete()
        return Response('Object removed')

    @action(detail=True) #setting detail=True helps to implement the decorator function on only a specific id 
    def deactivate(self, request, **kwargs):
        customer = self.get_object()
        customer.active = False
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    @action(detail=False)
    def deactivate_all(self, request, **kwargs):
        customers = Customer.objects.all()
        customers.update(active=False)
        # customer.save()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def activate_all(self, request, **kwargs):
        customers = Customer.objects.all()
        customers.update(active=True)
        # customers.save()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST']) #setting detail=True helps to implement the decorator function on only a specific id 
    def change_status(self, request, **kwargs):
        status = True if request.data['active'] == 'True' else False
        customers = Customer.objects.all()
        customers.update(active=status)
        serializer = CustomerSerializer(customers, many= True)
        return Response(serializer.data)

class ProfessionsViewSet(viewsets.ModelViewSet):
    queryset = Professions.objects.all()
    serializer_class = ProfessionsSerializer

class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
