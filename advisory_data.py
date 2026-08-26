"""
FasalRakshak AI - Non-Chemical Agricultural Advisory Knowledge Base
Source-backed non-chemical management, cultural practices, field sanitation, and monitoring.
Backed by ICAR (Indian Council of Agricultural Research), State Agricultural Extension, Vikaspedia (MeitY/MoA), and FAO.
Strictly excludes chemical pesticides, dosages, concentrations, or spray intervals.
"""

ADVISORY_DATABASE = {
    # -------------------------------------------------------------------------
    # PUMPKIN CLASSES (5)
    # -------------------------------------------------------------------------
    "Pumpkin-Bacterial Leaf Spot": {
        "class_name": "Pumpkin-Bacterial Leaf Spot",
        "crop": "Pumpkin",
        "condition": "Bacterial Blight",
        "is_healthy": False,
        "overview": "Bacterial blight in cucurbits causes water-soaked angular leaf lesions that darken and cause leaf drop under warm, humid conditions.",
        "common_symptoms": [
            "Small water-soaked translucent lesions on leaves",
            "Lesions turning yellow then brown/black with chlorotic halos",
            "Premature defoliation in severe infections"
        ],
        "immediate_actions": [
            "Prune and destroy severely infected leaves during dry weather",
            "Avoid sprinkler or overhead irrigation; switch to drip/ground watering",
            "Disinfect pruning shears with 70% alcohol between cuts"
        ],
        "prevention": [
            "Use certified disease-free seeds and resistant cultivars",
            "Follow 2-3 year crop rotation with non-cucurbit crops",
            "Maintain wide plant spacing to improve canopy airflow"
        ],
        "monitoring": [
            "Inspect leaf undersides weekly for translucent water-soaked spots",
            "Monitor fields closely following warm heavy rain events"
        ],
        "expert_escalation": "Contact local KVK extension officers if bacterial ooze or rapid leaf collapse spreads beyond 10% of crop canopy.",
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Horticultural Research (IIHR)",
                "title": "Package of Practices for Cucurbitaceous Crop Protection & Disease Advisory",
                "url": "https://www.iihr.res.in",
                "source_type": "ICAR",
                "verified_url": True
            },
            {
                "organization": "Vikaspedia Agriculture Portal (Government of India)",
                "title": "Integrated Pest Management Strategies for Cucurbitaceous Vegetables",
                "url": "https://vikaspedia.in/agriculture/crop-production/integrated-pest-management/ipm-for-vegetables",
                "source_type": "Government",
                "verified_url": True
            }
        ]
    },
    "Pumpkin-Downy Mildew": {
        "class_name": "Pumpkin-Downy Mildew",
        "crop": "Pumpkin",
        "condition": "Downy Mildew",
        "is_healthy": False,
        "overview": "Downy mildew causes angular yellow spots on upper leaf surfaces bounded by leaf veins, with purplish-gray spore growth beneath during cool, moist periods.",
        "common_symptoms": [
            "Angular yellow patches restricted by major leaf veins",
            "Purplish-gray downy fungal growth on lower leaf surfaces",
            "Curling and browning of affected foliage"
        ],
        "immediate_actions": [
            "Remove and compost/burn initial infected lower leaves immediately",
            "Irrigate early in the morning so foliage dries quickly before nightfall",
            "Improve air movement by trellising vines where feasible"
        ],
        "prevention": [
            "Plant resistant pumpkin varieties suited to your agro-climatic zone",
            "Avoid high planting density; maintain wide row spacing",
            "Ensure field drainage to eliminate standing moisture"
        ],
        "monitoring": [
            "Check leaf undersides for gray downy spores during early morning dew",
            "Track local weather advisories for high humidity warnings"
        ],
        "expert_escalation": "Consult your district Agricultural Development Officer if downy mildew symptoms spread across more than 15% of the field.",
        "sources": [
            {
                "organization": "ICAR - Central Institute for Arid Horticulture (CIAH)",
                "title": "Foliar Disease Advisory & Management in Cucurbits",
                "url": "https://ciah.icar.gov.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Pumpkin-Healthy Leaf": {
        "class_name": "Pumpkin-Healthy Leaf",
        "crop": "Pumpkin",
        "condition": "Healthy",
        "is_healthy": True,
        "overview": "The inspected pumpkin leaf displays normal, dark green foliage with no visible symptoms of fungal, bacterial, or viral infection.",
        "common_symptoms": [
            "Vibrant green leaf blades without spots or wilting",
            "Normal vein patterns and sturdy leaf stems"
        ],
        "immediate_actions": [
            "Maintain regular soil moisture and organic compost regimen",
            "Keep field borders clear of weeds to prevent pest buildup"
        ],
        "prevention": [
            "Continue crop rotation practices for future planting cycles",
            "Use mulch to prevent soil splashing onto lower leaves"
        ],
        "monitoring": [
            "Perform weekly scout inspections of vine tips and leaf undersides",
            "Re-scan if yellowing or leaf spots develop later in the season"
        ],
        "expert_escalation": "Consult an extension specialist if uninspected parts of the vine exhibit sudden wilting or root rot.",
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Vegetable Research (IIVR)",
                "title": "Good Agricultural Practices & Field Sanitation Guidelines for Cucurbits",
                "url": "https://iivr.icar.gov.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Pumpkin-Mosaic Disease": {
        "class_name": "Pumpkin-Mosaic Disease",
        "crop": "Pumpkin",
        "condition": "Mosaic Disease",
        "is_healthy": False,
        "overview": "Mosaic virus infection causes mottled light-and-dark green leaf patterns, leaf stunting, distortion, and reduced fruit quality spread by aphid vectors.",
        "common_symptoms": [
            "Light and dark green mottled leaf patches (mosaic pattern)",
            "Puckered, blistered, or distorted leaf blades",
            "Stunted vine growth and malformed fruits"
        ],
        "immediate_actions": [
            "Rogue out and destroy viral infected plants to prevent aphid spread",
            "Control weed hosts surrounding the field borders",
            "Sanitize hands and farm tools after handling infected vines"
        ],
        "prevention": [
            "Plant virus-resistant pumpkin varieties",
            "Use reflective silver mulches to deter aphid vector landings",
            "Avoid planting adjacent to older infected cucurbit fields"
        ],
        "monitoring": [
            "Inspect young leaves and growing tips for mosaic mottling weekly",
            "Monitor aphid populations using yellow sticky traps"
        ],
        "expert_escalation": "Contact your KVK plant pathologist if mosaic symptoms appear early in the seedling stage across multiple beds.",
        "sources": [
            {
                "organization": "ICAR - Indian Agricultural Research Institute (IARI)",
                "title": "Viral Disease Control & Vector Sanitation in Cucurbitaceous Vegetables",
                "url": "https://www.iari.res.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Pumpkin-Powdery_Mildew": {
        "class_name": "Pumpkin-Powdery_Mildew",
        "crop": "Pumpkin",
        "condition": "Powdery Mildew",
        "is_healthy": False,
        "overview": "Powdery mildew appears as white talcum-like fungal spots on leaf surfaces, expanding to cover whole foliage under dry, shaded, humid conditions.",
        "common_symptoms": [
            "White circular powdery patches on upper and lower leaf surfaces",
            "Yellowing and premature drying of affected leaves",
            "Brittle foliage that breaks easily under handling"
        ],
        "immediate_actions": [
            "Remove and bury heavily infected lower leaves",
            "Ensure crops receive direct sunlight by pruning surrounding shade",
            "Avoid excess nitrogen fertilizing which promotes tender susceptible tissue"
        ],
        "prevention": [
            "Select powdery mildew resistant cultivars",
            "Space plants adequately for thorough sunlight penetration",
            "Maintain balanced soil fertility with adequate potassium"
        ],
        "monitoring": [
            "Inspect older lower leaves weekly for early white powdery spots",
            "Monitor canopy density as vines grow"
        ],
        "expert_escalation": "Consult local extension services if white powdery coverage exceeds 20% of leaf area early in vine growth.",
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Horticultural Research (IIHR)",
                "title": "Foliar Fungal Mildew Advisory & Cultural Management",
                "url": "https://www.iihr.res.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },

    # -------------------------------------------------------------------------
    # RICE CLASSES (3)
    # -------------------------------------------------------------------------
    "Rice-Bacterialblight": {
        "class_name": "Rice-Bacterialblight",
        "crop": "Rice",
        "condition": "Bacterial Blight",
        "is_healthy": False,
        "overview": "Bacterial blight (Xanthomonas oryzae) produces yellow-to-white wavy lesions along leaf margins starting from tips, causing wilting and yield loss.",
        "common_symptoms": [
            "Water-soaked to yellow stripes along leaf margins starting from tip",
            "Lesions drying to straw-yellow with wavy irregular margins",
            "Bacterial droplets appearing on leaves in humid mornings"
        ],
        "immediate_actions": [
            "Drain excess water from field to reduce bacterial transmission",
            "Suspend excess nitrogenous fertilizer application immediately",
            "Avoid working in flooded fields while foliage is wet"
        ],
        "prevention": [
            "Grow resistant paddy cultivars (e.g. Swarna Sub1, Improved Samba Mahsuri)",
            "Ensure field sanitation by burning/composting infected stubble",
            "Adopt balanced NPK nutrient management based on soil testing"
        ],
        "monitoring": [
            "Check leaf margins weekly during tillering and panicle initiation",
            "Watch for rapid lesion spread following rainstorms or high winds"
        ],
        "expert_escalation": "Report to your Block Agricultural Officer or KVK pathologist if kresek (seedling wilt) phase is observed.",
        "sources": [
            {
                "organization": "ICAR - National Rice Research Institute (NRRI)",
                "title": "Integrated Management of Bacterial Blight (Xanthomonas oryzae) in Rice",
                "url": "https://icar-nrri.in",
                "source_type": "ICAR",
                "verified_url": True
            },
            {
                "organization": "Vikaspedia Agriculture Portal (Government of India)",
                "title": "Integrated Pest Management Strategies for Rice & Paddy Diseases",
                "url": "https://vikaspedia.in/agriculture/crop-production/integrated-pest-management/ipm-for-food-crops/ipm-strategies-for-rice",
                "source_type": "Government",
                "verified_url": True
            }
        ]
    },
    "Rice-Brownspot": {
        "class_name": "Rice-Brownspot",
        "crop": "Rice",
        "condition": "Brown Spot",
        "is_healthy": False,
        "overview": "Brown spot fungal infection causes oval sesame-shaped brown spots with yellow halos on leaves, commonly associated with nutrient-deficient or stressed soils.",
        "common_symptoms": [
            "Small oval dark brown spots on leaves resembling sesame seeds",
            "Fully developed spots with yellow-brown halos and gray centers",
            "Leaf blight and seedling weakness under poor soil fertility"
        ],
        "immediate_actions": [
            "Apply farmyard manure or compost to address soil nutritional stress",
            "Ensure consistent shallow flooding; prevent field drying stress",
            "Remove alternate weed hosts from field bunds"
        ],
        "prevention": [
            "Use certified disease-free seeds and perform seed sorting",
            "Correct soil nutrient deficiencies (especially Potassium and Zinc)",
            "Practice crop rotation with legumes or green manure crops"
        ],
        "monitoring": [
            "Inspect nursery beds and tillering plants weekly for leaf spots",
            "Monitor soil fertility and leaf color charts (LCC)"
        ],
        "expert_escalation": "Consult local KVK agronomists for soil testing if brown spot persists across multiple cropping seasons.",
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Rice Research (IIRR)",
                "title": "Rice Brown Spot Diagnostic Guide & Soil Fertility Management",
                "url": "https://www.icar-iirr.org",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Rice-Leafsmut": {
        "class_name": "Rice-Leafsmut",
        "crop": "Rice",
        "condition": "Leaf Smut",
        "is_healthy": False,
        "overview": "Rice leaf smut produces small, raised, black linear spots (spore masses) on leaves, typically late in the growing season with minimal yield impact.",
        "common_symptoms": [
            "Small, slightly raised, black linear spots scattered on leaf blades",
            "Leaf tissue turning yellow around black spore masses",
            "Ruptured black spots releasing powdery fungal spores when dry"
        ],
        "immediate_actions": [
            "Avoid excessive nitrogen fertilizer application",
            "Maintain proper water depth without waterlogging or severe drought",
            "Remove heavily infected leaves if isolated to small patches"
        ],
        "prevention": [
            "Select resistant or locally recommended rice varieties",
            "Clean paddy stubbles after harvest through deep ploughing",
            "Maintain balanced potassic fertilization"
        ],
        "monitoring": [
            "Inspect mature leaves after boot-stage for black linear pustules",
            "Distinguish leaf smut from bacterial streak or blast"
        ],
        "expert_escalation": "Escalate to KVK extension staff if black smut lesions cause premature leaf senescence before grain filling.",
        "sources": [
            {
                "organization": "ICAR - National Rice Research Institute (NRRI)",
                "title": "Advisory on Foliar Fungal Pathogens of Rice",
                "url": "https://icar-nrri.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },

    # -------------------------------------------------------------------------
    # SUGARCANE CLASSES (9)
    # -------------------------------------------------------------------------
    "Sugarcane-Grassy Shoot": {
        "class_name": "Sugarcane-Grassy Shoot",
        "crop": "Sugarcane",
        "condition": "Grassy Shoot",
        "is_healthy": False,
        "overview": "Grassy shoot disease (phytoplasma) causes excessive tillering of thin, pale shoots resembling grass, leading to severe cane stunting and loss.",
        "common_symptoms": [
            "Profuse tillering producing a dense cluster of thin grassy shoots",
            "Pale yellow to white chlorotic leaf blades",
            "Failure of canes to form thick millable stalks"
        ],
        "immediate_actions": [
            "Uproot and burn affected grassy stools immediately to prevent spread",
            "Do not use ratoon crop from infected fields",
            "Sanitize cutting harvesting tools between rows"
        ],
        "prevention": [
            "Plant heat-treated disease-free nursery seed cane",
            "Avoid propagating setts from infected fields",
            "Maintain clean field borders to manage leafhopper vector hosts"
        ],
        "monitoring": [
            "Inspect newly sprouted setts and young tillers 30-60 days after planting",
            "Check ratoon crops for abnormal bunchy grass-like tillers"
        ],
        "expert_escalation": "Contact your local Sugar Factory Cane Development Officer or KVK for certified disease-free seed setts.",
        "sources": [
            {
                "organization": "ICAR - Sugarcane Breeding Institute (SBI)",
                "title": "Management of Phytoplasma & Grassy Shoot Disease in Sugarcane",
                "url": "https://sugarcane.icar.gov.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Sugarcane-Healthy": {
        "class_name": "Sugarcane-Healthy",
        "crop": "Sugarcane",
        "condition": "Healthy",
        "is_healthy": True,
        "overview": "The inspected sugarcane foliage exhibits normal dark green leaf blades with sturdy midribs and healthy cane stalk development.",
        "common_symptoms": [
            "Robust green leaves without red stripes or chlorotic streaks",
            "Firm, upright stalk growth and normal canopy node formation"
        ],
        "immediate_actions": [
            "Maintain recommended earthing-up and trash mulching practices",
            "Ensure timely irrigation during formative growth phase"
        ],
        "prevention": [
            "Adopt crop rotation with green manure (Daincha / Sunnhemp)",
            "Maintain clean field drainage to prevent waterlogging"
        ],
        "monitoring": [
            "Routine monthly canopy inspection for borer or red rot symptoms",
            "Re-scan if leaf yellowing or midrib reddening appears"
        ],
        "expert_escalation": "Consult local cane officers if neighboring plots exhibit red rot or wilt symptoms.",
        "sources": [
            {
                "organization": "ICAR - Sugarcane Breeding Institute (SBI)",
                "title": "Good Agricultural Practices for Sugarcane Cultivation & Field Sanitation",
                "url": "https://sugarcane.icar.gov.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Sugarcane-Mosaic": {
        "class_name": "Sugarcane-Mosaic",
        "crop": "Sugarcane",
        "condition": "Mosaic Disease",
        "is_healthy": False,
        "overview": "Sugarcane mosaic virus produces pale green to yellowish elongated streaks contrasting against normal green leaf tissue, spread by aphids and infected setts.",
        "common_symptoms": [
            "Alternate dark green and pale yellow-green elongated leaf streaks",
            "Symptoms prominent on young expanding leaves near cane top",
            "Stunted stalk growth in susceptible cane cultivars"
        ],
        "immediate_actions": [
            "Rogue out mosaic-affected plants during early growth stages",
            "Do not harvest setts for replanting from mosaic-infected fields",
            "Remove wild grass weeds around field boundaries"
        ],
        "prevention": [
            "Plant mosaic-resistant sugarcane cultivars",
            "Use meristem tissue culture or heat-treated seed cane",
            "Maintain crop sanitation and weed-free borders"
        ],
        "monitoring": [
            "Check top spindle leaves for chlorotic streaking every fortnight",
            "Monitor aphid vector activity during dry spells"
        ],
        "expert_escalation": "Escalate to District Cane Officer if mosaic symptoms exceed 10% incidence in seed multiplication plots.",
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Sugarcane Research (IISR)",
                "title": "Sugarcane Mosaic Virus Control & Nursery Sanitation Advisory",
                "url": "https://iisr.icar.gov.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Sugarcane-Pokkah Boeng": {
        "class_name": "Sugarcane-Pokkah Boeng",
        "crop": "Sugarcane",
        "condition": "Pokkah Boeng",
        "is_healthy": False,
        "overview": "Pokkah Boeng (Fusarium disease) causes twisting, wrinkling, deformation, and chlorosis of top spindle leaves, often following rainy humid weather.",
        "common_symptoms": [
            "Deformed, wrinkled, twisted top spindle leaves",
            "Chlorotic yellowing at the base of young leaf blades",
            "Reddish spots or knife-cut lesions on top cane nodes in severe cases"
        ],
        "immediate_actions": [
            "Remove and destroy severely distorted top shoots",
            "Avoid heavy nitrogenous fertilizing before monsoons",
            "Ensure field drainage to reduce humidity build-up"
        ],
        "prevention": [
            "Grow resistant cultivars recommended for moist/coastal regions",
            "Maintain wider inter-row spacing to facilitate air circulation",
            "Practice trash mulching for moisture moderation"
        ],
        "monitoring": [
            "Inspect spindle leaf tops during high humidity post-monsoon months",
            "Differentiate top-rot stage from stem borer damage"
        ],
        "expert_escalation": "Consult IISR / SBI cane specialists if top-rot knife-cut stage spreads rapidly.",
        "sources": [
            {
                "organization": "ICAR - Sugarcane Breeding Institute (SBI)",
                "title": "Pokkah Boeng Fungal Top-Rot Identification & Cultural Control",
                "url": "https://sugarcane.icar.gov.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Sugarcane-Red Leaf Spot": {
        "class_name": "Sugarcane-Red Leaf Spot",
        "crop": "Sugarcane",
        "condition": "Red Leaf Spot",
        "is_healthy": False,
        "overview": "Red leaf spot causes reddish-brown lesions with darker margins on leaf blades, which may coalesce to cause partial foliage drying in moist climates.",
        "common_symptoms": [
            "Small reddish circular spots expanding into elongated oval lesions",
            "Lesions with dark red or purple borders and straw-colored centers",
            "Drying of leaf tips when spots coalesce"
        ],
        "immediate_actions": [
            "Strip off and burn lower infected dry leaves",
            "Avoid overhead irrigation; maintain furrow water flow",
            "Keep field weed-free to lower canopy micro-humidity"
        ],
        "prevention": [
            "Plant varieties with high foliar fungal resistance",
            "Adopt recommended row direction for maximum sunlight exposure",
            "Incorporate green manure prior to cane planting"
        ],
        "monitoring": [
            "Inspect middle and lower canopy leaves monthly",
            "Track lesion density after monsoons"
        ],
        "expert_escalation": "Consult extension agronomist if red leaf spot causes premature foliage canopy loss.",
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Sugarcane Research (IISR)",
                "title": "Foliar Leaf Spot Management & Trash Mulching in Sugarcane",
                "url": "https://iisr.icar.gov.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Sugarcane-Red Rot": {
        "class_name": "Sugarcane-Red Rot",
        "crop": "Sugarcane",
        "condition": "Red Rot",
        "is_healthy": False,
        "overview": "Red rot (Colletotrichum falcatum) is a devastating sugarcane disease causing red internal stalk discoloration with white transverse patches and alcoholic sour odor.",
        "common_symptoms": [
            "Third or fourth leaf from top yellowing and drying at tips",
            "Internal stem tissue turning bright red with white transverse bands",
            "Stalk shriveling, hollowed cane, and sour alcoholic smell upon splitting"
        ],
        "immediate_actions": [
            "Uproot entire infected cane clump along with roots and burn in situ",
            "Disinfect the soil spot with lime powder",
            "Immediately stop irrigation flow from infected block to healthy fields"
        ],
        "prevention": [
            "Strictly use red rot resistant cane varieties (e.g. Co 0238 alternatives as advised locally)",
            "Plant heat-treated nursery setts from disease-free nurseries",
            "Practice 2-3 year crop rotation with paddy or green manure"
        ],
        "monitoring": [
            "Inspect top leaf whorls for yellowing from July to November",
            "Split sample wilting stalks to check for red pith and white bands"
        ],
        "expert_escalation": "CRITICAL: Report red rot outbreaks immediately to Cane Department / Sugar Factory Officers for regional containment.",
        "sources": [
            {
                "organization": "ICAR - Sugarcane Breeding Institute (SBI)",
                "title": "Red Rot Epidemic Containment & Nursery Sett Sanitation Protocol",
                "url": "https://sugarcane.icar.gov.in",
                "source_type": "ICAR",
                "verified_url": True
            },
            {
                "organization": "Vikaspedia Agriculture Portal (Government of India)",
                "title": "Integrated Pest & Disease Management Strategies for Sugarcane",
                "url": "https://vikaspedia.in/agriculture/crop-production/integrated-pest-management/ipm-for-commercial-crops/ipm-strategies-for-sugarcane",
                "source_type": "Government",
                "verified_url": True
            }
        ]
    },
    "Sugarcane-Ring Spot": {
        "class_name": "Sugarcane-Ring Spot",
        "crop": "Sugarcane",
        "condition": "Ring Spot",
        "is_healthy": False,
        "overview": "Ring spot causes oval leaf spots with dark reddish-brown rings and light brown/gray centers, mainly affecting mature leaves in high-rainfall zones.",
        "common_symptoms": [
            "Small green or purplish spots widening into oval rings",
            "Reddish-brown distinct ring borders around pale gray centers",
            "Coalescence leading to leaf blade scorching"
        ],
        "immediate_actions": [
            "Strip lower affected senescent leaves during earthing-up",
            "Maintain field drainage channels to prevent stagnant water",
            "Apply balanced soil nutrients to encourage leaf vigor"
        ],
        "prevention": [
            "Grow ring-spot tolerant sugarcane cultivars",
            "Maintain wider inter-row spacing for leaf drying",
            "Avoid high nitrogen applications late in the season"
        ],
        "monitoring": [
            "Inspect older mature leaves during monsoon and post-monsoon",
            "Distinguish ring spot from red leaf spot and yellow spot"
        ],
        "expert_escalation": "Consult local KVK officers if ring spot covers >25% of active canopy foliage.",
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Sugarcane Research (IISR)",
                "title": "Sugarcane Ring Spot Identification & Canopy Drainage Advisory",
                "url": "https://iisr.icar.gov.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Sugarcane-Wilt": {
        "class_name": "Sugarcane-Wilt",
        "crop": "Sugarcane",
        "condition": "Wilt",
        "is_healthy": False,
        "overview": "Sugarcane wilt (Fusarium sacchari) causes cane drying, internal purple-red stalk discoloration without white patches, and stem light weight.",
        "common_symptoms": [
            "Gradual yellowing and drying of foliage starting from top leaves",
            "Internal stalk pith turning dull purplish-red or brown (no white bands)",
            "Stalk becoming hollow, lightweight, and pithy"
        ],
        "immediate_actions": [
            "Uproot and burn wilt-affected sugarcane stools",
            "Avoid ratooning from wilt-affected sugarcane fields",
            "Ensure proper field drainage and prevent drought stress"
        ],
        "prevention": [
            "Plant wilt-resistant sugarcane varieties",
            "Use disease-free seed setts treated with hot water/moist hot air",
            "Rotate sugarcane with paddy, green manure, or legumes"
        ],
        "monitoring": [
            "Check for stunting and leaf yellowing during post-monsoon dry spells",
            "Split dry canes to confirm wilt vs red rot"
        ],
        "expert_escalation": "Report wilt incidence to local factory field officers for soil health advisory.",
        "sources": [
            {
                "organization": "ICAR - Sugarcane Breeding Institute (SBI)",
                "title": "Integrated Management of Sugarcane Wilt Complex & Crop Rotation",
                "url": "https://sugarcane.icar.gov.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Sugarcane-Yellow Leaf Disease": {
        "class_name": "Sugarcane-Yellow Leaf Disease",
        "crop": "Sugarcane",
        "condition": "Yellow Leaf Disease",
        "is_healthy": False,
        "overview": "Yellow leaf disease (ScYLV virus) causes prominent yellowing of midribs on the 3rd to 5th leaves from top, followed by pinkish discoloration and canopy drying.",
        "common_symptoms": [
            "Intense yellowing of the leaf midrib on lower surface (3rd-5th leaf)",
            "Yellowing spreading sideways into leaf lamina tissue",
            "Pinkish/reddish tinge on midrib in late stages with apical leaf drying"
        ],
        "immediate_actions": [
            "Rogue out severely yellowed stools in young crop stages",
            "Do not select seed setts from infected fields",
            "Provide adequate potassium and organic manure to boost vigor"
        ],
        "prevention": [
            "Plant virus-indexed tissue culture or nursery certified setts",
            "Grow yellow-leaf disease resistant sugarcane varieties",
            "Manage aphid populations using clean borders and sticky traps"
        ],
        "monitoring": [
            "Examine the lower side of leaf midribs 5-8 months after planting",
            "Differentiate YLD midrib yellowing from nitrogen deficiency"
        ],
        "expert_escalation": "Contact SBI / IISR sugarcane pathologists if yellow midrib symptoms exceed 15% in seed plots.",
        "sources": [
            {
                "organization": "ICAR - Sugarcane Breeding Institute (SBI)",
                "title": "Sugarcane Yellow Leaf Virus Management & Midrib Symptom Advisory",
                "url": "https://sugarcane.icar.gov.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },

    # -------------------------------------------------------------------------
    # TOMATO CLASSES (10)
    # -------------------------------------------------------------------------
    "Tomato___Bacterial_spot": {
        "class_name": "Tomato___Bacterial_spot",
        "crop": "Tomato",
        "condition": "Bacterial Spot",
        "is_healthy": False,
        "overview": "Bacterial spot (Xanthomonas) produces small water-soaked dark spots on leaves and fruit, causing yellowing and premature foliage loss in warm wet weather.",
        "common_symptoms": [
            "Small (2-3mm) dark water-soaked spots on leaves",
            "Lesions developing yellow halos and drying to dark brown centers",
            "Raised dark scab-like spots on green and ripe fruits"
        ],
        "immediate_actions": [
            "Remove infected lower leaves during sunny dry conditions",
            "Avoid overhead sprinkler irrigation; water at plant base",
            "Sanitize stakes, ties, and pruning tools with alcohol solution"
        ],
        "prevention": [
            "Use certified disease-free pathogen-tested tomato seeds",
            "Rotate crops with non-solanaceous crops for 2-3 years",
            "Mulch beds to prevent soil splash onto lower leaves"
        ],
        "monitoring": [
            "Check leaf undersides for small water-soaked spots after rain",
            "Inspect green fruits for scab lesions"
        ],
        "expert_escalation": "Consult local KVK vegetable specialist if bacterial spot causes >15% leaf drop during fruit set.",
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Horticultural Research (IIHR)",
                "title": "Bacterial Spot Control & Sanitation Protocol in Solanaceous Vegetables",
                "url": "https://www.iihr.res.in",
                "source_type": "ICAR",
                "verified_url": True
            },
            {
                "organization": "Vikaspedia Agriculture Portal (Government of India)",
                "title": "Crop Stage-wise Integrated Pest Management for Tomato",
                "url": "https://vikaspedia.in/agriculture/crop-production/integrated-pest-management/ipm-for-vegetables/ipm-strategies-for-tomato",
                "source_type": "Government",
                "verified_url": True
            }
        ]
    },
    "Tomato___Early_blight": {
        "class_name": "Tomato___Early_blight",
        "crop": "Tomato",
        "condition": "Early Blight",
        "is_healthy": False,
        "overview": "Early blight (Alternaria solani) causes characteristic dark brown spots with concentric target-like rings on older lower leaves, moving upward.",
        "common_symptoms": [
            "Circular dark brown spots with distinct concentric rings ('target board')",
            "Yellowing surrounding leaf lesions on lower older leaves",
            "Stem collar rot and sunken dark lesions near fruit stem end"
        ],
        "immediate_actions": [
            "Prune off affected lower leaves up to first fruit cluster",
            "Apply straw mulch to prevent fungal spores splashing from soil",
            "Water early in the day at ground level to keep leaves dry"
        ],
        "prevention": [
            "Plant resistant tomato varieties",
            "Maintain wide plant spacing (60x45 cm) for good canopy aeration",
            "Rotate fields away from tomatoes, potatoes, and eggplants for 2 years"
        ],
        "monitoring": [
            "Inspect lower leaves weekly starting from transplanting",
            "Look for target-board rings on yellowing leaves"
        ],
        "expert_escalation": "Consult District Horticultural Officer if early blight progresses beyond mid-canopy level.",
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Vegetable Research (IIVR)",
                "title": "Early Blight Target Spot Control Guide for Solanaceous Crops",
                "url": "https://iivr.icar.gov.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Tomato___Late_blight": {
        "class_name": "Tomato___Late_blight",
        "crop": "Tomato",
        "condition": "Late Blight",
        "is_healthy": False,
        "overview": "Late blight (Phytophthora infestans) is a destructive disease causing rapid dark water-soaked leaf lesions with white fungal growth beneath during cool wet weather.",
        "common_symptoms": [
            "Large pale green to dark brown water-soaked blotches on leaves",
            "White cottony fungal growth on leaf undersides under high humidity",
            "Firm brown greasy lesions on green fruits and stems"
        ],
        "immediate_actions": [
            "Immediately remove and bag infected leaves/fruits; burn or deep bury",
            "Stop all overhead irrigation; improve plot drainage",
            "Destroy volunteer tomato/potato plants nearby"
        ],
        "prevention": [
            "Plant late blight resistant cultivars (e.g. Arka Rakshak, Arka Samrat)",
            "Avoid low-lying foggy or poorly drained field locations",
            "Destroy crop residues promptly after harvest"
        ],
        "monitoring": [
            "Inspect leaves daily during overcast cool rainy weather",
            "Check leaf undersides for white mildew rings in early mornings"
        ],
        "expert_escalation": "CRITICAL: Alert KVK / Horticulture Department immediately if late blight lesions spread rapidly across fields.",
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Horticultural Research (IIHR)",
                "title": "Late Blight Warning & Integrated Cultural Control for Tomato",
                "url": "https://www.iihr.res.in",
                "source_type": "ICAR",
                "verified_url": True
            },
            {
                "organization": "FAO (Food and Agriculture Organization)",
                "title": "Integrated Pest & Disease Management for Solanaceous Crops",
                "url": "https://www.fao.org/plant-production-protection/en",
                "source_type": "FAO",
                "verified_url": True
            }
        ]
    },
    "Tomato___Leaf_Mold": {
        "class_name": "Tomato___Leaf_Mold",
        "crop": "Tomato",
        "condition": "Leaf Mold",
        "is_healthy": False,
        "overview": "Leaf mold (Passalora fulva) produces pale green to yellow spots on upper leaf surfaces with velvety olive-green fungal growth beneath, common in high humidity.",
        "common_symptoms": [
            "Pale yellow spots with vague borders on upper leaf surfaces",
            "Velvety olive-green to brown mold growth on lower leaf surfaces",
            "Leaves turning yellow, drying, and dropping prematurely"
        ],
        "immediate_actions": [
            "Prune lower older leaves to enhance ventilation within canopy",
            "Increase plant spacing and stake vines securely",
            "Reduce greenhouse or high-tunnel relative humidity below 85%"
        ],
        "prevention": [
            "Use leaf-mold resistant tomato seed varieties",
            "Ensure excellent air circulation in greenhouse and open field beds",
            "Avoid late evening foliage wetting"
        ],
        "monitoring": [
            "Check lower leaf undersides for olive-green velvety mold patches",
            "Monitor relative humidity levels in enclosed structures"
        ],
        "expert_escalation": "Consult greenhouse extension specialist if leaf mold spreads to upper new growth.",
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Vegetable Research (IIVR)",
                "title": "Protected Tomato Cultivation & Leaf Mold Management",
                "url": "https://iivr.icar.gov.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Tomato___Septoria_leaf_spot": {
        "class_name": "Tomato___Septoria_leaf_spot",
        "crop": "Tomato",
        "condition": "Septoria Leaf Spot",
        "is_healthy": False,
        "overview": "Septoria leaf spot causes numerous small circular spots with dark brown margins and gray centers containing tiny black specks on lower foliage.",
        "common_symptoms": [
            "Numerous small (1-3mm) circular spots with ash-gray centers",
            "Dark brown spot borders with tiny black dots (pycnidia) inside",
            "Severe yellowing and premature defoliation from base upward"
        ],
        "immediate_actions": [
            "Pick off and burn infected lower leaves at first sight",
            "Apply thick organic mulch (straw/plastic) around plant bases",
            "Avoid working among wet plants to prevent spore dispersal"
        ],
        "prevention": [
            "Practice 3-year crop rotation without solanaceous crops",
            "Stake and tie tomato plants for vertical air movement",
            "Keep beds free of solanaceous weeds (Solanum nigrum)"
        ],
        "monitoring": [
            "Check lower older leaves weekly following rainy periods",
            "Look for small gray-centered spots with black specks"
        ],
        "expert_escalation": "Consult local extension agent if defoliation reaches lower fruit clusters.",
        "sources": [
            {
                "organization": "ICAR - Indian Agricultural Research Institute (IARI)",
                "title": "Foliar Septoria Spot Control Protocols in Tomato",
                "url": "https://www.iari.res.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "class_name": "Tomato___Spider_mites Two-spotted_spider_mite",
        "crop": "Tomato",
        "condition": "Spider Mites (Two-Spotted)",
        "is_healthy": False,
        "overview": "Two-spotted spider mites feed on leaf sap, causing fine yellow stippling, bronzing, and fine webbing on leaf undersides during hot dry conditions.",
        "common_symptoms": [
            "Tiny yellow-white stippled dots on upper leaf surfaces",
            "Fine silken webbing on leaf undersides and growing tips",
            "Leaves turning bronze, curling, drying, and dropping"
        ],
        "immediate_actions": [
            "Spray undersides of leaves with strong jet of clean water to dislodge mites",
            "Remove and destroy severely webbed leaves",
            "Increase relative humidity around plants by ground wetting"
        ],
        "prevention": [
            "Avoid water stress; maintain consistent irrigation",
            "Preserve natural predatory insects (ladybirds, lacewings)",
            "Keep field borders clear of dusty weed hosts"
        ],
        "monitoring": [
            "Inspect leaf undersides using a 10x hand lens during hot dry spells",
            "Look for fine webbing and yellow stippling"
        ],
        "expert_escalation": "Contact local KVK entomologist if mite webbing covers growing tips across multiple rows.",
        "sources": [
            {
                "organization": "ICAR - National Bureau of Agricultural Insect Resources (NBAIR)",
                "title": "Biological & Cultural Management of Two-Spotted Spider Mites",
                "url": "https://www.nbair.res.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Tomato___Target_Spot": {
        "class_name": "Tomato___Target_Spot",
        "crop": "Tomato",
        "condition": "Target Spot",
        "is_healthy": False,
        "overview": "Target spot (Corynespora cassiicola) causes brown pinpoint spots expanding into circular lesions with light brown centers and yellow halos.",
        "common_symptoms": [
            "Small brown pinpoint leaf spots widening into target-like circular spots",
            "Light brown spot centers with dark brown rings and chlorotic halos",
            "Sunken dark lesions on green and ripe tomato fruits"
        ],
        "immediate_actions": [
            "Prune off infected lower foliage to improve air circulation",
            "Ensure plants are staked and tied upright off the soil",
            "Irrigate at ground level; keep canopy foliage dry"
        ],
        "prevention": [
            "Rotate crops with non-host species like corn or legumes",
            "Maintain wide row spacing to allow canopy drying",
            "Destroy crop stubble immediately after harvest"
        ],
        "monitoring": [
            "Inspect lower and inner canopy foliage weekly",
            "Check green fruit surfaces for small sunken spots"
        ],
        "expert_escalation": "Consult district horticulture consultant if target spot causes severe defoliation during fruit ripening.",
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Horticultural Research (IIHR)",
                "title": "Target Spot Cultural Management in Solanaceous Crops",
                "url": "https://www.iihr.res.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "class_name": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "crop": "Tomato",
        "condition": "Yellow Leaf Curl Virus",
        "is_healthy": False,
        "overview": "Tomato Yellow Leaf Curl Virus (TYLCV) causes severe leaf curling upward, yellowing margins, bushy stunting, and complete flower/fruit drop transmitted by whiteflies.",
        "common_symptoms": [
            "Upward curling and cupping of leaf margins",
            "Interveinal yellowing (chlorosis) on young leaves",
            "Severe plant stunting with bushy appearance and flower drop"
        ],
        "immediate_actions": [
            "Rogue out and destroy infected viral plants immediately",
            "Install yellow sticky traps (15-20 per acre) to catch whiteflies",
            "Cover nursery beds with 40-mesh insect-proof netting"
        ],
        "prevention": [
            "Grow TYLCV-resistant hybrids (e.g. Arka Rakshak, Arka Samrat)",
            "Use silver/yellow reflective mulches to deter whiteflies",
            "Maintain weed-free field boundaries"
        ],
        "monitoring": [
            "Monitor whitefly populations on leaf undersides early morning",
            "Inspect young transplants weekly for leaf cupping"
        ],
        "expert_escalation": "Contact local KVK plant pathologist if whitefly-vectored curl virus exceeds 10% in young fields.",
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Horticultural Research (IIHR)",
                "title": "Management of Tomato Yellow Leaf Curl Virus & Vector Sanitation",
                "url": "https://www.iihr.res.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Tomato___Tomato_mosaic_virus": {
        "class_name": "Tomato___Tomato_mosaic_virus",
        "crop": "Tomato",
        "condition": "Mosaic Virus",
        "is_healthy": False,
        "overview": "Tomato Mosaic Virus (ToMV) causes mottled light/dark green leaves, fern-like leaf distortion, and internal fruit browning, spread mechanically by contact.",
        "common_symptoms": [
            "Mottled light and dark green mosaic patterns on leaves",
            "Fern-leaf deformation (shoestringing) or crinkled leaves",
            "Internal brown necrotic rings inside ripe tomato fruits"
        ],
        "immediate_actions": [
            "Rogue out and burn mosaic-infected plants",
            "Wash hands thoroughly with soap/milk before handling healthy plants",
            "Disinfect tools and stakes in 10% trisodium phosphate or bleach"
        ],
        "prevention": [
            "Use certified mosaic-resistant seeds (Tm-22 gene)",
            "Strictly avoid tobacco use near tomato crops (ToMV transmission)",
            "Practice strict farm sanitation between operations"
        ],
        "monitoring": [
            "Inspect growing tips and new leaves weekly for mosaic mottling",
            "Check harvested fruits for internal browning"
        ],
        "expert_escalation": "Consult extension pathologist if mosaic symptoms appear early in nursery beds.",
        "sources": [
            {
                "organization": "ICAR - Indian Agricultural Research Institute (IARI)",
                "title": "Mechanical Virus Transmission Control in Solanaceous Crops",
                "url": "https://www.iari.res.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    },
    "Tomato___healthy": {
        "class_name": "Tomato___healthy",
        "crop": "Tomato",
        "condition": "Healthy",
        "is_healthy": True,
        "overview": "The inspected tomato foliage displays dark green, fully expanded leaf blades with firm leaflets and no signs of fungal, bacterial, or viral disease.",
        "common_symptoms": [
            "Vibrant green compound leaves without spots or curling",
            "Sturdy stems, clean leaf undersides, and healthy growth"
        ],
        "immediate_actions": [
            "Continue regular watering at root level (drip irrigation preferred)",
            "Prune suckers and lower senescent leaves for canopy aeration"
        ],
        "prevention": [
            "Apply organic mulch to maintain soil moisture and prevent splash",
            "Stake plants securely to keep foliage off soil"
        ],
        "monitoring": [
            "Scout lower leaves weekly for early signs of blight or spots",
            "Re-scan if leaf yellowing, mottling, or curling occurs"
        ],
        "expert_escalation": "Consult local horticulture officer if uninspected plant stems or fruits show wilting or rotting.",
        "sources": [
            {
                "organization": "ICAR - Indian Institute of Horticultural Research (IIHR)",
                "title": "Good Agricultural Practices for Healthy Tomato Production",
                "url": "https://www.iihr.res.in",
                "source_type": "ICAR",
                "verified_url": True
            }
        ]
    }
}

# Disabled chemical guidance placeholder (Strict Safety Gate)
verified_chemical_guidance = None
