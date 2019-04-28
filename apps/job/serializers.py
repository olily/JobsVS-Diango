from rest_framework import serializers
from .models import Jobs, JobFunctions


class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = "__all__"


class JobFunctionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobFunctions
        fields = "__all__"
