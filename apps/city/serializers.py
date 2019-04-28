from rest_framework import serializers
from .models import Cities, Provinces


class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = "__all__"


class ProvincesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provinces
        fields = "__all__"
