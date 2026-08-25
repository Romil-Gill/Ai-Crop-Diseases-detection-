"""
FasalRakshak AI - SQLite Persistence Layer (Hardened Phase 6.1)
Handles local scan history persistence and anonymized community disease signals.
Privacy Enforcement: Public API coordinates are coarsened to 1 decimal place max (map_lat, map_lon).
Images, base64 payloads, and exact GPS coordinates are NEVER stored or transmitted.
"""

import sqlite3
import os
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fasalrakshak.db")


def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    path = db_path or os.environ.get("FASALRAKSHAK_DB_PATH") or DEFAULT_DB_PATH
    conn = sqlite3.connect(path, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Optional[str] = None):
    """Initializes and migrates SQLite tables safely if they do not exist."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # 1. Scans Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        crop TEXT NOT NULL,
        class_name TEXT NOT NULL,
        condition TEXT NOT NULL,
        model_confidence REAL NOT NULL,
        is_healthy INTEGER NOT NULL,
        diagnosis_reliable INTEGER NOT NULL DEFAULT 1,
        symptom_agreement TEXT,
        symptom_match_score REAL,
        field_concern TEXT,
        weather_favorability TEXT,
        location_name TEXT,
        community_shared INTEGER DEFAULT 0
    );
    """)

    # Safe Schema Migration Check for diagnosis_reliable column
    cursor.execute("PRAGMA table_info(scans)")
    columns = [col["name"] for col in cursor.fetchall()]
    if "diagnosis_reliable" not in columns:
        cursor.execute("ALTER TABLE scans ADD COLUMN diagnosis_reliable INTEGER NOT NULL DEFAULT 1")

    # 2. Community Signals Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS community_signals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        source_scan_id INTEGER UNIQUE,
        crop TEXT NOT NULL,
        class_name TEXT NOT NULL,
        condition TEXT NOT NULL,
        area_name TEXT NOT NULL,
        approx_lat REAL,
        approx_lon REAL,
        symptom_agreement TEXT,
        field_concern TEXT,
        weather_favorability TEXT,
        status TEXT DEFAULT 'reported_signal',
        FOREIGN KEY (source_scan_id) REFERENCES scans (id) ON DELETE SET NULL
    );
    """)

    conn.commit()
    conn.close()


def create_scan(data: Dict[str, Any], db_path: Optional[str] = None) -> Dict[str, Any]:
    """Inserts a new scan record. Server-side enforces diagnosis_reliable check."""
    is_reliable = 1 if data.get("diagnosis_reliable", True) else 0

    if not is_reliable:
        raise ValueError("Uncertain diagnoses are caught by the Safe Diagnosis Gate and cannot be saved to history.")

    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO scans (
        created_at, crop, class_name, condition, model_confidence, is_healthy,
        diagnosis_reliable, symptom_agreement, symptom_match_score, field_concern,
        weather_favorability, location_name, community_shared
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
    """, (
        created_at,
        data.get("crop"),
        data.get("class_name"),
        data.get("condition"),
        float(data.get("model_confidence", 0.0)),
        1 if data.get("is_healthy") else 0,
        is_reliable,
        data.get("symptom_agreement"),
        float(data["symptom_match_score"]) if data.get("symptom_match_score") is not None else None,
        data.get("field_concern"),
        data.get("weather_favorability"),
        data.get("location_name", "Local Field")
    ))

    scan_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return get_scan_by_id(scan_id, db_path) # type: ignore


def get_scans(crop_filter: Optional[str] = None, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves saved local scan records, optionally filtered by crop."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    if crop_filter and crop_filter.lower() != "all":
        cursor.execute("SELECT * FROM scans WHERE LOWER(crop) = LOWER(?) ORDER BY id DESC", (crop_filter,))
    else:
        cursor.execute("SELECT * FROM scans ORDER BY id DESC")

    rows = cursor.fetchall()
    conn.close()

    return [_row_to_scan_dict(row) for row in rows]


def get_scan_by_id(scan_id: int, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Fetches a single scan record by ID."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scans WHERE id = ?", (scan_id,))
    row = cursor.fetchone()
    conn.close()

    return _row_to_scan_dict(row) if row else None


def delete_scan(scan_id: int, db_path: Optional[str] = None) -> bool:
    """
    Deletes a scan record by ID.
    Delete Integrity: Sets source_scan_id to NULL in community_signals so anonymized summary data
    remains clean without orphan crashes or foreign key corruption.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # Disassociate community signal source_scan_id safely before deletion
    cursor.execute("UPDATE community_signals SET source_scan_id = NULL WHERE source_scan_id = ?", (scan_id,))

    # Delete scan
    cursor.execute("DELETE FROM scans WHERE id = ?", (scan_id,))
    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted


def create_community_signal(scan_id: int, approx_lat: Optional[float] = None, approx_lon: Optional[float] = None, db_path: Optional[str] = None) -> Tuple[Dict[str, Any], bool]:
    """
    Server-Side Eligibility Verification & Opt-in Sharing:
    - Source scan must exist
    - Must be a reliable diagnosis (diagnosis_reliable == 1)
    - Must be a disease condition (is_healthy == 0)
    - Duplicate protection: Returns (existing_signal, True) if already shared without creating duplicate row.
    """
    scan = get_scan_by_id(scan_id, db_path)

    if not scan:
        raise ValueError("Source scan record not found.")

    if not scan.get("diagnosis_reliable"):
        raise ValueError("Uncertain diagnoses are caught by the Safe Diagnosis Gate and cannot be submitted as community signals.")

    if scan.get("is_healthy"):
        raise ValueError("Healthy crop assessments cannot be submitted as disease signals.")

    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # Duplicate Protection Check: Lookup by source_scan_id
    cursor.execute("SELECT * FROM community_signals WHERE source_scan_id = ?", (scan_id,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return _row_to_signal_dict(existing), True # Already shared

    # Coordinate Coarsening for Storage (1 decimal place)
    c_lat = round(float(approx_lat), 1) if approx_lat is not None else 30.4
    c_lon = round(float(approx_lon), 1) if approx_lon is not None else 76.8

    created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    area_name = scan.get("location_name") or "Local District"

    try:
        cursor.execute("""
        INSERT INTO community_signals (
            created_at, source_scan_id, crop, class_name, condition, area_name,
            approx_lat, approx_lon, symptom_agreement, field_concern, weather_favorability, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'reported_signal')
        """, (
            created_at,
            scan_id,
            scan["crop"],
            scan["class_name"],
            scan["condition"],
            area_name,
            c_lat,
            c_lon,
            scan.get("symptom_agreement"),
            scan.get("field_concern"),
            scan.get("weather_favorability")
        ))

        signal_id = cursor.lastrowid

        # Update scan record community_shared flag
        cursor.execute("UPDATE scans SET community_shared = 1 WHERE id = ?", (scan_id,))
        conn.commit()

        cursor.execute("SELECT * FROM community_signals WHERE id = ?", (signal_id,))
        row = cursor.fetchone()
        conn.close()

        return _row_to_signal_dict(row), False # Newly created
    except sqlite3.IntegrityError:
        # Fallback if race condition triggers UNIQUE constraint
        cursor.execute("SELECT * FROM community_signals WHERE source_scan_id = ?", (scan_id,))
        row = cursor.fetchone()
        conn.close()
        return _row_to_signal_dict(row), True


def get_community_signals(limit: int = 50, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves public community disease signals. Public APIs use map_lat and map_lon (1 decimal coarsening)."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM community_signals ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()

    return [_row_to_signal_dict(row) for row in rows]


def get_community_summary(db_path: Optional[str] = None) -> Dict[str, Any]:
    """Calculates safe aggregate community disease signal statistics."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # Total reported signals
    cursor.execute("SELECT COUNT(*) FROM community_signals")
    total_signals = cursor.fetchone()[0]

    # Signals in last 7 days
    seven_days_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("SELECT COUNT(*) FROM community_signals WHERE created_at >= ?", (seven_days_ago,))
    signals_7d = cursor.fetchone()[0]

    # Most reported disease condition
    cursor.execute("""
    SELECT condition, COUNT(*) as cnt FROM community_signals
    GROUP BY condition ORDER BY cnt DESC LIMIT 1
    """)
    top_row = cursor.fetchone()
    top_condition = top_row["condition"] if top_row else "None reported"

    # Area breakdown
    cursor.execute("""
    SELECT area_name, condition, COUNT(*) as cnt FROM community_signals
    GROUP BY area_name, condition ORDER BY cnt DESC LIMIT 10
    """)
    area_rows = cursor.fetchall()
    conn.close()

    area_breakdown = [
        {
            "area_name": row["area_name"],
            "condition": row["condition"],
            "reported_signals": row["cnt"]
        }
        for row in area_rows
    ]

    return {
        "status": "success",
        "total_reported_signals": total_signals,
        "signals_last_7_days": signals_7d,
        "most_reported_condition": top_condition,
        "area_breakdown": area_breakdown,
        "disclaimer": "Community signals represent anonymized user reports and are not laboratory-confirmed disease cases."
    }


def get_community_radar(mode: str = 'live', days: int = 7, crop: str = 'All', condition: Optional[str] = None, db_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Returns anonymized, area-aggregated Community Disease Radar intelligence.
    Supports live SQLite signals and synthetic Demo Mode signals.
    """
    mode = mode.lower() if mode else 'live'

    if mode == 'demo':
        from demo_community_data import get_demo_signals
        raw_signals = get_demo_signals()
    else:
        raw_signals = get_community_signals(limit=500, db_path=db_path)

    now = datetime.utcnow()

    # Filter signals by time window and crop
    filtered = []
    for sig in raw_signals:
        created_str = sig["created_at"]
        try:
            created_dt = datetime.strptime(created_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            created_dt = now

        if days > 0:
            cutoff = now - timedelta(days=days)
            if created_dt < cutoff:
                continue

        # Crop Filter
        if crop and crop.lower() != 'all':
            if sig["crop"].lower() != crop.lower():
                continue

        # Condition Filter
        if condition and condition.strip():
            if sig["class_name"].lower() != condition.strip().lower():
                continue

        filtered.append((sig, created_dt))

    # 1. Area Clustering & Activity Level calculation
    areas_map: Dict[str, Dict[str, Any]] = {}
    for sig, created_dt in filtered:
        area_key = f"{sig['area_name']}_{sig.get('map_lat', 30.4)}_{sig.get('map_lon', 76.8)}"
        if area_key not in areas_map:
            areas_map[area_key] = {
                "area_name": sig["area_name"],
                "map_lat": sig.get("map_lat", 30.4),
                "map_lon": sig.get("map_lon", 76.8),
                "signal_count": 0,
                "conditions_count": {},
                "last_signal_at": sig["created_at"],
                "_last_dt": created_dt
            }

        item = areas_map[area_key]
        item["signal_count"] += 1

        cond_key = f"{sig['crop']}|||{sig['condition']}"
        item["conditions_count"][cond_key] = item["conditions_count"].get(cond_key, 0) + 1

        if created_dt > item["_last_dt"]:
            item["last_signal_at"] = sig["created_at"]
            item["_last_dt"] = created_dt

    areas_list = []
    for item in areas_map.values():
        cnt = item["signal_count"]
        if cnt >= 4:
            act_level = "ELEVATED"
        elif cnt >= 2:
            act_level = "MODERATE"
        else:
            act_level = "LOW"

        cond_list = []
        for ck, count in item["conditions_count"].items():
            crp, cond = ck.split("|||", 1)
            cond_list.append({"crop": crp, "condition": cond, "count": count})
        cond_list.sort(key=lambda x: x["count"], reverse=True)

        areas_list.append({
            "area_name": item["area_name"],
            "map_lat": item["map_lat"],
            "map_lon": item["map_lon"],
            "signal_count": cnt,
            "activity_level": act_level,
            "conditions": cond_list,
            "last_signal_at": item["last_signal_at"]
        })

    areas_list.sort(key=lambda x: x["signal_count"], reverse=True)

    # 2. Daily Trend calculation
    trend_map: Dict[str, int] = {}
    for sig, created_dt in filtered:
        d_str = created_dt.strftime("%Y-%m-%d")
        trend_map[d_str] = trend_map.get(d_str, 0) + 1

    sorted_dates = sorted(trend_map.keys())
    daily_trend = [{"date": d, "signals": trend_map[d]} for d in sorted_dates]

    # 3. Crop Breakdown & Summary
    crop_map: Dict[str, int] = {}
    cond_map: Dict[str, int] = {}
    for sig, _ in filtered:
        crp = sig["crop"]
        cnd = sig["condition"]
        crop_map[crp] = crop_map.get(crp, 0) + 1
        cond_map[cnd] = cond_map.get(cnd, 0) + 1

    crop_breakdown = [{"crop": c, "signals": count} for c, count in sorted(crop_map.items(), key=lambda x: x[1], reverse=True)]

    top_crop = max(crop_map.items(), key=lambda x: x[1])[0] if crop_map else "None"
    top_condition = max(cond_map.items(), key=lambda x: x[1])[0] if cond_map else "None"

    recent_signals = [sig for sig, _ in sorted(filtered, key=lambda x: x[1], reverse=True)[:10]]

    return {
        "status": "success",
        "mode": mode,
        "filters": {
            "days": days,
            "crop": crop,
            "condition": condition
        },
        "summary": {
            "total_signals": len(filtered),
            "active_areas": len(areas_list),
            "most_reported_crop": top_crop,
            "most_reported_condition": top_condition
        },
        "areas": areas_list,
        "daily_trend": daily_trend,
        "crop_breakdown": crop_breakdown,
        "recent_signals": recent_signals,
        "disclaimer": "Map locations are coarsened for farmer privacy. Signals represent community-reported assessments, not laboratory-confirmed cases."
    }


def _row_to_scan_dict(row: sqlite3.Row) -> Dict[str, Any]:
    keys = row.keys()
    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "crop": row["crop"],
        "class_name": row["class_name"],
        "condition": row["condition"],
        "model_confidence": row["model_confidence"],
        "is_healthy": bool(row["is_healthy"]),
        "diagnosis_reliable": bool(row["diagnosis_reliable"]) if "diagnosis_reliable" in keys else True,
        "symptom_agreement": row["symptom_agreement"],
        "symptom_match_score": row["symptom_match_score"],
        "field_concern": row["field_concern"],
        "weather_favorability": row["weather_favorability"],
        "location_name": row["location_name"],
        "community_shared": bool(row["community_shared"])
    }


def _row_to_signal_dict(row: sqlite3.Row) -> Dict[str, Any]:
    """
    Converts SQLite row to sanitized public signal dict.
    Hardened Privacy: Coarsens map coordinates to 1 decimal place max (map_lat, map_lon).
    Contains ZERO image fields, ZERO raw lat/lon, ZERO personal identifiers.
    """
    raw_lat = row["approx_lat"]
    raw_lon = row["approx_lon"]

    map_lat = round(float(raw_lat), 1) if raw_lat is not None else 30.4
    map_lon = round(float(raw_lon), 1) if raw_lon is not None else 76.8

    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "crop": row["crop"],
        "class_name": row["class_name"],
        "condition": row["condition"],
        "area_name": row["area_name"],
        "map_lat": map_lat,
        "map_lon": map_lon,
        "symptom_agreement": row["symptom_agreement"],
        "field_concern": row["field_concern"],
        "weather_favorability": row["weather_favorability"],
        "status": row["status"]
    }
