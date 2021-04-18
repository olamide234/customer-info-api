from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser, 
DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly)
from django_filters.rest_framework import  DjangoFilterBackend
from .models import Customer, Professions, DataSheet, Document
from rest_framework import viewsets
from .serializer import CustomerSerializer, ProfessionsSerializer, DataSheetSerializer, DocumentSerializer

# Create your views here.
# ViewSets define the view behavior.
class CustomerViewSet(viewsets.ModelViewSet):
    #queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_fields = ['name']
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['name', 'address', 'data_sheet__description']
    ordering_fields = ['id', 'name']
    lookup_fields = 'name' #field(s) here should have unique input
    authentication_classes = [TokenAuthentication,]

    #to override the method get_queryset
    def get_queryset(self):
        address = self.request.query_params.get('address', None)
        if self.request.query_params.get('active')== 'False':
            status = False
        else:
            status = True
        if address:
            customers = Customer.objects.filter(address__icontains= address, active=status)
        else:
            customers = Customer.objects.filter(active=status)
        return customers

    # def list(self, request, *args, **kwargs):
    #     # import pdb; pdb.set_trace()
    #     # customers = Customer.objects.filter(id=3)
    #     customers = self.get_queryset()
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        obj = self.get_object()
        serializer = CustomerSerializer(obj)
        return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     customer = Customer.objects.create(
    #         name = data['name'], address = data['address'], data_sheet_id = data['data_sheet'],
    #     )
    #     professions = Professions.objects.get(id = data['profession'])
    #     customer.profession.add(professions)
    #     customer.save()
    #     serializer = CustomerSerializer(customer)
        
    #     return Response(serializer.data)
    
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
        customers = self.get_queryset()
        customers.update(active=False)
        # customer.save()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def activate_all(self, request, **kwargs):
        customers = self.get_queryset()
        customers.update(active=True)
        # customers.save()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST']) #setting detail=True helps to implement the decorator function on only a specific id 
    def change_status(self, request, **kwargs):
        status = True if request.data['active'] == 'True' else False
        customers = self.get_queryset()
        customers.update(active=status)
        serializer = CustomerSerializer(customers, many= True)
        return Response(serializer.data)

class ProfessionsViewSet(viewsets.ModelViewSet):
    queryset = Professions.objects.all()
    serializer_class = ProfessionsSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAdminUser,]

class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer
    permission_classes = [AllowAny, ]

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    authentication_classes= [TokenAuthentication,]
    # permission_classes = [IsAuthenticatedOrReadOnly,]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly,]
