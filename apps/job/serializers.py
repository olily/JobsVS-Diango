from rest_framework import serializers
from .models import Jobs, JobFunctions
from apps.users.models import UserWantJob
from apps.company.models import Industries
from sklearn.metrics.pairwise import cosine_similarity


JobFunctionsDict = {}
for i in range(3,66):
    jobfunction_ss = JobFunctions.objects.filter(category=i)
    count = jobfunction_ss.count()
    jobfunction_s = jobfunction_ss.first()
    JobFunctionsDict[i]={
        "first":jobfunction_s.id,
        "count":count
    }
# print(JobFunctionsDict)
IndustriesDict = {}
for i in range(3,12):
    indusries_ss = Industries.objects.filter(category=i)
    count = indusries_ss.count()
    indusries_s = indusries_ss.first()
    IndustriesDict[i]={
        "first":indusries_s.id,
        "count":count
    }
# print(IndustriesDict)


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
        # print(self.context['request'].user)
        userwant = UserWantJob.objects.get(user=self.context['request'].user)

        #向量计算
        user_education = userwant.want_education_id * 10/7
        user_industry_category = userwant.want_industry.category_id
        user_function_category = userwant.want_jobfunction.category_id
        user_industry = user_industry_category *20/65+(userwant.want_industry_id-IndustriesDict[user_industry_category]['first'])/IndustriesDict[user_industry_category]['first']
        user_jobfun = user_function_category *20/11 + (userwant.want_jobfunction_id-JobFunctionsDict[user_function_category]['first'])/JobFunctionsDict[user_function_category]['count']

        user_comsize = userwant.want_companysize_id * 10/8

        # print(education,industry_category,industry,comsize,jobfun)

        # user_vector = []
        user_vector=[user_education,user_comsize,user_industry,user_jobfun]


        education = obj.education_id * 10/7
        comsize = obj.company.size_id * 10/8

        # print(obj.company.id)
        # print(obj.company.industries)
        # print(obj.company.industries.all())
        industries = obj.company.industries.all()
        if industries.count() > 0:


            print(">0")
            industry = industries[0] # 取第一个
            print(industry)
            print(industry.id)

            for industry in industries:
                print("迭代去取值")
                print(industry)


        industry_category = obj.company.industries.category_id
        function_category = obj.jobfunction.category_id
        industry = industry_category * 20 / 65 + (
                obj.company.industries_id - IndustriesDict[industry_category]['first']) / \
                        IndustriesDict[industry_category]['first']
        jobfun = function_category * 20 / 11 + (
                obj.jobfunction.category_id - JobFunctionsDict[function_category]['first']) / \
                      JobFunctionsDict[function_category]['count']

        vector = [education,comsize,industry,jobfun]

        compare = [user_vector,vector]

        cosine= cosine_similarity(compare)
        print(cosine[0][1])

        return cosine[0][1]

    class Meta:
        model = Jobs
        fields = "__all__"


class JobFunctionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobFunctions
        fields = "__all__"
