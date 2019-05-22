from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import JobMap, JobPoint,FareCloud
from .filters import JobsMapFilter, JobsPointFilter,FareCloudFilter
from .serializers import JobsMapSerializer, JobsPointSerializer,FareCloudSerializer

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
    queryset = JobPoint.objects.all()
    serializer_class = JobsPointSerializer
    pagination_class = FareCloudPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = JobsPointFilter


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
