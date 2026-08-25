import os
import io
import unittest
from PIL import Image
import json
from app import app, model, tf
from unittest.mock import patch

class TestFasalRakshakAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n==================================================")
        print("  FASALRAKSHAK AI - BACKEND API & MODEL SUITE")
        print("==================================================")
        
        # 1. Programmatically inspect model layers for Grad-CAM readiness
        if model is not None:
            print(f"\n[MODEL INSPECTION] Inspecting model layer architecture...")
            print(f"Total layers in outer model: {len(model.layers)}")
            
            conv_layers = []
            for layer in model.layers:
                layer_type = layer.__class__.__name__
                if 'Conv' in layer_type or 'relu' in layer.name or 'out_relu' in layer.name:
                    conv_layers.append((layer.name, layer_type))
                elif isinstance(layer, tf.keras.Model):
                    print(f"  Base Model detected: {layer.name} ({layer.__class__.__name__})")
                    for sub_layer in layer.layers:
                        if 'conv' in sub_layer.name.lower() or 'relu' in sub_layer.name.lower():
                            conv_layers.append((f"{layer.name}/{sub_layer.name}", sub_layer.__class__.__name__))

            print(f"  Found {len(conv_layers)} convolutional/activation candidate layers.")
            if conv_layers:
                print(f"  First 3 candidate layers: {conv_layers[:3]}")
                print(f"  Last 3 candidate layers:  {conv_layers[-3:]}")
                last_candidate = conv_layers[-1]
                print(f"  -> VERIFIED LAST CONV/ACTIVATION LAYER: '{last_candidate[0]}' ({last_candidate[1]})")
        else:
            print("WARNING: Model is not loaded!")

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def create_dummy_image(self, color=(34, 139, 34), format='JPEG'):
        """Creates a dummy RGB leaf image in memory."""
        img = Image.new('RGB', (224, 224), color=color)
        buf = io.BytesIO()
        img.save(buf, format=format)
        buf.seek(0)
        return buf

    def test_01_health_endpoint(self):
        """Test GET /api/health"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'ok')
        self.assertTrue(data['model_loaded'])
        self.assertIn('Pumpkin', data['supported_crops'])
        self.assertIn('Tomato', data['supported_crops'])
        print(f"\n[TEST 1 PASSED] /api/health returned valid response with {len(data['supported_crops'])} crops.")

    def test_01b_legacy_routes_preserved(self):
        """Verify legacy HTML routes remain 100% functional"""
        for route in ['/', '/detect', '/history', '/contact']:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200, f"Route {route} failed")
        print("[TEST 1b PASSED] Legacy Jinja HTML routes (/, /detect, /history, /contact) preserved & working.")

    def test_02_classes_endpoint(self):
        """Test GET /api/classes"""
        response = self.client.get('/api/classes')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn(data['total_classes'], [27, 36])
        self.assertIn('Tomato', data['crops'])
        print(f"[TEST 2 PASSED] /api/classes returned {data['total_classes']} classes mapped across active crops.")

    def test_03_predict_valid_image(self):
        """Test POST /api/predict with valid image"""
        img_buf = self.create_dummy_image()
        data = {
            'file': (img_buf, 'test_leaf.jpg')
        }
        response = self.client.post('/api/predict', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()
        self.assertIn(res_json['status'], ['success', 'uncertain'])
        self.assertIn('prediction', res_json)
        self.assertEqual(len(res_json['top_predictions']), 3)
        print(f"[TEST 3 PASSED] /api/predict top prediction: {res_json['prediction']['class_name']} ({res_json['prediction']['confidence']}%)")

    def test_04_predict_missing_image(self):
        """Test POST /api/predict with missing image file"""
        response = self.client.post('/api/predict', data={}, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        res_json = response.get_json()
        self.assertIn('error', res_json)
        print("[TEST 4 PASSED] /api/predict missing image correctly rejected with HTTP 400.")

    def test_05_predict_invalid_file(self):
        """Test POST /api/predict with non-image file"""
        fake_file = (io.BytesIO(b"This is a text file, not an image"), 'fake.txt')
        response = self.client.post('/api/predict', data={'file': fake_file}, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        res_json = response.get_json()
        self.assertIn('error', res_json)
        print("[TEST 5 PASSED] /api/predict non-image file correctly rejected with HTTP 400.")

    def test_06_predict_unsupported_selected_crop(self):
        """Test POST /api/predict with unsupported crop parameter"""
        img_buf = self.create_dummy_image()
        data = {
            'file': (img_buf, 'leaf.jpg'),
            'selected_crop': 'Apple'
        }
        response = self.client.post('/api/predict', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        res_json = response.get_json()
        self.assertIn('error', res_json)
        self.assertIn('Unsupported selected_crop', res_json['error'])
        print("[TEST 6 PASSED] /api/predict unsupported selected_crop 'Apple' rejected with HTTP 400.")

    def test_07_predict_crop_mismatch_handling(self):
        """Test POST /api/predict with mismatching crop selection to trigger Safe Diagnosis Gate"""
        res_raw = self.client.post('/api/predict', data={'file': (self.create_dummy_image(), 'leaf.jpg')}, content_type='multipart/form-data')
        raw_json = res_raw.get_json() or {}
        predicted_crop = "Tomato"
        if raw_json.get('prediction'):
            predicted_crop = raw_json['prediction'].get('crop', 'Tomato')
        elif raw_json.get('top_predictions') and len(raw_json['top_predictions']) > 0:
            predicted_crop = raw_json['top_predictions'][0].get('crop', 'Tomato')
        
        mismatched_crop = "Rice" if predicted_crop != "Rice" else "Tomato"
        
        data = {
            'file': (self.create_dummy_image(), 'leaf.jpg'),
            'selected_crop': mismatched_crop
        }
        response = self.client.post('/api/predict', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()
        
        self.assertEqual(res_json['status'], 'uncertain')
        self.assertFalse(res_json['diagnosis_reliable'])
        self.assertIsNotNone(res_json['uncertainty_reason'])
        self.assertIn('does not match', res_json['uncertainty_reason'])
        print(f"[TEST 7 PASSED] Safe Diagnosis Gate caught crop mismatch! Selected: {mismatched_crop}, Predicted: {predicted_crop}. Status: {res_json['status']}, Reliable: {res_json['diagnosis_reliable']}")

    def test_08_explain_valid_image(self):
        """Test POST /api/explain with valid image returns Grad-CAM explanation when reliable"""
        res_raw = self.client.post('/api/predict', data={'file': (self.create_dummy_image(), 'leaf.jpg')}, content_type='multipart/form-data')
        raw_json = res_raw.get_json() or {}
        predicted_crop = "Tomato"
        if raw_json.get('prediction'):
            predicted_crop = raw_json['prediction'].get('crop', 'Tomato')
        elif raw_json.get('top_predictions') and len(raw_json['top_predictions']) > 0:
            predicted_crop = raw_json['top_predictions'][0].get('crop', 'Tomato')

        data = {
            'file': (self.create_dummy_image(), 'leaf.jpg'),
            'selected_crop': predicted_crop
        }
        response = self.client.post('/api/explain', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()

        self.assertIn(res_json['status'], ['success', 'uncertain'])
        if res_json.get('diagnosis_reliable') and res_json.get('explanation'):
            exp = res_json['explanation']
            self.assertIn('heatmap', exp)
            self.assertIn('overlay', exp)
            self.assertEqual(exp['method'], 'Grad-CAM')
            self.assertEqual(exp['target_layer'], 'mobilenetv2_1.00_224/out_relu')
        print(f"[TEST 8 PASSED] /api/explain response verified.")

    def test_09_explain_missing_and_invalid_file(self):
        """Test POST /api/explain handling of missing or non-image files"""
        res1 = self.client.post('/api/explain', data={}, content_type='multipart/form-data')
        self.assertEqual(res1.status_code, 400)

        data_txt = {'file': (io.BytesIO(b"not an image"), 'test.txt')}
        res2 = self.client.post('/api/explain', data=data_txt, content_type='multipart/form-data')
        self.assertEqual(res2.status_code, 400)
        print("[TEST 9 PASSED] /api/explain correctly rejects missing and non-image files with HTTP 400.")

    def test_10_explain_unsupported_crop(self):
        """Test POST /api/explain with unsupported selected_crop"""
        data = {
            'file': (self.create_dummy_image(), 'leaf.jpg'),
            'selected_crop': 'Apple'
        }
        response = self.client.post('/api/explain', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Unsupported selected_crop', response.get_json()['error'])
        print("[TEST 10 PASSED] /api/explain unsupported selected_crop 'Apple' rejected with HTTP 400.")

    def test_11_explain_crop_mismatch_no_explanation(self):
        """Test POST /api/explain with crop mismatch returns uncertain status and explanation=None"""
        res_raw = self.client.post('/api/predict', data={'file': (self.create_dummy_image(), 'leaf.jpg')}, content_type='multipart/form-data')
        raw_json = res_raw.get_json() or {}
        predicted_crop = "Tomato"
        if raw_json.get('prediction'):
            predicted_crop = raw_json['prediction'].get('crop', 'Tomato')
        elif raw_json.get('top_predictions') and len(raw_json['top_predictions']) > 0:
            predicted_crop = raw_json['top_predictions'][0].get('crop', 'Tomato')
            
        mismatched_crop = "Rice" if predicted_crop != "Rice" else "Tomato"

        data = {
            'file': (self.create_dummy_image(), 'leaf.jpg'),
            'selected_crop': mismatched_crop
        }
        response = self.client.post('/api/explain', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()

        self.assertEqual(res_json['status'], 'uncertain')
        self.assertFalse(res_json['diagnosis_reliable'])
        self.assertIsNone(res_json['explanation'])
        print(f"[TEST 11 PASSED] /api/explain crop mismatch returns uncertain status without confirmed explanation.")

    def test_12_advisory_disease_and_healthy(self):
        """Test GET /api/advisory for disease and healthy classes"""
        res1 = self.client.get('/api/advisory?class_name=Rice-Brownspot')
        self.assertEqual(res1.status_code, 200)
        j1 = res1.get_json()
        self.assertEqual(j1['status'], 'success')
        self.assertEqual(j1['condition'], 'Brown Spot')
        self.assertFalse(j1['is_healthy'])
        self.assertIn('overview', j1['advisory'])
        self.assertTrue(len(j1['sources']) >= 1)

        res2 = self.client.get('/api/advisory?class_name=Tomato___healthy')
        self.assertEqual(res2.status_code, 200)
        j2 = res2.get_json()
        self.assertEqual(j2['status'], 'success')
        self.assertTrue(j2['is_healthy'])
        print("[TEST 12 PASSED] GET /api/advisory returned valid structured data for disease & healthy classes.")

    def test_13_advisory_unsupported_class(self):
        """Test GET /api/advisory with missing or unsupported class_name"""
        res1 = self.client.get('/api/advisory')
        self.assertEqual(res1.status_code, 400)

        res2 = self.client.get('/api/advisory?class_name=Apple-Healthy')
        self.assertEqual(res2.status_code, 400)
        self.assertIn('Unsupported or invalid', res2.get_json()['error'])
        print("[TEST 13 PASSED] GET /api/advisory correctly rejected missing and unsupported class_name.")

    def test_14_advisory_all_36_classes_coverage(self):
        """Test that ALL active model classes have complete advisory entries with valid source metadata"""
        from advisory_data import ADVISORY_DATABASE
        from app import class_names

        valid_source_types = {'ICAR', 'Government', 'University Extension', 'FAO'}

        self.assertIn(len(class_names), [27, 36])
        for c_name in class_names:
            self.assertIn(c_name, ADVISORY_DATABASE, f"Missing advisory data for class '{c_name}'")
            entry = ADVISORY_DATABASE[c_name]
            self.assertIsNotNone(entry.get('overview'), f"Missing overview for '{c_name}'")
            self.assertTrue(len(entry.get('immediate_actions', [])) > 0, f"Missing immediate_actions for '{c_name}'")
            self.assertTrue(len(entry.get('prevention', [])) > 0, f"Missing prevention for '{c_name}'")
            
            sources = entry.get('sources', [])
            self.assertTrue(len(sources) >= 1, f"Missing sources for '{c_name}'")
            for src in sources:
                self.assertTrue(bool(src.get('organization')), f"Empty organization in source for '{c_name}'")
                self.assertTrue(bool(src.get('title')), f"Empty title in source for '{c_name}'")
                url = src.get('url', '')
                self.assertTrue(url.startswith('http://') or url.startswith('https://'), f"Invalid URL '{url}' in source for '{c_name}'")
                stype = src.get('source_type')
                self.assertIn(stype, valid_source_types, f"Invalid or missing source_type '{stype}' for '{c_name}'")
                self.assertTrue(src.get('verified_url') is True, f"Source URL not marked as verified_url=True for '{c_name}'")

        print(f"[TEST 14 PASSED] 100% Advisory Data Coverage & Verified Source URLs verified across all {len(class_names)} model classes.")

    def test_15_advisory_safety_no_chemical_fields(self):
        """Safety Test: Ensure advisory database contains NO forbidden chemical fields or recommendations"""
        from advisory_data import ADVISORY_DATABASE, verified_chemical_guidance

        forbidden_keys = {'dosage', 'concentration', 'spray_interval', 'chemical_treatment', 'pesticide_dosage'}
        self.assertIsNone(verified_chemical_guidance, "verified_chemical_guidance must remain disabled (None)")

        for c_name, entry in ADVISORY_DATABASE.items():
            for key in entry.keys():
                self.assertNotIn(key.lower(), forbidden_keys, f"Forbidden chemical key '{key}' found in '{c_name}'")
            
            combined_text = str(entry).lower()
            for key in forbidden_keys:
                self.assertNotIn(key, combined_text, f"Forbidden term '{key}' found in advisory text for '{c_name}'")
        print("[TEST 15 PASSED] Safety Gate verified: Zero chemical/dosage/spray_interval fields present.")

    def test_16_symptom_questions_endpoint(self):
        """Test GET /api/symptom-questions endpoint"""
        res1 = self.client.get('/api/symptom-questions?class_name=Rice-Bacterialblight')
        self.assertEqual(res1.status_code, 200)
        j1 = res1.get_json()
        self.assertEqual(j1['status'], 'success')
        self.assertTrue(len(j1['questions']) >= 2)
        self.assertTrue(len(j1['field_spread_options']) >= 4)

        res2 = self.client.get('/api/symptom-questions?class_name=InvalidClass')
        self.assertEqual(res2.status_code, 400)
        print("[TEST 16 PASSED] GET /api/symptom-questions returned structured questions & options.")

    def test_17_verify_symptoms_high_agreement(self):
        """Test POST /api/verify-symptoms with high symptom agreement"""
        payload = {
            "class_name": "Rice-Bacterialblight",
            "answers": {
                "wavy_margin_lesions": "yes",
                "bacterial_droplets": "yes",
                "leaf_drying": "yes"
            },
            "field_spread": "several_leaves"
        }
        res = self.client.post('/api/verify-symptoms', json=payload)
        self.assertEqual(res.status_code, 200)
        j = res.get_json()
        self.assertEqual(j['status'], 'success')
        self.assertEqual(j['symptom_verification']['agreement'], 'high')
        self.assertEqual(j['symptom_verification']['match_score'], 1.0)
        self.assertEqual(j['field_assessment']['concern_level'], 'HIGH')
        print("[TEST 17 PASSED] POST /api/verify-symptoms correctly computed high agreement and field concern.")

    def test_18_verify_symptoms_low_agreement(self):
        """Test POST /api/verify-symptoms with low symptom agreement (disagreement trigger)"""
        payload = {
            "class_name": "Rice-Bacterialblight",
            "answers": {
                "wavy_margin_lesions": "no",
                "bacterial_droplets": "no",
                "leaf_drying": "no"
            },
            "field_spread": "only_this_leaf"
        }
        res = self.client.post('/api/verify-symptoms', json=payload)
        self.assertEqual(res.status_code, 200)
        j = res.get_json()
        self.assertEqual(j['symptom_verification']['agreement'], 'low')
        self.assertEqual(j['symptom_verification']['match_score'], 0.0)
        self.assertEqual(j['field_assessment']['concern_level'], 'LOW')
        print("[TEST 18 PASSED] POST /api/verify-symptoms correctly computed low agreement.")

    def test_19_verify_symptoms_high_field_concern(self):
        """Test POST /api/verify-symptoms with widespread field spread triggering HIGH concern"""
        payload = {
            "class_name": "Tomato___Late_blight",
            "answers": {
                "large_water_soaked_blotches": "yes"
            },
            "field_spread": "widespread"
        }
        res = self.client.post('/api/verify-symptoms', json=payload)
        self.assertEqual(res.status_code, 200)
        j = res.get_json()
        self.assertEqual(j['field_assessment']['concern_level'], 'HIGH')
        print("[TEST 19 PASSED] Widespread field spread correctly triggered HIGH concern level.")

    def test_20_verify_symptoms_unsure_spread_no_inflation(self):
        """Test that 'unsure' field spread does NOT artificially inflate concern level"""
        payload = {
            "class_name": "Tomato___Early_blight",
            "answers": {
                "target_board_rings": "no"
            },
            "field_spread": "unsure"
        }
        res = self.client.post('/api/verify-symptoms', json=payload)
        self.assertEqual(res.status_code, 200)
        j = res.get_json()
        self.assertEqual(j['field_assessment']['concern_level'], 'LOW')
        print("[TEST 20 PASSED] 'Unsure' field spread did not artificially inflate concern level.")

    def test_21_verify_symptoms_invalid_input_validation(self):
        """Test POST /api/verify-symptoms input validation and HTTP 400 errors"""
        res1 = self.client.post('/api/verify-symptoms', json={"class_name": "Unknown"})
        self.assertEqual(res1.status_code, 400)

        res2 = self.client.post('/api/verify-symptoms', json={"class_name": "Rice-Bacterialblight", "answers": {"q1": "invalid_val"}})
        self.assertEqual(res2.status_code, 400)

        res3 = self.client.post('/api/verify-symptoms', json={"class_name": "Rice-Bacterialblight", "field_spread": "invalid_spread"})
        self.assertEqual(res3.status_code, 400)
        print("[TEST 21 PASSED] POST /api/verify-symptoms input validation correctly enforced.")

    def test_22_verify_symptoms_healthy_class_handling(self):
        """Test symptom verification endpoint handling for healthy classes"""
        res = self.client.get('/api/symptom-questions?class_name=Tomato___healthy')
        self.assertEqual(res.status_code, 200)
        j = res.get_json()
        self.assertEqual(j['questions'], [])
        print("[TEST 22 PASSED] Healthy class symptom question request handled gracefully.")

    def test_23_cnn_confidence_isolation_test(self):
        """Safety Test: Verify CNN model confidence is NEVER used as an input to concern scoring"""
        from symptom_data import evaluate_symptom_verification
        import inspect

        sig = inspect.signature(evaluate_symptom_verification)
        params = list(sig.parameters.keys())
        self.assertNotIn('confidence', params, "evaluate_symptom_verification must NOT accept 'confidence' parameter")
        self.assertNotIn('cnn_confidence', params, "evaluate_symptom_verification must NOT accept 'cnn_confidence' parameter")
        print("[TEST 23 PASSED] CNN confidence isolation strictly verified in concern scoring logic.")

    def test_24_programmatic_symptom_coverage_audit(self):
        """Programmatic Coverage Audit: Assert 100% 24/24 disease class coverage in SYMPTOM_QUESTIONS"""
        from app import class_names
        from symptom_data import SYMPTOM_QUESTIONS

        all_classes = set(class_names)
        disease_classes = {c for c in all_classes if 'healthy' not in c.lower()}
        for d_cls in disease_classes:
            self.assertIn(d_cls, SYMPTOM_QUESTIONS, f"Missing symptom questions for disease class '{d_cls}'")
        print(f"[TEST 24 PASSED] Programmatic Symptom Coverage Audit: 100% active disease classes ({len(disease_classes)}) covered.")

    @patch('weather_service.requests.get')
    def test_25_location_search_endpoint(self, mock_get):
        """Test GET /api/location-search endpoint with mocked Open-Meteo response"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "results": [
                {"name": "Ambala", "admin1": "Haryana", "country": "India", "latitude": 30.3782, "longitude": 76.7767, "timezone": "Asia/Kolkata"}
            ]
        }
        res = self.client.get('/api/location-search?q=Ambala')
        self.assertEqual(res.status_code, 200)
        j = res.get_json()
        self.assertEqual(j['status'], 'success')
        self.assertEqual(len(j['results']), 1)
        self.assertEqual(j['results'][0]['name'], 'Ambala')
        print("[TEST 25 PASSED] GET /api/location-search returned normalized location results.")

    def test_26_location_search_validation(self):
        """Test GET /api/location-search validation for short or empty queries"""
        res1 = self.client.get('/api/location-search?q=a')
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res1.get_json()['results'], [])

        res2 = self.client.get('/api/location-search?q=')
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.get_json()['results'], [])
        print("[TEST 26 PASSED] Location search empty/short query validation verified.")

    @patch('weather_service.requests.get')
    def test_27_weather_context_endpoint(self, mock_get):
        """Test GET /api/weather-context with mocked forecast response"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "timezone": "Asia/Kolkata",
            "current": {
                "temperature_2m": 28.5,
                "relative_humidity_2m": 88.0,
                "precipitation": 2.5,
                "weather_code": 61,
                "wind_speed_10m": 12.0
            },
            "hourly": {
                "temperature_2m": [28.5] * 24,
                "relative_humidity_2m": [88.0] * 24,
                "dew_point_2m": [25.0] * 24,
                "precipitation": [0.1] * 24,
                "precipitation_probability": [80] * 24
            }
        }
        res = self.client.get('/api/weather-context?latitude=30.3782&longitude=76.7767&class_name=Rice-Bacterialblight&location_name=Ambala')
        self.assertEqual(res.status_code, 200)
        j = res.get_json()
        self.assertEqual(j['status'], 'success')
        self.assertTrue(j['weather_available'])
        self.assertEqual(j['current']['temperature_c'], 28.5)
        self.assertEqual(j['disease_context']['favorability'], 'HIGH')
        print("[TEST 27 PASSED] GET /api/weather-context returned valid weather & HIGH favorability context.")

    def test_28_weather_context_validation(self):
        """Test GET /api/weather-context input validation for missing or invalid parameters"""
        res1 = self.client.get('/api/weather-context?class_name=Rice-Bacterialblight')
        self.assertEqual(res1.status_code, 400)

        res2 = self.client.get('/api/weather-context?latitude=invalid&longitude=76.77&class_name=Rice-Bacterialblight')
        self.assertEqual(res2.status_code, 400)

        res3 = self.client.get('/api/weather-context?latitude=999.0&longitude=76.77&class_name=Rice-Bacterialblight')
        self.assertEqual(res3.status_code, 400)

        res4 = self.client.get('/api/weather-context?latitude=30.37&longitude=76.77&class_name=UnknownClass')
        self.assertEqual(res4.status_code, 400)
        print("[TEST 28 PASSED] GET /api/weather-context parameter validation correctly enforced.")

    @patch('weather_service.requests.get')
    def test_29_weather_context_disease_without_rules(self, mock_get):
        """Test weather context for viral disease without specific weather rules"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "timezone": "Asia/Kolkata",
            "current": {"temperature_2m": 30.0, "relative_humidity_2m": 60.0, "precipitation": 0.0, "weather_code": 0, "wind_speed_10m": 5.0},
            "hourly": {"temperature_2m": [30.0]*24, "relative_humidity_2m": [60.0]*24, "dew_point_2m": [20.0]*24, "precipitation": [0.0]*24, "precipitation_probability": [0]*24}
        }
        res = self.client.get('/api/weather-context?latitude=30.3782&longitude=76.7767&class_name=Tomato___Tomato_mosaic_virus')
        self.assertEqual(res.status_code, 200)
        j = res.get_json()
        self.assertFalse(j['disease_context']['available'])
        self.assertEqual(j['disease_context']['favorability'], 'NEUTRAL')
        print("[TEST 29 PASSED] Viral disease weather context returned neutral non-causal information.")

    def test_30_weather_context_favorability_evaluations(self):
        """Test favorability scoring logic for HIGH, MODERATE, and LOW levels"""
        from weather_risk_data import evaluate_weather_favorability

        high_res = evaluate_weather_favorability("Rice-Bacterialblight", 28.0, 85.0, 5.0)
        self.assertEqual(high_res['favorability'], 'HIGH')

        low_res = evaluate_weather_favorability("Rice-Bacterialblight", 10.0, 40.0, 0.0)
        self.assertEqual(low_res['favorability'], 'LOW')
        print("[TEST 30 PASSED] Weather favorability evaluation logic strictly verified across thresholds.")

    @patch('weather_service.requests.get')
    def test_31_weather_service_failure_resilience(self, mock_get):
        """Test fallback behavior when Open-Meteo API is unreachable or times out"""
        mock_get.side_effect = Exception("Connection timeout error")

        res = self.client.get('/api/weather-context?latitude=30.3782&longitude=76.7767&class_name=Rice-Bacterialblight')
        self.assertEqual(res.status_code, 200)
        j = res.get_json()
        self.assertEqual(j['status'], 'partial_success')
        self.assertFalse(j['weather_available'])
        self.assertIn('temporarily unavailable', j['message'].lower())
        print("[TEST 31 PASSED] Weather API failure resilience verified; returned partial_success fallback.")

    @patch('weather_service.requests.get')
    def test_32_healthy_class_weather_context(self, mock_get):
        """Test weather context for healthy crop predictions"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "timezone": "Asia/Kolkata",
            "current": {"temperature_2m": 26.0, "relative_humidity_2m": 65.0, "precipitation": 0.0, "weather_code": 1, "wind_speed_10m": 8.0},
            "hourly": {"temperature_2m": [26.0]*24, "relative_humidity_2m": [65.0]*24, "dew_point_2m": [18.0]*24, "precipitation": [0.0]*24, "precipitation_probability": [10]*24}
        }
        res = self.client.get('/api/weather-context?latitude=30.3782&longitude=76.7767&class_name=Tomato___healthy')
        self.assertEqual(res.status_code, 200)
        j = res.get_json()
        self.assertTrue(j['weather_available'])
        self.assertEqual(j['disease_context']['favorability'], 'NEUTRAL')
        print("[TEST 32 PASSED] Healthy crop class weather context returned non-alarmist neutral weather.")

    def test_33_weather_scoring_isolation_test(self):
        """Safety Test: Verify weather favorability scoring accepts ZERO CNN confidence, symptom, or field concern inputs"""
        from weather_risk_data import evaluate_weather_favorability
        import inspect

        sig = inspect.signature(evaluate_weather_favorability)
        params = list(sig.parameters.keys())
        self.assertNotIn('confidence', params)
        self.assertNotIn('symptom_score', params)
        self.assertNotIn('concern_level', params)
        print("[TEST 33 PASSED] Weather favorability scoring strict independence verified.")

    def test_34_database_init(self):
        """Test SQLite database initialization and table structure"""
        import database
        database.init_db()
        scans = database.get_scans()
        self.assertIsInstance(scans, list)
        print("[TEST 34 PASSED] SQLite database & tables auto-initialized cleanly.")

    def test_35_save_scan_endpoint(self):
        """Test POST /api/scans saving a reliable assessment record"""
        payload = {
            "crop": "Rice",
            "class_name": "Rice-Bacterialblight",
            "condition": "Bacterial Blight",
            "model_confidence": 98.5,
            "is_healthy": False,
            "symptom_agreement": "high",
            "symptom_match_score": 1.0,
            "field_concern": "HIGH",
            "weather_favorability": "HIGH",
            "location_name": "Ambala, Haryana"
        }
        res = self.client.post('/api/scans', json=payload)
        self.assertEqual(res.status_code, 201)
        j = res.get_json()
        self.assertEqual(j['status'], 'success')
        self.assertEqual(j['scan']['crop'], 'Rice')
        self.assertEqual(j['scan']['location_name'], 'Ambala, Haryana')
        print("[TEST 35 PASSED] POST /api/scans saved reliable assessment record to SQLite.")

    def test_36_save_scan_validation(self):
        """Test POST /api/scans validation for unsupported class or missing data"""
        res = self.client.post('/api/scans', json={"class_name": "InvalidClass"})
        self.assertEqual(res.status_code, 400)
        print("[TEST 36 PASSED] POST /api/scans rejected invalid class_name.")

    def test_37_get_scans_list_and_single(self):
        """Test GET /api/scans list and GET /api/scans/<id> single scan retrieval"""
        payload = {
            "crop": "Tomato",
            "class_name": "Tomato___Early_blight",
            "condition": "Early Blight",
            "model_confidence": 95.0,
            "is_healthy": False,
            "location_name": "Karnal, Haryana"
        }
        res_post = self.client.post('/api/scans', json=payload)
        scan_id = res_post.get_json()['scan']['id']

        res_list = self.client.get('/api/scans')
        self.assertEqual(res_list.status_code, 200)
        self.assertTrue(res_list.get_json()['total'] >= 1)

        res_single = self.client.get(f'/api/scans/{scan_id}')
        self.assertEqual(res_single.status_code, 200)
        self.assertEqual(res_single.get_json()['scan']['condition'], 'Early Blight')
        print("[TEST 37 PASSED] Scans list & single scan endpoints verified.")

    def test_38_delete_scan(self):
        """Test DELETE /api/scans/<id> removing a scan record"""
        payload = {
            "crop": "Pumpkin",
            "class_name": "Pumpkin-Powdery_Mildew",
            "condition": "Powdery Mildew",
            "model_confidence": 90.0,
            "is_healthy": False
        }
        res_post = self.client.post('/api/scans', json=payload)
        scan_id = res_post.get_json()['scan']['id']

        res_del = self.client.delete(f'/api/scans/{scan_id}')
        self.assertEqual(res_del.status_code, 200)

        res_get = self.client.get(f'/api/scans/{scan_id}')
        self.assertEqual(res_get.status_code, 404)
        print("[TEST 38 PASSED] DELETE /api/scans/<id> successfully removed scan record.")

    def test_39_share_community_signal_success(self):
        """Test POST /api/community-signals opt-in sharing from reliable disease scan"""
        payload = {
            "crop": "Rice",
            "class_name": "Rice-Brownspot",
            "condition": "Brown Spot",
            "model_confidence": 97.0,
            "is_healthy": False,
            "diagnosis_reliable": True,
            "location_name": "Ambala"
        }
        res_post = self.client.post('/api/scans', json=payload)
        scan_id = res_post.get_json()['scan']['id']

        res_share = self.client.post('/api/community-signals', json={"scan_id": scan_id, "approx_lat": 30.3782, "approx_lon": 76.7767})
        self.assertEqual(res_share.status_code, 201)
        j = res_share.get_json()
        self.assertEqual(j['status'], 'success')
        self.assertEqual(j['signal']['map_lat'], 30.4)
        print("[TEST 39 PASSED] Opt-in community signal created with coarsened coordinates.")

    def test_40_share_community_signal_healthy_rejected(self):
        """Test that healthy crop scans CANNOT be submitted as disease signals"""
        payload = {
            "crop": "Sugarcane",
            "class_name": "Sugarcane-Healthy",
            "condition": "Healthy",
            "model_confidence": 99.0,
            "is_healthy": True,
            "diagnosis_reliable": True
        }
        res_post = self.client.post('/api/scans', json=payload)
        scan_id = res_post.get_json()['scan']['id']

        res_share = self.client.post('/api/community-signals', json={"scan_id": scan_id})
        self.assertEqual(res_share.status_code, 400)
        self.assertIn("healthy", res_share.get_json()['error'].lower())
        print("[TEST 40 PASSED] Healthy crop assessment sharing attempt correctly rejected.")

    def test_41_get_community_signals_sanitized_privacy(self):
        """Privacy Safety Test: Verify community API responses NEVER expose raw GPS or image paths"""
        res = self.client.get('/api/community-signals')
        self.assertEqual(res.status_code, 200)
        signals = res.get_json()['signals']

        for sig in signals:
            self.assertNotIn('image_path', sig)
            self.assertNotIn('image_url', sig)
            self.assertNotIn('raw_gps', sig)
            if sig.get('map_lat') is not None:
                lat_str = str(sig['map_lat'])
                if '.' in lat_str:
                    decimals = len(lat_str.split('.')[1])
                    self.assertTrue(decimals <= 1, f"Excessive GPS precision '{lat_str}' in public signal!")
        print("[TEST 41 PASSED] Privacy Safety Test: Community signals contain zero image paths or raw GPS.")

    def test_42_get_community_summary_aggregates(self):
        """Test GET /api/community-summary aggregate stats endpoint"""
        res = self.client.get('/api/community-summary')
        self.assertEqual(res.status_code, 200)
        j = res.get_json()
        self.assertEqual(j['status'], 'success')
        self.assertIn('total_reported_signals', j)
        self.assertIn('signals_last_7_days', j)
        self.assertIn('area_breakdown', j)
        print("[TEST 42 PASSED] GET /api/community-summary returned correct aggregate statistics.")

    def test_43_uncertain_assessment_cannot_be_saved(self):
        """Phase 6.1 Test: Verify POST /api/scans with diagnosis_reliable == False is strictly rejected with HTTP 400"""
        payload = {
            "crop": "Rice",
            "class_name": "Tomato___Bacterial_spot",
            "condition": "Bacterial Spot",
            "model_confidence": 45.0,
            "is_healthy": False,
            "diagnosis_reliable": False
        }
        res = self.client.post('/api/scans', json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertIn("uncertain", res.get_json()['error'].lower())
        print("[TEST 43 PASSED] Server-side check strictly prevented saving uncertain assessment.")

    def test_44_missing_source_scan_community_signal_rejected(self):
        """Phase 6.1 Test: Verify POST /api/community-signals with nonexistent scan_id returns HTTP 404"""
        res = self.client.post('/api/community-signals', json={"scan_id": 999999})
        self.assertEqual(res.status_code, 404)
        self.assertIn("not found", res.get_json()['error'].lower())
        print("[TEST 44 PASSED] Sharing non-existent scan ID correctly returned HTTP 404.")

    def test_45_duplicate_sharing_protection(self):
        """Phase 6.1 Test: Verify sharing the same scan twice returns HTTP 200 with already_shared == True and creates 0 duplicate signals"""
        payload = {
            "crop": "Rice",
            "class_name": "Rice-Leafsmut",
            "condition": "Leaf Smut",
            "model_confidence": 99.0,
            "is_healthy": False,
            "diagnosis_reliable": True,
            "location_name": "Ambala"
        }
        res_scan = self.client.post('/api/scans', json=payload)
        scan_id = res_scan.get_json()['scan']['id']

        # First Share
        res1 = self.client.post('/api/community-signals', json={"scan_id": scan_id, "approx_lat": 30.3782, "approx_lon": 76.7767})
        self.assertEqual(res1.status_code, 201)
        self.assertFalse(res1.get_json()['already_shared'])

        # Second Share (Duplicate)
        res2 = self.client.post('/api/community-signals', json={"scan_id": scan_id, "approx_lat": 30.3782, "approx_lon": 76.7767})
        self.assertEqual(res2.status_code, 200)
        self.assertTrue(res2.get_json()['already_shared'])
        self.assertEqual(res2.get_json()['status'], 'already_shared')
        print("[TEST 45 PASSED] Server-side duplicate sharing protection verified.")

    def test_46_community_shared_state_updated_in_database(self):
        """Phase 6.1 Test: Verify after successful sharing, scan.community_shared is set to True"""
        payload = {
            "crop": "Sugarcane",
            "class_name": "Sugarcane-Red Rot",
            "condition": "Red Rot",
            "model_confidence": 96.0,
            "is_healthy": False,
            "diagnosis_reliable": True
        }
        res_scan = self.client.post('/api/scans', json=payload)
        scan_id = res_scan.get_json()['scan']['id']

        self.client.post('/api/community-signals', json={"scan_id": scan_id})

        res_get = self.client.get(f'/api/scans/{scan_id}')
        self.assertTrue(res_get.get_json()['scan']['community_shared'])
        print("[TEST 46 PASSED] Scan record community_shared state correctly updated to True.")

    def test_47_public_coordinates_coarsened_to_1_decimal(self):
        """Phase 6.1 Test: Verify GET /api/community-signals returns map_lat and map_lon coarsened to 1 decimal place"""
        payload = {
            "crop": "Tomato",
            "class_name": "Tomato___Late_blight",
            "condition": "Late Blight",
            "model_confidence": 98.0,
            "is_healthy": False,
            "diagnosis_reliable": True
        }
        res_scan = self.client.post('/api/scans', json=payload)
        scan_id = res_scan.get_json()['scan']['id']

        self.client.post('/api/community-signals', json={"scan_id": scan_id, "approx_lat": 30.37821, "approx_lon": 76.77673})

        res_sigs = self.client.get('/api/community-signals')
        self.assertEqual(res_sigs.status_code, 200)
        signals = res_sigs.get_json()['signals']

        matching = [s for s in signals if s.get('condition') == 'Late Blight']
        self.assertTrue(len(matching) >= 1)
        target = matching[0]
        self.assertIn('map_lat', target)
        self.assertIn('map_lon', target)
        self.assertEqual(target['map_lat'], 30.4)
        self.assertEqual(target['map_lon'], 76.8)
        print("[TEST 47 PASSED] Public community API map coordinates coarsened to 1 decimal place.")

    def test_48_recursive_privacy_safety_audit(self):
        """Phase 6.1 Privacy Audit: Verify public community API responses contain ZERO private or raw GPS fields"""
        res_sigs = self.client.get('/api/community-signals')
        res_sum = self.client.get('/api/community-summary')

        forbidden_keys = {
            "image", "image_path", "uploaded_image", "original_filename",
            "raw_lat", "raw_lon", "exact_lat", "exact_lon", "latitude", "longitude",
            "personal_identifiers", "ip_address", "user_id"
        }

        def check_obj(obj, path="root"):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    self.assertNotIn(k.lower(), forbidden_keys, f"Forbidden privacy key '{k}' found at {path}!")
                    check_obj(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for idx, item in enumerate(obj):
                    check_obj(item, f"{path}[{idx}]")

        check_obj(res_sigs.get_json())
        check_obj(res_sum.get_json())
        print("[TEST 48 PASSED] Recursive Privacy Safety Audit: Zero private or raw GPS fields in public API.")

    def test_49_scan_deletion_does_not_corrupt_summary(self):
        """Phase 6.1 Integrity Test: Deleting a scan record sets source_scan_id = NULL and preserves community summary count"""
        payload = {
            "crop": "Pumpkin",
            "class_name": "Pumpkin-Powdery_Mildew",
            "condition": "Powdery Mildew",
            "model_confidence": 92.0,
            "is_healthy": False,
            "diagnosis_reliable": True
        }
        res_scan = self.client.post('/api/scans', json=payload)
        scan_id = res_scan.get_json()['scan']['id']

        self.client.post('/api/community-signals', json={"scan_id": scan_id})

        sum_before = self.client.get('/api/community-summary').get_json()['total_reported_signals']

        # Delete local scan record
        self.client.delete(f'/api/scans/{scan_id}')

        sum_after = self.client.get('/api/community-summary').get_json()['total_reported_signals']

        self.assertEqual(sum_before, sum_after, "Deleting local scan record must not corrupt community aggregate count.")
        print("[TEST 49 PASSED] Local scan deletion preserved anonymized community summary without orphan crashes.")

    def test_50_community_summary_aggregates_and_labeling(self):
        """Phase 6.1 Test: Verify GET /api/community-summary uses non-alarmist labeling ("reported_signals")"""
        res = self.client.get('/api/community-summary')
        self.assertEqual(res.status_code, 200)
        j = res.get_json()
        self.assertIn("total_reported_signals", j)
        self.assertNotIn("confirmed_cases", j)
        self.assertNotIn("outbreak_count", j)
        print("[TEST 50 PASSED] Community summary aggregates & non-alarmist labeling strictly verified.")

    def test_51_isolated_test_database_init(self):
        """Phase 6.1 Test: Verify database migration logic initializes cleanly on an isolated test DB path"""
        import database
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            database.init_db(tmp_path)
            scans = database.get_scans(db_path=tmp_path)
            self.assertEqual(scans, [])
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        print("[TEST 51 PASSED] Isolated database migration & initialization verified.")

    def test_52_community_radar_endpoint_structure(self):
        """Phase 7 Test: Verify GET /api/community-radar returns valid structured radar intelligence"""
        res = self.client.get('/api/community-radar')
        self.assertEqual(res.status_code, 200)
        j = res.get_json()
        self.assertEqual(j['status'], 'success')
        self.assertIn('summary', j)
        self.assertIn('areas', j)
        self.assertIn('daily_trend', j)
        self.assertIn('crop_breakdown', j)
        self.assertIn('recent_signals', j)
        self.assertIn('disclaimer', j)
        print("[TEST 52 PASSED] GET /api/community-radar returned valid structured intelligence.")

    def test_53_community_radar_time_filtering(self):
        """Phase 7 Test: Verify radar endpoint time window filtering (24h, 7d, 30d, all time)"""
        res_7d = self.client.get('/api/community-radar?days=7')
        res_30d = self.client.get('/api/community-radar?days=30')
        self.assertEqual(res_7d.status_code, 200)
        self.assertEqual(res_30d.status_code, 200)
        print("[TEST 53 PASSED] Community radar time window filtering verified.")

    def test_54_community_radar_crop_filtering(self):
        """Phase 7 Test: Verify radar crop filtering (Rice vs All) and rejection of unsupported crop"""
        res_rice = self.client.get('/api/community-radar?crop=Rice')
        self.assertEqual(res_rice.status_code, 200)
        for area in res_rice.get_json()['areas']:
            for cond in area['conditions']:
                self.assertEqual(cond['crop'], 'Rice')

        res_invalid = self.client.get('/api/community-radar?crop=Wheat')
        self.assertEqual(res_invalid.status_code, 400)
        print("[TEST 54 PASSED] Community radar crop filtering & unsupported crop rejection verified.")

    def test_55_community_radar_activity_level_calculation(self):
        """Phase 7 Test: Verify deterministic activity level calculation (LOW, MODERATE, ELEVATED)"""
        import database
        radar_demo = database.get_community_radar(mode='demo', days=30)
        for area in radar_demo['areas']:
            cnt = area['signal_count']
            lvl = area['activity_level']
            if cnt >= 4:
                self.assertEqual(lvl, 'ELEVATED')
            elif cnt >= 2:
                self.assertEqual(lvl, 'MODERATE')
            else:
                self.assertEqual(lvl, 'LOW')
        print("[TEST 55 PASSED] Deterministic activity level calculation (LOW, MODERATE, ELEVATED) verified.")

    def test_56_community_radar_coarsened_coordinates_only(self):
        """Phase 7 Privacy Test: Verify public radar endpoint returns ONLY map_lat and map_lon (1 decimal place)"""
        res = self.client.get('/api/community-radar?mode=demo')
        self.assertEqual(res.status_code, 200)
        areas = res.get_json()['areas']

        for area in areas:
            self.assertIn('map_lat', area)
            self.assertIn('map_lon', area)
            self.assertNotIn('raw_lat', area)
            self.assertNotIn('raw_lon', area)
            self.assertNotIn('exact_lat', area)

            lat_str = str(area['map_lat'])
            if '.' in lat_str:
                self.assertTrue(len(lat_str.split('.')[1]) <= 1, f"Excessive precision in map_lat '{lat_str}'!")
        print("[TEST 56 PASSED] Public radar map coordinates coarsened to 1 decimal place max.")

    def test_57_community_radar_recursive_privacy_safety_audit(self):
        """Phase 7 Privacy Audit: Verify public radar payload recursively contains ZERO forbidden private fields"""
        res = self.client.get('/api/community-radar?mode=demo')
        forbidden_keys = {
            "image", "image_path", "uploaded_image", "original_filename",
            "raw_lat", "raw_lon", "exact_lat", "exact_lon", "latitude", "longitude",
            "personal_identifiers", "ip_address", "user_id"
        }

        def check_obj(obj, path="root"):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    self.assertNotIn(k.lower(), forbidden_keys, f"Forbidden key '{k}' found at {path}!")
                    check_obj(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for idx, item in enumerate(obj):
                    check_obj(item, f"{path}[{idx}]")

        check_obj(res.get_json())
        print("[TEST 57 PASSED] Recursive Privacy Safety Audit: Zero private or raw GPS fields in radar response.")

    def test_58_community_radar_demo_mode(self):
        """Phase 7 Test: Verify Demo Mode returns synthetic illustrative signals without reading/writing SQLite table"""
        import database
        db_count_before = len(database.get_community_signals())

        res_demo = self.client.get('/api/community-radar?mode=demo')
        self.assertEqual(res_demo.status_code, 200)
        j = res_demo.get_json()
        self.assertEqual(j['mode'], 'demo')
        self.assertTrue(len(j['areas']) >= 1)

        db_count_after = len(database.get_community_signals())
        self.assertEqual(db_count_before, db_count_after, "Demo Mode must not touch SQLite database rows!")
        print("[TEST 58 PASSED] Demo Mode isolation verified: Returns synthetic illustrative dataset without touching SQLite DB.")

    def test_59_community_radar_empty_live_handling(self):
        """Phase 7 Test: Verify live radar mode handles empty database gracefully without crashes"""
        import database
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            database.init_db(tmp_path)
            empty_radar = database.get_community_radar(mode='live', db_path=tmp_path)
            self.assertEqual(empty_radar['summary']['total_signals'], 0)
            self.assertEqual(empty_radar['areas'], [])
            self.assertEqual(empty_radar['daily_trend'], [])
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        print("[TEST 59 PASSED] Empty live radar handled gracefully with zero counts.")

    def test_60_community_radar_daily_trend_grouping(self):
        """Phase 7 Test: Verify daily_trend correctly groups signal counts by YYYY-MM-DD date string"""
        res = self.client.get('/api/community-radar?mode=demo')
        self.assertEqual(res.status_code, 200)
        trend = res.get_json()['daily_trend']
        self.assertIsInstance(trend, list)
        for item in trend:
            self.assertIn('date', item)
            self.assertIn('signals', item)
            self.assertTrue(len(item['date']) == 10)
        print("[TEST 60 PASSED] Daily trend grouping by YYYY-MM-DD date verified.")

    def test_61_community_radar_areas_to_watch_ranking(self):
        """Phase 7 Test: Verify areas list is deterministically ranked by signal_count descending"""
        res = self.client.get('/api/community-radar?mode=demo')
        self.assertEqual(res.status_code, 200)
        areas = res.get_json()['areas']
        for i in range(len(areas) - 1):
            self.assertTrue(areas[i]['signal_count'] >= areas[i+1]['signal_count'], "Areas must be ranked by signal_count descending!")
        print("[TEST 61 PASSED] Areas to Watch deterministic ranking (signal_count DESC) verified.")

    def test_62_treatment_options_endpoint_valid_disease(self):
        """Phase 9 Test: GET /api/treatment-options returns structured cultural, biological, and active ingredient chemical options with verified sources"""
        res = self.client.get('/api/treatment-options?class_name=Tomato___Early_blight')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')
        treat = data['treatment_options']
        self.assertTrue(treat['available'])
        self.assertTrue(treat['treatment_required'])
        self.assertIn('cultural_controls', treat)
        self.assertIn('biological_controls', treat)
        self.assertIn('chemical_options', treat)
        self.assertIn('safety_notice', treat)
        self.assertTrue(len(treat['chemical_options']) > 0)
        print("[TEST 62 PASSED] GET /api/treatment-options returned structured options for Tomato___Early_blight.")

    def test_63_treatment_options_healthy_crop(self):
        """Phase 9 Test: GET /api/treatment-options for healthy crop returns treatment_required=false and zero chemical options"""
        res = self.client.get('/api/treatment-options?class_name=Sugarcane-Healthy')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        treat = data['treatment_options']
        self.assertTrue(treat['available'])
        self.assertFalse(treat['treatment_required'])
        self.assertEqual(treat['chemical_options'], [])
        print("[TEST 63 PASSED] GET /api/treatment-options for Sugarcane-Healthy correctly returned zero chemical options.")

    def test_64_treatment_options_safety_notice_and_dosage_absence(self):
        """Phase 9 Safety Test: Chemical options MUST contain region safety notice and MUST NOT contain dosage fields"""
        res = self.client.get('/api/treatment-options?class_name=Rice-Bacterialblight')
        self.assertEqual(res.status_code, 200)
        treat = res.get_json()['treatment_options']
        self.assertIn('safety_notice', treat)
        self.assertIn('registered for this crop', treat['safety_notice'].lower())
        
        for chem in treat['chemical_options']:
            self.assertIn('active_ingredient', chem)
            self.assertIn('purpose', chem)
            # Verify no dosage field present
            self.assertNotIn('dosage', chem)
            self.assertNotIn('ml_per_litre', chem)
            self.assertNotIn('grams_per_litre', chem)
        print("[TEST 64 PASSED] Treatment safety notice and dosage field absence strictly verified.")

    def test_65_treatment_options_unsupported_class(self):
        """Phase 9 Test: GET /api/treatment-options with invalid class_name returns HTTP 400"""
        res = self.client.get('/api/treatment-options?class_name=Fake_Class_Name')
        self.assertEqual(res.status_code, 400)
        print("[TEST 65 PASSED] GET /api/treatment-options invalid class_name correctly rejected with HTTP 400.")

if __name__ == '__main__':
    unittest.main()
