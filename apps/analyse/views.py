from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import JobMap, JobPoint, FareCloud, CompanyHot, CompanyMap, CompanyParallel
from .filters import JobsMapFilter, JobsPointFilter, FareCloudFilter, CompanyHotFilter, CompanyMapFilter, \
    CompanyParallelFilter
from .serializers import JobsMapSerializer, JobsPointSerializer, FareCloudSerializer, CompanyHotSerializer, \
    CompanyMapSerializer, CompanyParallelSerializer

# Create your views here.


class MapsPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100000


class JobsMapViewSet(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = JobMap.objects.all()
    serializer_class = JobsMapSerializer
    pagination_class = MapsPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = JobsMapFilter


class FareCloudPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100000


class FareCloudViewSet(mixins.ListModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    queryset = FareCloud.objects.all()
    serializer_class = FareCloudSerializer
    pagination_class = FareCloudPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = FareCloudFilter


class PointsPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100000


class JobsPointViewSet(mixins.ListModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    queryset = JobPoint.objects.all()
    serializer_class = JobsPointSerializer
    pagination_class = PointsPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = JobsPointFilter


class CompanyHotPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100000


class CompanyHotViewSet(mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    queryset = CompanyHot.objects.all()
    serializer_class = CompanyHotSerializer
    pagination_class = PointsPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = CompanyHotFilter


class CompanyMapPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100000


class CompanyMapViewSet(mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    queryset = CompanyMap.objects.all()
    serializer_class = CompanyMapSerializer
    pagination_class = CompanyMapPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = CompanyMapFilter


class CompanyParallelPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 1000000


class CompanyParallelViewSet(mixins.ListModelMixin,
                             mixins.UpdateModelMixin,
                             viewsets.GenericViewSet):
    queryset = CompanyParallel.objects.all()
    serializer_class = CompanyParallelSerializer
    pagination_class = CompanyParallelPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = CompanyParallelFilter
