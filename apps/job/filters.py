from django_filters import rest_framework
import django_filters
from .models import Jobs, JobFunctions
from apps.user_operation.models import UserFocusCompany


class JobsFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    salary_low_min = django_filters.NumberFilter("salary_low", lookup_expr='gte')
    salary_high_max = django_filters.NumberFilter("salary_high", lookup_expr='lte')
    work_year_min = django_filters.NumberFilter("work_year", lookup_expr='gte')
    work_year_max = django_filters.NumberFilter("work_year", lookup_expr='lte')
    focuscompany_filter = django_filters.NumberFilter(
        method='focuscompany_Filter', label='focuscompany')

    def focuscompany_Filter(self, queryset, name, value):
        if value == '':
            return queryset.all()
        elif value == 1:
            companies = UserFocusCompany.objects.filter(
                user=self.request.user).values('company')
            return queryset.filter(company__in=companies)

    class Meta:
        model = Jobs
        fields = [
            'name',
            'city',
            'education',
            'salary_low_min',
            'salary_high_max',
            'work_year_min',
            'work_year_max',
            'put_time'
        ]


class JobFunctionsFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = JobFunctions
        fields = ['name']
