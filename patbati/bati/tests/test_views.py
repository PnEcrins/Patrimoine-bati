from django.http import HttpRequest
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from patbati.bati.models import (
    Bati, DemandeTravaux, Travaux, Nomenclature, NomenclatureType,
    Structure, MateriauxFinFinitionStructure, SecondOeuvre,
    MateriauxFinFinitionSecondOeuvre, Perspective, Enquetes
)
from patbati.bati.views import (
    BatiDetail, BatiList, BatiFormat, BatiViewSet,
    EnquetesCreate, EnquetesUpdate, EnquetesDelete,
    PerspectiveCreate, PerspectiveUpdate, PerspectiveDelete,
    DemandeTravauxCreate, DemandeTravauxUpdate, DemandeTravauxDelete,
    TravauxCreate, StructureFinitionCreate, StructureFinitionUpdate, StructureFinitionDelete,
    SecondOeuvreCreate, SecondOeuvreUpdate, SecondOeuvreDelete,
    SecondOeuvreFinitionCreate, SecondOeuvreFinitionUpdate, SecondOeuvreFinitionDelete,
    BatiDocumentPdfPublic, BatiDocumentPdfDetail
)
from patbati.bati.forms import BatiForm


class BatiDetailViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        ntype = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        nom = Nomenclature.objects.create(id_type=ntype, label="TYPE_BAT_label")
        self.bati = Bati.objects.create(appelation="Test", type_bat=nom, classe=nom)
        self.demande = DemandeTravaux.objects.create(
            bati=self.bati,
            demande_dep=True,
            autorisation_p=True,
            date_permis="2025-01-01",
            date_demande_permis="2024-12-01",
            num_permis="12345"
        )
        self.travaux = Travaux.objects.create(
            date="2025-02-01",
            demande=self.demande,
            usage=nom,
            nature=nom,
            autorisation=True,
            subvention_pne=1000
        )

    def test_get_context_data_sorts_demandes_and_travaux(self):
        view = BatiDetail()
        request = self.factory.get(f"/bati/{self.bati.pk}/")
        request.user = AnonymousUser()
        view.request = request
        view.object = self.bati
        view.kwargs = {"pk": self.bati.pk}
        context = view.get_context_data()
        self.assertEqual(context["mapwidth"], "90%")
        self.assertIn("demandes_travaux_sorted", context)
        demandes_travaux_sorted = context["demandes_travaux_sorted"]
        self.assertTrue(len(demandes_travaux_sorted) > 0)
        demande, travaux_sorted = demandes_travaux_sorted[0]
        self.assertEqual(demande, self.demande)
        self.assertEqual(list(travaux_sorted)[0], self.travaux)

class BatiListViewTest(TestCase):
    def setUp(self):
        ntype = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        nom = Nomenclature.objects.create(id_type=ntype, label="TYPE_BAT_label")
        self.bati = Bati.objects.create(appelation="Test", type_bat=nom, classe=nom)

    def test_list_columns(self):
        view = BatiList()
        self.assertIn("appelation", view.columns)
        self.assertIn("secteurs", view.columns)
        self.assertIn("appelation", view.searchable_columns)
        
class BatiCreateViewTest(TestCase):
    def setUp(self):
        # Create all needed NomenclatureTypes
        types = {}
        for code in [
            "TYPE_BAT", "CL_ARCHI", "IMPLA", "FAITAGE", "EXPO", "NOTE_PAT",
            "CONSERVATION", "MASQUE", "PERSP"
        ]:
            types[code], _ = NomenclatureType.objects.get_or_create(label=code, code=code)
        noms = {}
        for code, typ in types.items():
            noms[code] = Nomenclature.objects.create(id_type=typ, label=f"{code}_label")

        # Create ManyToMany objects
        masque = noms["MASQUE"]
        perspective = noms["PERSP"]

        self.data = {
            "appelation": "Bâtiment A",
            "type_bat": noms["TYPE_BAT"].pk,
            "classe": noms["CL_ARCHI"].pk,
            "implantation": noms["IMPLA"].pk,
            "faitage": noms["FAITAGE"].pk,
            "indivision": True,
            "proprietaire": "Alice",
            "cadastre": "CadA",
            "lieu_dit": "LieuA",
            "altitude": 123.4,
            "x": 1.1,
            "y": 2.2,
            "situation_geo": "SituA",
            "denivelle": 10.5,
            "exposition": noms["EXPO"].pk,
            "pente": 15.0,
            "capacite": 100.0,
            "bat_suppr": False,
            "notepatri": noms["NOTE_PAT"].pk,
            "patrimonialite": "PatriA",
            "ancien_index": 1.23,
            "conservation": noms["CONSERVATION"].pk,
            "commentaire_masque": "MasqueA",
            "remarque_risque": "RisqueA",
            "geom": "POINT(1 2)",
            "remarque_generale": "RemarqueA",
            "masques": [masque.pk],
            "perspectives": [perspective.pk],
        }

    def test_create_form(self):
        form = BatiForm(data=self.data)
        print(form.errors)
        self.assertTrue(form.is_valid())
        
class BatiFormatViewTest(TestCase):
    def test_format_inherits(self):
        view = BatiFormat()
        self.assertTrue(hasattr(view, "columns"))

class BatiViewSetTest(TestCase):
    def setUp(self):
        ntype = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        nom = Nomenclature.objects.create(id_type=ntype, label="TYPE_BAT_label")
        self.bati = Bati.objects.create(appelation="Test", type_bat=nom, classe=nom)

    def test_viewset_queryset(self):
        viewset = BatiViewSet()
        self.assertEqual(viewset.queryset.count(), Bati.objects.count())
        self.assertEqual(viewset.get_view_perm(), "bati.view_bati")

class EnquetesViewTest(TestCase):
    def setUp(self):
        ntype = NomenclatureType.objects.create(label="PERSONNES", code="PERSONNES")
        nom = Nomenclature.objects.create(id_type=ntype, label="PERSONNES_label")
        ntype_bat = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        nom_bat = Nomenclature.objects.create(id_type=ntype_bat, label="TYPE_BAT_label")
        self.bati = Bati.objects.create(appelation="Test", type_bat=nom_bat, classe=nom_bat)
        self.enquete = Enquetes.objects.create(personne=nom, bati=self.bati)

    def test_enquetes_create(self):
        view = EnquetesCreate()
        self.assertEqual(view.model, Enquetes)
        self.assertEqual(view.parent_model, Bati)
        self.assertEqual(view.form_class.__name__, "EnquetesForm")

    def test_enquetes_update(self):
        view = EnquetesUpdate()
        self.assertEqual(view.model, Enquetes)
        self.assertEqual(view.parent_model, Bati)

    def test_enquetes_delete(self):
        view = EnquetesDelete()
        self.assertEqual(view.model, Enquetes)
        self.assertEqual(view.parent_model, Bati)

class PerspectiveViewTest(TestCase):
    def setUp(self):
        ntype = NomenclatureType.objects.create(label="PERSP", code="PERSP")
        nom = Nomenclature.objects.create(id_type=ntype, label="PERSP_label")
        ntype_bat = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        nom_bat = Nomenclature.objects.create(id_type=ntype_bat, label="TYPE_BAT_label")
        self.bati = Bati.objects.create(appelation="Test", type_bat=nom_bat, classe=nom_bat)
        self.perspective = Perspective.objects.create(perspective=nom, bati=self.bati)

    def test_perspective_create(self):
        view = PerspectiveCreate()
        self.assertEqual(view.model, Perspective)
        self.assertEqual(view.parent_model, Bati)

    def test_perspective_update(self):
        view = PerspectiveUpdate()
        self.assertEqual(view.model, Perspective)
        self.assertEqual(view.parent_model, Bati)

    def test_perspective_delete(self):
        view = PerspectiveDelete()
        self.assertEqual(view.model, Perspective)
        self.assertEqual(view.parent_model, Bati)

class DemandeTravauxViewTest(TestCase):
    def setUp(self):
        ntype = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        nom = Nomenclature.objects.create(id_type=ntype, label="TYPE_BAT_label")
        self.bati = Bati.objects.create(appelation="Test", type_bat=nom, classe=nom)
        self.demande = DemandeTravaux.objects.create(
            bati=self.bati,
            demande_dep=True,
            autorisation_p=True,
            date_permis="2025-01-01",
            date_demande_permis="2024-12-01",
            num_permis="12345"
        )

    def test_demande_create(self):
        view = DemandeTravauxCreate()
        self.assertEqual(view.model, DemandeTravaux)
        self.assertEqual(view.parent_model, Bati)

    def test_demande_update(self):
        view = DemandeTravauxUpdate()
        self.assertEqual(view.model, DemandeTravaux)
        self.assertEqual(view.parent_model, Bati)

    def test_demande_delete(self):
        view = DemandeTravauxDelete()
        self.assertEqual(view.model, DemandeTravaux)
        self.assertEqual(view.parent_model, Bati)

class TravauxViewTest(TestCase):
    def setUp(self):
        ntype = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        nom = Nomenclature.objects.create(id_type=ntype, label="TYPE_BAT_label")
        self.bati = Bati.objects.create(appelation="Test", type_bat=nom, classe=nom)
        self.demande = DemandeTravaux.objects.create(
            bati=self.bati,
            demande_dep=True,
            autorisation_p=True,
            date_permis="2025-01-01",
            date_demande_permis="2024-12-01",
            num_permis="12345"
        )
        self.travaux = Travaux.objects.create(
            date="2025-02-01",
            demande=self.demande,
            usage=nom,
            nature=nom,
            autorisation=True,
            subvention_pne=1000
        )

    def test_dispatch_sets_demande(self):
        view = TravauxCreate()
        request = HttpRequest()
        request.user = AnonymousUser()
        request.method = "GET"
        view.request = request
        kwargs = {"pk": self.demande.pk, "parent_pk": self.demande.pk}
        view.dispatch(request, **kwargs)
        self.assertEqual(view.demande, self.demande)
        self.assertEqual(view.parent_object, self.demande)

    def test_form_valid_sets_demande(self):
        view = TravauxCreate()
        view.demande = self.demande
        view.parent_object = self.bati
        class DummyForm:
            instance = Travaux()
            def save(self):
                return self.instance
        result = view.form_valid(DummyForm())
        self.assertEqual(DummyForm.instance.demande, self.demande)

    def test_get_context_data_includes_demande(self):
        view = TravauxCreate()
        view.demande = self.demande
        view.parent_object = self.bati
        view.object = self.travaux
        request = HttpRequest()
        request.user = AnonymousUser()
        view.request = request
        context = view.get_context_data()
        self.assertIn("demande", context)
        self.assertEqual(context["demande"], self.demande)

    def test_get_success_url_returns_bati_url(self):
        view = TravauxCreate()
        view.demande = self.demande
        url = view.get_success_url()
        self.assertEqual(url, self.bati.get_detail_url())
        
class StructureFinitionViewTest(TestCase):
    def setUp(self):
        ntype = NomenclatureType.objects.create(label="STRUCT", code="STRUCT")
        nom = Nomenclature.objects.create(id_type=ntype, label="STRUCT_label")
        ntype_bat = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        nom_bat = Nomenclature.objects.create(id_type=ntype_bat, label="TYPE_BAT_label")
        self.bati = Bati.objects.create(appelation="Test", type_bat=nom_bat, classe=nom_bat)
        self.structure = Structure.objects.create(
            bati=self.bati,
            conservation=nom,
            materiaux_principal=nom,
            type=nom,
            mise_en_oeuvre=nom,
            info_structure="Info",
            est_remarquable=True
        )
        self.mff_structure = MateriauxFinFinitionStructure.objects.create(
            structure=self.structure,
            materiaux_fin=nom,
            finition=nom
        )

    def test_structure_finition_create(self):
        view = StructureFinitionCreate()
        self.assertEqual(view.model, MateriauxFinFinitionStructure)
        self.assertEqual(view.parent_model, Structure)

    def test_structure_finition_update(self):
        view = StructureFinitionUpdate()
        self.assertEqual(view.model, MateriauxFinFinitionStructure)
        self.assertEqual(view.parent_model, Structure)

    def test_structure_finition_delete(self):
        view = StructureFinitionDelete()
        self.assertEqual(view.model, MateriauxFinFinitionStructure)
        self.assertEqual(view.parent_model, Structure)

class SecondOeuvreViewTest(TestCase):
    def setUp(self):
        ntype = NomenclatureType.objects.create(label="SO", code="SO")
        nom = Nomenclature.objects.create(id_type=ntype, label="SO_label")
        ntype_bat = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        nom_bat = Nomenclature.objects.create(id_type=ntype_bat, label="TYPE_BAT_label")
        self.bati = Bati.objects.create(appelation="Test", type_bat=nom_bat, classe=nom_bat)
        self.second_oeuvre = SecondOeuvre.objects.create(
            bati=self.bati,
            type=nom,
            conservation=nom,
            commentaire="Commentaire",
            est_remarquable=True
        )

    def test_second_oeuvre_create(self):
        view = SecondOeuvreCreate()
        self.assertEqual(view.model, SecondOeuvre)
        self.assertEqual(view.parent_model, Bati)

    def test_second_oeuvre_update(self):
        view = SecondOeuvreUpdate()
        self.assertEqual(view.model, SecondOeuvre)
        self.assertEqual(view.parent_model, Bati)

    def test_second_oeuvre_delete(self):
        view = SecondOeuvreDelete()
        self.assertEqual(view.model, SecondOeuvre)
        self.assertEqual(view.parent_model, Bati)

class SecondOeuvreFinitionViewTest(TestCase):
    def setUp(self):
        ntype = NomenclatureType.objects.create(label="SO", code="SO")
        nom = Nomenclature.objects.create(id_type=ntype, label="SO_label")
        ntype_bat = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        nom_bat = Nomenclature.objects.create(id_type=ntype_bat, label="TYPE_BAT_label")
        self.bati = Bati.objects.create(appelation="Test", type_bat=nom_bat, classe=nom_bat)
        self.second_oeuvre = SecondOeuvre.objects.create(
            bati=self.bati,
            type=nom,
            conservation=nom,
            commentaire="Commentaire",
            est_remarquable=True
        )
        self.mff_second_oeuvre = MateriauxFinFinitionSecondOeuvre.objects.create(
            second_oeuvre=self.second_oeuvre,
            materiaux_fin=nom,
            finition=nom
        )

    def test_second_oeuvre_finition_create(self):
        view = SecondOeuvreFinitionCreate()
        self.assertEqual(view.model, MateriauxFinFinitionSecondOeuvre)
        self.assertEqual(view.parent_model, SecondOeuvre)

    def test_second_oeuvre_finition_update(self):
        view = SecondOeuvreFinitionUpdate()
        self.assertEqual(view.model, MateriauxFinFinitionSecondOeuvre)
        self.assertEqual(view.parent_model, SecondOeuvre)

    def test_second_oeuvre_finition_delete(self):
        view = SecondOeuvreFinitionDelete()
        self.assertEqual(view.model, MateriauxFinFinitionSecondOeuvre)
        self.assertEqual(view.parent_model, SecondOeuvre)

class BatiDocumentPdfPublicTest(TestCase):
    def test_pdf_public_template(self):
        view = BatiDocumentPdfPublic()
        self.assertEqual(view.template_name, "bati/bati_public_pdf.html")
        self.assertEqual(view.model, Bati)

class BatiDocumentPdfDetailTest(TestCase):
    def test_pdf_detail_template(self):
        view = BatiDocumentPdfDetail()
        self.assertEqual(view.template_name, "bati/bati_detail_pdf.html")
        self.assertEqual(view.model, Bati)

class StructureFinitionCreateViewTest(TestCase):
    def setUp(self):
        ntype = NomenclatureType.objects.create(label="STRUCT", code="STRUCT")
        nom = Nomenclature.objects.create(id_type=ntype, label="STRUCT_label")
        ntype_bat = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        nom_bat = Nomenclature.objects.create(id_type=ntype_bat, label="TYPE_BAT_label")
        self.bati = Bati.objects.create(appelation="Test", type_bat=nom_bat, classe=nom_bat)
        self.structure = Structure.objects.create(
            bati=self.bati,
            conservation=nom,
            materiaux_principal=nom,
            type=nom,
            mise_en_oeuvre=nom,
            info_structure="Info",
            est_remarquable=True
        )

    def test_dispatch_sets_structure(self):
        view = StructureFinitionCreate()
        request = HttpRequest()
        request.user = AnonymousUser()
        request.method = "GET"
        view.request = request
        kwargs = {"structure_pk": self.structure.pk, "parent_pk": self.structure.pk}
        view.dispatch(request, **kwargs)
        self.assertEqual(view.structure, self.structure)

    def test_form_valid_sets_structure(self):
        view = StructureFinitionCreate()
        view.structure = self.structure
        view.parent_object = self.structure 
        class DummyForm:
            instance = MateriauxFinFinitionStructure()
            def save(self):
                return self.instance
        view.form_valid(DummyForm())
        self.assertEqual(DummyForm.instance.structure, self.structure)

    def test_get_success_url_returns_structure_url(self):
        view = StructureFinitionCreate()
        view.object = MateriauxFinFinitionStructure(structure=self.structure)
        url = view.get_success_url()
        self.assertEqual(url, self.structure.get_detail_url())

class StructureFinitionUpdateViewTest(TestCase):
    def setUp(self):
        ntype = NomenclatureType.objects.create(label="STRUCT", code="STRUCT")
        nom = Nomenclature.objects.create(id_type=ntype, label="STRUCT_label")
        ntype_bat = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        nom_bat = Nomenclature.objects.create(id_type=ntype_bat, label="TYPE_BAT_label")
        self.bati = Bati.objects.create(appelation="Test", type_bat=nom_bat, classe=nom_bat)
        self.structure = Structure.objects.create(
            bati=self.bati,
            conservation=nom,
            materiaux_principal=nom,
            type=nom,
            mise_en_oeuvre=nom,
            info_structure="Info",
            est_remarquable=True
        )
        self.mff_structure = MateriauxFinFinitionStructure.objects.create(
            structure=self.structure,
            materiaux_fin=nom,
            finition=nom
        )

    def test_dispatch_sets_structure(self):
        view = StructureFinitionUpdate()
        request = HttpRequest()
        request.user = AnonymousUser()
        request.method = "GET"
        view.request = request
        kwargs = {
            "structure_pk": self.structure.pk,
            "parent_pk": self.structure.pk,
            "pk": self.mff_structure.pk,
        }
        view.kwargs = kwargs
        view.dispatch(request, **kwargs)
        self.assertEqual(view.structure, self.structure)

    def test_form_valid_sets_structure(self):
        view = StructureFinitionUpdate()
        view.structure = self.structure
        view.parent_object = self.structure
        class DummyForm:
            instance = MateriauxFinFinitionStructure()
            def save(self):
                return self.instance
        view.form_valid(DummyForm())
        self.assertEqual(DummyForm.instance.structure, self.structure)

    def test_get_success_url_returns_structure_url(self):
        view = StructureFinitionUpdate()
        view.object = MateriauxFinFinitionStructure(structure=self.structure)
        url = view.get_success_url()
        self.assertEqual(url, self.structure.get_detail_url())


class SecondOeuvreFinitionCreateViewTest(TestCase):
    def setUp(self):
        ntype = NomenclatureType.objects.create(label="SO", code="SO")
        nom = Nomenclature.objects.create(id_type=ntype, label="SO_label")
        ntype_bat = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        nom_bat = Nomenclature.objects.create(id_type=ntype_bat, label="TYPE_BAT_label")
        self.bati = Bati.objects.create(appelation="Test", type_bat=nom_bat, classe=nom_bat)
        self.second_oeuvre = SecondOeuvre.objects.create(
            bati=self.bati,
            type=nom,
            conservation=nom,
            commentaire="Commentaire",
            est_remarquable=True
        )

    def test_dispatch_sets_second_oeuvre(self):
        view = SecondOeuvreFinitionCreate()
        request = HttpRequest()
        request.user = AnonymousUser()
        request.method = "GET"
        view.request = request
        kwargs = {"second_pk": self.second_oeuvre.pk, "parent_pk": self.second_oeuvre.pk}
        view.dispatch(request, **kwargs)
        self.assertEqual(view.second_oeuvre, self.second_oeuvre)

    def test_form_valid_sets_second_oeuvre(self):
        view = SecondOeuvreFinitionCreate()
        view.second_oeuvre = self.second_oeuvre
        view.parent_object = self.second_oeuvre
        class DummyForm:
            instance = MateriauxFinFinitionSecondOeuvre()
            def save(self):
                return self.instance
        view.form_valid(DummyForm())
        self.assertEqual(DummyForm.instance.second_oeuvre, self.second_oeuvre)

    def test_get_success_url_returns_second_oeuvre_url(self):
        view = SecondOeuvreFinitionCreate()
        view.object = MateriauxFinFinitionSecondOeuvre(second_oeuvre=self.second_oeuvre)
        url = view.get_success_url()
        self.assertEqual(url, self.second_oeuvre.get_detail_url())

class SecondOeuvreFinitionUpdateViewTest(TestCase):
    def setUp(self):
        ntype = NomenclatureType.objects.create(label="SO", code="SO")
        nom = Nomenclature.objects.create(id_type=ntype, label="SO_label")
        ntype_bat = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        nom_bat = Nomenclature.objects.create(id_type=ntype_bat, label="TYPE_BAT_label")
        self.bati = Bati.objects.create(appelation="Test", type_bat=nom_bat, classe=nom_bat)
        self.second_oeuvre = SecondOeuvre.objects.create(
            bati=self.bati,
            type=nom,
            conservation=nom,
            commentaire="Commentaire",
            est_remarquable=True
        )
        self.mff_second_oeuvre = MateriauxFinFinitionSecondOeuvre.objects.create(
            second_oeuvre=self.second_oeuvre,
            materiaux_fin=nom,
            finition=nom
        )

    def test_dispatch_sets_second_oeuvre(self):
        view = SecondOeuvreFinitionUpdate()
        request = HttpRequest()
        request.user = AnonymousUser()
        request.method = "GET"
        view.request = request
        kwargs = {
            "second_pk": self.second_oeuvre.pk,
            "parent_pk": self.second_oeuvre.pk,
            "pk": self.mff_second_oeuvre.pk,
        }
        view.kwargs = kwargs
        view.dispatch(request, **kwargs)
        self.assertEqual(view.second_oeuvre, self.second_oeuvre)

    def test_form_valid_sets_second_oeuvre(self):
        view = SecondOeuvreFinitionUpdate()
        view.second_oeuvre = self.second_oeuvre
        view.parent_object = self.second_oeuvre
        class DummyForm:
            instance = MateriauxFinFinitionSecondOeuvre()
            def save(self):
                return self.instance
        view.form_valid(DummyForm())
        self.assertEqual(DummyForm.instance.second_oeuvre, self.second_oeuvre)

    def test_get_success_url_returns_second_oeuvre_url(self):
        view = SecondOeuvreFinitionUpdate()
        view.object = MateriauxFinFinitionSecondOeuvre(second_oeuvre=self.second_oeuvre)
        url = view.get_success_url()
        self.assertEqual(url, self.second_oeuvre.get_detail_url())
