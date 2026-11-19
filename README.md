# Suivi de flotte géolocalisée - SAÉ 3.02

Application client/serveur en Python : des véhicules simulés envoient
leur position GPS en UDP à un serveur, qui les enregistre dans
PostgreSQL et les affiche sur une carte web.

## Équipe

  -----------------------------------------------------------------------------
  Membre                  Pseudo GitHub                 Rôle
  ----------------------- ----------------------------- -----------------------
  Raed AROUA              RaedAroua0                    Serveur et protocole

  Rayan CHERIFI           raytchux                      Serveur et protocole

  Nael KHARI              nlz1974k-commits              Base de données et
                                                        authentification

  Jathushan RAJAKUMAR     rajakumarjathushan07-glitch   Base de données et
                                                        authentification
  -----------------------------------------------------------------------------

## Architecture

À compléter.

## Protocole applicatif

À compléter (format des messages, types, codes d'erreur).

## Simulateur de véhicules

Le simulateur rejoue des trajets GPS réalistes (routes de Villetaneuse et
alentours) pour simuler un véhicule qui envoie sa position.

### Fonctionnement

1. `module_gen.py` tire un départ et une arrivée au hasard, demande l'itinéraire
   à l'API OSRM (OpenStreetMap), puis calcule un point GPS toutes les 5 secondes.
   Les 30 trajets sont enregistrés dans `data/trips.json`.
2. `simulate_trips.py` choisit un trajet au hasard et affiche ses positions
   (identifiant du véhicule, latitude, longitude, heure) en respectant le
   rythme réel entre deux points.

Les 30 trajets sont déjà fournis dans le dépôt : il n'est pas nécessaire de
les régénérer.

### Format de `trips.json`

```json
{"trips":[{"id":1,"distance_m":8322,"duration_s":856,"points":[[0,48.949622,2.241374],[5,48.949759,2.242097]]}]}
```

Chaque point est de la forme `[temps_en_secondes, latitude, longitude]`.

### Utilisation

```bash
cd simulator
python simulate_trips.py
```

La vitesse de lecture se règle avec `PLAYBACK_SPEED` dans `simulate_trips.py`
(`1.0` = temps réel, `10.0` = dix fois plus vite).

### Générer de nouveaux trajets (optionnel)

```bash
cd simulator
python module_gen.py
```

## Base de données

### Installation de PostgreSQL (macOS)

``` bash
brew install postgresql@16
brew services start postgresql@16
```

### Création de la base et de l'utilisateur applicatif

``` sql
psql postgres
CREATE DATABASE flotte;
CREATE USER flotte_app WITH PASSWORD 'votre-mot-de-passe';
GRANT CONNECT ON DATABASE flotte TO flotte_app;
```

### Création des tables et des droits

``` bash
psql flotte -f database/schema.sql
psql flotte -f database/droits.sql
```

L'utilisateur `flotte_app` peut lire et ajouter des données, mais ne
peut rien supprimer.

## Configuration

Les identifiants de la base sont lus depuis un fichier `.env` placé à la
racine du projet. Ce fichier est ignoré par Git : aucun mot de passe
n'est stocké dans le dépôt.

``` dotenv
DB_NAME=flotte
DB_USER=flotte_app
DB_PASSWORD=votre-mot-de-passe
DB_HOST=localhost
DB_PORT=5432
```

## Authentification

À compléter.

## Interface web

À compléter.

## Lancement

À compléter.
