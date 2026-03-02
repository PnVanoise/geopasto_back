from datetime import date
from django.test import TestCase

from alpages.models import (
    QuartierPasto, SituationDExploitation, Exploiter, Ruche,
    Eleveur, Elever, AbriDUrgence, Commodite, AbriDUrgenceCommodite
)


class ModelsSmokeTest(TestCase):

    def test_create_basic_models_and_relations(self):
        quartier = QuartierPasto.objects.create(id_quartier=10, code_quartier='Q10', nom_quartier='Q10')
        orig = SituationDExploitation.objects.create(
            id_situation=10, nom_situation='S10', situation_active=True, date_debut=date(2020, 1, 1)
        )

        Exploiter.objects.create(id_exploiter=10, quartier=quartier, situation_exploitation=orig, date_debut=date(2020,1,1))
        ruche = Ruche.objects.create(id_ruche=10, description='R10', geometry='POINT(0 0)', situation_exploitation=orig)

        eleveur = Eleveur.objects.create(id_eleveur=10, nom_eleveur='E10')
        Elever.objects.create(id_elever=10, situation_exploitation=orig, type_cheptel=None, eleveur=eleveur, nombre_animaux=1, pension='P')

        abri = AbriDUrgence.objects.create(id_abri_urgence=10, description='A10', etat='OK')
        commod = Commodite.objects.create(id_commodite=10, description='C10')
        AbriDUrgenceCommodite.objects.create(id_abri_urgence_commodite=10, abri_urgence=abri, commodite=commod, etat='OK')

        # Simple assertions
        self.assertEqual(QuartierPasto.objects.count(), 1)
        self.assertEqual(SituationDExploitation.objects.count(), 1)
        self.assertEqual(orig.ruches.count(), 1)
        self.assertEqual(orig.exploitations.count(), 1)
        self.assertEqual(Elever.objects.filter(situation_exploitation=orig).count(), 1)
        self.assertEqual(abri.commodites.count(), 1)
