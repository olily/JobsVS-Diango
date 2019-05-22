from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import JobMap,JobFunctions,JobPoint
from .filters import JobsMapFilter,JobsPointFilter
from .serializers import JobsMapSerializer,JobsPointSerializer

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

class JobsPointViewSet(mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset = JobPoint.objects.all()
    serializer_class = JobsMapSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = JobsPointFilter

