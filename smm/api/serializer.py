from rest_framework import serializers
from smm.models import Gestion
from smm.models import Pagos

class GestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gestion
        fields = "__all__"
 
class PagosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagos
        fields = '__all__'        