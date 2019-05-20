from rest_framework import serializers
from .models import UserCollectJob, UserFocusCompany


class UserCollectJobSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(
        read_only=True, format="%Y-%m-%d %H:%M:%S")
    job_name = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    edu_name = serializers.SerializerMethodField()
    salary_low = serializers.SerializerMethodField()
    salary_high = serializers.SerializerMethodField()
    work_year = serializers.SerializerMethodField()
    put_time = serializers.SerializerMethodField()

    def get_job_name(self, obj):
        return obj.job.name

    def get_company_name(self, obj):
        return obj.job.company.name

    def get_city_name(self, obj):
        return obj.job.city.name

    def get_edu_name(self, obj):
        return obj.job.education.name

    def get_salary_low(self, obj):
        return obj.job.salary_low

    def get_salary_high(self, obj):
        return obj.job.salary_high

    def get_work_year(self, obj):
        return obj.job.work_year

    def get_put_time(self, obj):
        return obj.job.put_time

    class Meta:
        model = UserCollectJob
        fields = "__all__"


class UserFocusCompanySerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(
        read_only=True, format="%Y-%m-%d %H:%M:%S")
    company_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    size_name = serializers.SerializerMethodField()
    quality_name = serializers.SerializerMethodField()

    def get_company_name(self, obj):
        return obj.company.name

    def get_city_name(self, obj):
        return obj.company.city.name

    def get_size_name(self, obj):
        return obj.company.size.name

    def get_quality_name(self, obj):
        return obj.company.quality.name

    class Meta:
        model = UserFocusCompany
        fields = "__all__"
