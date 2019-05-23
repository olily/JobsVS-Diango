from django_filters import rest_framework
import django_filters
from .models import JobMap, JobPoint, FareCloud, CompanyMap, CompanyHot


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


class CompanyMapFilter(rest_framework.FilterSet):
    class Meta:
        model = CompanyMap
        fields = ["city"]


class CompanyHotFilter(rest_framework.FilterSet):
    class Meta:
        model = CompanyHot
        fields = ["industries", "quality"]
