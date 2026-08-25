from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os
import json
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
frontend_origin = os.environ.get("FRONTEND_ORIGIN")
if frontend_origin:
    CORS(app, resources={r"/*": {"origins": [frontend_origin, "http://localhost:5173", "http://127.0.0.1:5173"]}})
else:
    CORS(app)

# Configuration
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp'}
MIN_CONFIDENCE_THRESHOLD = 50.0  # Percentage
MIN_MARGIN_THRESHOLD = 10.0      # Top-1 vs Top-2 percentage margin

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB max upload size
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File too large. Maximum upload size is 10 MB."}), 413

# Load pre-trained model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_V2_PATH = os.path.join(BASE_DIR, "crop_disease_model_v2_6crop.keras")
MODEL_V1_PATH = os.path.join(BASE_DIR, "crop_disease_model.keras")
MAPPING_V2_PATH = os.path.join(BASE_DIR, "class_mapping_v2.json")

ORIGINAL_27_CLASSES = [
    'Pumpkin-Bacterial Leaf Spot', 'Pumpkin-Downy Mildew', 'Pumpkin-Healthy Leaf', 
    'Pumpkin-Mosaic Disease', 'Pumpkin-Powdery_Mildew', 'Rice-Bacterialblight', 
    'Rice-Brownspot', 'Rice-Leafsmut', 'Sugarcane-Grassy Shoot', 'Sugarcane-Healthy', 
    'Sugarcane-Mosaic', 'Sugarcane-Pokkah Boeng', 'Sugarcane-Red Leaf Spot', 
    'Sugarcane-Red Rot', 'Sugarcane-Ring Spot', 'Sugarcane-Wilt', 
    'Sugarcane-Yellow Leaf Disease', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 
    'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 
    'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
]

model = None
IS_V2_ACTIVE = False
V2_ERROR = None

if os.path.exists(MODEL_V2_PATH):
    try:
        try:
            model = tf.keras.models.load_model(MODEL_V2_PATH, compile=False)
        except Exception as inner_e:
            model = tf.keras.models.load_model(MODEL_V2_PATH)
            
        if model.output_shape[-1] == 36 and os.path.exists(MAPPING_V2_PATH):
            with open(MAPPING_V2_PATH, "r", encoding="utf-8") as f:
                mapping_dict = json.load(f)
                class_names = [mapping_dict[str(i)] for i in range(len(mapping_dict))]
            IS_V2_ACTIVE = True
            print(f"V2 Model loaded successfully from {MODEL_V2_PATH} ({len(class_names)} classes).")
        else:
            model = None
            IS_V2_ACTIVE = False
            V2_ERROR = f"Output shape mismatch: {model.output_shape if model else None} or mapping missing: {os.path.exists(MAPPING_V2_PATH)}"
    except Exception as e:
        print(f"WARNING: Unable to load V2 model ({e}), falling back to V1...")
        V2_ERROR = str(e)
        model = None
        IS_V2_ACTIVE = False
else:
    V2_ERROR = f"MODEL_V2_PATH does not exist at {MODEL_V2_PATH}"

if model is None and os.path.exists(MODEL_V1_PATH):
    try:
        model = tf.keras.models.load_model(MODEL_V1_PATH)
        class_names = ORIGINAL_27_CLASSES
        IS_V2_ACTIVE = False
        print(f"V1 Production Model loaded successfully from {MODEL_V1_PATH} ({len(class_names)} classes).")
    except Exception as e:
        print(f"ERROR loading V1 model: {e}")
        class_names = ORIGINAL_27_CLASSES
        IS_V2_ACTIVE = False
else:
    if model is None:
        class_names = ORIGINAL_27_CLASSES
        IS_V2_ACTIVE = False

SUPPORTED_CROPS = ["Pumpkin", "Rice", "Sugarcane", "Tomato", "Wheat", "Maize"] if IS_V2_ACTIVE else ["Pumpkin", "Rice", "Sugarcane", "Tomato"]

HUMAN_CONDITION_MAP = {
    "bacterialblight": "Bacterial Blight",
    "downymildew": "Downy Mildew",
    "mosaicdisease": "Mosaic Disease",
    "powderymildew": "Powdery Mildew",
    "brownspot": "Brown Spot",
    "leafsmut": "Leaf Smut",
    "bacterial spot": "Bacterial Spot",
    "early blight": "Early Blight",
    "late blight": "Late Blight",
    "leaf mold": "Leaf Mold",
    "septoria leaf spot": "Septoria Leaf Spot",
    "spider mites two-spotted spider mite": "Spider Mites (Two-Spotted)",
    "target spot": "Target Spot",
    "tomato yellow leaf curl virus": "Yellow Leaf Curl Virus",
    "tomato mosaic virus": "Mosaic Virus",
    "pokkah boeng": "Pokkah Boeng",
    "red leaf spot": "Red Leaf Spot",
    "red rot": "Red Rot",
    "ring spot": "Ring Spot",
    "yellow leaf disease": "Yellow Leaf Disease",
    "grassy shoot": "Grassy Shoot",
    "leaf rust": "Leaf Rust",
    "stripe rust": "Stripe Rust",
    "septoria": "Septoria Leaf Spot",
    "common rust": "Common Rust",
    "northern leaf blight": "Northern Leaf Blight",
    "gray leaf spot": "Gray Leaf Spot",
    "healthy": "Healthy"
}

def parse_class_info(class_name):
    """Parses a class string into crop, condition, and healthy status with human-readable formatting."""
    if '___' in class_name:
        crop, condition_raw = class_name.split('___', 1)
    elif '-' in class_name:
        crop, condition_raw = class_name.split('-', 1)
    else:
        crop, condition_raw = "Unknown", class_name
    
    crop = crop.strip()
    cond_clean = condition_raw.replace('_', ' ').strip()
    cond_lower = cond_clean.lower()
    
    condition = HUMAN_CONDITION_MAP.get(cond_lower, cond_clean.title())
    is_healthy = 'healthy' in cond_lower
    return crop, condition, is_healthy

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_and_predict(filepath):
    """
    Preprocesses an image (224x224 RGB, / 255.0) and passes it through model.
    Returns sorted list of dicts with predictions.
    """
    img = image.load_img(filepath, target_size=(224, 224))
    img_array = image.img_to_array(img)
    if IS_V2_ACTIVE:
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(np.expand_dims(img_array, axis=0))
    else:
        img_array = np.expand_dims(img_array, axis=0) / 255.0

    predictions = model.predict(img_array)[0]
    
    results = []
    for idx, prob in enumerate(predictions):
        conf_pct = float(prob * 100)
        c_name = class_names[idx]
        crop, condition, is_healthy = parse_class_info(c_name)
        results.append({
            "class_name": c_name,
            "crop": crop,
            "condition": condition,
            "confidence": round(conf_pct, 2),
            "is_healthy": is_healthy
        })
    
    # Sort descending by confidence
    results.sort(key=lambda x: x['confidence'], reverse=True)
    return results

# Legacy predict function for Jinja frontend
def predict_image(img_path):
    results = process_and_predict(img_path)
    top = results[0]
    return top["class_name"], top["confidence"]

# --- LEGACY PAGE ROUTES ---

@app.route('/')
def home():
    return render_template('index.html', page_name='home')

@app.route('/detect')
def detect():
    return render_template('detect.html', page_name='detect')

@app.route('/history')
def history():
    return render_template('history.html', page_name='history')

@app.route('/contact')
def contact():
    return render_template('contact.html', page_name='contact')

# --- LEGACY API ENDPOINT ---

@app.route('/predict', methods=['POST'])
def predict_api():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            result, confidence = predict_image(filepath)
            return jsonify({
                "prediction": result,
                "confidence": round(confidence, 2),
                "status": "success"
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

# --- NEW REST API ENDPOINTS (FasalRakshak AI Phase 1A/1B) ---

from advisory_data import ADVISORY_DATABASE
from symptom_data import SYMPTOM_QUESTIONS, FIELD_SPREAD_OPTIONS, evaluate_symptom_verification
from weather_service import search_location, fetch_weather_context
from treatment_data import get_treatment_options
import database

# Initialize SQLite database tables automatically
try:
    database.init_db()
except Exception as e:
    print(f"[DATABASE WARNING] SQLite init_db warning: {e}")

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "is_v2_active": IS_V2_ACTIVE,
        "v2_error": V2_ERROR if 'V2_ERROR' in globals() else None,
        "total_classes": len(class_names),
        "supported_crops": SUPPORTED_CROPS
    }), 200

@app.route('/api/location-search', methods=['GET'])
def api_location_search():
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return jsonify({
            "status": "success",
            "results": []
        }), 200

    results = search_location(q)
    return jsonify({
        "status": "success",
        "query": q,
        "results": results
    }), 200

@app.route('/api/weather-context', methods=['GET'])
def api_weather_context():
    lat_raw = request.args.get('latitude')
    lon_raw = request.args.get('longitude')
    c_name = request.args.get('class_name')
    loc_name = request.args.get('location_name')

    if not lat_raw or not lon_raw or not c_name:
        return jsonify({
            "error": "Missing required query parameters: 'latitude', 'longitude', and 'class_name'."
        }), 400

    c_name = c_name.strip()
    if c_name not in class_names:
        return jsonify({
            "error": f"Unsupported or invalid class_name '{c_name}'."
        }), 400

    try:
        lat = float(lat_raw)
        lon = float(lon_raw)
    except ValueError:
        return jsonify({
            "error": f"Invalid numeric format for latitude ('{lat_raw}') or longitude ('{lon_raw}')."
        }), 400

    if not (-90.0 <= lat <= 90.0) or not (-180.0 <= lon <= 180.0):
        return jsonify({
            "error": "Latitude must be between -90 and 90, Longitude between -180 and 180."
        }), 400

    res = fetch_weather_context(lat, lon, c_name, location_name=loc_name)
    return jsonify(res), 200

# --- SCAN HISTORY & COMMUNITY SIGNALS ENDPOINTS (FasalRakshak AI Phase 6) ---

@app.route('/api/scans', methods=['POST'])
def api_save_scan():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    c_name = data.get('class_name')
    if not c_name or c_name not in class_names:
        return jsonify({"error": f"Invalid or unsupported class_name '{c_name}'."}), 400

    if data.get('diagnosis_reliable') is False or data.get('diagnosis_reliable') == 0:
        return jsonify({"error": "Uncertain diagnoses are caught by the Safe Diagnosis Gate and cannot be saved to history."}), 400

    try:
        scan_record = database.create_scan(data)
        return jsonify({
            "status": "success",
            "message": "Assessment record saved successfully.",
            "scan": scan_record
        }), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Assessment could not be saved ({str(e)})."
        }), 500

@app.route('/api/scans', methods=['GET'])
def api_get_scans():
    crop_filter = request.args.get('crop')
    try:
        scans = database.get_scans(crop_filter=crop_filter)
        return jsonify({
            "status": "success",
            "total": len(scans),
            "scans": scans
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve scan history ({str(e)})."}), 500

@app.route('/api/scans/<int:scan_id>', methods=['GET'])
def api_get_scan_by_id(scan_id):
    try:
        scan = database.get_scan_by_id(scan_id)
        if not scan:
            return jsonify({"error": f"Scan record #{scan_id} not found."}), 404
        return jsonify({"status": "success", "scan": scan}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve scan ({str(e)})."}), 500

@app.route('/api/scans/<int:scan_id>', methods=['DELETE'])
def api_delete_scan(scan_id):
    try:
        deleted = database.delete_scan(scan_id)
        if not deleted:
            return jsonify({"error": f"Scan record #{scan_id} not found."}), 404
        return jsonify({"status": "success", "message": f"Scan #{scan_id} deleted."}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to delete scan ({str(e)})."}), 500

@app.route('/api/community-signals', methods=['POST'])
def api_create_community_signal():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    scan_id = data.get('scan_id')
    if not scan_id:
        return jsonify({"error": "Missing required field 'scan_id'"}), 400

    approx_lat = data.get('approx_lat')
    approx_lon = data.get('approx_lon')

    try:
        signal, already_shared = database.create_community_signal(int(scan_id), approx_lat=approx_lat, approx_lon=approx_lon)
        if already_shared:
            return jsonify({
                "status": "already_shared",
                "already_shared": True,
                "message": "Signal has already been shared for this scan assessment.",
                "signal": signal
            }), 200
        return jsonify({
            "status": "success",
            "already_shared": False,
            "message": "Anonymized community disease signal shared successfully.",
            "signal": signal
        }), 201
    except ValueError as ve:
        err_msg = str(ve)
        status_code = 404 if "not found" in err_msg.lower() else 400
        return jsonify({"error": err_msg}), status_code
    except Exception as e:
        return jsonify({"error": f"Failed to share community signal ({str(e)})."}), 500

@app.route('/api/community-signals', methods=['GET'])
def api_get_community_signals():
    try:
        signals = database.get_community_signals()
        return jsonify({
            "status": "success",
            "total": len(signals),
            "signals": signals
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve community signals ({str(e)})."}), 500

@app.route('/api/community-summary', methods=['GET'])
def api_get_community_summary():
    try:
        summary = database.get_community_summary()
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve community summary ({str(e)})."}), 500

@app.route('/api/community-radar', methods=['GET'])
def api_get_community_radar():
    mode = request.args.get('mode', 'live')
    days_raw = request.args.get('days', '7')
    crop = request.args.get('crop', 'All')
    condition = request.args.get('condition')

    try:
        days = int(days_raw)
    except ValueError:
        days = 7

    if crop and crop.lower() != 'all':
        valid_crops = {'tomato', 'rice', 'sugarcane', 'pumpkin'}
        if crop.lower() not in valid_crops:
            return jsonify({"error": f"Unsupported crop filter '{crop}'. Must be one of: Tomato, Rice, Sugarcane, Pumpkin, All."}), 400

    try:
        radar_data = database.get_community_radar(mode=mode, days=days, crop=crop, condition=condition)
        return jsonify(radar_data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve community radar ({str(e)})."}), 500

@app.route('/api/treatment-options', methods=['GET'])
def api_treatment_options():
    c_name = request.args.get('class_name')
    if not c_name:
        return jsonify({"error": "Missing required query parameter 'class_name'."}), 400

    c_name = c_name.strip()
    if c_name not in class_names:
        return jsonify({
            "error": f"Unsupported or invalid class_name '{c_name}'."
        }), 400

    treatment = get_treatment_options(c_name, diagnosis_reliable=True)
    return jsonify({
        "status": "success",
        "class_name": c_name,
        "treatment_options": treatment
    }), 200

@app.route('/api/symptom-questions', methods=['GET'])
def api_symptom_questions():
    c_name = request.args.get('class_name')
    if not c_name:
        return jsonify({"error": "Missing required query parameter 'class_name'"}), 400
    
    c_name = c_name.strip()
    if c_name not in class_names:
        return jsonify({
            "error": f"Unsupported or invalid class_name '{c_name}'. Must be one of the 27 model classes."
        }), 400

    questions = SYMPTOM_QUESTIONS.get(c_name, [])
    options_list = [
        {"id": k, "label": v["label"], "description": v["description"]}
        for k, v in FIELD_SPREAD_OPTIONS.items()
    ]

    return jsonify({
        "status": "success",
        "class_name": c_name,
        "questions": questions,
        "field_spread_options": options_list
    }), 200

@app.route('/api/verify-symptoms', methods=['POST'])
def api_verify_symptoms():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    c_name = data.get('class_name')
    answers = data.get('answers')
    field_spread = data.get('field_spread')

    if not c_name or c_name not in class_names:
        return jsonify({
            "error": f"Unsupported or invalid class_name '{c_name}'."
        }), 400

    if answers is not None and not isinstance(answers, dict):
        return jsonify({"error": "'answers' must be a dictionary object"}), 400

    if answers:
        for q_id, val in answers.items():
            if str(val).lower() not in ("yes", "no", "unsure"):
                return jsonify({
                    "error": f"Invalid answer value '{val}' for question '{q_id}'. Allowed: 'yes', 'no', 'unsure'."
                }), 400

    if field_spread and str(field_spread).lower() not in FIELD_SPREAD_OPTIONS:
        return jsonify({
            "error": f"Invalid field_spread value '{field_spread}'. Allowed: {list(FIELD_SPREAD_OPTIONS.keys())}"
        }), 400

    res = evaluate_symptom_verification(c_name, answers or {}, field_spread or "unsure")
    res["status"] = "success"
    res["class_name"] = c_name

    return jsonify(res), 200

@app.route('/api/advisory', methods=['GET'])
def api_advisory():
    c_name = request.args.get('class_name')
    if not c_name:
        return jsonify({"error": "Missing required query parameter 'class_name'"}), 400
    
    c_name = c_name.strip()
    if c_name not in ADVISORY_DATABASE:
        return jsonify({
            "error": f"Unsupported or invalid class_name '{c_name}'. Must be one of the 27 model classes."
        }), 400

    item = ADVISORY_DATABASE[c_name]
    return jsonify({
        "status": "success",
        "class_name": item["class_name"],
        "crop": item["crop"],
        "condition": item["condition"],
        "is_healthy": item["is_healthy"],
        "advisory": {
            "overview": item["overview"],
            "common_symptoms": item["common_symptoms"],
            "immediate_actions": item["immediate_actions"],
            "prevention": item["prevention"],
            "monitoring": item["monitoring"],
            "expert_escalation": item["expert_escalation"]
        },
        "sources": item["sources"]
    }), 200

@app.route('/api/classes', methods=['GET'])
def api_classes():
    crops_map = {crop: [] for crop in SUPPORTED_CROPS}
    for c_name in class_names:
        crop, condition, is_healthy = parse_class_info(c_name)
        if crop in crops_map:
            crops_map[crop].append({
                "class_name": c_name,
                "condition": condition,
                "is_healthy": is_healthy
            })
    
    return jsonify({
        "crops": crops_map,
        "supported_crops": SUPPORTED_CROPS,
        "total_classes": len(class_names)
    }), 200

@app.route('/api/predict', methods=['POST'])
def api_predict():
    if model is None:
        return jsonify({"error": "ML model is not loaded"}), 500

    if 'file' not in request.files:
        return jsonify({"error": "No image file provided in request"}), 400
    
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({"error": "No image file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": f"Invalid file type. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}"}), 400

    # User selected crop (optional in request, but evaluated against prediction if provided)
    selected_crop = request.form.get('selected_crop') or request.args.get('selected_crop')
    if selected_crop:
        selected_crop = selected_crop.strip()
        matched_crop = next((c for c in SUPPORTED_CROPS if c.lower() == selected_crop.lower()), None)
        if not matched_crop:
            return jsonify({
                "error": f"Unsupported selected_crop '{selected_crop}'. Supported crops: {', '.join(SUPPORTED_CROPS)}"
            }), 400
        selected_crop = matched_crop

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Validate image file readability/integrity
    try:
        with Image.open(filepath) as img_check:
            img_check.verify()
    except Exception:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"error": "Uploaded file is not a valid or readable image"}), 400

    try:
        all_preds = process_and_predict(filepath)
        top1 = all_preds[0]
        top2 = all_preds[1] if len(all_preds) > 1 else None
        top3 = all_preds[:3]

        # Safe Diagnosis Gate Evaluation
        diagnosis_reliable = True
        uncertainty_reason = None

        top1_conf = top1["confidence"]
        top2_conf = top2["confidence"] if top2 else 0.0
        margin = top1_conf - top2_conf

        # Gate 1: Selected crop alignment
        if selected_crop and top1["crop"].lower() != selected_crop.lower():
            diagnosis_reliable = False
            uncertainty_reason = f"Predicted crop ({top1['crop']}) does not match user-selected crop ({selected_crop})."
        
        # Gate 2: Confidence threshold
        elif top1_conf < MIN_CONFIDENCE_THRESHOLD:
            diagnosis_reliable = False
            uncertainty_reason = f"Prediction confidence ({top1_conf:.1f}%) is below minimum threshold ({MIN_CONFIDENCE_THRESHOLD}%)."

        # Gate 3: Confidence margin threshold
        elif margin < MIN_MARGIN_THRESHOLD:
            diagnosis_reliable = False
            uncertainty_reason = f"High prediction ambiguity (confidence margin between top predictions is only {margin:.1f}%)."

        status = "success" if diagnosis_reliable else "uncertain"

        top_predictions_formatted = [
            {
                "class_name": p["class_name"],
                "crop": p["crop"],
                "condition": p["condition"],
                "confidence": p["confidence"]
            }
            for p in top3
        ]

        treatment_options = get_treatment_options(top1["class_name"], diagnosis_reliable=diagnosis_reliable)

        return jsonify({
            "status": status,
            "selected_crop": selected_crop,
            "prediction": {
                "class_name": top1["class_name"],
                "crop": top1["crop"],
                "condition": top1["condition"],
                "confidence": top1["confidence"]
            },
            "top_predictions": top_predictions_formatted,
            "diagnosis_reliable": diagnosis_reliable,
            "uncertainty_reason": uncertainty_reason,
            "is_healthy": top1["is_healthy"],
            "treatment_options": treatment_options
        }), 200

    except Exception as e:
        return jsonify({"error": f"Model inference error: {str(e)}"}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

from gradcam import generate_gradcam

@app.route('/api/explain', methods=['POST'])
def api_explain():
    if model is None:
        return jsonify({"error": "ML model is not loaded"}), 500

    if 'file' not in request.files:
        return jsonify({"error": "No image file provided in request"}), 400
    
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({"error": "No image file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": f"Invalid file type. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}"}), 400

    selected_crop = request.form.get('selected_crop') or request.args.get('selected_crop')
    if selected_crop:
        selected_crop = selected_crop.strip()
        matched_crop = next((c for c in SUPPORTED_CROPS if c.lower() == selected_crop.lower()), None)
        if not matched_crop:
            return jsonify({
                "error": f"Unsupported selected_crop '{selected_crop}'. Supported crops: {', '.join(SUPPORTED_CROPS)}"
            }), 400
        selected_crop = matched_crop

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        with Image.open(filepath) as img_check:
            img_check.verify()
    except Exception:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"error": "Uploaded file is not a valid or readable image"}), 400

    try:
        pil_img = Image.open(filepath).convert('RGB')
        img = image.load_img(filepath, target_size=(224, 224))
        img_array = image.img_to_array(img)
        if IS_V2_ACTIVE:
            img_array = tf.keras.applications.mobilenet_v2.preprocess_input(np.expand_dims(img_array, axis=0))
        else:
            img_array = np.expand_dims(img_array, axis=0) / 255.0

        predictions = model.predict(img_array)[0]
        
        all_preds = []
        for idx, prob in enumerate(predictions):
            conf_pct = float(prob * 100)
            c_name = class_names[idx]
            crop, condition, is_healthy = parse_class_info(c_name)
            all_preds.append({
                "index": idx,
                "class_name": c_name,
                "crop": crop,
                "condition": condition,
                "confidence": round(conf_pct, 2),
                "is_healthy": is_healthy
            })
        
        all_preds.sort(key=lambda x: x['confidence'], reverse=True)
        top1 = all_preds[0]
        top2 = all_preds[1] if len(all_preds) > 1 else None
        top3 = all_preds[:3]

        diagnosis_reliable = True
        uncertainty_reason = None

        top1_conf = top1["confidence"]
        top2_conf = top2["confidence"] if top2 else 0.0
        margin = top1_conf - top2_conf

        if selected_crop and top1["crop"].lower() != selected_crop.lower():
            diagnosis_reliable = False
            uncertainty_reason = f"Predicted crop ({top1['crop']}) does not match user-selected crop ({selected_crop})."
        elif top1_conf < MIN_CONFIDENCE_THRESHOLD:
            diagnosis_reliable = False
            uncertainty_reason = f"Prediction confidence ({top1_conf:.1f}%) is below minimum threshold ({MIN_CONFIDENCE_THRESHOLD}%)."
        elif margin < MIN_MARGIN_THRESHOLD:
            diagnosis_reliable = False
            uncertainty_reason = f"High prediction ambiguity (confidence margin between top predictions is only {margin:.1f}%)."

        status = "success" if diagnosis_reliable else "uncertain"

        top_predictions_formatted = [
            {
                "class_name": p["class_name"],
                "crop": p["crop"],
                "condition": p["condition"],
                "confidence": p["confidence"]
            }
            for p in top3
        ]

        explanation = None
        advisory_info = None

        if diagnosis_reliable:
            explanation = generate_gradcam(
                model=model,
                img_array=img_array,
                target_class_idx=top1["index"],
                original_pil_image=pil_img
            )
            adv_raw = ADVISORY_DATABASE.get(top1["class_name"])
            if adv_raw:
                advisory_info = {
                    "overview": adv_raw["overview"],
                    "common_symptoms": adv_raw["common_symptoms"],
                    "immediate_actions": adv_raw["immediate_actions"],
                    "prevention": adv_raw["prevention"],
                    "monitoring": adv_raw["monitoring"],
                    "expert_escalation": adv_raw["expert_escalation"],
                    "sources": adv_raw["sources"]
                }

        return jsonify({
            "status": status,
            "selected_crop": selected_crop,
            "prediction": {
                "class_name": top1["class_name"],
                "crop": top1["crop"],
                "condition": top1["condition"],
                "confidence": top1["confidence"]
            },
            "top_predictions": top_predictions_formatted,
            "diagnosis_reliable": diagnosis_reliable,
            "uncertainty_reason": uncertainty_reason,
            "is_healthy": top1["is_healthy"],
            "explanation": explanation,
            "advisory": advisory_info
        }), 200

    except Exception as e:
        return jsonify({"error": f"Grad-CAM explanation error: {str(e)}"}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    use_reloader = os.environ.get("FLASK_RELOAD", "false").lower() == "true"
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode, use_reloader=use_reloader, port=5000)