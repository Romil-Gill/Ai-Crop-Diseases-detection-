"""
FasalRakshak AI - Knowledge Base Coverage Audit (Phase 9.10)
Verifies 100% complete coverage for all 36 classes across Advisory, Symptoms, Weather Rules, and Treatment Options.
"""

import os
import json
from advisory_data import ADVISORY_DATABASE
from symptom_data import SYMPTOM_QUESTIONS
from weather_risk_data import WEATHER_DISEASE_RULES
from treatment_data import TREATMENT_DATABASE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAPPING_V2_PATH = os.path.join(BASE_DIR, "class_mapping_v2.json")

def audit_coverage():
    print("==================================================")
    print("  FASALRAKSHAK AI - KNOWLEDGE BASE COVERAGE AUDIT")
    print("==================================================")
    
    with open(MAPPING_V2_PATH, "r", encoding="utf-8") as f:
        mapping = json.load(f)
        
    classes = [mapping[str(i)] for i in range(len(mapping))]
    total_classes = len(classes)
    print(f"Auditing total model classes: {total_classes}\n")
    
    missing_advisory = []
    missing_symptoms = []
    missing_weather = []
    missing_treatment = []
    
    header = f"{'Class Name':<45} | {'Adv?':<5} | {'Sym?':<5} | {'Weat?':<5} | {'Treat?':<5}"
    print(header)
    print("-" * len(header))
    
    for cname in classes:
        is_healthy = "healthy" in cname.lower()
        has_adv = cname in ADVISORY_DATABASE
        has_sym = (cname in SYMPTOM_QUESTIONS) or is_healthy
        has_weat = (cname in WEATHER_DISEASE_RULES) or is_healthy
        has_treat = cname in TREATMENT_DATABASE
        
        if not has_adv: missing_advisory.append(cname)
        if not has_sym: missing_symptoms.append(cname)
        if not has_weat: missing_weather.append(cname)
        if not has_treat: missing_treatment.append(cname)
        
        print(f"{cname:<45} | {str(has_adv):<5} | {str(has_sym):<5} | {str(has_weat):<5} | {str(has_treat):<5}")
        
    print("\n--------------------------------------------------")
    print("AUDIT SUMMARY:")
    print(f"Total Classes Audited:      {total_classes}")
    print(f"Advisory Coverage:          {total_classes - len(missing_advisory)}/{total_classes}")
    print(f"Symptom Coverage:           {total_classes - len(missing_symptoms)}/{total_classes}")
    print(f"Weather Rule Coverage:      {total_classes - len(missing_weather)}/{total_classes}")
    print(f"Treatment Option Coverage:  {total_classes - len(missing_treatment)}/{total_classes}")
    
    if missing_advisory or missing_symptoms or missing_weather or missing_treatment:
        print("\nCRITICAL AUDIT FAILURE: Missing coverage detected!")
        if missing_advisory: print(f"Missing Advisory: {missing_advisory}")
        if missing_symptoms: print(f"Missing Symptoms: {missing_symptoms}")
        if missing_weather: print(f"Missing Weather: {missing_weather}")
        if missing_treatment: print(f"Missing Treatment: {missing_treatment}")
        return False
    
    print("\n[SUCCESS] 100% Knowledge Base Coverage Verified across all 36 classes!")
    return True

if __name__ == "__main__":
    success = audit_coverage()
    if not success:
        exit(1)
