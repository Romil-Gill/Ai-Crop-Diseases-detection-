"""
FasalRakshak AI - SQLite Persistence Layer
Handles local scan history persistence and anonymized community disease signals.
Privacy Enforcement: Raw GPS coordinates are coarsened to 2 decimal places max; images are never transmitted.
"""

import sqlite3
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fasalrakshak.db")


def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    path = db_path or DEFAULT_DB_PATH
    conn = sqlite3.connect(path, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Optional[str] = None):
    """Initializes SQLite tables automatically if they do not exist."""
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
        symptom_agreement TEXT,
        symptom_match_score REAL,
        field_concern TEXT,
        weather_favorability TEXT,
        location_name TEXT,
        community_shared INTEGER DEFAULT 0
    );
    """)

    # 2. Community Signals Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS community_signals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        source_scan_id INTEGER NOT NULL,
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
        FOREIGN KEY (source_scan_id) REFERENCES scans (id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()


def create_scan(data: Dict[str, Any], db_path: Optional[str] = None) -> Dict[str, Any]:
    """Inserts a new reliable assessment scan record."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO scans (
        created_at, crop, class_name, condition, model_confidence, is_healthy,
        symptom_agreement, symptom_match_score, field_concern, weather_favorability,
        location_name, community_shared
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
    """, (
        created_at,
        data.get("crop"),
        data.get("class_name"),
        data.get("condition"),
        float(data.get("model_confidence", 0.0)),
        1 if data.get("is_healthy") else 0,
        data.get("symptom_agreement"),
        float(data["symptom_match_score"]) if data.get("symptom_match_score") is not None else None,
        data.get("field_concern"),
        data.get("weather_favorability"),
        data.get("location_name", "Local Field")
    ))

    scan_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return get_scan_by_id(scan_id, db_path)


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
    """Deletes a scan record by ID."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM scans WHERE id = ?", (scan_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()

    return deleted


def create_community_signal(scan_id: int, approx_lat: Optional[float] = None, approx_lon: Optional[float] = None, db_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Opt-in sharing: Creates an anonymized community disease signal from a reliable disease scan.
    Coarsens latitude and longitude to 2 decimal places for privacy protection.
    """
    scan = get_scan_by_id(scan_id, db_path)

    if not scan:
        raise ValueError("Source scan record not found.")

    if scan.get("is_healthy"):
        raise ValueError("Healthy crop assessments cannot be submitted as disease signals.")

    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # Check if already shared
    cursor.execute("SELECT * FROM community_signals WHERE source_scan_id = ?", (scan_id,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return _row_to_signal_dict(existing)

    # Privacy Coarsening: Round lat/lon to 2 decimal places max
    c_lat = round(float(approx_lat), 2) if approx_lat is not None else 30.38
    c_lon = round(float(approx_lon), 2) if approx_lon is not None else 76.78

    created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    area_name = scan.get("location_name") or "Local District"

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

    return _row_to_signal_dict(row)


def get_community_signals(limit: int = 50, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves sanitized community disease signals. Never returns precise GPS or raw image paths."""
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


def _row_to_scan_dict(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "crop": row["crop"],
        "class_name": row["class_name"],
        "condition": row["condition"],
        "model_confidence": row["model_confidence"],
        "is_healthy": bool(row["is_healthy"]),
        "symptom_agreement": row["symptom_agreement"],
        "symptom_match_score": row["symptom_match_score"],
        "field_concern": row["field_concern"],
        "weather_favorability": row["weather_favorability"],
        "location_name": row["location_name"],
        "community_shared": bool(row["community_shared"])
    }


def _row_to_signal_dict(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "source_scan_id": row["source_scan_id"],
        "crop": row["crop"],
        "class_name": row["class_name"],
        "condition": row["condition"],
        "area_name": row["area_name"],
        "approx_lat": row["approx_lat"],
        "approx_lon": row["approx_lon"],
        "symptom_agreement": row["symptom_agreement"],
        "field_concern": row["field_concern"],
        "weather_favorability": row["weather_favorability"],
        "status": row["status"]
    }
