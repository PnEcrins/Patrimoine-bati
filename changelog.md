# Changelog

## 11.08.2025 : 2.0.0 

Cette version 2.0.0 marque une refonte complète de l’application Patrimoine Bâti.  
L’application a été entièrement réécrite pour remplacer l’ancienne version.

### Principales nouveautés et changements

- **Migration vers Django**  
  L’application utilise désormais le framework Django.

- **Intégration de Mapentity**  
  Utilisation de Mapentity pour la gestion cartographique, la recherche, les exports et l’interface utilisateur.

- **Refonte des modèles de données**  
  - Les anciennes tables `bib_*` ont été transformées en nomenclatures centralisées.
  - Les modèles principaux (`Bati`, `Travaux`, `Structures`, etc.) ont été repensés et simplifiés notament par l'ajout d'un champ de dâte pour les enquètes

- **Nouveau système d’authentification**  
  - Support du SSO via OpenID Connect (Keycloak, Authlib).
  - Gestion des permissions.

- **Modernisation de l’interface**  
  - Regroupement des onglets pour la page détail d'un bâtiment.
  - Nouvelles vues de détail, listes, formulaires.

- **Gestion avancée des fichiers et images**  
  - Stockage et gestion des pièces jointes et illustrations améliorés

- **Scripts d’import et d’export**  
  - Script pour migrer les anciennes données vers la nouvelle structure.

- **Documentation et déploiement**  
  - Documentation d’installation et de déploiement revue.
  - Support natif pour Gunicorn, systemd et Apache en production.

---

Pour consulter l’ancienne version : [Patrimoine Bâti version 1](https://github.com/PnEcrins/PatBati)

---