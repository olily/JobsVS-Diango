from rest_framework import serializers
from .models import UserCollectJob, UserFocusCompany


class UserCollectJobSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(
        read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UserCollectJob
        fields = "__all__"


class UserFocusCompanySerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(
        read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = UserFocusCompany
        fields = "__all__"
