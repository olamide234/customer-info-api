from rest_framework import serializers
from .models import Customer, Professions, DataSheet, Document

# Serializers define the API representation.
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'address', 'profession', 'data_sheet', 'active']

class ProfessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professions
        fields = ['id', 'description']

class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = ['id', 'description', 'historical_data']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'dtype', 'doc_number', 'documents']