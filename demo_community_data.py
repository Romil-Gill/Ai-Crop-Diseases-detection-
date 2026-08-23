"""
FasalRakshak AI - Synthetic Demo Community Signal Dataset
Provides realistic regional disease signal records for hackathon presentation and SIH demonstration.
Privacy Enforcement: Public map coordinates use 1 decimal coarsening (map_lat, map_lon).
Separation: Demo data is strictly separated from SQLite live community signals and is never saved to fasalrakshak.db.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any

# Synthetic regional demo dataset centered around Haryana & North India agricultural clusters
def get_demo_signals() -> List[Dict[str, Any]]:
    now = datetime.utcnow()
    
    # Base timestamp offsets for realistic recency spread over 30 days
    demo_records = [
        # Ambala Cluster (Elevated Activity - Rice & Tomato)
        {
            "id": 9001,
            "created_at": (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Rice",
            "class_name": "Rice-Leafsmut",
            "condition": "Leaf Smut",
            "area_name": "Ambala",
            "map_lat": 30.4,
            "map_lon": 76.8,
            "symptom_agreement": "high",
            "field_concern": "HIGH",
            "weather_favorability": "HIGH",
            "status": "reported_signal"
        },
        {
            "id": 9002,
            "created_at": (now - timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Rice",
            "class_name": "Rice-Leafsmut",
            "condition": "Leaf Smut",
            "area_name": "Ambala",
            "map_lat": 30.4,
            "map_lon": 76.8,
            "symptom_agreement": "high",
            "field_concern": "MODERATE",
            "weather_favorability": "HIGH",
            "status": "reported_signal"
        },
        {
            "id": 9003,
            "created_at": (now - timedelta(days=1, hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Rice",
            "class_name": "Rice-Bacterialblight",
            "condition": "Bacterial Blight",
            "area_name": "Ambala",
            "map_lat": 30.4,
            "map_lon": 76.8,
            "symptom_agreement": "high",
            "field_concern": "HIGH",
            "weather_favorability": "HIGH",
            "status": "reported_signal"
        },
        {
            "id": 9004,
            "created_at": (now - timedelta(days=2, hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Rice",
            "class_name": "Rice-Leafsmut",
            "condition": "Leaf Smut",
            "area_name": "Ambala",
            "map_lat": 30.4,
            "map_lon": 76.8,
            "symptom_agreement": "moderate",
            "field_concern": "MODERATE",
            "weather_favorability": "MODERATE",
            "status": "reported_signal"
        },
        {
            "id": 9005,
            "created_at": (now - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Tomato",
            "class_name": "Tomato___Early_blight",
            "condition": "Early Blight",
            "area_name": "Ambala",
            "map_lat": 30.4,
            "map_lon": 76.8,
            "symptom_agreement": "high",
            "field_concern": "MODERATE",
            "weather_favorability": "HIGH",
            "status": "reported_signal"
        },

        # Karnal Cluster (Moderate Activity - Tomato & Sugarcane)
        {
            "id": 9006,
            "created_at": (now - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Tomato",
            "class_name": "Tomato___Late_blight",
            "condition": "Late Blight",
            "area_name": "Karnal",
            "map_lat": 29.7,
            "map_lon": 77.0,
            "symptom_agreement": "high",
            "field_concern": "HIGH",
            "weather_favorability": "HIGH",
            "status": "reported_signal"
        },
        {
            "id": 9007,
            "created_at": (now - timedelta(days=1, hours=8)).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Tomato",
            "class_name": "Tomato___Early_blight",
            "condition": "Early Blight",
            "area_name": "Karnal",
            "map_lat": 29.7,
            "map_lon": 77.0,
            "symptom_agreement": "high",
            "field_concern": "MODERATE",
            "weather_favorability": "HIGH",
            "status": "reported_signal"
        },
        {
            "id": 9008,
            "created_at": (now - timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Sugarcane",
            "class_name": "Sugarcane-Red Rot",
            "condition": "Red Rot",
            "area_name": "Karnal",
            "map_lat": 29.7,
            "map_lon": 77.0,
            "symptom_agreement": "moderate",
            "field_concern": "HIGH",
            "weather_favorability": "MODERATE",
            "status": "reported_signal"
        },

        # Kurukshetra Cluster (Moderate Activity - Rice & Pumpkin)
        {
            "id": 9009,
            "created_at": (now - timedelta(days=1, hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Rice",
            "class_name": "Rice-Brownspot",
            "condition": "Brown Spot",
            "area_name": "Kurukshetra",
            "map_lat": 29.9,
            "map_lon": 76.8,
            "symptom_agreement": "high",
            "field_concern": "MODERATE",
            "weather_favorability": "MODERATE",
            "status": "reported_signal"
        },
        {
            "id": 9010,
            "created_at": (now - timedelta(days=2, hours=5)).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Pumpkin",
            "class_name": "Pumpkin-Powdery_Mildew",
            "condition": "Powdery Mildew",
            "area_name": "Kurukshetra",
            "map_lat": 29.9,
            "map_lon": 76.8,
            "symptom_agreement": "high",
            "field_concern": "LOW",
            "weather_favorability": "HIGH",
            "status": "reported_signal"
        },

        # Yamunanagar Cluster (Moderate Activity - Sugarcane)
        {
            "id": 9011,
            "created_at": (now - timedelta(hours=10)).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Sugarcane",
            "class_name": "Sugarcane-Red Rot",
            "condition": "Red Rot",
            "area_name": "Yamunanagar",
            "map_lat": 30.1,
            "map_lon": 77.3,
            "symptom_agreement": "high",
            "field_concern": "HIGH",
            "weather_favorability": "HIGH",
            "status": "reported_signal"
        },
        {
            "id": 9012,
            "created_at": (now - timedelta(days=3, hours=4)).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Sugarcane",
            "class_name": "Sugarcane-Red Leaf Spot",
            "condition": "Red Leaf Spot",
            "area_name": "Yamunanagar",
            "map_lat": 30.1,
            "map_lon": 77.3,
            "symptom_agreement": "moderate",
            "field_concern": "MODERATE",
            "weather_favorability": "MODERATE",
            "status": "reported_signal"
        },

        # Panchkula Cluster (Low Activity - Tomato)
        {
            "id": 9013,
            "created_at": (now - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Tomato",
            "class_name": "Tomato___Septoria_leaf_spot",
            "condition": "Septoria Leaf Spot",
            "area_name": "Panchkula",
            "map_lat": 30.7,
            "map_lon": 76.9,
            "symptom_agreement": "high",
            "field_concern": "LOW",
            "weather_favorability": "MODERATE",
            "status": "reported_signal"
        }
    ]
    
    return demo_records
