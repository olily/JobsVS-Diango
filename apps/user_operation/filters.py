from django_filters import rest_framework
import django_filters
from .models import UserCollectJob, UserFocusCompany


class UserCollectJobFilter(rest_framework.FilterSet):
    job__name = django_filters.CharFilter(lookup_expr="icontains")
    job__company__name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = UserCollectJob
        fields = ['job__name', 'user', 'job', 'job__company__name']


class UserFocusCompanyFilter(rest_framework.FilterSet):
    company__name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = UserFocusCompany
        fields = ['user', 'company', 'company__name']
