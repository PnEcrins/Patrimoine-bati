import csv
from django.db import migrations


def import_nomenclaturetype_from_csv(apps, schema_editor):
    NomenclatureType = apps.get_model("bati", "NomenclatureType")
    csv_path = "csv/bib_nomenclatures_types_202506231336.csv"

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            NomenclatureType.objects.update_or_create(
                id_type=int(row["id_type"]),
                defaults={
                    "label": row["label"],
                    "definition": row["definition"],
                    "code": row["code"],
                },
            )


def import_nomenclatures_from_csv(apps, schema_editor):
    Nomenclature = apps.get_model("bati", "Nomenclature")
    csv_path = "csv/t_nomenclatures_202506231428.csv"

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            label = row["label"]
            if label and type(label) is str:
                label = label.strip()
            Nomenclature.objects.update_or_create(
                id_nomenclature=int(row["id_nomenclature"]),
                defaults={
                    "id_type_id": int(row["id_type"]),
                    "label": label,
                    "description": row.get("description", "") or None,
                    "parentId": int(row["parentid"]) if row.get("parentid") else None,
                },
            )


class Migration(migrations.Migration):

    dependencies = [
        ("bati", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(import_nomenclaturetype_from_csv),
        migrations.RunPython(import_nomenclatures_from_csv),
    ]
