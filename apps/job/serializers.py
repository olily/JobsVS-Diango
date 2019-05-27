from rest_framework import serializers
from .models import Jobs, JobFunctions
from apps.users.models import UserWantJob


class JobsSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    edu_name = serializers.SerializerMethodField()
    companysize_name = serializers.SerializerMethodField()
    company_image = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()

    def get_company_name(self, obj):
        return obj.company.name

    def get_city_name(self, obj):
        return obj.city.name

    def get_edu_name(self, obj):
        return obj.education.name

    def get_companysize_name(self, obj):
        return obj.company.size.name

    def get_company_image(self, obj):
        return obj.company.img_url

    def get_result(self, obj):
        print(self.context['request'].user)
        userwant = UserWantJob.objects.get(user=self.context['request'].user)

        #筛选字段
        print("want_city", userwant.want_city_id)
        print("want_salary_low", userwant.want_salary_low)
        print("want_salary_high", userwant.want_salary_high)

        #向量计算

        print("want_education", userwant.want_education_id)
        print("want_workyear", userwant.want_workyear_id)
        print("want_city", userwant.want_city_id)
        print("want_industry", userwant.want_industry_id)
        print("want_jobfunction", userwant.want_jobfunction_id)

        print("want_companysize", userwant.want_companysize_id)
        return 0

    class Meta:
        model = Jobs
        fields = "__all__"


class JobFunctionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobFunctions
        fields = "__all__"
