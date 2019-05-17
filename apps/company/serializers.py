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
    city_name = serializers.SerializerMethodField()
    quality_name = serializers.SerializerMethodField()
    size_name = serializers.SerializerMethodField()

    def get_city_name(self, obj):
        return obj.city.name

    def get_quality_name(self, obj):
        return obj.quality.name

    def get_size_name(self, obj):
        return obj.size.name

    class Meta:
        model = Companies
        fields = "__all__"
