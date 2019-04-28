from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import UserCollectJob, UserFocusCompany, UserFocusIndustry, UserFocusJobFunction
from .filters import UserCollectJobFilter, UserFocusCompanyFilter, UserFocusIndustryFilter, UserFocusJobFunctionFilter
from .serializers import UserCollectJobSerializer, UserFocusCompanySerializer, UserFocusIndustrySerializer, UserFocusJobFunctionSerializer

# Create your views here.


class UserCollectJobViewSet(mixins.ListModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    queryset = UserCollectJob.objects.all()
    serializer_class = UserCollectJobSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = UserCollectJobFilter


class UserFocusCompanyViewSet(mixins.ListModelMixin,
                              mixins.UpdateModelMixin,
                              viewsets.GenericViewSet):
    queryset = UserFocusCompany.objects.all()
    serializer_class = UserFocusCompanySerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = UserFocusCompanyFilter


class UserFocusIndustryViewSet(mixins.ListModelMixin,
                               mixins.UpdateModelMixin,
                               viewsets.GenericViewSet):
    queryset = UserFocusIndustry.objects.all()
    serializer_class = UserFocusIndustrySerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = UserFocusIndustryFilter


class UserFocusJobFunctionViewSet(mixins.ListModelMixin,
                                  mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):
    queryset = UserFocusJobFunction.objects.all()
    serializer_class = UserFocusJobFunctionSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = UserFocusJobFunctionFilter
