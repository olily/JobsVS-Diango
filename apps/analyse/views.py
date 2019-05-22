from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import JobMap, JobPoint
from .filters import JobsMapFilter, JobsPointFilter
from .serializers import JobsMapSerializer, JobsPointSerializer

# Create your views here.


class JobsMapViewSet(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = JobMap.objects.all()
    serializer_class = JobsMapSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = JobsMapFilter

class CompaniesPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100000


class JobsPointViewSet(mixins.ListModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    queryset = JobPoint.objects.all()
    serializer_class = JobsPointSerializer
    pagination_class = CompaniesPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = JobsPointFilter