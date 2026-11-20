import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def connexion():
    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

def enregistrer_position(vehicle_id, lat, lon, ts):
    conn = connexion()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO positions (vehicle_id, lat, lon, recorded_at) VALUES (%s, %s, %s, %s)",
        (vehicle_id, lat, lon, ts),
    )
    conn.commit()
    conn.close()
