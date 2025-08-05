# Application Patrimoine bati



## Installation

python3-pip python3-venv libpq-dev python3-dev binutils libproj-dev gdal-bin
libjpeg62 zlib1g-dev libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
postgresql-15-postgis-3
desampler le settings_local

TODO : tout mettre dans le settings_local

creer l'extension postgis dans la BDD
create extension postgis;


## Deploiement prod

Installer gunicorn

pip install gunicorn

#### Référentiel géographique

L'application doit être connecté à un reférentiel géographique pour afficher et filtrer les zonages intersectées (communes, sites d'interêt etc...). L'application est fournie avec un app django (`zoning`) qui s'appuie sur deux tables `l_areas` et `bib_areas_type`. Django s'attend a les trouver dans le schéma public. 
Pour le déploiement en production on crée un schéma `ref_geo` en FDW (voic doc/fdw.md) vers la base de référentiel, puis on crée des vues dans le schéma public pour les besoins de l'application : 

    CREATE VIEW public.bib_areas_types AS 
    SELECT * FROM ref_geo.bib_areas_types;

    CREATE VIEW public.l_areas AS 
    SELECT * FROM ref_geo.l_areas;


#### Mise à jour des permissions : 

Mapentity implémente des permissions supplémentaires aux permissions de Django. De plus la permission "view" est appelé "read" dans mapentity.
Lancer cette commande pour avoir toutes les permissions disponible dans mapentity : 

    python manage.py update_permissions_mapentity


## Développement

Installer les dépendances de tests : 

    pip install -r requirements-dev.in

Lancer les tests : 

    python manage.py tests