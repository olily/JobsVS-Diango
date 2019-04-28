from django_filters import rest_framework
import django_filters
from .models import Cities, Provinces


class CitiesFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    province__name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Cities
        fields = ['name', 'province__name']


class ProvincesFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Provinces
        fields = ['name']
