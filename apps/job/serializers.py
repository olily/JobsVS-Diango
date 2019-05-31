from rest_framework import serializers
from .models import Jobs, JobFunctions
from apps.users.models import UserWantJob
from apps.company.models import Industries
from sklearn.metrics.pairwise import cosine_similarity


JobFunctionsDict = {}
for i in range(3, 66):
    jobfunction_ss = JobFunctions.objects.filter(category=i)
    count = jobfunction_ss.count()
    jobfunction_s = jobfunction_ss.first()
    JobFunctionsDict[i] = {
        "first": jobfunction_s.id,
        "count": count
    }

IndustriesDict = {}
for i in range(3, 14):
    indusries_ss = Industries.objects.filter(category=i)
    count = indusries_ss.count()
    indusries_s = indusries_ss.first()
    IndustriesDict[i] = {
        "first": indusries_s.id,
        "count": count
    }


class JobsSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    edu_name = serializers.SerializerMethodField()
    companysize_name = serializers.SerializerMethodField()
    company_image = serializers.SerializerMethodField()
    # result = serializers.SerializerMethodField()

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
    '''
    def get_result(self, obj):
        # userwant = UserWantJob.objects.get(user=self.context['request'].user)

        # 向量计算
        user_education = 7.14
        # user_industry_category = 3
        # user_function_category = 4
        # user_industry = 3 * 20 / 65 + \
        #     (14 - IndustriesDict[user_industry_category]['first']) / IndustriesDict[user_industry_category]['first']
        # user_jobfun = user_function_category * 20 / 11 + \
        #     (72 - JobFunctionsDict[4]['first']) / JobFunctionsDict[user_function_category]['count']
        user_industry = 0.92
        user_jobfun = 7.33
        user_comsize = 6.25
        user_vector = [
            user_education,
            user_comsize,
            user_industry,
            user_jobfun]

        education = obj.education_id * 10 / 7
        comsize = obj.company.size_id * 10 / 8

        industry = 0
        industries = obj.company.industries.all()
        if industries.count() > 0:
            # for industry in industries:
            #     print("迭代去取值")
            #     print(industry)
            industry_f = industries[0]  # 取第一个
            industry_category = industry_f.category_id
            if industry_category == 1:
                industry = 0
            else:
                industry = industry_category * 20 / 65 + (
                    industry_f.id - IndustriesDict[industry_category]['first']) / \
                    IndustriesDict[industry_category]['first']
        jobfun = 0

        jobfunctions = obj.jobfunction.all()
        if jobfunctions.count() > 0:
            jobfunctions_f = jobfunctions[0]  # 取第一个
            function_category = jobfunctions_f.category_id
            if function_category == 67 or function_category == 66 or function_category is None:
                jobfun = 0
            else:
                if function_category == 1:
                    jobfun = 0
                else:
                    jobfun = function_category * 20 / 11 + (
                        jobfunctions_f.id - JobFunctionsDict[function_category]['first']) / \
                        JobFunctionsDict[function_category]['count']

        vector = [education, comsize, industry, jobfun]

        compare = [user_vector, vector]

        cosine = cosine_similarity(compare)
        # print(cosine[0][1])

        return cosine[0][1]
    '''
    class Meta:
        model = Jobs
        fields = "__all__"


class JobFunctionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobFunctions
        fields = "__all__"
