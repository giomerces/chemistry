from compounds.models import Compound
from reactions.models import Reaction, ReactionCompound
from rest_framework import serializers


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = "__all__"


class ReactionCompoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReactionCompound
        fields = "__all__"


class ReactionRequestSerializer(serializers.Serializer):
    method = serializers.CharField(required=False)
    reaction_name = serializers.CharField()
    product_name = serializers.CharField()
    target_amount = serializers.DecimalField(max_digits=16, decimal_places=8)
    origin_coordinates = serializers.ListField(
        child=serializers.DecimalField(max_digits=16, decimal_places=8), min_length=2, max_length=2
    )

    def validate(self, attrs):
        ret = super().validate(attrs)
        reaction_name = attrs["reaction_name"]
        product_name = attrs["product_name"]

        try:
            reaction = Reaction.objects.get(name=reaction_name)
            ret["reaction"] = reaction
        except Reaction.DoesNotExist:
            raise serializers.ValidationError({"name": f"Reaction {reaction_name} is not registered on database."})

        try:
            product = Compound.objects.get(name=product_name)
            ret["product"] = product
        except Compound.DoesNotExist:
            raise serializers.ValidationError({"name": f"Product {product_name} is not registered on database."})

        if product not in reaction.products:
            raise serializers.ValidationError({"name": f"{product_name} is not a product of {reaction_name} reaction."})

        return ret

    class Meta:
        fields = ["method", "reaction_name", "product_name", "target_amount"]