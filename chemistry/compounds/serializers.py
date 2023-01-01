from compounds.models import Compound, CompoundStore, Store
from rest_framework import serializers


class CompoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compound
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


class CompoundStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompoundStore
        fields = "__all__"


class CompoundCalculatedSerializer(serializers.ModelSerializer):
    required_mass = serializers.SerializerMethodField(method_name="_required_mass")
    better_deal = serializers.SerializerMethodField(method_name="_better_deal")

    class Meta:
        model = Compound
        fields = ["name", "required_mass", "better_deal"]

    def _required_mass(self, obj) -> str:
        participants_stoichiometry = self.context.get("participants_stoichiometry")
        proportion = self.context.get("proportion")
        mass = participants_stoichiometry.get(obj) * obj.molar_mass

        return "%.2f" % (mass * proportion)

    def _better_deal(self, obj) -> dict:
        participants_stoichiometry = self.context.get("participants_stoichiometry")
        proportion = self.context.get("proportion")
        mass = participants_stoichiometry.get(obj) * obj.molar_mass
        origin_coordinates = self.context.get("origin_coordinates")
        return obj.search_min_cost_for_unit_of_mass(amount=mass * proportion, origin_coordinates=origin_coordinates)
