from rest_framework import serializers
from .models import UserCollectJob, UserFocusCompany


class UserCollectJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCollectJob
        fields = "__all__"


class UserFocusCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFocusCompany
        fields = "__all__"
