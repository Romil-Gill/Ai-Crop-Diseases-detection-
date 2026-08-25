"""
FasalRakshak AI - Symptom Verification & Field Concern Knowledge Base
Observable, disease-specific symptom verification questions and deterministic field concern scoring.
Strictly separates CNN model confidence from user-reported symptom agreement.
"""

SYMPTOM_QUESTIONS = {
    # -------------------------------------------------------------------------
    # PUMPKIN DISEASE CLASSES (4)
    # -------------------------------------------------------------------------
    "Pumpkin-Bacterial Leaf Spot": [
        {
            "id": "water_soaked_spots",
            "question": "Are there small, angular, water-soaked spots on the leaf blade?",
            "weight": 1.0
        },
        {
            "id": "yellow_halos",
            "question": "Do the leaf spots have yellowish margins or chlorotic halos around them?",
            "weight": 1.0
        },
        {
            "id": "leaf_browning",
            "question": "Are older leaves turning dark brown/black and drying up prematurely?",
            "weight": 1.0
        }
    ],
    "Pumpkin-Downy Mildew": [
        {
            "id": "angular_yellow_patches",
            "question": "Are there angular yellow patches on the upper leaf surface bounded by veins?",
            "weight": 1.0
        },
        {
            "id": "gray_downy_underside",
            "question": "Is there purplish-gray downy or velvety fungal growth beneath the yellow leaf spots?",
            "weight": 1.0
        },
        {
            "id": "leaf_curling",
            "question": "Are affected leaf edges curling upwards and browning?",
            "weight": 1.0
        }
    ],
    "Pumpkin-Mosaic Disease": [
        {
            "id": "mottled_pattern",
            "question": "Does the leaf exhibit a patchy light and dark green mottled mosaic pattern?",
            "weight": 1.0
        },
        {
            "id": "puckered_leaves",
            "question": "Are young leaves puckered, blistered, or distorted in shape?",
            "weight": 1.0
        },
        {
            "id": "stunted_vines",
            "question": "Is the vine growth noticeably stunted or bunchy near the tips?",
            "weight": 1.0
        }
    ],
    "Pumpkin-Powdery_Mildew": [
        {
            "id": "white_powdery_patches",
            "question": "Are white, talcum-like powdery spots visible on the upper or lower leaf surface?",
            "weight": 1.0
        },
        {
            "id": "expanding_white_layer",
            "question": "Is the white powdery growth spreading to cover whole leaf blades?",
            "weight": 1.0
        },
        {
            "id": "brittle_leaves",
            "question": "Do affected leaves feel dry, yellowed, or brittle when touched?",
            "weight": 1.0
        }
    ],

    # -------------------------------------------------------------------------
    # RICE DISEASE CLASSES (3)
    # -------------------------------------------------------------------------
    "Rice-Bacterialblight": [
        {
            "id": "wavy_margin_lesions",
            "question": "Are straw-yellow wavy lesions running along the leaf margins starting from the tip?",
            "weight": 1.0
        },
        {
            "id": "bacterial_droplets",
            "question": "Are tiny yellowish droplets visible on infected leaf margins in humid mornings?",
            "weight": 1.0
        },
        {
            "id": "leaf_drying",
            "question": "Are whole leaf blades turning grayish-white and drying prematurely?",
            "weight": 1.0
        }
    ],
    "Rice-Brownspot": [
        {
            "id": "sesame_spots",
            "question": "Are oval or circular dark brown spots resembling sesame seeds visible on the leaf?",
            "weight": 1.0
        },
        {
            "id": "yellow_halo_around_spot",
            "question": "Do mature brown spots have gray centers with distinct yellow halos?",
            "weight": 1.0
        },
        {
            "id": "multiple_leaves_affected",
            "question": "Are lower leaves showing numerous brown spots across the nursery/field?",
            "weight": 1.0
        }
    ],
    "Rice-Leafsmut": [
        {
            "id": "black_linear_pustules",
            "question": "Are small, slightly raised, linear black spots visible scattered on the leaf?",
            "weight": 1.0
        },
        {
            "id": "yellow_border_black_spot",
            "question": "Does leaf tissue turn yellow immediately surrounding the small black spots?",
            "weight": 1.0
        },
        {
            "id": "powdery_black_rupture",
            "question": "Do the black spots rupture to release fine black powdery spore mass when dry?",
            "weight": 1.0
        }
    ],

    # -------------------------------------------------------------------------
    # SUGARCANE DISEASE CLASSES (8)
    # -------------------------------------------------------------------------
    "Sugarcane-Grassy Shoot": [
        {
            "id": "grassy_tillers",
            "question": "Is there a dense bunch of thin, grass-like shoots emerging from the clump base?",
            "weight": 1.0
        },
        {
            "id": "pale_chlorotic_leaves",
            "question": "Are the leaf blades of the young shoots pale yellow or complete white?",
            "weight": 1.0
        },
        {
            "id": "stunted_stalks",
            "question": "Has the stool failed to form thick, normal cane stalks?",
            "weight": 1.0
        }
    ],
    "Sugarcane-Mosaic": [
        {
            "id": "chlorotic_leaf_streaks",
            "question": "Are elongated pale green to yellowish streaks visible on dark green leaves?",
            "weight": 1.0
        },
        {
            "id": "young_leaves_mottled",
            "question": "Is the mottled pattern most clear on young expanding leaves near the top whorl?",
            "weight": 1.0
        }
    ],
    "Sugarcane-Pokkah Boeng": [
        {
            "id": "twisted_top_leaves",
            "question": "Are top spindle leaves wrinkled, twisted, or distorted at the base?",
            "weight": 1.0
        },
        {
            "id": "chlorosis_spindle_base",
            "question": "Is yellowing or whitish chlorosis visible near the base of young top leaves?",
            "weight": 1.0
        },
        {
            "id": "red_knife_cut_lesions",
            "question": "Are reddish spots or knife-cut lesions visible on top cane stalk nodes?",
            "weight": 1.0
        }
    ],
    "Sugarcane-Red Leaf Spot": [
        {
            "id": "red_oval_lesions",
            "question": "Are small reddish spots expanding into oval lesions with purple borders on leaves?",
            "weight": 1.0
        },
        {
            "id": "straw_colored_centers",
            "question": "Do older leaf spots have dark red margins and straw-colored dry centers?",
            "weight": 1.0
        }
    ],
    "Sugarcane-Red Rot": [
        {
            "id": "top_leaf_yellowing",
            "question": "Are upper leaves (3rd or 4th from top) yellowing and drying at the tips?",
            "weight": 1.0
        },
        {
            "id": "red_pith_white_bands",
            "question": "Does splitting the stalk reveal internal bright red tissue with white transverse bands?",
            "weight": 1.0
        },
        {
            "id": "sour_alcoholic_smell",
            "question": "Does the split cane stalk emit a sour, alcoholic fermentation odor?",
            "weight": 1.0
        }
    ],
    "Sugarcane-Ring Spot": [
        {
            "id": "ring_shaped_spots",
            "question": "Are distinct oval spots with dark reddish-brown ring margins visible on mature leaves?",
            "weight": 1.0
        },
        {
            "id": "pale_gray_spot_center",
            "question": "Are the centers of the ring spots pale gray or light brown?",
            "weight": 1.0
        }
    ],
    "Sugarcane-Wilt": [
        {
            "id": "gradual_top_drying",
            "question": "Are top leaves gradually yellowing and drying up across the cane clump?",
            "weight": 1.0
        },
        {
            "id": "dull_purple_pith",
            "question": "Does internal stalk tissue turn dull purplish-red or dark brown (without white bands)?",
            "weight": 1.0
        },
        {
            "id": "hollow_light_stalk",
            "question": "Is the stalk hollowed out, lightweight, and dry inside?",
            "weight": 1.0
        }
    ],
    "Sugarcane-Yellow Leaf Disease": [
        {
            "id": "yellow_midrib_underside",
            "question": "Is intense yellowing visible along the lower surface of leaf midribs (3rd-5th leaf)?",
            "weight": 1.0
        },
        {
            "id": "midrib_pinkish_tinge",
            "question": "Does the yellow midrib turn pinkish or reddish in advanced stages?",
            "weight": 1.0
        }
    ],

    # -------------------------------------------------------------------------
    # TOMATO DISEASE CLASSES (9)
    # -------------------------------------------------------------------------
    "Tomato___Bacterial_spot": [
        {
            "id": "dark_water_soaked_spots",
            "question": "Are small (2-3mm) dark water-soaked spots present on leaves or green fruit?",
            "weight": 1.0
        },
        {
            "id": "yellow_spot_surrounds",
            "question": "Do leaf spots have thin yellow chlorotic rings surrounding them?",
            "weight": 1.0
        },
        {
            "id": "scab_on_fruits",
            "question": "Are raised black scab-like spots visible on green or ripe tomatoes?",
            "weight": 1.0
        }
    ],
    "Tomato___Early_blight": [
        {
            "id": "target_board_rings",
            "question": "Are dark brown circular spots with distinct concentric target-like rings visible on lower leaves?",
            "weight": 1.0
        },
        {
            "id": "lower_leaf_yellowing",
            "question": "Are older lower leaves yellowing and dying while upper canopy remains green?",
            "weight": 1.0
        },
        {
            "id": "stem_end_fruit_rot",
            "question": "Are dark sunken lesions present near the fruit stem attachment area?",
            "weight": 1.0
        }
    ],
    "Tomato___Late_blight": [
        {
            "id": "large_water_soaked_blotches",
            "question": "Are large dark brown or water-soaked greasy blotches spreading quickly on leaves?",
            "weight": 1.0
        },
        {
            "id": "white_cottony_underside",
            "question": "Is white cottony fungal down visible on leaf undersides during moist mornings?",
            "weight": 1.0
        },
        {
            "id": "firm_brown_fruit_rot",
            "question": "Are firm, brown, greasy-looking patches covering green tomato fruits?",
            "weight": 1.0
        }
    ],
    "Tomato___Leaf_Mold": [
        {
            "id": "upper_yellow_spots",
            "question": "Are pale yellow spots with vague borders visible on upper leaf surfaces?",
            "weight": 1.0
        },
        {
            "id": "olive_green_mold_underneath",
            "question": "Is velvety olive-green to brown mold growth present on lower leaf undersides?",
            "weight": 1.0
        }
    ],
    "Tomato___Septoria_leaf_spot": [
        {
            "id": "ash_gray_center_spots",
            "question": "Are numerous small circular spots with ash-gray centers and dark borders on lower leaves?",
            "weight": 1.0
        },
        {
            "id": "black_dots_in_spot",
            "question": "Are tiny black pinhead specks visible inside the gray spot centers?",
            "weight": 1.0
        },
        {
            "id": "defoliation_upwards",
            "question": "Are lower leaves yellowing and dropping rapidly from plant base upwards?",
            "weight": 1.0
        }
    ],
    "Tomato___Spider_mites Two-spotted_spider_mite": [
        {
            "id": "yellow_stippled_dots",
            "question": "Are fine yellow or white stippled dots covering upper leaf surfaces?",
            "weight": 1.0
        },
        {
            "id": "silken_webbing",
            "question": "Is fine silken webbing visible on leaf undersides or growing shoot tips?",
            "weight": 1.0
        },
        {
            "id": "leaf_bronzing",
            "question": "Are leaves turning bronze, curling, and drying under hot sunny conditions?",
            "weight": 1.0
        }
    ],
    "Tomato___Target_Spot": [
        {
            "id": "pinpoint_target_spots",
            "question": "Are brown pinpoint spots expanding into target-like circular leaf spots with yellow halos?",
            "weight": 1.0
        },
        {
            "id": "sunken_fruit_lesions",
            "question": "Are sunken circular brown lesions visible on green or ripe fruits?",
            "weight": 1.0
        }
    ],
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": [
        {
            "id": "upward_leaf_curling",
            "question": "Are young leaves curling and cupping upwards with yellowed leaf margins?",
            "weight": 1.0
        },
        {
            "id": "bushy_stunted_plant",
            "question": "Is the top plant growth severely stunted, bushy, or failing to set fruit?",
            "weight": 1.0
        },
        {
            "id": "whitefly_presence",
            "question": "Are tiny whiteflies visible flying off leaf undersides when disturbed?",
            "weight": 1.0
        }
    ],
    "Tomato___Tomato_mosaic_virus": [
        {
            "id": "mosaic_mottled_leaves",
            "question": "Are leaves showing alternating light and dark green mosaic patterns?",
            "weight": 1.0
        },
        {
            "id": "fern_leaf_distortion",
            "question": "Are leaves crinkled, distorted, or narrowed into fern-like shoestrings?",
            "weight": 1.0
        },
        {
            "id": "internal_fruit_browning",
            "question": "Do harvested tomato fruits show internal brown necrotic rings when cut?",
            "weight": 1.0
        }
    ],
    # -------------------------------------------------------------------------
    # WHEAT DISEASE CLASSES (4)
    # -------------------------------------------------------------------------
    "Wheat___Leaf_Rust": [
        {
            "id": "orange_brown_pustules",
            "question": "Are there small, round, orange-brown pustules scattered across upper leaf surfaces?",
            "weight": 1.0
        },
        {
            "id": "powdery_spores",
            "question": "Do the spots release a brownish powder when rubbed gently with a finger or cloth?",
            "weight": 1.0
        },
        {
            "id": "leaf_browning",
            "question": "Are affected leaf tips turning brown and drying prematurely?",
            "weight": 1.0
        }
    ],
    "Wheat___Stripe_Rust": [
        {
            "id": "yellow_parallel_stripes",
            "question": "Are there bright yellow pustules aligned in long, parallel stripes along leaf veins?",
            "weight": 1.0
        },
        {
            "id": "yellow_spore_dust",
            "question": "Do yellow powdery spores rub off easily onto fingers or clothing?",
            "weight": 1.0
        },
        {
            "id": "cool_weather_foci",
            "question": "Did symptoms appear rapidly during recent cool, foggy morning conditions?",
            "weight": 1.0
        }
    ],
    "Wheat___Powdery_Mildew": [
        {
            "id": "white_cottony_patches",
            "question": "Are there white or greyish cottony fungal patches on leaves or sheath bases?",
            "weight": 1.0
        },
        {
            "id": "black_dots_in_patches",
            "question": "Do mature patches turn greyish-brown with tiny black dots inside?",
            "weight": 1.0
        },
        {
            "id": "lower_leaf_yellowing",
            "question": "Are lower leaves near the soil turning yellow and dying?",
            "weight": 1.0
        }
    ],
    "Wheat___Septoria": [
        {
            "id": "oval_brown_blotches",
            "question": "Are there irregular greyish-brown oval lesions on leaf blades?",
            "weight": 1.0
        },
        {
            "id": "black_pycnidia_specks",
            "question": "Are tiny black specks (pycnidia) clearly visible inside the brown spots?",
            "weight": 1.0
        },
        {
            "id": "tip_drying",
            "question": "Are affected leaf tips drying out and curling?",
            "weight": 1.0
        }
    ],

    # -------------------------------------------------------------------------
    # MAIZE DISEASE CLASSES (3)
    # -------------------------------------------------------------------------
    "Maize___Common_Rust": [
        {
            "id": "reddish_brown_pustules",
            "question": "Are there small oval brownish-red pustules on both upper and lower leaf surfaces?",
            "weight": 1.0
        },
        {
            "id": "powdery_rust_spores",
            "question": "Do pustules rupture and leave reddish-brown spore dust on fingers?",
            "weight": 1.0
        },
        {
            "id": "leaf_yellowing",
            "question": "Is yellowing spreading around dense clusters of rust spots?",
            "weight": 1.0
        }
    ],
    "Maize___Northern_Leaf_Blight": [
        {
            "id": "cigar_shaped_lesions",
            "question": "Are there long, elliptical, cigar-shaped tan or greyish lesions (2 to 15 cm long) on the leaves?",
            "weight": 1.0
        },
        {
            "id": "dark_fungal_fuzz",
            "question": "Is dark fungal growth visible inside the centers of lesions during damp weather?",
            "weight": 1.0
        },
        {
            "id": "extensive_blighting",
            "question": "Are multiple spots coalescing to cause large areas of the leaf to dry out?",
            "weight": 1.0
        }
    ],
    "Maize___Gray_Leaf_Spot": [
        {
            "id": "rectangular_vein_lesions",
            "question": "Are there narrow rectangular tan-to-grey spots strictly bounded by parallel leaf veins?",
            "weight": 1.0
        },
        {
            "id": "greyish_cast",
            "question": "Do spots take on a distinct greyish cast under humid morning dew?",
            "weight": 1.0
        },
        {
            "id": "lower_leaf_spread",
            "question": "Did symptoms start on lower leaves and move upward toward the ear?",
            "weight": 1.0
        }
    ]
}

FIELD_SPREAD_OPTIONS = {
    "only_this_leaf": {
        "id": "only_this_leaf",
        "label": "Only this leaf / very few leaves",
        "description": "Symptoms isolated to 1-2 leaves on a single plant.",
        "weight": 1
    },
    "several_leaves": {
        "id": "several_leaves",
        "label": "Several leaves on one plant",
        "description": "Symptoms present across multiple leaves on the same plant.",
        "weight": 2
    },
    "several_plants": {
        "id": "several_plants",
        "label": "Several plants nearby",
        "description": "Symptoms observed on neighboring plants in the bed/row.",
        "weight": 3
    },
    "widespread": {
        "id": "widespread",
        "label": "Many plants / spreading quickly",
        "description": "Widespread symptoms across multiple rows or field blocks.",
        "weight": 4
    },
    "unsure": {
        "id": "unsure",
        "label": "Not sure / Not observed",
        "description": "Uncertain about wider field spread.",
        "weight": 0
    }
}


def evaluate_symptom_verification(class_name: str, answers: dict, field_spread: str):
    """
    Evaluates user symptom answers and field spread deterministically.
    CNN model confidence is NEVER passed or used in this calculation.
    """
    questions = SYMPTOM_QUESTIONS.get(class_name, [])
    
    total_answered = 0
    yes_weights = 0.0
    total_weights = 0.0

    for q in questions:
        q_id = q["id"]
        weight = q.get("weight", 1.0)
        ans = str(answers.get(q_id, "")).lower()

        if ans in ("yes", "no", "unsure"):
            total_answered += 1
            total_weights += weight
            if ans == "yes":
                yes_weights += weight

    if total_weights > 0:
        match_score = round(yes_weights / total_weights, 2)
    else:
        match_score = 0.0

    if match_score >= 0.70:
        agreement = "high"
        agreement_label = "Strong symptom agreement"
    elif match_score >= 0.40:
        agreement = "moderate"
        agreement_label = "Moderate symptom agreement"
    else:
        agreement = "low"
        agreement_label = "Low symptom agreement"

    # Field Concern Assessment Logic
    spread = str(field_spread).lower()
    
    if spread == "widespread" or spread == "several_plants":
        concern_level = "HIGH"
        concern_reason = f"Symptoms reported as appearing on {FIELD_SPREAD_OPTIONS.get(spread, {}).get('label', spread).lower()}."
    elif spread == "several_leaves":
        if agreement == "high":
            concern_level = "HIGH"
            concern_reason = "Strong symptom agreement observed across several leaves on the plant."
        else:
            concern_level = "MODERATE"
            concern_reason = "Symptoms reported on several leaves with moderate symptom alignment."
    elif spread == "only_this_leaf":
        if agreement == "high":
            concern_level = "MODERATE"
            concern_reason = "Strong symptom agreement, but isolated to very few leaves."
        else:
            concern_level = "LOW"
            concern_reason = "Symptoms isolated to single leaf with low-to-moderate alignment."
    else:  # unsure or unknown
        if agreement == "high":
            concern_level = "MODERATE"
            concern_reason = "High symptom agreement, but field spread is unconfirmed."
        else:
            concern_level = "LOW"
            concern_reason = "Field spread unconfirmed and symptom agreement is limited."

    return {
        "symptom_verification": {
            "answered": total_answered,
            "agreement": agreement,
            "agreement_label": agreement_label,
            "match_score": match_score
        },
        "field_assessment": {
            "concern_level": concern_level,
            "reason": concern_reason,
            "field_spread": spread
        },
        "disclaimer": "Field concern is based on user-reported symptoms and field spread and is not a laboratory severity measurement."
    }
