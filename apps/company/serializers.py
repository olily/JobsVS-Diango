from rest_framework import serializers
from .models import Industries, CompanyQuality, CompanySize, Companies


class IndustriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Industries
        fields = "__all__"


class CompanyQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyQuality
        fields = "__all__"


class CompanySizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySize
        fields = "__all__"


class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = "__all__"
