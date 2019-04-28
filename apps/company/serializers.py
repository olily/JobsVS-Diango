from rest_framework import serializers
from .models import Industries, Companies


class IndustriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Industries
        fields = "__all__"


class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = "__all__"
