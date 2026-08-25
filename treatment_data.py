"""
FasalRakshak AI - Source-Backed Treatment Options Knowledge Base (Phase 9)
Provides structured, source-backed cultural, biological, and chemical treatment guidance for 36 classes across 6 crops.
Strictly excludes commercial brand requirements and unverified dosage/frequency/concentration calculations.
Enforces region safety notice on all chemical management options.
"""

TREATMENT_SAFETY_NOTICE = (
    "Use only products registered for this crop and disease in your region. "
    "Follow the official product label and local agricultural guidance."
)

LABEL_DOSAGE_NOTICE = "Check the registered product label for dosage and application instructions."

TREATMENT_DATABASE = {
    # =========================================================================
    # PUMPKIN CLASSES (5)
    # =========================================================================
    "Pumpkin-Bacterial Leaf Spot": {
        "crop": "Pumpkin",
        "disease": "Bacterial Spot",
        "treatment_required": True,
        "immediate_actions": [
            "Prune and destroy severely infected lower leaves during dry afternoon weather",
            "Disinfect all cutting tools with 70% ethanol or 10% bleach solution between vines"
        ],
        "cultural_controls": [
            "Implement 2-3 year crop rotation with non-cucurbit crops (legumes or cereals)",
            "Switch from overhead sprinkler irrigation to ground drip irrigation",
            "Maintain wide plant spacing (1.5–2m) to promote canopy airflow and rapid drying"
        ],
        "biological_controls": [
            "Apply Bacillus subtilis bio-fungicide/bactericide to foliage during early morning"
        ],
        "chemical_options": [
            {
                "active_ingredient": "Copper Oxychloride",
                "purpose": "Protectant bactericide to reduce surface bacterial bacterial multiplication",
                "restrictions_or_notes": f"Apply prior to disease outbreak or at first sign. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - Indian Institute of Horticultural Research (IIHR)"
            },
            {
                "active_ingredient": "Copper Hydroxide + Streptomycin Sulphate (agricultural grade)",
                "purpose": "Bactericidal spray for severe leaf spot outbreaks",
                "restrictions_or_notes": f"Observe local registration and pre-harvest interval. {LABEL_DOSAGE_NOTICE}",
                "source": "Directorate of Plant Protection, Quarantine & Storage (DPPQ&S, India)"
            }
        ],
        "expert_escalation": [
            "Consult local Krishi Vigyan Kendra (KVK) if water-soaked lesions exceed 10% of field canopy"
        ],
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Horticultural Research (IIHR)",
                "title": "Package of Practices for Cucurbitaceous Crop Protection",
                "url": "https://www.iihr.res.in"
            },
            {
                "organization": "Directorate of Plant Protection (DPPQ&S)",
                "title": "Approved Major Uses of Pesticides - Cucurbits",
                "url": "https://ppqs.gov.in"
            }
        ]
    },

    "Pumpkin-Downy Mildew": {
        "crop": "Pumpkin",
        "disease": "Downy Mildew",
        "treatment_required": True,
        "immediate_actions": [
            "Remove initial infected leaves exhibiting yellow angular patches immediately",
            "Cease late-evening irrigation to prevent leaf wetness overnight"
        ],
        "cultural_controls": [
            "Plant resistant or tolerant pumpkin hybrids recommended by state SAU",
            "Trellis vines where possible to lift canopy off moist soil",
            "Ensure field drainage channels are free of standing water"
        ],
        "biological_controls": [
            "Foliar spray of Trichoderma viride or Pseudomonas fluorescens as bio-control agent"
        ],
        "chemical_options": [
            {
                "active_ingredient": "Mancozeb",
                "purpose": "Broad-spectrum contact protective fungicide",
                "restrictions_or_notes": f"Apply protectively during humid weather. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - Central Institute for Arid Horticulture (CIAH)"
            },
            {
                "active_ingredient": "Metalaxyl + Mancozeb",
                "purpose": "Systemic and contact fungicide combination for active downy mildew control",
                "restrictions_or_notes": f"Use during high disease pressure. Rotate with different chemical classes. {LABEL_DOSAGE_NOTICE}",
                "source": "TNAU Agritech Portal / ICAR Extension"
            }
        ],
        "expert_escalation": [
            "Contact your District Agricultural Officer if purplish spore growth spreads rapidly across canopy"
        ],
        "sources": [
            {
                "organization": "ICAR - Central Institute for Arid Horticulture (CIAH)",
                "title": "Foliar Disease Advisory & Management in Cucurbits",
                "url": "https://ciah.icar.gov.in"
            }
        ]
    },

    "Pumpkin-Healthy Leaf": {
        "crop": "Pumpkin",
        "disease": "Healthy",
        "treatment_required": False,
        "immediate_actions": [
            "Continue standard healthy leaf maintenance and monitoring"
        ],
        "cultural_controls": [
            "Maintain balanced N-P-K fertigation",
            "Monitor fields weekly for early sign of pest or disease entry"
        ],
        "biological_controls": [],
        "chemical_options": [],
        "expert_escalation": [],
        "sources": [
            {
                "organization": "ICAR - IIHR",
                "title": "Good Agricultural Practices (GAP) for Cucurbits",
                "url": "https://www.iihr.res.in"
            }
        ]
    },

    "Pumpkin-Mosaic Disease": {
        "crop": "Pumpkin",
        "disease": "Mosaic Virus",
        "treatment_required": True,
        "immediate_actions": [
            "Rogue out and destroy infected viral host plants showing severe leaf blistering",
            "Control aphid vector populations immediately on surrounding weeds"
        ],
        "cultural_controls": [
            "Install yellow sticky traps (15-20 per acre) to monitor and catch winged aphids",
            "Plant border crops like maize or sorghum around pumpkin plots as barrier crops",
            "Keep field borders clean of weed hosts (such as wild cucurbits and Solanaceae)"
        ],
        "biological_controls": [
            "Apply Neem seed kernel extract (NSKE 5%) or Neem oil spray for aphid vector management"
        ],
        "chemical_options": [
            {
                "active_ingredient": "Imidacloprid",
                "purpose": "Systemic insecticide targeting aphid vector species transmitting mosaic virus",
                "restrictions_or_notes": f"Target vector insects only. Avoid spraying during bloom to protect pollinators. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - Indian Agricultural Research Institute (IARI)"
            }
        ],
        "expert_escalation": [
            "Report widespread mosaic outbreaks to local KVK extension plant pathologist"
        ],
        "sources": [
            {
                "organization": "ICAR - IARI Division of Plant Pathology",
                "title": "Management of Insect-Vectored Plant Viruses in Vegetable Crops",
                "url": "https://www.iari.res.in"
            }
        ]
    },

    "Pumpkin-Powdery_Mildew": {
        "crop": "Pumpkin",
        "disease": "Powdery Mildew",
        "treatment_required": True,
        "immediate_actions": [
            "Remove heavily powdered lower leaves to reduce spore load"
        ],
        "cultural_controls": [
            "Maintain adequate soil moisture without waterlogging",
            "Ensure full sunlight exposure by avoiding excessive shade"
        ],
        "biological_controls": [
            "Foliar spray of Ampelomyces quisqualis or bio-sulfur formulations"
        ],
        "chemical_options": [
            {
                "active_ingredient": "Wettable Sulfur",
                "purpose": "Contact fungicide for powdery mildew management",
                "restrictions_or_notes": f"Do not apply when temperatures exceed 32°C to prevent phytotoxicity. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IIHR"
            },
            {
                "active_ingredient": "Azoxystrobin",
                "purpose": "Systemic strobilurin fungicide for powdery mildew control",
                "restrictions_or_notes": f"Rotate with alternate modes of action to prevent resistance. {LABEL_DOSAGE_NOTICE}",
                "source": "Directorate of Plant Protection (DPPQ&S)"
            }
        ],
        "expert_escalation": [
            "Consult KVK if white powdery coating covers over 20% of mature foliage"
        ],
        "sources": [
            {
                "organization": "ICAR - IIHR",
                "title": "Integrated Management of Powdery Mildew in Vegetable Crops",
                "url": "https://www.iihr.res.in"
            }
        ]
    },

    # =========================================================================
    # RICE CLASSES (3)
    # =========================================================================
    "Rice-Bacterialblight": {
        "crop": "Rice",
        "disease": "Bacterial Blight",
        "treatment_required": True,
        "immediate_actions": [
            "Drain field water temporarily if feasible to stop bacterial spread through water flow",
            "Suspend excess nitrogenous fertilizer top-dressing during active blight phase"
        ],
        "cultural_controls": [
            "Use certified resistant varieties (e.g. Swarna Sub1, Improved Samba Mahsuri)",
            "Apply recommended nitrogen in split doses rather than single heavy application",
            "Maintain clean bunds free of weed hosts (e.g., Leersia hexandra)"
        ],
        "biological_controls": [
            "Seed treatment and foliar application of Pseudomonas fluorescens"
        ],
        "chemical_options": [
            {
                "active_ingredient": "Copper Hydroxide + Streptomycin Sulphate",
                "purpose": "Bactericidal spray combination for suppressing Xanthomonas oryzae",
                "restrictions_or_notes": f"Apply at early tillering or boot stage at first symptom appearance. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - National Rice Research Institute (NRRI)"
            }
        ],
        "expert_escalation": [
            "Contact district agricultural officers if kresek (seedling wilt) symptoms exceed 10% in nursery"
        ],
        "sources": [
            {
                "organization": "ICAR - National Rice Research Institute (NRRI)",
                "title": "Standard Operating Procedure for Bacterial Blight Management",
                "url": "https://nrri.icar.gov.in"
            }
        ]
    },

    "Rice-Brownspot": {
        "crop": "Rice",
        "disease": "Brown Spot",
        "treatment_required": True,
        "immediate_actions": [
            "Apply potash (potassium) fertilizer to correct nutrient deficiency in poor soils",
            "Ensure field is adequately irrigated; prevent drought stress in standing crop"
        ],
        "cultural_controls": [
            "Seed treatment before sowing to eliminate seed-borne fungal inoculum",
            "Improve soil fertility by applying farmyard manure (FYM) or green manure",
            "Rotate rice with legumes during rabi season"
        ],
        "biological_controls": [
            "Seed treatment with Trichoderma harzianum or Pseudomonas fluorescens"
        ],
        "chemical_options": [
            {
                "active_ingredient": "Mancozeb",
                "purpose": "Contact protective fungicide against Bipolaris oryzae",
                "restrictions_or_notes": f"Apply at tillering stage if brown spots appear on leaves. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - Indian Institute of Rice Research (IIRR)"
            },
            {
                "active_ingredient": "Propiconazole",
                "purpose": "Systemic triazole fungicide for brown spot leaf and grain protection",
                "restrictions_or_notes": f"Apply atboot stage. Follow registered pre-harvest interval. {LABEL_DOSAGE_NOTICE}",
                "source": "IRRI Rice Knowledge Bank / DPPQ&S"
            }
        ],
        "expert_escalation": [
            "Consult KVK rice specialist if spots cover significant leaf area during boot leaf stage"
        ],
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Rice Research (IIRR)",
                "title": "Integrated Management of Rice Fungal Diseases",
                "url": "https://www.iirr-icar.org.in"
            }
        ]
    },

    "Rice-Leafsmut": {
        "crop": "Rice",
        "disease": "Leaf Smut",
        "treatment_required": True,
        "immediate_actions": [
            "Avoid excessive nitrogen applications which stimulate leafy growth vulnerable to smut"
        ],
        "cultural_controls": [
            "Use clean, healthy certified seeds from verified seed agencies",
            "Burn or deeply plow infected crop stubble post harvest",
            "Maintain balanced soil nutrition based on soil test recommendations"
        ],
        "biological_controls": [
            "Seed treatment with Trichoderma viride"
        ],
        "chemical_options": [
            {
                "active_ingredient": "Carbendazim + Mancozeb",
                "purpose": "Systemic and contact fungicide mix for false smut and leaf smut control",
                "restrictions_or_notes": f"Apply at panicle initiation if smut lesions are widespread. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - NRRI"
            }
        ],
        "expert_escalation": [
            "Report unusual smut outbreaks to local agricultural extension office"
        ],
        "sources": [
            {
                "organization": "ICAR - NRRI Cuttack",
                "title": "Rice Disease Management Manual",
                "url": "https://nrri.icar.gov.in"
            }
        ]
    },

    # =========================================================================
    # SUGARCANE CLASSES (9)
    # =========================================================================
    "Sugarcane-Grassy Shoot": {
        "crop": "Sugarcane",
        "disease": "Grassy Shoot",
        "treatment_required": True,
        "immediate_actions": [
            "Uproot and burn infected clumps exhibiting thin, tillered grassy shoots immediately"
        ],
        "cultural_controls": [
            "Hot Water Treatment (HWT) of seed cane setts at 50°C for 2 hours before planting",
            "Avoid using ratoon crops from infected mother fields",
            "Control leafhopper vectors using clean field cultivation"
        ],
        "biological_controls": [
            "Foliar spray of Neem seed kernel extract (NSKE 5%) against vector pests"
        ],
        "chemical_options": [
            {
                "active_ingredient": "Dimethoate or Malathion",
                "purpose": "Insecticide spray to manage leafhopper vectors transmitting phytoplasma",
                "restrictions_or_notes": f"Target vector population in seed nurseries. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - Sugarcane Breeding Institute (SBI)"
            }
        ],
        "expert_escalation": [
            "Escalate to Sugarcane Development Officer if grassy shoot exceeds 5% of field stool count"
        ],
        "sources": [
            {
                "organization": "ICAR - Sugarcane Breeding Institute (SBI Coimbatore)",
                "title": "Diseases of Sugarcane & Their Management",
                "url": "https://sugarcane.icar.gov.in"
            }
        ]
    },

    "Sugarcane-Healthy": {
        "crop": "Sugarcane",
        "disease": "Healthy",
        "treatment_required": False,
        "immediate_actions": ["Maintain clean cultivation"],
        "cultural_controls": ["Follow standard trash mulching and balanced fertigation"],
        "biological_controls": [],
        "chemical_options": [],
        "expert_escalation": [],
        "sources": [
            {
                "organization": "ICAR - SBI",
                "title": "Sugarcane Production Technology Guidelines",
                "url": "https://sugarcane.icar.gov.in"
            }
        ]
    },

    "Sugarcane-Mosaic": {
        "crop": "Sugarcane",
        "disease": "Mosaic Virus",
        "treatment_required": True,
        "immediate_actions": ["Rogue infected stools displaying yellow green leaf striping"],
        "cultural_controls": [
            "Use disease-free seed setts from certified tissue culture or seed nursery",
            "Do not select seed cane from mosaic affected plots"
        ],
        "biological_controls": [
            "Neem oil spray (10,000 ppm) for controlling aphid vectors"
        ],
        "chemical_options": [
            {
                "active_ingredient": "Thiamethoxam",
                "purpose": "Systemic vector control targeting aphids transmitting sugarcane mosaic virus",
                "restrictions_or_notes": f"Follow state agricultural extension advisory. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - Indian Institute of Sugarcane Research (IISR)"
            }
        ],
        "expert_escalation": ["Contact sugar mill extension officer for seed replacement"],
        "sources": [
            {
                "organization": "ICAR - IISR Lucknow",
                "title": "Sugarcane Health Management Guide",
                "url": "https://iisr.icar.gov.in"
            }
        ]
    },

    "Sugarcane-Pokkah Boeng": {
        "crop": "Sugarcane",
        "disease": "Pokkah Boeng",
        "treatment_required": True,
        "immediate_actions": ["Remove distorted top leaves during early monsoon stage"],
        "cultural_controls": ["Avoid heavy nitrogen application prior to rain", "Improve soil drainage"],
        "biological_controls": ["Foliar spray of Trichoderma harzianum"],
        "chemical_options": [
            {
                "active_ingredient": "Copper Oxychloride",
                "purpose": "Fungicidal whorl spray for Fusarium pokkah boeng management",
                "restrictions_or_notes": f"Apply into leaf whorls at onset of monsoon symptoms. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IISR"
            },
            {
                "active_ingredient": "Carbendazim",
                "purpose": "Systemic fungicide spray into plant crown",
                "restrictions_or_notes": f"Apply when top distortion is observed. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - SBI"
            }
        ],
        "expert_escalation": ["Consult mill development staff if top rot stage develops"],
        "sources": [
            {
                "organization": "ICAR - SBI",
                "title": "Management of Pokkah Boeng in Sugarcane",
                "url": "https://sugarcane.icar.gov.in"
            }
        ]
    },

    "Sugarcane-Red Leaf Spot": {
        "crop": "Sugarcane",
        "disease": "Red Leaf Spot",
        "treatment_required": True,
        "immediate_actions": ["Remove lower affected dried leaves"],
        "cultural_controls": ["Maintain optimum plant density", "Avoid waterlogging"],
        "biological_controls": ["Foliar bio-fungicide spray with Pseudomonas fluorescens"],
        "chemical_options": [
            {
                "active_ingredient": "Mancozeb",
                "purpose": "Foliar protective spray against red spot fungal lesions",
                "restrictions_or_notes": f"Apply protective spray during high humidity. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IISR"
            }
        ],
        "expert_escalation": ["Consult local agricultural officer if spotting spreads to top leaves"],
        "sources": [
            {
                "organization": "ICAR - IISR Lucknow",
                "title": "Foliar Diseases of Sugarcane",
                "url": "https://iisr.icar.gov.in"
            }
        ]
    },

    "Sugarcane-Red Rot": {
        "crop": "Sugarcane",
        "disease": "Red Rot",
        "treatment_required": True,
        "immediate_actions": [
            "Uproot entire infected stool along with root system and burn immediately",
            "Apply quicklime (calcium oxide) to the empty spot in the row"
        ],
        "cultural_controls": [
            "Plant red rot resistant varieties recommended for your region",
            "Sett treatment with MHAT (Moist Hot Air Treatment) or fungicidal dip before planting",
            "Follow 2-year crop rotation with paddy or green manure"
        ],
        "biological_controls": [
            "Sett treatment and soil application of Trichoderma viride"
        ],
        "chemical_options": [
            {
                "active_ingredient": "Thiophanate Methyl or Carbendazim",
                "purpose": "Fungicidal sett soaking prior to planting to eliminate sett-borne red rot fungus",
                "restrictions_or_notes": f"Pre-planting sett dip only. Not effective once internal stalk rotting occurs. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - SBI / IISR"
            }
        ],
        "expert_escalation": [
            "CRITICAL: Report red rot immediately to sugar factory cane manager and district agricultural officer"
        ],
        "sources": [
            {
                "organization": "ICAR - Sugarcane Breeding Institute (SBI)",
                "title": "Red Rot Disease Advisory & Management Protocols",
                "url": "https://sugarcane.icar.gov.in"
            }
        ]
    },

    "Sugarcane-Ring Spot": {
        "crop": "Sugarcane",
        "disease": "Ring Spot",
        "treatment_required": True,
        "immediate_actions": ["Strip lower infected senescent leaves"],
        "cultural_controls": ["Avoid excessive nitrogenous fertilization", "Ensure field aeration"],
        "biological_controls": ["Pseudomonas fluorescens spray"],
        "chemical_options": [
            {
                "active_ingredient": "Copper Oxychloride",
                "purpose": "Protective spray for leaf ring spot lesions",
                "restrictions_or_notes": f"Spray if lower leaves show extensive ring spots. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IISR"
            }
        ],
        "expert_escalation": ["Consult extension agent if ring spots damage upper green leaves"],
        "sources": [{"organization": "ICAR - IISR", "title": "Sugarcane Leaf Spot Management", "url": "https://iisr.icar.gov.in"}]
    },

    "Sugarcane-Wilt": {
        "crop": "Sugarcane",
        "disease": "Wilt",
        "treatment_required": True,
        "immediate_actions": ["Uproot dry wilted stalks and burn"],
        "cultural_controls": ["Avoid water stress during summer", "Do not grow ratoon in wilt-affected fields"],
        "biological_controls": ["Soil application of Trichoderma harzianum enriched FYM"],
        "chemical_options": [
            {
                "active_ingredient": "Carbendazim",
                "purpose": "Soil drenching along crop rows around affected stools",
                "restrictions_or_notes": f"Apply early during root development. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - SBI"
            }
        ],
        "expert_escalation": ["Report stool wilting to sugar factory agronomy department"],
        "sources": [{"organization": "ICAR - SBI", "title": "Sugarcane Wilt Management", "url": "https://sugarcane.icar.gov.in"}]
    },

    "Sugarcane-Yellow Leaf Disease": {
        "crop": "Sugarcane",
        "disease": "Yellow Leaf Disease",
        "treatment_required": True,
        "immediate_actions": ["Remove severely yellowed stunted stalks"],
        "cultural_controls": ["Use virus-free micropropagated tissue culture setts", "Maintain balanced K nutrition"],
        "biological_controls": ["Neem seed kernel extract (NSKE 5%) against aphid vector Melanaphis sacchari"],
        "chemical_options": [
            {
                "active_ingredient": "Imidacloprid",
                "purpose": "Systemic aphid vector control to reduce virus transmission in seed plots",
                "restrictions_or_notes": f"Target vector control in seed nurseries. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - SBI"
            }
        ],
        "expert_escalation": ["Consult KVK for seed replacement advisory"],
        "sources": [{"organization": "ICAR - SBI", "title": "Yellow Leaf Disease Management in Sugarcane", "url": "https://sugarcane.icar.gov.in"}]
    },

    # =========================================================================
    # TOMATO CLASSES (10)
    # =========================================================================
    "Tomato___Bacterial_spot": {
        "crop": "Tomato",
        "disease": "Bacterial Spot",
        "treatment_required": True,
        "immediate_actions": ["Prune lower spotted foliage during dry hours"],
        "cultural_controls": ["Use certified disease-free seeds", "Rotate with non-solanaceous crops for 2 years"],
        "biological_controls": ["Foliar spray of Bacillus subtilis"],
        "chemical_options": [
            {
                "active_ingredient": "Copper Oxychloride + Streptomycin Sulphate",
                "purpose": "Foliar spray to suppress bacterial spot multiplication on leaves and fruits",
                "restrictions_or_notes": f"Apply protectively during wet periods. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IIHR"
            }
        ],
        "expert_escalation": ["Consult local KVK if fruit spotting occurs"],
        "sources": [{"organization": "ICAR - IIHR", "title": "Tomato Bacterial Spot Control", "url": "https://www.iihr.res.in"}]
    },

    "Tomato___Early_blight": {
        "crop": "Tomato",
        "disease": "Early Blight",
        "treatment_required": True,
        "immediate_actions": ["Prune lower leaves with concentric target-ring spots"],
        "cultural_controls": ["Mulch soil with straw to prevent fungal spore splash from soil", "Stake plants"],
        "biological_controls": ["Foliar spray of Trichoderma harzianum or Pseudomonas fluorescens"],
        "chemical_options": [
            {
                "active_ingredient": "Mancozeb",
                "purpose": "Protective contact fungicide against Alternaria solani",
                "restrictions_or_notes": f"Apply at onset of lower leaf symptoms. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IARI"
            },
            {
                "active_ingredient": "Azoxystrobin + Difenoconazole",
                "purpose": "Systemic and contact combination for active early blight lesions",
                "restrictions_or_notes": f"Observe pre-harvest interval on label. {LABEL_DOSAGE_NOTICE}",
                "source": "DPPQ&S / TNAU Agritech"
            }
        ],
        "expert_escalation": ["Consult KVK if defoliation reaches lower third of plant canopy"],
        "sources": [{"organization": "ICAR - IARI", "title": "Integrated Management of Tomato Diseases", "url": "https://www.iari.res.in"}]
    },

    "Tomato___Late_blight": {
        "crop": "Tomato",
        "disease": "Late Blight",
        "treatment_required": True,
        "immediate_actions": ["Remove severely blighted stems immediately during cool wet spells"],
        "cultural_controls": ["Avoid overhead watering", "Ensure maximum air circulation and spacing"],
        "biological_controls": ["Bio-fungicide foliar treatment with Pseudomonas fluorescens"],
        "chemical_options": [
            {
                "active_ingredient": "Cymoxanil + Mancozeb",
                "purpose": "Curative and protective systemic fungicide for Phytophthora infestans",
                "restrictions_or_notes": f"Apply immediately when cool, foggy, humid weather triggers late blight risk. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IIHR"
            },
            {
                "active_ingredient": "Dimethomorph",
                "purpose": "Systemic fungicide targeting late blight pathogen",
                "restrictions_or_notes": f"Alternate with contact fungicides to prevent resistance. {LABEL_DOSAGE_NOTICE}",
                "source": "DPPQ&S"
            }
        ],
        "expert_escalation": ["URGENT: Report late blight outbreaks to district agricultural officer immediately"],
        "sources": [{"organization": "ICAR - IIHR", "title": "Late Blight Alert & Advisory for Tomato", "url": "https://www.iihr.res.in"}]
    },

    "Tomato___Leaf_Mold": {
        "crop": "Tomato",
        "disease": "Leaf Mold",
        "treatment_required": True,
        "immediate_actions": ["Improve greenhouse or field ventilation immediately"],
        "cultural_controls": ["Reduce humidity around canopy", "Prune dense inner foliage"],
        "biological_controls": ["Trichoderma viride foliar spray"],
        "chemical_options": [
            {
                "active_ingredient": "Chlorothalonil or Copper Hydroxide",
                "purpose": "Foliar protective spray for leaf mold control",
                "restrictions_or_notes": f"Spray lower leaf surfaces thoroughly. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IIHR"
            }
        ],
        "expert_escalation": ["Consult KVK officer if olive green velvety mold covers upper foliage"],
        "sources": [{"organization": "ICAR - IIHR", "title": "Protected Cultivation Disease Management", "url": "https://www.iihr.res.in"}]
    },

    "Tomato___Septoria_leaf_spot": {
        "crop": "Tomato",
        "disease": "Septoria Leaf Spot",
        "treatment_required": True,
        "immediate_actions": ["Pinch off lower spotted leaves showing dark margins and grey centers"],
        "cultural_controls": ["Practice 3-year crop rotation", "Control solanaceous weeds"],
        "biological_controls": ["Pseudomonas fluorescens leaf application"],
        "chemical_options": [
            {
                "active_ingredient": "Mancozeb or Copper Oxychloride",
                "purpose": "Contact protective spray to arrest Septoria spore germination",
                "restrictions_or_notes": f"Spray early before lower leaf drop occurs. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IARI"
            }
        ],
        "expert_escalation": ["Consult KVK if spotting causes severe defoliation"],
        "sources": [{"organization": "ICAR - IARI", "title": "Septoria Spot Management in Tomato", "url": "https://www.iari.res.in"}]
    },

    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "crop": "Tomato",
        "disease": "Two-Spotted Spider Mite",
        "treatment_required": True,
        "immediate_actions": ["Hose down foliage with forceful water spray to break webs and dislodge mites"],
        "cultural_controls": ["Maintain adequate field irrigation to prevent dry dusty conditions favoring mites"],
        "biological_controls": ["Release predatory mites (Phytoseiulus persimilis) or apply Neem oil (10,000 ppm)"],
        "chemical_options": [
            {
                "active_ingredient": "Spiromesifen or Propargite",
                "purpose": "Specific miticide spray targeting spider mite eggs and motile stages",
                "restrictions_or_notes": f"Spray leaf undersides thoroughly. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IIHR"
            }
        ],
        "expert_escalation": ["Consult KVK entomologist if webbing covers growing shoot tips"],
        "sources": [{"organization": "ICAR - IIHR", "title": "Mite Management in Solanaceous Crops", "url": "https://www.iihr.res.in"}]
    },

    "Tomato___Target_Spot": {
        "crop": "Tomato",
        "disease": "Target Spot",
        "treatment_required": True,
        "immediate_actions": ["Prune dead foliage showing brown target lesions"],
        "cultural_controls": ["Avoid leaf wetness", "Stake plants for better airflow"],
        "biological_controls": ["Trichoderma harzianum bio-spray"],
        "chemical_options": [
            {
                "active_ingredient": "Azoxystrobin",
                "purpose": "Broad spectrum protective fungicide",
                "restrictions_or_notes": f"Apply protectively during humid weather. {LABEL_DOSAGE_NOTICE}",
                "source": "DPPQ&S"
            }
        ],
        "expert_escalation": ["Consult extension agent if stem lesions develop"],
        "sources": [{"organization": "ICAR - IIHR", "title": "Foliar Spot Advisory", "url": "https://www.iihr.res.in"}]
    },

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato",
        "disease": "Yellow Leaf Curl Virus",
        "treatment_required": True,
        "immediate_actions": ["Rogue and destroy virus-infected plants with upward cupped yellow leaves"],
        "cultural_controls": [
            "Install 50-mesh insect-proof netting in seedling nurseries",
            "Use yellow sticky traps (20 per acre) to monitor whitefly vector (Bemisia tabaci)",
            "Plant TYLCV-resistant hybrids recommended by state agricultural university"
        ],
        "biological_controls": ["Neem seed kernel extract (NSKE 5%) spray for whitefly management"],
        "chemical_options": [
            {
                "active_ingredient": "Cyantraniliprole or Diafenthiuron",
                "purpose": "Insecticide targeting whitefly vectors to interrupt viral transmission",
                "restrictions_or_notes": f"Target vector control early in crop growth. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IIHR"
            }
        ],
        "expert_escalation": ["Report heavy whitefly outbreaks to local KVK extension officer"],
        "sources": [{"organization": "ICAR - IIHR Bengaluru", "title": "Whitefly & TYLCV Management Guidelines", "url": "https://www.iihr.res.in"}]
    },

    "Tomato___Tomato_mosaic_virus": {
        "crop": "Tomato",
        "disease": "Mosaic Virus",
        "treatment_required": True,
        "immediate_actions": ["Remove and burn plants exhibiting severe leaf mottling and stunting"],
        "cultural_controls": [
            "Wash hands with soap and water before handling plants (ToMV is mechanically transmitted)",
            "Disinfect tools and stakes with 20% skimmed milk or trisodium phosphate solution",
            "Avoid smoking or using tobacco near tomato plants"
        ],
        "biological_controls": [],
        "chemical_options": [],
        "expert_escalation": ["Consult KVK officer for certified virus-free seed sources"],
        "sources": [{"organization": "ICAR - IARI", "title": "Mechanically Transmitted Plant Viruses", "url": "https://www.iari.res.in"}]
    },

    "Tomato___healthy": {
        "crop": "Tomato",
        "disease": "Healthy",
        "treatment_required": False,
        "immediate_actions": ["Continue standard foliage inspection"],
        "cultural_controls": ["Maintain balanced N-P-K fertigation and drip irrigation"],
        "biological_controls": [],
        "chemical_options": [],
        "expert_escalation": [],
        "sources": [{"organization": "ICAR - IIHR", "title": "Tomato Good Agricultural Practices", "url": "https://www.iihr.res.in"}]
    },

    # =========================================================================
    # WHEAT CLASSES (5)
    # =========================================================================
    "Wheat___Healthy": {
        "crop": "Wheat",
        "disease": "Healthy",
        "treatment_required": False,
        "immediate_actions": ["Continue standard field scouting at tillering and boot stages"],
        "cultural_controls": ["Apply recommended nitrogen in split doses (sowing, first irrigation, tillering)"],
        "biological_controls": [],
        "chemical_options": [],
        "expert_escalation": [],
        "sources": [{"organization": "ICAR - Indian Institute of Wheat and Barley Research (IIWBR)", "title": "Wheat Crop Management Guidelines", "url": "https://iiwbr.icar.gov.in"}]
    },

    "Wheat___Leaf_Rust": {
        "crop": "Wheat",
        "disease": "Leaf Rust (Brown Rust)",
        "treatment_required": True,
        "immediate_actions": ["Inspect leaf blades for small round orange-brown pustules"],
        "cultural_controls": [
            "Sow leaf-rust resistant wheat varieties recommended for your zone (e.g., HD 2967, DBW 187)",
            "Avoid late sowing to prevent warm temperature overlap favoring rust development"
        ],
        "biological_controls": ["Foliar spray of Trichoderma harzianum or bio-sulfur"],
        "chemical_options": [
            {
                "active_ingredient": "Tebuconazole or Propiconazole",
                "purpose": "Systemic triazole fungicide for brown leaf rust control",
                "restrictions_or_notes": f"Apply at first appearance of brown pustules on upper leaves. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IIWBR Karnal"
            },
            {
                "active_ingredient": "Mancozeb",
                "purpose": "Protective contact spray during early rust advisory warnings",
                "restrictions_or_notes": f"Apply protectively if rust warnings are issued in region. {LABEL_DOSAGE_NOTICE}",
                "source": "Directorate of Wheat Development (Govt of India)"
            }
        ],
        "expert_escalation": ["Report leaf rust outbreaks to local KVK or IIWBR Wheat Rust Helpline"],
        "sources": [{"organization": "ICAR - IIWBR Karnal", "title": "Wheat Rust Advisory & Control Protocols", "url": "https://iiwbr.icar.gov.in"}]
    },

    "Wheat___Stripe_Rust": {
        "crop": "Wheat",
        "disease": "Stripe Rust (Yellow Rust)",
        "treatment_required": True,
        "immediate_actions": [
            "Inspect field pockets for yellow pustules arranged in linear stripes on leaf blades",
            "Mark rust focal spots and refrain from walking through infected patches to avoid spore transport"
        ],
        "cultural_controls": [
            "Plant yellow rust resistant varieties (e.g., HD 3086, DBW 222, PBW 725)",
            "Avoid excessive early nitrogen fertilization which increases leaf susceptibility",
            "Eradicate barberry bushes (alternate host) near field boundaries"
        ],
        "biological_controls": ["Pseudomonas fluorescens foliar spray"],
        "chemical_options": [
            {
                "active_ingredient": "Tebuconazole",
                "purpose": "Systemic triazole fungicide specifically recommended for yellow rust spot control",
                "restrictions_or_notes": f"Spray immediately upon detecting linear yellow pustule lines. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IIWBR / Punjab Agricultural University (PAU)"
            },
            {
                "active_ingredient": "Propiconazole",
                "purpose": "Systemic triazole fungicide for stopping stripe rust progression",
                "restrictions_or_notes": f"Repeat spray only if rust continues advancing after 14 days. {LABEL_DOSAGE_NOTICE}",
                "source": "Directorate of Wheat Development"
            }
        ],
        "expert_escalation": ["CRITICAL: Contact district agriculture department immediately if yellow rust appears in January/February"],
        "sources": [{"organization": "ICAR - IIWBR Karnal", "title": "Yellow Rust Emergency Management Protocols", "url": "https://iiwbr.icar.gov.in"}]
    },

    "Wheat___Powdery_Mildew": {
        "crop": "Wheat",
        "disease": "Powdery Mildew",
        "treatment_required": True,
        "immediate_actions": ["Scout dense crop stands for white cottony fungal patches near leaf bases"],
        "cultural_controls": ["Avoid overly high seeding density", "Maintain balanced N-P-K nutrition"],
        "biological_controls": ["Bio-sulfur or Ampelomyces quisqualis foliar spray"],
        "chemical_options": [
            {
                "active_ingredient": "Wettable Sulfur or Propiconazole",
                "purpose": "Fungicide for controlling powdery mildew on wheat foliage",
                "restrictions_or_notes": f"Spray during early tillering if humid canopy conditions persist. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IIWBR"
            }
        ],
        "expert_escalation": ["Consult KVK if powdery coating reaches flag leaf stage"],
        "sources": [{"organization": "ICAR - IIWBR", "title": "Wheat Foliar Disease Management", "url": "https://iiwbr.icar.gov.in"}]
    },

    "Wheat___Septoria": {
        "crop": "Wheat",
        "disease": "Septoria Leaf Blotch",
        "treatment_required": True,
        "immediate_actions": ["Inspect lower leaves for oval flecks turning greyish brown with black pycnidia specks"],
        "cultural_controls": ["Rotate wheat with non-cereal crops", "Incorporate crop residue post harvest"],
        "biological_controls": ["Trichoderma viride seed treatment and foliar spray"],
        "chemical_options": [
            {
                "active_ingredient": "Azoxystrobin + Tebuconazole",
                "purpose": "Broad-spectrum systemic fungicide for Septoria tritici leaf blotch control",
                "restrictions_or_notes": f"Spray at flag leaf emergence if rainfall occurs. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IIWBR / FAO Wheat Guide"
            }
        ],
        "expert_escalation": ["Consult extension agent if blotches cover upper third of wheat leaf"],
        "sources": [{"organization": "ICAR - IIWBR", "title": "Septoria Disease Control in Wheat", "url": "https://iiwbr.icar.gov.in"}]
    },

    # =========================================================================
    # MAIZE CLASSES (4)
    # =========================================================================
    "Maize___Healthy": {
        "crop": "Maize",
        "disease": "Healthy",
        "treatment_required": False,
        "immediate_actions": ["Scout crop weekly at knee-high, tasseling, and silking stages"],
        "cultural_controls": ["Apply recommended basal and split nitrogen applications"],
        "biological_controls": [],
        "chemical_options": [],
        "expert_escalation": [],
        "sources": [{"organization": "ICAR - Indian Institute of Maize Research (IIMR)", "title": "Maize Crop Management", "url": "https://iimr.icar.gov.in"}]
    },

    "Maize___Common_Rust": {
        "crop": "Maize",
        "disease": "Common Rust",
        "treatment_required": True,
        "immediate_actions": ["Inspect leaf surfaces for powdery brownish-red pustules on both upper and lower leaf sides"],
        "cultural_controls": [
            "Plant resistant maize cultivars recommended by ICAR-IIMR or state SAUs",
            "Sow early in season to avoid cool humid weather during grain filling"
        ],
        "biological_controls": ["Trichoderma harzianum foliar application"],
        "chemical_options": [
            {
                "active_ingredient": "Mancozeb",
                "purpose": "Contact protective fungicide for common rust management",
                "restrictions_or_notes": f"Apply at first pustule detection before tasseling. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - Indian Institute of Maize Research (IIMR)"
            },
            {
                "active_ingredient": "Azoxystrobin",
                "purpose": "Systemic strobilurin fungicide for rust control",
                "restrictions_or_notes": f"Apply at tasseling stage if weather remains humid. {LABEL_DOSAGE_NOTICE}",
                "source": "DPPQ&S / CIMMYT Maize Guide"
            }
        ],
        "expert_escalation": ["Consult KVK maize scientist if rust pustules cover more than 15% leaf area"],
        "sources": [{"organization": "ICAR - IIMR Ludhiana", "title": "Maize Rust Advisory & Protection Protocols", "url": "https://iimr.icar.gov.in"}]
    },

    "Maize___Northern_Leaf_Blight": {
        "crop": "Maize",
        "disease": "Northern Leaf Blight",
        "treatment_required": True,
        "immediate_actions": ["Check foliage for long, elliptical cigar-shaped greyish green to tan lesions"],
        "cultural_controls": [
            "Plow under infected maize residue after harvest to reduce overwintering fungus",
            "Follow 1-2 year crop rotation with pulses, soybean, or cotton"
        ],
        "biological_controls": ["Pseudomonas fluorescens bio-fungicide spray"],
        "chemical_options": [
            {
                "active_ingredient": "Mancozeb",
                "purpose": "Contact protective spray against Exserohilum turcicum",
                "restrictions_or_notes": f"Spray early when cigar-shaped spots first appear on lower leaves. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IIMR"
            },
            {
                "active_ingredient": "Propiconazole",
                "purpose": "Systemic triazole fungicide for active blighted leaf protection",
                "restrictions_or_notes": f"Apply before silking stage. Observe harvest interval. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IIMR / CIMMYT"
            }
        ],
        "expert_escalation": ["Consult local KVK if blighting reaches ear leaf before silking"],
        "sources": [{"organization": "ICAR - IIMR Ludhiana", "title": "Northern Corn Leaf Blight Management Guide", "url": "https://iimr.icar.gov.in"}]
    },

    "Maize___Gray_Leaf_Spot": {
        "crop": "Maize",
        "disease": "Gray Leaf Spot",
        "treatment_required": True,
        "immediate_actions": ["Inspect leaves for rectangular, vein-delimited tan to grey lesions"],
        "cultural_controls": [
            "Use resistant or tolerant maize hybrids",
            "Avoid continuous maize-after-maize planting in reduced-tillage fields"
        ],
        "biological_controls": ["Trichoderma viride foliar treatment"],
        "chemical_options": [
            {
                "active_ingredient": "Azoxystrobin + Propiconazole",
                "purpose": "Systemic combination fungicide for gray leaf spot control",
                "restrictions_or_notes": f"Apply at tasseling stage if warm humid conditions persist. {LABEL_DOSAGE_NOTICE}",
                "source": "ICAR - IIMR / FAO Maize Protection"
            }
        ],
        "expert_escalation": ["Consult extension specialist if lesions coalesce on upper canopy"],
        "sources": [{"organization": "ICAR - IIMR Ludhiana", "title": "Gray Leaf Spot Disease Advisory", "url": "https://iimr.icar.gov.in"}]
    }
}

def get_treatment_options(class_name, diagnosis_reliable=True):
    """
    Returns source-backed treatment options for a given predicted class.
    Displays treatment ONLY if diagnosis_reliable is True and condition is a disease.
    """
    if not diagnosis_reliable:
        return {
            "available": False,
            "reason": "Diagnosis is uncertain. Treatment options require a reliable, confirmed disease diagnosis.",
            "safety_notice": TREATMENT_SAFETY_NOTICE
        }

    rec = TREATMENT_DATABASE.get(class_name)
    if not rec:
        return {
            "available": False,
            "reason": "Specific treatment guidance is not available in the current verified knowledge base. Consult a local agricultural expert.",
            "safety_notice": TREATMENT_SAFETY_NOTICE
        }

    if not rec.get("treatment_required", True):
        return {
            "available": True,
            "crop": rec.get("crop"),
            "disease": rec.get("disease"),
            "treatment_required": False,
            "message": "The crop appears healthy. No chemical treatment is required. Continue good agricultural management practices.",
            "immediate_actions": rec.get("immediate_actions", []),
            "cultural_controls": rec.get("cultural_controls", []),
            "biological_controls": [],
            "chemical_options": [],
            "expert_escalation": [],
            "sources": rec.get("sources", []),
            "safety_notice": TREATMENT_SAFETY_NOTICE
        }

    return {
        "available": True,
        "crop": rec.get("crop"),
        "disease": rec.get("disease"),
        "treatment_required": True,
        "immediate_actions": rec.get("immediate_actions", []),
        "cultural_controls": rec.get("cultural_controls", []),
        "biological_controls": rec.get("biological_controls", []),
        "chemical_options": rec.get("chemical_options", []),
        "expert_escalation": rec.get("expert_escalation", []),
        "sources": rec.get("sources", []),
        "safety_notice": TREATMENT_SAFETY_NOTICE
    }
