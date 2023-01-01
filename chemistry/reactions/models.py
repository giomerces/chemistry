from decimal import Decimal
from typing import List

from compounds.models import Compound
from compounds.serializers import CompoundCalculatedSerializer
from core.models import BaseNameMixin, ChemistryModelMixin
from django.db import models
from reactions.models_manager import ReactCompoundQuerySet


class Reaction(ChemistryModelMixin, BaseNameMixin):
    temperature = models.DecimalField(decimal_places=8, max_digits=16)
    pressure = models.DecimalField(decimal_places=8, max_digits=16)
    compounds = models.ManyToManyField(
        "compounds.Compound", through="reactions.ReactionCompound", related_name="reactions"
    )

    def __str__(self):
        return self.name

    @property
    def products(self):
        if not hasattr(self, "_products"):
            self._products = [
                compound for compound in self.compounds.all() if self.participants_stoichiometry.get(compound) > 0
            ]

        return self._products

    @property
    def reagents(self):
        if not hasattr(self, "_reagents"):
            self._reagents = [
                compound for compound in self.compounds.all() if self.participants_stoichiometry.get(compound) < 0
            ]

        return self._reagents

    @property
    def participants_stoichiometry(self):
        if not hasattr(self, "_participants"):
            self._participants = {
                value.compound: value.stoichiometry for value in ReactionCompound.objects.for_reaction(self)
            }
        return self._participants

    def calculate_chemical_reaction(self, **kwargs) -> list:
        method = kwargs.pop("method", "mass")
        if not hasattr(self, f"calculate_based_on_{method}"):
            raise NotImplementedError

        return getattr(self, f"calculate_based_on_{method}")(**kwargs)

    def calculate_based_on_mass(
        self, product: Compound, target_amount: Decimal, origin_coordinates: List[Decimal], **kwargs
    ) -> List[CompoundCalculatedSerializer]:
        initial_mass = self.participants_stoichiometry.get(product) * product.molar_mass
        proportion = target_amount / initial_mass
        required_reagents = CompoundCalculatedSerializer(
            self.reagents,
            many=True,
            context={
                "participants_stoichiometry": self.participants_stoichiometry,
                "proportion": proportion,
                "origin_coordinates": origin_coordinates,
            },
        ).data

        return required_reagents


class ReactionCompound(ChemistryModelMixin):
    compound = models.ForeignKey("compounds.Compound", on_delete=models.CASCADE)
    reaction = models.ForeignKey("reactions.Reaction", on_delete=models.CASCADE)
    stoichiometry = models.DecimalField(decimal_places=8, max_digits=16)

    objects = models.Manager.from_queryset(ReactCompoundQuerySet)()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["compound", "reaction"], name="compound_reaction_unique")]

    def __str__(self):
        return "%s, %s" % (self.compound.name, self.reaction.name)
