"""
FasalRakshak AI - Weather-Aware Disease Risk Knowledge Base
Source-backed environmental thresholds for crop disease favorability assessment.
Strictly isolated from ML model confidence, symptom verification scores, and field concern logic.
"""

# Environmental thresholds for diseases with established agricultural extension weather rules
WEATHER_DISEASE_RULES = {
    # -------------------------------------------------------------------------
    # RICE DISEASES
    # -------------------------------------------------------------------------
    "Rice-Bacterialblight": {
        "has_rules": True,
        "temp_range": (25.0, 34.0),       # Warm temperatures favor Xanthomonas oryzae
        "humidity_min": 75.0,            # Relative humidity > 75-80%
        "rain_favorable": True,           # Rainstorms/splashing promote leaf infection
        "description": "Bacterial leaf blight thrives in warm temperatures (25-34°C), high humidity (>75%), and rainy or stormy conditions which cause leaf splashing and micro-wounds.",
        "sources": ["ICAR - Indian Institute of Rice Research (IIRR)", "IRRI Rice Knowledge Bank"]
    },
    "Rice-Brownspot": {
        "has_rules": True,
        "temp_range": (20.0, 30.0),       # Moderate temperatures (20-30°C)
        "humidity_min": 85.0,            # High relative humidity (>85%) or prolonged dew
        "rain_favorable": True,
        "description": "Brown spot fungal spore germination is favored by high relative humidity (>85%), prolonged leaf wetness, and moderate temperatures (20-30°C).",
        "sources": ["ICAR - National Rice Research Institute (NRRI)"]
    },
    "Rice-Leafsmut": {
        "has_rules": True,
        "temp_range": (22.0, 32.0),
        "humidity_min": 80.0,
        "rain_favorable": True,
        "description": "Rice leaf smut spore release and germination occur rapidly during warm, humid conditions (>80% RH) following light rains.",
        "sources": ["ICAR - National Rice Research Institute (NRRI)"]
    },

    # -------------------------------------------------------------------------
    # TOMATO DISEASES
    # -------------------------------------------------------------------------
    "Tomato___Bacterial_spot": {
        "has_rules": True,
        "temp_range": (24.0, 32.0),       # Warm temperatures
        "humidity_min": 80.0,            # High humidity
        "rain_favorable": True,           # Rain splashing spreads bacteria
        "description": "Bacterial spot on tomato is highly favored by warm temperatures (24-32°C), high relative humidity (>80%), and wind-driven rain.",
        "sources": ["ICAR - Indian Institute of Horticultural Research (IIHR)", "USDA Extension"]
    },
    "Tomato___Early_blight": {
        "has_rules": True,
        "temp_range": (24.0, 29.0),       # Warm conditions (24-29°C)
        "humidity_min": 80.0,            # Wet/humid weather
        "rain_favorable": True,
        "description": "Alternaria solani requires heavy dew or rainfall combined with warm temperatures (24-29°C) and relative humidity >80% for rapid spore production.",
        "sources": ["ICAR - Indian Agricultural Research Institute (IARI)"]
    },
    "Tomato___Late_blight": {
        "has_rules": True,
        "temp_range": (15.0, 24.0),       # Cool to moderate conditions (15-24°C)
        "humidity_min": 85.0,            # Very high humidity (>85%)
        "rain_favorable": True,           # Wet leaves, fog, or rain essential
        "description": "Late blight (Phytophthora infestans) is extremely aggressive under cool-to-moderate temperatures (15-24°C), high humidity (>85%), and foggy or rainy days.",
        "sources": ["ICAR - Central Potato Research Institute / IIHR", "FAO Plant Production Guidelines"]
    },
    "Tomato___Leaf_Mold": {
        "has_rules": True,
        "temp_range": (20.0, 26.0),       # Moderate temperatures
        "humidity_min": 85.0,            # High humidity essential (>85%)
        "rain_favorable": False,
        "description": "Tomato leaf mold requires prolonged high relative humidity (>85%) and moderate temperatures (20-26°C), especially in dense or greenhouse canopies.",
        "sources": ["ICAR - Indian Institute of Vegetable Research (IIVR)"]
    },
    "Tomato___Septoria_leaf_spot": {
        "has_rules": True,
        "temp_range": (20.0, 28.0),
        "humidity_min": 80.0,
        "rain_favorable": True,
        "description": "Septoria lycopersici develops rapidly during extended periods of leaf wetness, rainfall, and moderate temperatures (20-28°C).",
        "sources": ["ICAR - Indian Institute of Vegetable Research (IIVR)"]
    },
    "Tomato___Target_Spot": {
        "has_rules": True,
        "temp_range": (20.0, 30.0),
        "humidity_min": 80.0,
        "rain_favorable": True,
        "description": "Target spot (Corynespora cassiicola) is favored by warm, moist conditions (>80% RH) and long periods of leaf wetness.",
        "sources": ["ICAR - IIHR"]
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "has_rules": True,
        "temp_range": (27.0, 38.0),       # Hot, dry conditions
        "humidity_min": 0.0,             # Thrives in LOW humidity (<50%)
        "max_humidity_for_risk": 55.0,   # Low humidity is favorable for spider mites!
        "rain_favorable": False,          # Rain washes away mites
        "description": "Two-spotted spider mites reproduce rapidly in hot (>27°C), dry, low-humidity (<55% RH) conditions. Rain and high humidity suppress mite populations.",
        "sources": ["ICAR - National Bureau of Agricultural Insect Resources (NBAIR)"]
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "has_rules": False,
        "description": "Viral conditions depend primarily on whitefly vector populations rather than direct weather thresholds. Weather risk rules are presented for general crop context only.",
        "sources": ["ICAR - IARI"]
    },
    "Tomato___Tomato_mosaic_virus": {
        "has_rules": False,
        "description": "Tomato mosaic virus is mechanically transmitted through seed, hands, and tools. Direct weather favorability rules are not applicable.",
        "sources": ["ICAR - IARI"]
    },

    # -------------------------------------------------------------------------
    # SUGARCANE DISEASES
    # -------------------------------------------------------------------------
    "Sugarcane-Pokkah Boeng": {
        "has_rules": True,
        "temp_range": (22.0, 30.0),
        "humidity_min": 80.0,
        "rain_favorable": True,
        "description": "Pokkah boeng fungal spores infect sugarcane spindle leaves during cloudy, rainy weather with high humidity (>80%) and moderate temperatures (22-30°C).",
        "sources": ["ICAR - Sugarcane Breeding Institute (SBI)"]
    },
    "Sugarcane-Red Leaf Spot": {
        "has_rules": True,
        "temp_range": (22.0, 30.0),
        "humidity_min": 80.0,
        "rain_favorable": True,
        "description": "Red leaf spot fungal development is favored by warm, humid weather with frequent rains during early growth stages.",
        "sources": ["ICAR - Indian Institute of Sugarcane Research (IISR)"]
    },
    "Sugarcane-Red Rot": {
        "has_rules": True,
        "temp_range": (25.0, 32.0),       # High temp & humidity
        "humidity_min": 80.0,
        "rain_favorable": True,           # Waterlogging / monsoon rain accelerates red rot spread
        "description": "Red rot (Colletotrichum falcatum) spreads aggressively during warm monsoonal periods (25-32°C), high humidity (>80%), and field waterlogging.",
        "sources": ["ICAR - Sugarcane Breeding Institute (SBI)"]
    },
    "Sugarcane-Ring Spot": {
        "has_rules": True,
        "temp_range": (20.0, 30.0),
        "humidity_min": 75.0,
        "rain_favorable": True,
        "description": "Ring spot lesions expand under cool to warm humid conditions with high dew or rainfall.",
        "sources": ["ICAR - IISR"]
    },
    "Sugarcane-Wilt": {
        "has_rules": True,
        "temp_range": (28.0, 38.0),       # Hot dry conditions following wet spells stress stalks
        "humidity_min": 0.0,
        "rain_favorable": False,
        "description": "Sugarcane wilt symptoms manifest intensely under high temperatures (28-38°C) and moisture-stress conditions following monsoonal wet spells.",
        "sources": ["ICAR - Sugarcane Breeding Institute (SBI)"]
    },
    "Sugarcane-Yellow Leaf Disease": {
        "has_rules": False,
        "description": "Sugarcane yellow leaf virus is spread by aphid vectors. Direct weather favorability rules are not applicable.",
        "sources": ["ICAR - SBI"]
    },
    "Sugarcane-Grassy Shoot": {
        "has_rules": False,
        "description": "Grassy shoot is caused by phytoplasmas spread through vector insects and infected setts. Direct weather favorability rules are not applicable.",
        "sources": ["ICAR - IISR"]
    },
    "Sugarcane-Mosaic": {
        "has_rules": False,
        "description": "Sugarcane mosaic virus is vector-transmitted by aphids. Direct weather favorability rules are not applicable.",
        "sources": ["ICAR - IISR"]
    },

    # -------------------------------------------------------------------------
    # PUMPKIN DISEASES
    # -------------------------------------------------------------------------
    "Pumpkin-Bacterial Leaf Spot": {
        "has_rules": True,
        "temp_range": (24.0, 32.0),
        "humidity_min": 80.0,
        "rain_favorable": True,
        "description": "Bacterial leaf spot in cucurbits is promoted by high relative humidity (>80%), warm temperatures (24-32°C), and splashing rainfall.",
        "sources": ["ICAR - Central Institute for Arid Horticulture (CIAH)"]
    },
    "Pumpkin-Downy Mildew": {
        "has_rules": True,
        "temp_range": (18.0, 26.0),       # Cool to moderate (18-26°C)
        "humidity_min": 85.0,            # Very high humidity & leaf wetness
        "rain_favorable": True,
        "description": "Downy mildew in pumpkin (Pseudoperonospora cubensis) spreads rapidly during cool mornings (18-26°C), high humidity (>85%), and wet foliage.",
        "sources": ["ICAR - Indian Institute of Horticultural Research (IIHR)"]
    },
    "Pumpkin-Powdery_Mildew": {
        "has_rules": True,
        "temp_range": (20.0, 28.0),       # Moderate temp
        "humidity_min": 60.0,            # Can thrive even in moderate humidity
        "rain_favorable": False,          # Heavy rain actually washes away powdery mildew spores!
        "description": "Powdery mildew thrives under warm, dry to moderately humid conditions (60-80% RH) and shaded leaf canopies. Heavy rain is unfavorable for spore survival.",
        "sources": ["ICAR - IIHR"]
    },
    "Pumpkin-Mosaic Disease": {
        "has_rules": False,
        "description": "Pumpkin mosaic virus is aphid-transmitted. Direct weather favorability rules are not applicable.",
        "sources": ["ICAR - IIHR"]
    },

    # -------------------------------------------------------------------------
    # WHEAT DISEASES
    # -------------------------------------------------------------------------
    "Wheat___Leaf_Rust": {
        "has_rules": True,
        "temp_range": (15.0, 25.0),
        "humidity_min": 75.0,
        "rain_favorable": True,
        "description": "Leaf rust (brown rust) spore germination is favored by moderate temperatures (15-25°C), high relative humidity (>75%), and heavy dew or rain.",
        "sources": ["ICAR - Indian Institute of Wheat and Barley Research (IIWBR)"]
    },
    "Wheat___Stripe_Rust": {
        "has_rules": True,
        "temp_range": (7.0, 18.0),        # Cool temperatures favor stripe rust
        "humidity_min": 80.0,
        "rain_favorable": True,
        "description": "Yellow/Stripe rust thrives in cool winter temperatures (7-18°C), persistent fog, high relative humidity (>80%), and frequent light rains.",
        "sources": ["ICAR - IIWBR Karnal", "PAU Ludhiana"]
    },
    "Wheat___Powdery_Mildew": {
        "has_rules": True,
        "temp_range": (15.0, 22.0),
        "humidity_min": 80.0,
        "rain_favorable": False,         # Heavy rain washes spores
        "description": "Powdery mildew on wheat is favored by cool, cloudy days (15-22°C) and high relative humidity (>80%) in dense crop canopies.",
        "sources": ["ICAR - IIWBR"]
    },
    "Wheat___Septoria": {
        "has_rules": True,
        "temp_range": (15.0, 24.0),
        "humidity_min": 85.0,
        "rain_favorable": True,
        "description": "Septoria leaf blotch pycnidiospores require splash rainfall and prolonged leaf wetness at moderate temperatures (15-24°C) for canopy spread.",
        "sources": ["ICAR - IIWBR"]
    },

    # -------------------------------------------------------------------------
    # MAIZE DISEASES
    # -------------------------------------------------------------------------
    "Maize___Common_Rust": {
        "has_rules": True,
        "temp_range": (16.0, 25.0),
        "humidity_min": 80.0,
        "rain_favorable": True,
        "description": "Common rust in maize is favored by cool-to-moderate temperatures (16-25°C), high humidity (>80%), and heavy morning dews.",
        "sources": ["ICAR - Indian Institute of Maize Research (IIMR)"]
    },
    "Maize___Northern_Leaf_Blight": {
        "has_rules": True,
        "temp_range": (18.0, 27.0),
        "humidity_min": 80.0,
        "rain_favorable": True,
        "description": "Northern leaf blight (Exserohilum turcicum) spore production requires moderate temperatures (18-27°C) and extended leaf wetness (dew or rain).",
        "sources": ["ICAR - IIMR Ludhiana"]
    },
    "Maize___Gray_Leaf_Spot": {
        "has_rules": True,
        "temp_range": (22.0, 30.0),
        "humidity_min": 85.0,
        "rain_favorable": True,
        "description": "Gray leaf spot thrives under warm, humid monsoonal conditions (22-30°C) with persistent high relative humidity (>85%).",
        "sources": ["ICAR - IIMR"]
    }
}


def evaluate_weather_favorability(class_name: str, temp_c: float, humidity_percent: float, precipitation_mm: float):
    """
    Evaluates weather favorability for a given disease class against current & forecast weather metrics.
    Deterministic output strictly isolated from ML confidence, symptom score, and field concern.
    """
    rule = WEATHER_DISEASE_RULES.get(class_name)

    if not rule or not rule.get("has_rules", False):
        return {
            "available": False,
            "favorability": "NEUTRAL",
            "favorability_label": "Weather Risk Context Not Applicable",
            "matched_factors": [],
            "unmatched_factors": [],
            "explanation": rule.get("description", "Weather-specific risk rules are not currently available for this condition.") if rule else "Weather-specific risk rules are not currently available for this condition.",
            "disclaimer": "Weather favorability indicates whether recent/forecast conditions match known conditions associated with this disease. It is not a disease probability.",
            "sources": rule.get("sources", []) if rule else []
        }

    matched_factors = []
    unmatched_factors = []
    factor_count = 0

    # 1. Temperature Range Factor
    temp_min, temp_max = rule.get("temp_range", (15.0, 35.0))
    if temp_min <= temp_c <= temp_max:
        matched_factors.append(f"Suitable temperature ({temp_c:.1f}°C within favorable {temp_min}-{temp_max}°C range)")
        factor_count += 1
    else:
        unmatched_factors.append(f"Temperature outside optimal range ({temp_c:.1f}°C vs {temp_min}-{temp_max}°C)")

    # 2. Relative Humidity Factor
    if "max_humidity_for_risk" in rule:
        max_h = rule["max_humidity_for_risk"]
        if humidity_percent <= max_h:
            matched_factors.append(f"Favorable dry conditions ({humidity_percent:.0f}% RH <= {max_h:.0f}%)")
            factor_count += 1
        else:
            unmatched_factors.append(f"High humidity suppresses pest ({humidity_percent:.0f}% RH > {max_h:.0f}%)")
    else:
        min_h = rule.get("humidity_min", 75.0)
        if humidity_percent >= min_h:
            matched_factors.append(f"High relative humidity ({humidity_percent:.0f}% RH >= {min_h:.0f}%)")
            factor_count += 1
        else:
            unmatched_factors.append(f"Relative humidity below optimal ({humidity_percent:.0f}% RH < {min_h:.0f}%)")

    # 3. Precipitation / Leaf Wetness Factor
    rain_fav = rule.get("rain_favorable", True)
    if rain_fav:
        if precipitation_mm > 0.1:
            matched_factors.append(f"Recent or forecast precipitation ({precipitation_mm:.1f} mm)")
            factor_count += 1
        else:
            unmatched_factors.append("No active rainfall reported")
    else:
        if precipitation_mm <= 0.1:
            matched_factors.append("Dry canopy conditions (favorable for spore buildup)")
            factor_count += 1
        else:
            unmatched_factors.append(f"Rainfall washes away spores ({precipitation_mm:.1f} mm)")

    # Compute Favorability Level
    if factor_count >= 3:
        favorability = "HIGH"
        favorability_label = "HIGH FAVORABILITY"
    elif factor_count >= 2:
        favorability = "MODERATE"
        favorability_label = "MODERATE FAVORABILITY"
    else:
        favorability = "LOW"
        favorability_label = "LOW FAVORABILITY"

    return {
        "available": True,
        "favorability": favorability,
        "favorability_label": favorability_label,
        "matched_factors": matched_factors,
        "unmatched_factors": unmatched_factors,
        "explanation": rule["description"],
        "disclaimer": "Weather favorability indicates whether recent/forecast conditions match known conditions associated with this disease. It is not a disease probability.",
        "sources": rule.get("sources", [])
    }
