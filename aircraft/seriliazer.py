from rest_framework import serializers
from aircraft.models import Aircraft
from airline.models import Airline

class AircraftSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    manufacturer_serial_number = serializers.CharField(max_length=50,required=True)
    type = serializers.CharField(max_length=50,required=True)
    model = serializers.CharField(required=True)
    number_of_engines = serializers.IntegerField(required=True)
    operator_airline = serializers.PrimaryKeyRelatedField(queryset=Airline.objects.all(), required=True)

    class Meta:
        model = Aircraft
        fields = ['id', 'manufacturer_serial_number', 'type', 'model', 'number_of_engines' , 'operator_airline']



    def validate_manufacturer_serial_number(self, value):
        
        if self.instance:
            if Aircraft.objects.filter(manufacturer_serial_number=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Aircraft with this manufacturer serial number already exists.")
        else:
            if Aircraft.objects.filter(manufacturer_serial_number=value).exists():
                raise serializers.ValidationError("Aircraft with this manufacturer serial number already exists.")
        return value

    def create(self, validated_data):
        
        return Aircraft.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.manufacturer_serial_number = validated_data.get("manufacturer_serial_number", instance.manufacturer_serial_number)
        instance.type = validated_data.get("type", instance.type)
        instance.model = validated_data.get("model", instance.model)
        instance.number_of_engines = validated_data.get("number_of_engines", instance.number_of_engines)
        instance.operator_airline = validated_data.get("operator_airline", instance.operator_airline)

        instance.save()
        return instance
