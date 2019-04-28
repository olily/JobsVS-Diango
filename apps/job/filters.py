from django_filters import rest_framework
import django_filters
from .models import Jobs, JobFunctions


class JobsFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Jobs
        fields = ['name']


class JobFunctionsFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = JobFunctions
        fields = ['name']
