# Installation geopasto_backend
## Synchronisation avec le repo
Créer un dossier vide

Se positionner dans ce dossier

Initialiser le repo : ```git init```

Définir la source distante : ```git remote add origin https://github.com/PnVanoise/geopasto_back.git```

Récupérer les données : ```git pull origin main```

## Configuration locale
Dans le répertoire, créer un environnement virtuel python : ```python3 -m venv venv```

Activer cet environnement : ```. ./venv/bin/activate```

Installer les modules python : ```pip install -r requirements.txt```

Récupérer la configuration système de l'application _settings.py_ (configuration de la base notamment, secret_key, paramètres CORS)

## Création du service
```
sudo vim /etc/systemd/system/geopasto_back.service
```

```
[Unit]
Description=gunicorn daemon for Geopasto
After=network.target

[Service]
User=geoagri
Group=geoagri
WorkingDirectory=<install_dir>
ExecStart=<install_dir>/venv/bin/gunicorn --access-logfile <install_dir>/gunicorn-access.log --error-logfile=<install_dir>/gunicorn-error.log --workers 3 --bind 0.0.0.0:8000 geoagri.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target

```

## Configuration nginx (proxy web)
```
sudo vim /etc/nginx/sites-available/geoagri_backend
```

```
server {
    listen 80;
    server_name <@ip_server>;

    location /static/ {
            alias <install_dir>/geoagri/static/;
            #autoindex on;
    }

    location /media/ {
            alias <install_dir>/geoagri/media/;
    }

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        rewrite ^/back/(.*)$ /$1 break;

        add_header "Cross-Origin-Opener-Policy" "";

        # CORS headers
        # add_header 'Access-Control-Allow-Origin' '*' always;
        # add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE' always;
        # add_header 'Access-Control-Allow-Headers' 'Origin, Authorization, X-requested-With, Accept, Content-Type';


        # Ajout des headers de sécurité
        add_header Cross-Origin-Opener-Policy same-origin;
        add_header Cross-Origin-Embedder-Policy require-corp;
    }
}

```

# Création d'une nouvelle instance
1. Créer une base de données vide, activer l'extension postgis (```create extension postgis```)
2. Créer un utilisateur propriétaire de la bdd
3. Récupérer les sources, créer venv, actualiser l'environnement python (```pip update -r -requirements.txt```)
4. Récupèrer un fichier settings.py, l'actualiser avec les infos de la nouvelle bdd
5. ```python manage.py makemigrations``` (ne va rien faire : les fichiers de migrations sont déjà existant)
6. ```python manage.py migrate``` (doit exécuter les 6x migrations passées)

La bdd doit être à jour.

