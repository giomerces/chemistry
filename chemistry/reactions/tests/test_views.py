from decimal import Decimal

from compounds.models import Compound
from django.test import TestCase
from reactions.models import Reaction, ReactionCompound


class ReactionViewTestCase(TestCase):
    def setUp(self):
        reaction = Reaction(name="Haber-Bosch: Ammonia", temperature=100, pressure=1)
        reaction.save()
        nh3 = Compound.objects.create(
            name="Ammonia",
            formula="NH3",
            boiling_point=100,
            melting_point=0,
            phase_at_room_temperature="L",
            density=1000,
            molar_mass=17,
        )
        h2 = Compound.objects.create(
            name="Hydrogen Gas",
            formula="H2",
            boiling_point=100,
            melting_point=0,
            phase_at_room_temperature="L",
            density=1000,
            molar_mass=2,
        )
        n2 = Compound.objects.create(
            name="Nitrogen Gas",
            formula="N2",
            boiling_point=100,
            melting_point=0,
            phase_at_room_temperature="L",
            density=1000,
            molar_mass=28,
        )
        ReactionCompound(
            compound=n2,
            reaction=reaction,
            stoichiometry=-1,
        ).save()
        ReactionCompound(
            compound=h2,
            reaction=reaction,
            stoichiometry=-3,
        ).save()
        ReactionCompound(
            compound=nh3,
            reaction=reaction,
            stoichiometry=2,
        ).save()

    def test_simulate_reaction(self):
        response = self.client.post(
            "/reactions/reaction/simulate/",
            data={
                "reaction_name": "Haber-Bosch: Ammonia",
                "product_name": "Ammonia",
                "target_amount": 28,
                "origin_coordinates": [45.7597, 4.8422],
            },
        )
        self.assertEqual(response.status_code, 200)
