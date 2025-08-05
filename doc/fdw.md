Fonctionnement du référentiel géographique
===========================================

Le référentiel géographique de l'application peut être fourni en FDW par une autre base : 


    CREATE EXTENSION IF NOT EXISTS postgres_fdw;

    # créer un serveur FDW en indiquant les identifiants de connexion
    CREATE SERVER geonaturedbserver FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host '$db_source_host', dbname '$db_source_name', port '$db_source_port');

    # Donner des droit sur le server FDW à l'utilisateur de l'application patbati
    ALTER SERVER geonaturedbserver OWNER TO <USER>;

    # Créer un mapping d'utilisateur entre la base source et destination
    CREATE USER MAPPING FOR $owner_atlas SERVER geonaturedbserver OPTIONS (user '$atlas_source_user', password '$atlas_source_pass') ;

    create schema ref_geo;
    # Créer un schema ref geo pour les table l_area et bib_area_type
    IMPORT FOREIGN SCHEMA ref_geo LIMIT TO (l_areas, bib_areas_types)
    FROM SERVER geonaturedbserver
    INTO ref_geo;