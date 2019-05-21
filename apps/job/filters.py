from django_filters import rest_framework
import django_filters
from .models import Jobs, JobFunctions
from apps.user_operation.models import UserFocusCompany


class JobsFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
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
            'work_year_min',
            'work_year_max',
            'put_time'
        ]


class JobFunctionsFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = JobFunctions
        fields = ['name']
