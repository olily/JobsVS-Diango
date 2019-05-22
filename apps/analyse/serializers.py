from rest_framework import serializers
from .models import JobMap, JobPoint,FareCloud


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
