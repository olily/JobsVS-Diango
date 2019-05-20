from django_filters import rest_framework
import django_filters
from .models import Industries, CompanyQuality, CompanySize, Companies


class IndustriesFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Industries
        fields = ['name']


class CompanyQualityFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = CompanyQuality
        fields = ['name']


class CompanySizeFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = CompanySize
        fields = ['name']


class CompaniesFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Companies
        fields = ['name', 'size', 'quality', 'city']
