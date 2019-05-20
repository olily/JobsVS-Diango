from django_filters import rest_framework
import django_filters
from .models import Jobs, JobFunctions


class JobsFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    work_year_min = django_filters.NumberFilter("work_year", lookup_expr='gte')
    work_year_max = django_filters.NumberFilter("work_year", lookup_expr='lte')

    class Meta:
        model = Jobs
        fields = [
            'name',
            'city',
            'education',
            'work_year_min',
            'work_year_max'
        ]


class JobFunctionsFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = JobFunctions
        fields = ['name']
