![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
[![Django](https://img.shields.io/badge/Django-5.2-success)](https://www.djangoproject.com/)
[![Mapentity](https://img.shields.io/badge/Mapentity-12.8.3-success)](https://github.com/makinacorpus/django-mapentity)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://www.postgresql.org/)
[![Last Commit](https://img.shields.io/github/last-commit/PnEcrins/Patrimoine-bati)](https://github.com/PnEcrins/Patrimoine-batu/commits/main)
[![Issues](https://img.shields.io/github/issues/PnEcrins/Patrimoine-bati)](https://github.com/PnEcrins/Patrimoine-bati/issues)

# Application Patrimoine bati

## Installation :

Avant d’installer l’application, il est nécessaire d’installer les bibliothèques nécéssaires avec le script suivant :

```bash
bash install_deps.sh
```

Créer la base de données PostgreSQL (vous pouvez choisir le nom que vous souhaitez, par exemple patbati) :

```SQL
CREATE DATABASE patbati;
```

Créer l'extension postgis dans la BDD :

```SQL
CREATE EXTENSION postgis;
```

Créer et activer un environnement virtuel Python :

```bash
python3 -m venv venv
source venv/bin/activate
```

Installer les dépendances Python du projet :

```bash
pip install -r requirements.txt
```

Configurer la base de données PostgreSQL (utilisateur, base, droits).

Configurer le fichier `settings_local.py` à partir de `settings_local.example.py` :

```bash
cp patbati/settings_local.example.py patbati/settings_local.py
```

Adaptez les paramètres (base de données, chemins, SSO, etc.) dans `settings_local.py`.

Effectuer les migrations de la base de données :

```bash
python manage.py migrate
```

Créer un superutilisateur Django :

```bash
python manage.py createsuperuser
```

Lancer le serveur de développement :

```bash
python manage.py runserver
```

## Deploiement prod :

Installer gunicorn

```bash
pip install gunicorn
```

Configurer un service systemd pour gunicorn (voir documentation Django/gunicorn).

Regroupez tous les fichiers statiques à un seul endroit :
```bash
python manage.py collectstatic
```

Modifiez les paramètres dans `settings_local.py` :
```bash
ALLOWED_HOSTS = ["myhost"]
CSRF_TRUSTED_ORIGINS = ["http://myhost"]
```

*Créer un service systemd*

Copiez et adaptez le fichier d’exemple `patbati.service` dans `/etc/systemd/system/patbati.service`

**N'oubliez pas de créer le dossier de logs et de donner les droits à l'utilisateur utilisé par le service :**

```bash
sudo mkdir -p /var/log/patbati
sudo chown <USER>:<USER> /var/log/patbati
```

Activez et démarrez le service :

```bash
sudo systemctl daemon-reload
sudo systemctl enable patbati.service
sudo systemctl start patbati.service
```

Le service est maintenant démarré !


*Configurer Apache*

      apt install apache2
      a2enmod proxy
      a2enmod proxy_http

Créez une configuration dans `/etc/apache2/sites-available` :

      <VirtualHost *:80>
		#ServerName <SERVER_NAME>

		Alias "/static/" "/var/www/html/patbati/static/"
		<Directory "/var/www/html/patbati/static/">
			Require all granted
		</Directory>

		Alias "/media/" /var/www/html/patbati/media/"
		<Directory "/var/www/html/patbati/media/">
		Require all granted
		</Directory>

		<Location "/">
			ProxyPass http://127.0.0.1:8000/
			ProxyPassReverse http://127.0.0.1:8000/
			ProxyPreserveHost On
		</Location>

		<Location "/static">
			ProxyPass !
		</Location>
      </VirtualHost>


#### Référentiel géographique : 

L'application doit être connectée à un référentiel géographique pour afficher et filtrer les zonages intersectés (communes, sites d'intérêt, etc.). L'application est fournie avec une app django (`zoning`) qui s'appuie sur deux tables `l_areas` et `bib_areas_type`. Django s'attend à les trouver dans le schéma public.  
Pour le déploiement en production, on crée un schéma `ref_geo` en FDW (voir doc/fdw.md) vers la base de référentiel, puis on crée des vues dans le schéma public pour les besoins de l'application : 

```sql
CREATE VIEW public.bib_areas_types AS 
SELECT * FROM ref_geo.bib_areas_types;

CREATE VIEW public.l_areas AS 
SELECT * FROM ref_geo.l_areas;
```

#### Mise à jour des permissions : 

Mapentity implémente des permissions supplémentaires aux permissions de Django. De plus, la permission "view" est appelée "read" dans mapentity.
Lancer cette commande pour avoir toutes les permissions disponibles dans mapentity : 

```bash
python manage.py update_permissions_mapentity
```

## Développement : 

Installer les dépendances de tests : 

```bash
pip install -r requirements-dev.in
```

Lancer les tests : 

```bash
python manage.py tests
```

## Configuration : 

Configurer les paramètres de la base de données dans le `settings_local.py`.

Possibilité d'utiliser le SSO avec OpenIDConnect et Authlib dans `settings_local.py` :

- Changer `SSO_LOGIN_ENABLED = True`
- Remplir le `CLIENT_ID`, `CLIENT_SECRET`, `SSO_ENDPOINT` de votre Identity and Access Management
