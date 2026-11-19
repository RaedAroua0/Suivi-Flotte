#!/usr/bin/env python3
"""Génère 30 trajets routiers via OSRM et les enregistre dans data/trips.json."""
import bisect
import json
import math
import os
import random
import time
import requests

NB_TRIPS = 30 # Nombre de trajets à générer
CENTER = (48.9569, 2.3427)  # Villetaneuse (latitude, longitude)
RADIUS_KM = 8.0  # Rayon de la zone autour de Villetaneuse
MIN_KM, MAX_KM = 1.5, 15.0  # Un trajet de moins de 1,5 km ou de plus de 15 km est rejeté
STEP_S = 5  # Un point GPS toutes les 5 secondes
OUTPUT_FILE = "data/trips.json" # Fichier d'output
OSRM_URL = "https://router.project-osrm.org/route/v1/driving/{},{};{},{}" # URL du serveur OSRM


def random_point():
    """Point aléatoire dans un disque autour de CENTER."""
    r = RADIUS_KM * 1000 * math.sqrt(random.random())  # sqrt = répartition uniforme
    a = random.random() * 2 * math.pi  # Direction aléatoire
    lat = CENTER[0] + r * math.cos(a) / 111_320  # 1° de latitude ≈ 111 320 m
    lon = CENTER[1] + r * math.sin(a) / (111_320 * math.cos(math.radians(CENTER[0])))
    return lat, lon


def fetch_route(start, end):
    """Demande l'itinéraire à OSRM (None en cas d'échec)."""
    url = OSRM_URL.format(start[1], start[0], end[1], end[0])  # OSRM veut lon,lat
    params = {"overview": "full", "geometries": "geojson", "annotations": "duration"}
    try:
        data = requests.get(url, params=params, timeout=20).json()
    except (requests.RequestException, ValueError):  # Réseau ou JSON invalide
        return None
    return data["routes"][0] if data.get("code") == "Ok" else None


def resample(route):
    """Un point GPS toutes les STEP_S secondes le long de l'itinéraire."""
    coords = route["geometry"]["coordinates"]  # Liste de [lon, lat]
    durations = route["legs"][0]["annotation"]["duration"]  # Durée de chaque segment
    times = [0]  # Temps cumulé à chaque sommet
    for d in durations:
        times.append(times[-1] + d)

    points = []
    t = 0
    while t <= times[-1]:
        i = min(bisect.bisect_right(times, t) - 1, len(durations) - 1)  # segment actuel
        span = times[i + 1] - times[i]
        f = (t - times[i]) / span if span else 0  # avancement dans le segment (0 à 1)
        lon = coords[i][0] + f * (coords[i + 1][0] - coords[i][0])  # interpolation
        lat = coords[i][1] + f * (coords[i + 1][1] - coords[i][1])
        points.append([t, round(lat, 6), round(lon, 6)])
        t += STEP_S

    lon, lat = coords[-1]  # on ajoute la destination exacte
    points.append([round(times[-1], 1), round(lat, 6), round(lon, 6)])
    return points


def main():
    """Fonction main principale."""
    trips = []
    attempts = 0
    while len(trips) < NB_TRIPS and attempts < NB_TRIPS * 10:  # limite anti-boucle infinie
        attempts += 1
        route = fetch_route(random_point(), random_point())
        time.sleep(1)  # Politesse envers le serveur OSRM public
        if route is None or not MIN_KM <= route["distance"] / 1000 <= MAX_KM:
            continue  # échec ou trajet trop court/long : on retente

        trips.append({
            "id": len(trips) + 1,
            "distance_m": round(route["distance"]),
            "duration_s": round(route["duration"]),
            "points": resample(route),  # format : [temps_s, lat, lon]
        })
        print(f"Trajet {len(trips)}/{NB_TRIPS} : {route['distance'] / 1000:.1f} km")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)  # crée data/ si besoin
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"trips": trips}, f, separators=(",", ":"))
    print(f"Terminé : {len(trips)} trajets dans {OUTPUT_FILE}")


if __name__ == "__main__":
    main()