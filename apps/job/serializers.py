from rest_framework import serializers
from .models import Jobs, JobFunctions


class JobsSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    edu_name = serializers.SerializerMethodField()
    companysize_name = serializers.SerializerMethodField()

    def get_company_name(self, obj):
        return obj.company.name

    def get_city_name(self, obj):
        return obj.city.name

    def get_edu_name(self, obj):
        return obj.education.name

    def get_companysize_name(self, obj):
        return obj.company.size.name

    class Meta:
        model = Jobs
        fields = "__all__"


class JobFunctionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobFunctions
        fields = "__all__"
