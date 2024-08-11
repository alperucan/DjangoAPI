from rest_framework import serializers
from airline.models import Airline


## Response'daki JSON Datada neler olacagını gosterir!
## isDeleted gozukmeyecek!
class AirlineSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50,required=True)
    callsign = serializers.CharField(max_length=50,required=True)
    founded_year = serializers.IntegerField(required=True)
    base_airport = serializers.CharField(max_length=50,required=True)
    #isDeleted = serializers.BooleanField()

    class Meta:
        model = Airline
        fields = ['id', 'name', 'callsign', 'founded_year', 'base_airport']
        

    def validate(self, data):
        ## founded_year is optional 
        ## user might change the other attributes!
        ## Founded_year'a belirli bir aralik koydugum icin kontrol ediyorum.
        ## Update'de founded_year gelmeyebilir o yüzden None kontrolü yaptim 
        founded_year = data.get('founded_year', None)
    
        if founded_year is not None:
            if founded_year > 2024 or founded_year < 1800:
                raise serializers.ValidationError('founded_year must be 1800 <= founded_year <= 2024 ')
        
        return data

    def create(self, validated_data):
        return Airline.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.callsign = validated_data.get("callsign", instance.callsign)
        instance.founded_year = validated_data.get("founded_year", instance.founded_year)
        instance.base_airport = validated_data.get("base_airport", instance.base_airport)
        
           
        instance.save()
        return instance
    
