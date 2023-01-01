from compounds.serializers import CompoundCalculatedSerializer
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from reactions.filters import ReactionCompoundFilterSet, ReactionFilterSet
from reactions.models import Reaction, ReactionCompound
from reactions.serializers import ReactionCompoundSerializer, ReactionRequestSerializer, ReactionSerializer
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class ReactionViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReactionFilterSet
    ordering_fields = "__all__"
    ordering = ["name"]
    serializer_class = ReactionSerializer
    queryset = Reaction.objects.all()

    @extend_schema(
        request=ReactionRequestSerializer,
        responses=CompoundCalculatedSerializer(many=True),
    )
    @action(detail=False, methods=["post"])
    def simulate(self, request):
        serializer = ReactionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        reaction = data.pop("reaction")

        return Response(reaction.calculate_chemical_reaction(**data))


class ReactionCompoundViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReactionCompoundFilterSet
    ordering_fields = "__all__"
    ordering = ["compound", "reaction"]
    serializer_class = ReactionCompoundSerializer
    queryset = ReactionCompound.objects.all()
