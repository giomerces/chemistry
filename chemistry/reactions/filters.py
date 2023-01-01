from django_filters import CharFilter, FilterSet
from reactions.models import Reaction, ReactionCompound


class ReactionFilterSet(FilterSet):
    name_icontains = CharFilter(field_name="name", lookup_expr=["icontains"])

    class Meta:
        model = Reaction
        fields = ["name_icontains"]

class ReactionCompoundFilterSet(FilterSet):
    compound_icontains = CharFilter(field_name="compound__name", lookup_expr=["icontains"])
    reaction_icontains = CharFilter(field_name="store__name", lookup_expr=["icontains"])

    class Meta:
        model = ReactionCompound
        fields = ["compound_icontains", "reaction_icontains"]