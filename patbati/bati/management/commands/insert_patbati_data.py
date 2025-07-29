import shutil
from argparse import FileType
from datetime import datetime
from collections import namedtuple
from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from psycopg2.extras import NamedTupleCursor
from pathlib import Path


from patbati.bati.models import (
    Bati,
    ClasseArchiNature,
    MateriauGeMiseEnOeuvre,
    MateriauxFinFinition,
    Nomenclature,
    NomenclatureType,
    Travaux,
    DemandeTravaux,
    Equipement,
    ElementPaysager,
    AuteurPhoto,
    Perspective,
    Structure,
    MateriauxFinFinitionStructure,
    SecondOeuvre,
    MateriauxFinFinitionSecondOeuvre,
)
from patbati.mapentitycommon.models import Attachment, License, FileType
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings


def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def namedtuplefetchall(cursor):
    """
    Return all rows from a cursor as a namedtuple.
    Assume the column names are unique.
    """
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def get_nomenclature(label, code_id_type):
    try:
        if label and type(label) is str:
            label = label.strip()
        return Nomenclature.objects.get(label=label, id_type__code=code_id_type)
    except Nomenclature.DoesNotExist as e:
        print(f"Not found for {label} - type {code_id_type} ")

def get_key_from_value(d, target_value):
    for key, value in d.items():
        if value == target_value:
            return key
    return None


class Command(BaseCommand):
    help = "Insert data from historical database"

    def handle(self, *args, **options):
        with connections["default"].cursor() as cursor:
            # PERSONNES
            sqlquery = "SELECT * FROM patbati.bib_personnes"
            cursor.execute(sqlquery)
            result = namedtuplefetchall(cursor)
            for pers in result:
                prenom, nom = pers.personne.split(" ")
                user = AuteurPhoto(
                    nom=nom,
                    prenom=prenom,
                    descriptif=pers.descriptif,
                )
                user.save()
            # BATI
            sqlquery = """
                SELECT * 
                FROM patbati.identification
                JOIN patbati.bib_classe_archi USING(codeclasse)
                LEFT JOIN patbati.bib_faitage USING(codefaitage)
                LEFT JOIN patbati.bib_exposition ON patbati.identification.exposition = patbati.bib_exposition.indexexposition
                LEFT JOIN patbati.bib_notepatri ON patbati.identification.notepatri = patbati.bib_notepatri.indexnotepatri
                LEFT JOIN patbati.bib_conservation USING(codeconservation)
            """
            cursor.execute(sqlquery)
            result = namedtuplefetchall(cursor)
            for r in result:
                bati = Bati(
                    valide=r.valide,
                    classe=get_nomenclature(r.classe, "CL_ARCHI"),
                    faitage=get_nomenclature(r.faitage, "FAITAGE"),
                    appelation=r.appelation,
                    indivision=r.indivision,
                    proprietaire=r.proprietaire,
                    cadastre=r.cadastre,
                    lieu_dit=r.lieu_dit,
                    altitude=r.altitude,
                    situation_geo=r.situationgeo,
                    denivelle=r.denivelle,
                    # todo secteur dans ref_geo,
                    exposition=get_nomenclature(r.nomexposition, "EXPO"),
                    pente=r.pente,
                    capacite=r.capacite,
                    date_insert=r.date_insert,
                    date_update=r.date_update,
                    bat_suppr=r.bat_suppr,
                    notepatri=get_nomenclature(r.valnotepatri, "NOTE_PAT"),
                    patrimonialite=r.patrimonialite,
                    conservation=get_nomenclature(r.conservation, "CONSERVATION"),
                    ancien_index=r.indexbatiment,
                    commentaire_masque=r.info_masque,
                    remarque_risque=r.info_risquenat,
                    geom=r.the_geom,
                    remarque_generale=r.remarques,
                )

                types = {
                    "abri": 598,
                    "hangar": 599,
                    "cabane": 600,
                    "bergerie": 601,
                    "microcentrale": 602,
                    "chalets": 603,
                    "chapelle": 604,
                    "ferme": 606,
                    "gîte": 606,
                    "grange": 607,
                    "maison": 608,
                    "oratoire": 609,
                    "refuge": 610,
                    "ruine": 611,
                }

                found = False
                if r.appelation:
                    app_name = r.appelation.lower()
                    for key, nom_id in types.items():
                        if key in app_name:
                            try:
                                bati.type_bat = Nomenclature.objects.get(
                                    id_nomenclature=nom_id
                                )
                                found = True
                                break
                            except Nomenclature.DoesNotExist:
                                print(f"Nomenclature TYPE_BAT id={nom_id} introuvable")
                if not found:
                    print(f"Aucun type_bat trouvé pour appelation '{r.appelation}'")

                bati.save()

                # get risques
                # les nomenclatures doivent êtres remplies
                risque_query = """
                    SELECT * FROM patbati.rel_risquenat rel
                    JOIN patbati.bib_risquenat bib USING(coderisque)
                    WHERE indexbatiment = %s
                """
                cursor.execute(risque_query, [r.indexbatiment])
                risques = namedtuplefetchall(cursor)
                bati.risques_nat.set(
                    [get_nomenclature(risque.risque, "RISQUE") for risque in risques]
                )

                # # get protection
                # protection_query = """
                #     SELECT * FROM patbati.rel_protection rel
                #     JOIN patbati.bib_protection bib USING(codeprotection)
                #     WHERE indexbatiment = %s
                # """
                # cursor.execute(protection_query, [r.indexbatiment])
                # protections = namedtuplefetchall(cursor)
                # bati.protection.set(
                #     [
                #         get_nomenclature(protection.protection, "PROT")
                #         for protection in protections
                #     ]
                # )

                # masques
                masque_query = """
                    SELECT * FROM patbati.rel_masque rel
                    JOIN patbati.bib_masque bib USING(codemasque)
                    WHERE indexbatiment = %s
                """
                cursor.execute(masque_query, [r.indexbatiment])
                masques = namedtuplefetchall(cursor)
                for masque in masques:
                    bati.masques.set(
                        [
                            get_nomenclature(masque.masque, "MASQUE")
                            for masque in masques
                        ]
                    )

                # Demande de travaux
                dem_travaux_sql = (
                    "SELECT * FROM patbati.demande where indexbatiment = %s"
                )
                cursor.execute(dem_travaux_sql, [r.indexbatiment])
                demandes = namedtuplefetchall(cursor)
                for dem in demandes:
                    demande = DemandeTravaux(
                        bati=bati,
                        demande_dep=dem.demandep,
                        autorisation_p=dem.autorisationp,
                        date_permis=dem.date_permis,
                        date_demande_permis=dem.date_demandep,
                        num_permis=dem.num_permis,
                    )
                    demande.save()

                    # Travaux
                    travaux_sql = """SELECT * FROM patbati.travaux
                            JOIN patbati.bib_nature nat USING (codenature)
                            JOIN patbati.bib_usage us using(codeusage)
                            WHERE indexdemande = %s
                        """
                    cursor.execute(travaux_sql, [dem.indexdemande])
                    travaux = namedtuplefetchall(cursor)
                    for tr in travaux:
                        travaux = Travaux(
                            demande=demande,
                            date=tr.date_travaux or datetime(1800, 1, 1),
                            usage=get_nomenclature(tr.usage, "USAGE_TRAVAUX"),
                            nature=get_nomenclature(tr.nature, "NATURE_TRAVAUX"),
                            autorisation=tr.autorisation,
                            subvention_pne=tr.subvention_pne,
                        )
                        travaux.save()

                # EQUIPEMENTS
                equipements_sql = """SELECT * FROM patbati.equipements 
                        JOIN patbati.bib_conservation USING(codeconservation)
                        JOIN patbati.bib_equipement USING(codeequipement)
                        WHERE indexbatiment = %s
                    """
                cursor.execute(equipements_sql, [r.indexbatiment])
                equipements = namedtuplefetchall(cursor)
                for eq in equipements:
                    equipement = Equipement(
                        bati=bati,
                        type=get_nomenclature(eq.equipement, "EQUIP"),
                        conservation=get_nomenclature(eq.conservation, "CONSERVATION"),
                        commentaire=eq.info_equip,
                        est_remarquable=eq.equipement_rem,
                    )
                    equipement.save()

                # ELEMENTS PAYSAGERS
                elmt_paysage_sql = """SELECT * 
                        FROM patbati.elements_paysagers 
                        JOIN patbati.bib_conservation USING(codeconservation)
                        JOIN patbati.bib_element_paysager USING(codeep)
                        WHERE indexbatiment = %s

                    """
                cursor.execute(elmt_paysage_sql, [r.indexbatiment])
                elements_paysagers = namedtuplefetchall(cursor)
                for el in elements_paysagers:
                    element = ElementPaysager(
                        bati=bati,
                        conservation=get_nomenclature(el.conservation, "CONSERVATION"),
                        type=get_nomenclature(el.elements_paysagers, "ELEM_PAYS"),
                        commentaire=el.info_ep,
                        est_remarquable=el.ep_rem,
                    )
                    element.save()

                # IMAGES
                illustrations_sql = """SELECT * FROM patbati.illustration ill 
                    JOIN patbati.bib_illustration USING (codeillustration)
                    LEFT JOIN patbati.bib_personnes USING(codepersonne) 
                    where indexbatiment = %s
                    """
                cursor.execute(illustrations_sql, [r.indexbatiment])
                illustrations = namedtuplefetchall(cursor)
                
                content_type = ContentType.objects.filter(model="bati").first()
                user = User.objects.filter(username="admin").first()
                nas = Path('/home/leopold/Documents/images')
                paperclip = Path(settings.BASE_DIR + '/media/paperclip/bati_bati')
                
                for ill in illustrations:
                    from PIL import Image
                    fichier_source = Path(ill.fichier_source)
                    (paperclip / str(bati.id)).mkdir(parents=True, exist_ok=True)
                    # Copy original image
                    shutil.copy(nas / ill.fichier_source, paperclip / str(bati.id) / fichier_source)

                    # Create thumbnail
                    thumb_name = fichier_source.stem + ".150x150_q85" + fichier_source.suffix
                    thumb_path = paperclip / str(bati.id) / thumb_name
                    try:
                        if thumb_path.name.endswith("pdf"):
                            continue
                        with Image.open(nas / ill.fichier_source) as img:
                            img.thumbnail((150, 150), Image.LANCZOS)
                            img.save(thumb_path, quality=85)
                    except Exception as e:
                        print(f"Error creating thumbnail for {ill.fichier_source}: {e}")
                    
                    filetype = FileType.objects.filter(type=ill.illustration).first()
                    illustration = Attachment(
                        content_type=content_type,
                        object_id=bati.id,
                        attachment_file=f"paperclip/bati_bati/{bati.id}/{ill.fichier_source}",
                        author="",
                        title="",
                        legend="",
                        starred=False,
                        is_image=True,
                        date_insert=ill.date_illustration,
                        date_update=ill.date_illustration,
                        random_suffix="-",
                        creator=user,
                        filetype=filetype,
                    )

                    # if ill.personne:
                    #     try:
                    #         auteur = AuteurPhoto.objects.get(nom__contains=ill.personne)
                    #         illustration.auteur = auteur
                    #     except AuteurPhoto.DoesNotExist:
                    #         pass
                    illustration.save()

                # DOCUMENTS
                documents_sql = """
                SELECT * 
                FROM patbati.documents doc
                WHERE indexbatiment = %s
                """
                cursor.execute(documents_sql, [r.indexbatiment])
                documents = namedtuplefetchall(cursor)

                docs_nas = Path('/home/leopold/Documents/documents')

                for doc in documents:
                    fichier_source = Path(doc.fichier_source)
                    (paperclip / str(bati.id)).mkdir(parents=True, exist_ok=True)

                    try:
                        import unicodedata

                        normalized_name = unicodedata.normalize('NFKD', fichier_source.name).encode('ASCII', 'ignore').decode('ASCII')
                        dest_filename = normalized_name.lower().replace(" ", "-").replace("..", ".")
                        dest_path = paperclip / str(bati.id) / dest_filename
                        print(dest_filename)
                        shutil.copy(docs_nas / doc.fichier_source, dest_path)

                        pdf = FileType.objects.filter(type="PDF").first()
                        autre = FileType.objects.filter(type="Autre").first()

                        document = Attachment(
                            content_type=content_type,
                            object_id=bati.id,
                            attachment_file=f"paperclip/bati_bati/{bati.id}/{dest_filename}",
                            author="",
                            title="",
                            legend="",
                            starred=False,
                            is_image=True if dest_filename.split(".")[1] == "jpg" else False,
                            date_insert=doc.date_document,     
                            date_update=doc.date_document,
                            random_suffix="-",
                            creator=user,
                            filetype=pdf if dest_filename.split(".")[1] == "pdf" else autre,
                        )
                        document.save()

                    except Exception as e:
                        print(f"Error copying document {doc.fichier_source}: {e}")
                        continue

                # PERSPECTIVES
                perspectives_sql = """SELECT * FROM patbati.rel_ident_perspective 
                        JOIN patbati.bib_perspective USING(codeperspective)
                        where indexbatiment = %s
                    """
                cursor.execute(perspectives_sql, [r.indexbatiment])
                perspectives = namedtuplefetchall(cursor)
                for r in perspectives:
                    persp = Perspective(
                        bati=bati, perspective=get_nomenclature(r.perspective, "PERSP")
                    )
                    persp.save()

                # STRUCTURES
                structure_sql = """
                    SELECT * 
                    FROM patbati.structures 
                    JOIN patbati.bib_conservation USING(codeconservation)
                    JOIN patbati.bib_materiaux_ge USING(codematge)
                    JOIN patbati.bib_meoeuvre USING(codemeo)
                    JOIN patbati.bib_structure USING(codestructure)
                        where indexbatiment = %s
                    """
                cursor.execute(structure_sql, [r.indexbatiment])
                structures = namedtuplefetchall(cursor)
                for struct in structures:
                    structure = Structure(
                        bati=bati,
                        conservation=get_nomenclature(
                            struct.conservation, "CONSERVATION"
                        ),
                        materiaux_principal=get_nomenclature(struct.matge, "MAT_GE"),
                        type=get_nomenclature(struct.structure, "STRUCT"),
                        mise_en_oeuvre=get_nomenclature(struct.meoeuvre, "MEOEUVRE"),
                        info_structure=struct.info_structure,
                        est_remarquable=struct.structure_rem,
                    )
                    structure.save()

                    mat_fin_finition_sql = """
                    SELECT *
                    FROM patbati.rel_structures_matfins
                    JOIN patbati.bib_finition USING(codefinition)
                    JOIN patbati.bib_materiaux_fins USING(codematfins)
                    WHERE indexstructure = %s
                    """

                    cursor.execute(mat_fin_finition_sql, [struct.indexstructure])
                    mat_fins = namedtuplefetchall(cursor)
                    for mat in mat_fins:
                        mat_object = MateriauxFinFinitionStructure(
                            structure=structure,
                            materiaux_fin=get_nomenclature(mat.matfins, "MAT_FIN"),
                            finition=get_nomenclature(mat.finition, "FIN"),
                        )
                        mat_object.save()

                # SECOND OEUVRE
                sql_second_oeuvre = """
                SELECT * 
                FROM patbati.second_oeuvre
                JOIN patbati.bib_conservation USING(codeconservation)
                JOIN patbati.bib_so USING(codeso)
                WHERE indexbatiment = %s
                """
                cursor.execute(sql_second_oeuvre, [r.indexbatiment])
                seconds_oeuvre = namedtuplefetchall(cursor)

                for sec in seconds_oeuvre:
                    second_oeuvre = SecondOeuvre(
                        bati=bati,
                        conservation=get_nomenclature(sec.conservation, "CONSERVATION"),
                        type=get_nomenclature(sec.second_oeuvre, "SO"),
                        commentaire=sec.info_so,
                        est_remarquable=sec.so_rem or False,
                    )
                    second_oeuvre.save()

                    mat_fin_finition_sec_sql = """
                    SELECT *
                    FROM patbati.rel_so_matfins
                    JOIN patbati.bib_finition USING(codefinition)
                    JOIN patbati.bib_materiaux_fins USING(codematfins)
                    WHERE indexso = %s
                    """

                    cursor.execute(mat_fin_finition_sec_sql, [sec.indexso])
                    mat_fins = namedtuplefetchall(cursor)
                    for mat in mat_fins:
                        mat_sec_object = MateriauxFinFinitionSecondOeuvre(
                            second_oeuvre=second_oeuvre,
                            materiaux_fin=get_nomenclature(mat.matfins, "MAT_FIN"),
                            finition=get_nomenclature(mat.finition, "FIN"),
                        )
                        mat_sec_object.save()

            # rel_recommande
            classe_archi_nature_sql = """
                SELECT *
                FROM patbati.rel_recommande
                JOIN patbati.bib_classe_archi USING(codeclasse)
                JOIN patbati.bib_nature USING(codenature)
                """

            cursor.execute(classe_archi_nature_sql)
            results = namedtuplefetchall(cursor)
            for r in results:
                cl_nat_object = ClasseArchiNature(
                    classe = get_nomenclature(r.classe, "CL_ARCHI"),
                    nature = get_nomenclature(r.nature, "NATURE_TRAVAUX"),
                )
                cl_nat_object.save()

            # rel_matfins_finition
            matfins_finition_sql = """
             SELECT *
                FROM patbati.rel_matfins_finition
                JOIN patbati.bib_materiaux_fins USING(codematfins)
                JOIN patbati.bib_finition USING(codefinition)
            """
            
            cursor.execute(matfins_finition_sql)
            results = namedtuplefetchall(cursor)
            for r in results:
                matfin_finition_obj = MateriauxFinFinition(
                    materiaux_fin = get_nomenclature(r.matfins, "MAT_FIN"),
                    finition = get_nomenclature(r.finition, "FIN")
                )

                matfin_finition_obj.save()   

            # rel_matge_meo
            matge_meo_sql = """
             SELECT *
                FROM patbati.rel_matge_meo
                JOIN patbati.bib_materiaux_ge USING(codematge)
                JOIN patbati.bib_meoeuvre USING(codemeo)
            """
            
            cursor.execute(matge_meo_sql)
            results = namedtuplefetchall(cursor)
            for r in results:
                matge_meo_obj = MateriauGeMiseEnOeuvre(
                    materiaux_ge = get_nomenclature(r.matge, "MAT_GE"),
                    mise_en_oeuvre = get_nomenclature(r.meoeuvre, "MEOEUVRE")
                )

                matge_meo_obj.save() 
# TODO :
# enquetes
# images (binaires) et document attaché dans mapentitycommon_attachement
# rel_protection = ref_geo
# rel_remplace = vide
