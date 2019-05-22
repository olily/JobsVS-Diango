from django_filters import rest_framework
import django_filters
from .models import JobMap, JobPoint, JobFunctions,FareCloud


class JobsMapFilter(rest_framework.FilterSet):
    class Meta:
        model = JobMap
        fields = ["jobfunction"]


class JobsPointFilter(rest_framework.FilterSet):
    class Meta:
        model = JobPoint
        fields = ["jobfunction"]


class FareCloudFilter(rest_framework.FilterSet):
    class Meta:
        model = FareCloud
        fields = ["jobfunction"]
