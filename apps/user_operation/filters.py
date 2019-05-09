from django_filters import rest_framework
import django_filters
from .models import UserCollectJob, UserFocusCompany


class UserCollectJobFilter(rest_framework.FilterSet):
    user__username = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = UserCollectJob
        fields = ['user__username']


class UserFocusCompanyFilter(rest_framework.FilterSet):
    user__username = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = UserFocusCompany
        fields = ['user__username']
