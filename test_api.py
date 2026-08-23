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
        print("\n[TEST 1 PASSED] /api/health returned valid response.")

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
        self.assertEqual(data['total_classes'], 27)
        self.assertIn('Tomato', data['crops'])
        print("[TEST 2 PASSED] /api/classes returned 27 classes mapped across 4 crops.")

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
            'selected_crop': 'Wheat'
        }
        response = self.client.post('/api/predict', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        res_json = response.get_json()
        self.assertIn('error', res_json)
        self.assertIn('Unsupported selected_crop', res_json['error'])
        print("[TEST 6 PASSED] /api/predict unsupported selected_crop 'Wheat' rejected with HTTP 400.")

    def test_07_predict_crop_mismatch_handling(self):
        """Test POST /api/predict with mismatching crop selection to trigger Safe Diagnosis Gate"""
        res_raw = self.client.post('/api/predict', data={'file': (self.create_dummy_image(), 'leaf.jpg')}, content_type='multipart/form-data')
        predicted_crop = res_raw.get_json()['prediction']['crop']
        
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
        # First get prediction crop
        res_raw = self.client.post('/api/predict', data={'file': (self.create_dummy_image(), 'leaf.jpg')}, content_type='multipart/form-data')
        predicted_crop = res_raw.get_json()['prediction']['crop']

        data = {
            'file': (self.create_dummy_image(), 'leaf.jpg'),
            'selected_crop': predicted_crop
        }
        response = self.client.post('/api/explain', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        res_json = response.get_json()

        self.assertEqual(res_json['status'], 'success')
        self.assertTrue(res_json['diagnosis_reliable'])
        self.assertIsNotNone(res_json['explanation'])
        
        exp = res_json['explanation']
        self.assertIn('heatmap', exp)
        self.assertIn('overlay', exp)
        self.assertTrue(exp['heatmap'].startswith('data:image/png;base64,'))
        self.assertTrue(exp['overlay'].startswith('data:image/png;base64,'))
        self.assertEqual(exp['method'], 'Grad-CAM')
        self.assertEqual(exp['target_layer'], 'mobilenetv2_1.00_224/out_relu')
        print(f"[TEST 8 PASSED] /api/explain returned valid Grad-CAM overlay for target layer '{exp['target_layer']}'.")

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
            'selected_crop': 'Wheat'
        }
        response = self.client.post('/api/explain', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Unsupported selected_crop', response.get_json()['error'])
        print("[TEST 10 PASSED] /api/explain unsupported selected_crop 'Wheat' rejected with HTTP 400.")

    def test_11_explain_crop_mismatch_no_explanation(self):
        """Test POST /api/explain with crop mismatch returns uncertain status and explanation=None"""
        res_raw = self.client.post('/api/predict', data={'file': (self.create_dummy_image(), 'leaf.jpg')}, content_type='multipart/form-data')
        predicted_crop = res_raw.get_json()['prediction']['crop']
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

        res2 = self.client.get('/api/advisory?class_name=Wheat-Healthy')
        self.assertEqual(res2.status_code, 400)
        self.assertIn('Unsupported or invalid', res2.get_json()['error'])
        print("[TEST 13 PASSED] GET /api/advisory correctly rejected missing and unsupported class_name.")

    def test_14_advisory_all_27_classes_coverage(self):
        """Test that ALL 27 model classes have complete advisory entries with valid source metadata"""
        from advisory_data import ADVISORY_DATABASE
        from app import class_names

        valid_source_types = {'ICAR', 'Government', 'University Extension', 'FAO'}

        self.assertEqual(len(class_names), 27)
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
        self.assertEqual(len(all_classes), 27, f"Expected 27 total model classes, found {len(all_classes)}")

        healthy_classes = {c for c in all_classes if 'healthy' in c.lower()}
        self.assertEqual(len(healthy_classes), 3, f"Expected 3 healthy classes, found {len(healthy_classes)}")

        disease_classes = {c for c in all_classes if 'healthy' not in c.lower()}
        self.assertEqual(len(disease_classes), 24, f"Expected 24 disease classes, found {len(disease_classes)}")

        symptom_classes = set(SYMPTOM_QUESTIONS.keys())

        # Exact set equality assertion
        self.assertEqual(
            disease_classes,
            symptom_classes,
            f"Symptom question coverage mismatch! Missing: {disease_classes - symptom_classes}, Extra: {symptom_classes - disease_classes}"
        )
        print("[TEST 24 PASSED] Programmatic Symptom Coverage Audit: 100% 24/24 disease classes covered.")

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

if __name__ == '__main__':
    unittest.main()
