from rest_framework import serializers
from .models import Customer, Professions, DataSheet, Document

# Serializers define the API representation.
class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = ['id', 'description', 'historical_data']
        
class ProfessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professions
        fields = ['id', 'description']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'dtype', 'doc_number', 'customer'] 

class DocumentSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['dtype', 'doc_number', 'customer'] #'id', 
        read_only_fields = ['customer']

class CustomerSerializer(serializers.ModelSerializer):
    num_professions = serializers.SerializerMethodField() #the SerilizerMethodField() by default looks for a method inside this very class
    # that have the same name num_professions with get preceding 
    # data_sheet = serializers.SerializerMethodField() #SerializerMethodField can also be used and implemented here
    # data_sheet = serializers.PrimaryKeyRelatedField(read_only=True)
    # profession = serializers.StringRelatedField(many=True)
    # document_set = serializers.StringRelatedField(many=True)
    #for nestedserializer to work for post, all relatinship between models should be nestedserializer and create() method 
    # in view should be left at default
    data_sheet = DataSheetSerializer() #read_only=True #this is called nested serializer
    profession = ProfessionsSerializer(many=True)
    document_set = DocumentSerializerCreate(many=True)#, read_only=True

    class Meta:
        model = Customer
        fields = ['id', 'name', 'address', 'profession', 'data_sheet', 'active', 'status_message', 'num_professions', 'document_set']

    def get_num_professions(self, obj):
        return obj.no_of_professions()

    # def get_data_sheet(self, obj):
    #     return obj.data_sheet.description

    def create(self, validated_data):
        profession_set = validated_data.pop('profession')
        document_part = validated_data.pop('document_set')
        data_sheet = validated_data.pop('data_sheet')

        d_sheet = DataSheet.objects.create(**data_sheet)
        customer = Customer.objects.create(**validated_data)
        customer.data_sheet = d_sheet
        for profession in profession_set:
            prof = Professions.objects.create(**profession)
            customer.profession.add(prof)
        
        for document in document_part:
            Document.objects.create(
                dtype= document['dtype'],
                doc_number= document['doc_number'],
                customer_id= customer.id
            )

        customer.save()

        return customer

