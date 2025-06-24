from collections import namedtuple
from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from psycopg2.extras import NamedTupleCursor

from patbati.bati.models import (
    Bati,
    Nomenclature,
    NomenclatureType,
    Travaux,
    DemandeTravaux,
    Equipement,
    ElementPaysager,
    Illustration,
    AuteurPhoto,
    DocumentAttache,
    Perspective
)


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
        Nomenclature.objects.get(label=label, id_type__code=code_id_type)
    except Nomenclature.DoesNotExist as e:
        print(f"Not found for {label}- type {code_id_type} ")


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
            sqlquery = "SELECT * FROM patbati.identification"
            cursor.execute(sqlquery)
            result = namedtuplefetchall(cursor)
            for r in result:
                print(r.valide)

                bati = Bati(
                    valide=r.valide,
                    classe=get_nomenclature(r.codeclasse, "CL_ARCHI"),
                    faitage=get_nomenclature(r.codefaitage, "FAITAGE"),
                    appelation=r.appelation,
                    indivision=r.indivision,
                    proprietaire=r.proprietaire,
                    cadastre=r.cadastre,
                    lieu_dit=r.lieu_dit,
                    altitude=r.altitude,
                    situation_geo=r.situationgeo,
                    denivelle=r.denivelle,
                    # todo secteur dans ref_geo,
                    exposition=get_nomenclature(r.exposition, "EXPO"),
                    pente=r.pente,
                    capacite=r.capacite,
                    date_insert=r.date_insert,
                    date_update=r.date_update,
                    bat_suppr=r.bat_suppr,
                    notepatri=get_nomenclature(r.notepatri, "NOTE_PAT"),
                    patrimonialite=r.patrimonialite,
                    conservation=get_nomenclature(r.codeconservation, "CONSERVATION"),
                    ancien_index=r.indexbatiment,
                    masques=get_nomenclature(r.info_masque, "MASQUE"),
                    commentaire_masque=r.info_masque,
                    remarque_risque=r.info_risquenat,
                    geom=r.the_geom,
                    remarque_generale=r.remarques,
                )
                bati.save()

                # get risques
                # les nomenclatures doivent êtres remplies
                risque_query = """
                    SELECT * FROM patbati.rel_risquenat rel
                    JOIN patbati.bib_risquenat bib USING(coderisque)
                    WHERE indexbatiment = %s
                """
                cursor.execute(risque_query,  [r.indexbatiment])
                risques = namedtuplefetchall(cursor)
                bati.risques_nat.set(
                    [get_nomenclature(risque.risque, 'RISQUE') for risque in risques]
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
                    travaux_sql = (
                        "SELECT * FROM patbati.travaux where indexdemande = %s"
                    )
                    cursor.execute(travaux_sql, [dem.indexdemande])
                    travaux = namedtuplefetchall(cursor)
                    for tr in travaux:
                        travaux = Travaux(
                            demande=demande,
                            date=tr.date_travaux,
                            usage=get_nomenclature(tr.codeusage, "USAGE_TRAVAUX"),
                            nature=get_nomenclature(tr.codenature, "NATURE_TRAVAUX"),
                            autorisation=tr.autorisation,
                            subvention_pne=tr.subvention_pne,
                        )
                        travaux.save()

                # EQUIPEMENTS
                equipements_sql = (
                    "SELECT * FROM patbati.demande where indexbatiment = %s"
                )
                cursor.execute(equipements_sql, [r.indexbatiment])
                equipements = namedtuplefetchall(cursor)
                for eq in equipements:
                    equipement = Equipement(
                        bati=bati,
                        type=get_nomenclature(eq.codeequipement, "TYPE_EQUIP"),
                        conservation=get_nomenclature(
                            eq.codeconservation, "CONSERVATION"
                        ),
                        commentaire=eq.info_equip,
                        est_remarquable=eq.equipement_rem,
                    )
                    equipement.save()

                # ELEMENTS PAYSAGERS
                elmt_paysage_sql = (
                    "SELECT * FROM patbati.elements_paysagers where indexbatiment = %s"
                )
                cursor.execute(elmt_paysage_sql, [r.indexbatiment])
                elements_paysagers = namedtuplefetchall(cursor)
                for el in elements_paysagers:
                    element = ElementPaysager(
                        bati=bati,
                        conservation=get_nomenclature(
                            el.codeconservation, "CONSERVATION"
                        ),
                        type=get_nomenclature(el.codeep, "ELEM_PAYS"),
                        commentaire=el.info_ep,
                        est_remarquable=el.ep_rem

                    )
                    element.save()

                
                illustrations_sql = (
                    "SELECT * FROM patbati.illustration ill JOIN patbati.bib_personnes USING(codepersonne) where indexbatiment = %s"
                )
                cursor.execute(illustrations_sql, [r.indexbatiment])
                illustrations = namedtuplefetchall(cursor)
                for ill in illustrations:
                    auteur = AuteurPhoto.objects.get(nom__contains=r.personne)
                    illustration = Illustration(
                        bati=bati,
                        auteur=auteur,
                        # TODO convertir les binaires en fichiers
                        fichier_src="test",
                        date=ill.date_illustration,
                        indexjaris=ill.indexjaris
                    )
                    illustration.save()

                # Documents attachés 
                documents_sql = (
                    "SELECT * FROM patbati.documents where indexbatiment = %s"
                )
                cursor.execute(documents_sql, [r.indexbatiment])
                documents = namedtuplefetchall(cursor)
                for doc in documents:
                    document = DocumentAttache(
                        bati=bati,
                        fichier_src=doc.fichier_source,
                        date=doc.date_document
                    )
                    document.save()


                # PERSPECTIVES
                perspectives_sql = (
                    "SELECT * FROM patbati.rel_ident_perspective where indexbatiment = %s"
                )
                cursor.execute(perspectives_sql, [r.indexbatiment])
                perspectives = namedtuplefetchall(cursor)
                for r in perspectives:
                    persp = Perspective(
                        bati=bati,
                        perspective=get_nomenclature(r.codeperspective, "PERSP")
                    )
                    persp.save()




# TODO : rel_matfins_finition, rel_matge_meo, rel_protection, rel_recommande, rel_remplace, rel_so_mat_fins, rel_structures_matfin, rel_masque

 




