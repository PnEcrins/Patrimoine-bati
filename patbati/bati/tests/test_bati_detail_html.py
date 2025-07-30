import datetime
from django.test import TestCase
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from patbati.bati.models import (
    Bati, Nomenclature, NomenclatureType,
    Enquetes, DemandeTravaux, Travaux, Structure,
    MateriauxFinFinitionStructure, SecondOeuvre,
    MateriauxFinFinitionSecondOeuvre, Equipement,
    ElementPaysager, Perspective
)

User = get_user_model()


class BatiDetailHTMLTest(TestCase):

    with open("patbati/bati/templates/bati/bati_detail.html") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    def test_tab_panes_exist(self):
        for pane_id in ["enq-pers", "travaux", "structure"]:
            self.assertIsNotNone(
                self.soup.find("div", {"id": pane_id}),
                f"Tab pane '{pane_id}' not found in HTML"
            )

    def test_nav_links(self):
        nav_links = self.soup.select("a.nav-link")
        self.assertTrue(any("Travaux" in link.text for link in nav_links))
        self.assertTrue(any("Gros et Second Oeuvre" in link.text for link in nav_links))
        self.assertTrue(any("Perspectives et Enquetes" in link.text for link in nav_links))
        self.assertTrue(any("Zonage" in link.text for link in nav_links))

    def test_perspectives_table_headers(self):
        pane = self.soup.find("div", {"id": "enq-pers"})
        self.assertIsNotNone(pane)
        table = pane.find("table", class_="table table-striped")
        self.assertIsNotNone(table)
        headers = [th.text.strip() for th in table.find_all("th")]
        expected = ["Date", "Perspective", "Actions"]
        for h in expected:
            self.assertIn(h, headers)

    def test_enquetes_table_headers(self):
        pane = self.soup.find("div", {"id": "enq-pers"})
        self.assertIsNotNone(pane)
        tables = pane.find_all("table", class_="table table-striped")
        self.assertTrue(len(tables) >= 2)
        enq_table = tables[1]
        headers = [th.text.strip() for th in enq_table.find_all("th")]
        expected = ["Personne", "Date enquête", "Date rédaction", "Actions"]
        for h in expected:
            self.assertIn(h, headers)

    def test_empty_state_enquetes(self):
        pane = self.soup.find("div", {"id": "enq-pers"})
        self.assertIsNotNone(pane)
        enq_table = pane.find_all("table", class_="table table-striped")[1]
        self.assertIn("Aucune enquête associée", enq_table.text)

    def test_travaux_header_row(self):
        pane = self.soup.find("div", {"id": "travaux"})
        self.assertIsNotNone(pane)
        header_row = pane.find("div", class_="row font-weight-bold border-bottom pb-2 mb-2")
        self.assertIsNotNone(header_row)
        expected = [
            "Permis", "Date demande", "Autorisation", "Date permis", "Numéro", "Actions"
        ]
        for h in expected:
            self.assertIn(h, header_row.text)

    def test_travaux_empty_state(self):
        pane = self.soup.find("div", {"id": "travaux"})
        self.assertIsNotNone(pane)
        self.assertIn("Aucune demande", pane.text)

    def test_travaux_accordion_structure(self):
        pane = self.soup.find("div", {"id": "travaux"})
        self.assertIsNotNone(pane)
        accordion = pane.find("div", {"id": "demandesAccordion"})
        self.assertIsNotNone(accordion)
        self.assertTrue("accordion" in accordion.get("class", []) or accordion.get("id") == "demandesAccordion")

    def test_travaux_table_headers(self):
        pane = self.soup.find("div", {"id": "travaux"})
        self.assertIsNotNone(pane)
        accordion = pane.find("div", {"id": "demandesAccordion"})
        table = accordion.find("table", class_="table table-sm table-bordered mb-0 text-center")
        if table:
            headers = [th.text.strip() for th in table.find_all("th")]
            expected = [
                "Date des travaux", "Autorisation du parc", "Subvention accordée",
                "Nature des Travaux", "Nouvel usage", "Actions"
            ]
            for h in expected:
                self.assertIn(h, headers)

    def test_travaux_empty_state_for_travaux(self):
        pane = self.soup.find("div", {"id": "travaux"})
        self.assertIsNotNone(pane)
        accordion = pane.find("div", {"id": "demandesAccordion"})
        if accordion:
            self.assertTrue(
                "Aucun travaux pour cette demande" in accordion.text or
                "Aucun travaux pour cette demande." in accordion.text
            )

    def test_structure_section_exists(self):
        pane = self.soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        self.assertIn("Liste des structures", pane.text)
        self.assertIn("Liste des éléments de second oeuvre", pane.text)

    def test_structure_empty_state(self):
        pane = self.soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        self.assertIn("Aucune structure", pane.text)
        self.assertIn("Aucun élément de second oeuvre", pane.text)

    def test_structure_table_headers(self):
        pane = self.soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        tables = pane.find_all("table", class_="table table-sm table-bordered mb-2")
        if tables:
            headers = [th.text.strip() for th in tables[0].find_all("th")]
            self.assertIn("Description de la structure", headers)
            self.assertIn("Structure", tables[0].text)
            self.assertIn("Structure remarquable", tables[0].text)
            self.assertIn("Conservation", tables[0].text)
            self.assertIn("Matériau principal", tables[0].text)
            self.assertIn("Mise en oeuvre", tables[0].text)
            self.assertIn("Commentaire", tables[0].text)

    def test_structure_finitions_table_headers(self):
        pane = self.soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        tables = pane.find_all("table", class_="table table-sm table-bordered mb-0")
        if tables:
            headers = [th.text.strip() for th in tables[0].find_all("th")]
            self.assertIn("Matériau fin", headers)
            self.assertIn("Finition", headers)
            self.assertIn("Actions", headers)

    def test_second_oeuvre_table_headers(self):
        pane = self.soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        tables = pane.find_all("table", class_="table table-sm table-bordered mb-2")
        if len(tables) > 1:
            headers = [th.text.strip() for th in tables[1].find_all("th")]
            self.assertIn("Description de l'élément", headers)
            self.assertIn("Catégorie", tables[1].text)
            self.assertIn("Remarquable", tables[1].text)
            self.assertIn("Conservation", tables[1].text)
            self.assertIn("Commentaire", tables[1].text)

    def test_second_oeuvre_finitions_table_headers(self):
        pane = self.soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        tables = pane.find_all("table", class_="table table-sm table-bordered mb-0")
        if len(tables) > 1:
            headers = [th.text.strip() for th in tables[1].find_all("th")]
            self.assertIn("Matériau fin", headers)
            self.assertIn("Finition", headers)
            self.assertIn("Actions", headers)

    def test_plus_icons_present(self):
        plus_icons = self.soup.select("i.bi-plus")
        self.assertTrue(len(plus_icons) > 0)

    def test_pencil_icons_present(self):
        pencil_icons = self.soup.select("i.bi-pencil")
        self.assertTrue(len(pencil_icons) > 0 or len(self.soup.select("i.bi-pencil-square")) > 0)

    def test_trash_icons_present(self):
        trash_icons = self.soup.select("i.bi-trash")
        self.assertTrue(len(trash_icons) > 0)

    def test_chevron_icons_present(self):
        chevron_icons = self.soup.select("i.bi-chevron-down")
        self.assertTrue(len(chevron_icons) > 0)

    def test_traverse_dom(self):
        tables = self.soup.find_all("table", class_="table-striped")
        found = False
        for table in tables:
            if table.find_parent("div", class_="mb-3") or table.find_parent("div", class_="card-body"):
                found = True
                break
        self.assertTrue(found)

User = get_user_model()

class BatiListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('testuser', 'test@example.com', 'password')
        # Create needed NomenclatureTypes and Nomenclatures
        ntype = NomenclatureType.objects.create(label="NOTE_PAT", code="NOTE_PAT")
        note_nomenclature = Nomenclature.objects.create(id_type=ntype, label="5")
        typebat_type = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        typebat_nom = Nomenclature.objects.create(id_type=typebat_type, label="TYPE_BAT_label")
        class_type = NomenclatureType.objects.create(label="CL_ARCHI", code="CL_ARCHI")
        class_nom = Nomenclature.objects.create(id_type=class_type, label="CL_ARCHI_label")

        # filled bati
        self.bati1 = Bati.objects.create(
            appelation="TestBati",  # str
            type_bat=typebat_nom,   # FK
            classe=class_nom,       # FK
            notepatri=note_nomenclature,  # int
            indivision=True,        # bool
            date_insert=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),  # date
            geom=Point(1.23, 4.56), # point
        )        

        # empty bati
        self.bati2 = Bati.objects.create(
            appelation="",  # empty string
            type_bat=typebat_nom,
            classe=class_nom,
            notepatri=None,  # empty int/float (FK)
            indivision=None,  # empty bool
            date_insert=None,  # empty date
            geom=Point(0, 0),
        )

    def test_bati_list_html_structure(self):
        self.client.force_login(self.user)
        response = self.client.get('/bati/list/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content)

        table = soup.find("table")
        self.assertIsNotNone(table)

        headers = [th.text.strip().lower() for th in table.find_all("th")]
        expected_headers = [
            "id", "validé", "appelation", "type bat", "notepatri",
            "conservation", "secteur"
        ]
        for header in expected_headers:
            self.assertIn(header, headers)

    def test_bati_detail_attributes_fields(self):
        self.client.force_login(self.user)
        response = self.client.get(f'/bati/{self.bati1.pk}/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content)

        # String field
        nom_td = soup.find("th", {"data-qa": "nom"}).find_next("td")
        self.assertIn("TestBati", nom_td.text)

        # Integer/float field
        valeur_patri = soup.find("th", {"data-qa": "valeurPat"}).find_next("td")
        self.assertIn("5", valeur_patri.text)

        # Boolean field
        indiv_td = soup.find("th", {"data-qa": "indiv"}).find_next("td")
        self.assertIn("Oui", indiv_td.text)

        # Date field
        date_td = soup.find("th", {"data-qa": "date"}).find_next("td")
        self.assertIn("2024", date_td.text)


    def test_bati_detail_attributes_empty_states(self):
        self.client.force_login(self.user)
        response = self.client.get(f'/bati/{self.bati2.pk}/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content)

        # empty str
        nom_td = soup.find("th", {"data-qa": "nom"}).find_next("td")
        self.assertIn(str(self.bati2), nom_td.text)

        # empty int
        valeur_patri = soup.find("th", {"data-qa": "valeurPat"}).find_next("td")
        self.assertEqual(valeur_patri.text.strip(), "-")

        # empty bool
        indivision = soup.find("th", {"data-qa": "indiv"}).find_next("td")
        self.assertEqual(indivision.text, "Non") # default for empty bool is Non

        # empty date
        date_td = soup.find("th", {"data-qa": "date"}).find_next("td")
        self.assertEqual(date_td.text.strip(), "-")