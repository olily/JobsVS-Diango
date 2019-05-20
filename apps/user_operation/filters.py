from django_filters import rest_framework
import django_filters
from .models import UserCollectJob, UserFocusCompany


class UserCollectJobFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = UserCollectJob
        fields = ['name', 'user', 'job']


class UserFocusCompanyFilter(rest_framework.FilterSet):
    class Meta:
        model = UserFocusCompany
        fields = ['user', 'company']
