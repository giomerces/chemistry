from compounds.models import Compound, Store
from rest_framework import serializers


class BaseMetaSerializer(serializers.ModelSerializer):
    fields = "__all__"


class CompoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compound
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"
