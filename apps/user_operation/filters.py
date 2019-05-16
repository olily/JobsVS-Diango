from django_filters import rest_framework
import django_filters
from .models import UserCollectJob, UserFocusCompany


class UserCollectJobFilter(rest_framework.FilterSet):
    class Meta:
        model = UserCollectJob
        fields = ['user', 'job']


class UserFocusCompanyFilter(rest_framework.FilterSet):
    class Meta:
        model = UserFocusCompany
        fields = ['user', 'company']
