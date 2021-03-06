from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Jobs, JobFunctions
from .filters import JobsFilter, JobFunctionsFilter
from .serializers import JobsSerializer, JobFunctionsSerializer
from rest_framework_extensions.cache.mixins import CacheResponseMixin


# Create your views here.

class JobsPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100000
class JobsViewSet(mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  CacheResponseMixin,
                  viewsets.GenericViewSet):
    # queryset = Jobs.objects.order_by('?')
    queryset = Jobs.objects.all()
    serializer_class = JobsSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    pagination_class = JobsPagination
    filter_class = JobsFilter


class JobFunctionsViewSet(mixins.ListModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    queryset = JobFunctions.objects.order_by('?')
    serializer_class = JobFunctionsSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = JobFunctionsFilter
