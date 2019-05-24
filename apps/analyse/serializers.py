from rest_framework import serializers
from .models import JobMap, JobPoint, FareCloud, CompanyMap, \
    CompanyHot, CompanyParallel, Jobbar


class JobsMapSerializer(serializers.ModelSerializer):
    jobfunction_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()

    def get_jobfunction_name(self, obj):
        return obj.jobfunction.name

    def get_city_name(self, obj):
        return obj.city.name

    class Meta:
        model = JobMap
        fields = "__all__"


class JobsPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPoint
        fields = "__all__"


class FareCloudSerializer(serializers.ModelSerializer):
    class Meta:
        model = FareCloud
        fields = "__all__"


class CompanyMapSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField()

    def get_city_name(self, obj):
        return obj.city.name

    class Meta:
        model = CompanyMap
        fields = "__all__"


class CompanyHotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyHot
        fields = "__all__"


class JobbarSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()

    def get_company_name(self, obj):
        return obj.company.name
    
    class Meta:
        model = Jobbar
        fields = "__all__"


class CompanyParallelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyParallel
        fields = ['p', 'c', 's', 'q', 'i']
