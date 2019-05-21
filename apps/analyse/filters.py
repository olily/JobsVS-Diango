from django_filters import rest_framework
import django_filters
from .models import JobMap


class JobsMapFilter(rest_framework.FilterSet):
    class Meta:
        model = JobMap
        fields = ["jobfunction"]
