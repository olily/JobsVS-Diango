from rest_framework import serializers
from .models import UserCollectJob, UserFocusCompany, UserFocusIndustry, UserFocusJobFunction


class UserCollectJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCollectJob
        fields = "__all__"


class UserFocusCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFocusCompany
        fields = "__all__"


class UserFocusIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFocusIndustry
        fields = "__all__"


class UserFocusJobFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFocusJobFunction
        fields = "__all__"
