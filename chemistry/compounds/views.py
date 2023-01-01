from compounds.filters import CompoundFilterSet, CompoundStoreFilterSet, StoreFilterSet
from compounds.models import Compound, CompoundStore, Store
from compounds.serializers import CompoundSerializer, CompoundStoreSerializer, StoreSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet


class CompoundViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CompoundFilterSet
    ordering_fields = "__all__"
    ordering = ["name"]
    serializer_class = CompoundSerializer
    queryset = Compound.objects.all()


class StoreViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = StoreFilterSet
    ordering_fields = "__all__"
    ordering = ["name"]
    serializer_class = StoreSerializer
    queryset = Store.objects.all()


class CompoundStoreViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CompoundStoreFilterSet
    ordering_fields = "__all__"
    ordering = ["compound", "store"]
    serializer_class = CompoundStoreSerializer
    queryset = CompoundStore.objects.all()
