from datetime import date
from django.test import TestCase

from alpages.models import SituationDExploitation, Commodite, AbriDUrgence, AbriDUrgenceCommodite
from alpages.serializers import SituationDExploitationSerializer, CommoditeSerializer, AbriDUrgenceCommoditeSerializer


class SerializersSmokeTest(TestCase):

    def test_situation_serializer_fields(self):
        s = SituationDExploitation.objects.create(id_situation=20, nom_situation='S20', situation_active=True, date_debut=date(2020,1,1))
        ser = SituationDExploitationSerializer(s)
        data = ser.data
        self.assertIn('id_situation', data)
        self.assertIn('nom_situation', data)

    def test_commodite_serializer(self):
        c = Commodite.objects.create(id_commodite=20, description='C20')
        ser = CommoditeSerializer(c)
        self.assertEqual(ser.data['description'], 'C20')

    def test_abri_commodite_serializer(self):
        a = AbriDUrgence.objects.create(id_abri_urgence=20, description='A20', etat='OK')
        c = Commodite.objects.create(id_commodite=21, description='C21')
        ac = AbriDUrgenceCommodite.objects.create(id_abri_urgence_commodite=20, abri_urgence=a, commodite=c, etat='OK')
        ser = AbriDUrgenceCommoditeSerializer(ac)
        self.assertIn('abri_urgence_description', ser.data)
        self.assertIn('commodite_desc', ser.data)
