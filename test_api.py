import os
import io
import unittest
from PIL import Image
import json
from app import app, model, tf

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

        print(f"[TEST 14 PASSED] 100% Advisory Data Coverage & Source Metadata verified across all {len(class_names)} model classes.")

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

if __name__ == '__main__':
    unittest.main()
