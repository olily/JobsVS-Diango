from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import UserCollectJob, UserFocusCompany
from .filters import UserCollectJobFilter, UserFocusCompanyFilter
from .serializers import UserCollectJobSerializer, UserFocusCompanySerializer

# Create your views here.


class UserCollectJobPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100000


class UserFocusCompanyPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100000


class UserCollectJobViewSet(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    queryset = UserCollectJob.objects.all()
    serializer_class = UserCollectJobSerializer
    pagination_class = UserCollectJobPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = UserCollectJobFilter


class UserFocusCompanyViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    queryset = UserFocusCompany.objects.all()
    serializer_class = UserFocusCompanySerializer
    pagination_class = UserFocusCompanyPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = UserFocusCompanyFilter
