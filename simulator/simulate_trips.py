# Import des modules
import json
import random
import time
from datetime import datetime

TRIPS_FILE = "data/trips.json"  # Fichier contenant 30 trajets de Villetaneuse
VEHICLE_ID = "VEHICULE_001" # Identifiant du véhicule
PLAYBACK_SPEED = 10.0  # Vitesse de lecture du trajet

with open(TRIPS_FILE, encoding="utf-8") as f:  # Charge le fichier JSON
    trips = json.load(f)["trips"]  # Construit la liste des 30 trajets

trip = random.choice(trips)  # Choisit un trajet au hasard
print(f"Trajet {trip['id']}") # Affichage du trajet choisi

previous_t = 0  # Temps du point précédent

# Boucle principale
for temps, latitude, longitude in trip["points"]: # Pour chaque point
    time.sleep((temps - previous_t) / PLAYBACK_SPEED)  # Attend l'écart avec le point précédent
    previous_t = temps # On retient le temps actuel pour le tour suivant
    now = datetime.now().strftime("%H:%M:%S")  # Heure (exemple : 23:52:08)
    print(f"{VEHICLE_ID} | Latitude = {latitude:.6f} | Longitude = {longitude:.6f} | Heure = {now}")  # Position simulée avec 6 chiffres après la virgule (.6f)

print("Trajet terminé.")