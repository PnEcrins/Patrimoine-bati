# Application Patrimoine bati



## Installation

TODO


#### Référentiel géographique

L'application doit être connecté à un reférentiel géographique pour afficher et filtrer les zonages intersectées (communes, sites d'interêt etc...). L'application est fournie avec un app django (`zoning`) qui s'appuie sur deux tables `l_areas` et `bib_areas_type`. Django s'attend a les trouver dans le schéma public. 
Pour le déploiement en production on crée un schéma `ref_geo` en FDW vers la base de référentiel, puis on crée des vues dans le schéma public pour les besoins de l'application : 

    CREATE VIEW public.bib_areas_types AS 
    SELECT * FROM ref_geo.bib_areas_types;

    CREATE VIEW public.l_areas AS 
    SELECT * FROM ref_geo.l_areas;


#### Mise à jour des permissions : 

Mapentity implémente des permissions supplémentaires aux permissions de Django. De plus la permission "view" est appelé "read" dans mapentity.
Lancer cette commande pour avoir toutes les permissions disponible dans mapentity : 

    python manage.py update_permissions_mapentity