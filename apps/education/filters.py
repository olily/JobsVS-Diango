from django_filters import rest_framework
import django_filters
from .models import Education


class EducationFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Education
        fields = ['name']
