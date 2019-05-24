from rest_framework import serializers
from .models import JobMap, JobPoint, FareCloud, CompanyMap, \
    CompanyHot, CompanyParallel, Jobbar,FunSunburst,CitySunburst,IndustrySunburst,ResponseCloud,RequestCloud


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


class ResponseCloudSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseCloud
        fields = "__all__"


class RequestCloudSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestCloud
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


class FunSunSerializer(serializers.ModelSerializer):
    fun_name = serializers.SerializerMethodField()
    catg_name = serializers.SerializerMethodField()

    def get_fun_name(self, obj):
        return obj.functions.name

    def get_catg_name(self, obj):
        return obj.functions.category.name

    class Meta:
        model = FunSunburst
        fields = "__all__"


class CitySunSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField()
    pro_name = serializers.SerializerMethodField()

    def get_city_name(self, obj):
        return obj.city.name

    def get_pro_name(self, obj):
        return obj.province.name

    class Meta:
        model = CitySunburst
        fields = "__all__"


class IndustrySerializer(serializers.ModelSerializer):
    in_name = serializers.SerializerMethodField()
    catg_name = serializers.SerializerMethodField()

    def get_in_name(self, obj):
        return obj.Industries.name

    def get_catg_name(self, obj):
        return obj.Industries.category.name

    class Meta:
        model = IndustrySunburst
        fields = "__all__"
