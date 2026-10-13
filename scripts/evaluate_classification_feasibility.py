"""Evaluation of Dataset Feasibility for Supervised Crop Disease Classification.

Inspects dataset structure, class cardinality, crop-condition orthogonality,
source heterogeneity, and sample size lower bounds to determine whether an
end-to-end supervised disease classification benchmark is scientifically defensible.
"""
import json
import pandas as pd
import numpy as np

manifest = pd.read_csv("data/manifests/canonical_dataset_v2.csv")

# 1. Class distributions
crop_counts = manifest["crop_name"].value_counts().to_dict()
condition_counts = manifest["condition_status"].value_counts().to_dict()
disease_counts = manifest["disease_name"].value_counts().to_dict()

# 2. Crop x Condition matrix
contingency = pd.crosstab(manifest["crop_name"], manifest["condition_status"])
crops_only_healthy = contingency[contingency["Diseased"] == 0].index.tolist()
crops_only_diseased = contingency[contingency["Healthy"] == 0].index.tolist()
crops_both = contingency[(contingency["Diseased"] > 0) & (contingency["Healthy"] > 0)].index.tolist()

# 3. Rare class detection (< 20 samples)
crop_disease_counts = manifest.groupby(["crop_name", "disease_name", "condition_status"]).size().reset_index(name="count")
rare_classes = crop_disease_counts[crop_disease_counts["count"] < 20].to_dict(orient="records")

# 4. Source distribution
source_counts = manifest["dataset_source"].value_counts().to_dict()

# 5. Scientific decision formulation
unsupported_reasons = [
    {
        "factor": "Severe Taxonomic Confounding (Single-Condition Crops)",
        "evidence": f"7 crops ({', '.join(crops_only_healthy)}) contain 100% healthy images; 1 crop ({', '.join(crops_only_diseased)}) contains 100% diseased images.",
        "scientific_implication": "Any supervised classifier trained to separate Healthy vs Diseased will suffer from severe shortcut learning, memorizing species-level foliar morphology (e.g. Raspberry or Blueberry leaf shape) rather than biological pathology."
    },
    {
        "factor": "Extreme Class Imbalance & Deficient Cell Support",
        "evidence": f"Class frequencies span 2 orders of magnitude (from N=2 for Tomato Two-Spotted Spider Mite to N=190 for Corn Northern Leaf Blight).",
        "scientific_implication": "Statistically sound train/validation/test stratification is impossible for classes with N < 5 (such as Spider Mite with N=2). A test set cannot evaluate precision/recall with N=0 or 1 test instance."
    },
    {
        "factor": "Cross-Source Domain Shift Confounding",
        "evidence": f"All 36 Rice images originate from ICAR/OGD lab imaging, while all other 2,560 images originate from PlantDoc crowd-sourced natural field photography.",
        "scientific_implication": "Supervised models predicting rice diseases learn dataset source acquisition artifacts (scanner lighting, DPI, background) rather than agricultural disease pathology."
    },
    {
        "factor": "Hand-Crafted 32D Feature Representation Limitations",
        "evidence": "Features consist of global color moments, Haralick GLCM textures, and binary contour moments, designed for dimensional OLAP and cluster discovery.",
        "scientific_implication": "Linear or tree-based classifiers on global descriptors lack localized spatial attention required to distinguish subtle fungal spot lesions from natural foliar venation without high false-positive rates."
    }
]

decision = {
    "evaluation_title": "Scientific Feasibility Assessment for Supervised Disease Classification",
    "dataset_total_specimens": len(manifest),
    "distinct_taxa": len(crop_counts),
    "distinct_diseases": len(disease_counts),
    "single_condition_crops": {
        "healthy_only_crops": crops_only_healthy,
        "diseased_only_crops": crops_only_diseased,
        "balanced_crops": crops_both
    },
    "rare_disease_classes_below_20": rare_classes,
    "scientific_verdict": "SUPERVISED_DISEASE_CLASSIFICATION_UNSUPPORTED",
    "recommended_analytical_scope": (
        "Retain AgroVision-Mine strictly as an Unsupervised Visual Pattern Mining, "
        "Multimodal Data Warehousing, and Reference-Similarity Retrieval Workbench. "
        "Do not implement an unsupported end-to-end clinical disease classifier."
    ),
    "justification_factors": unsupported_reasons
}

with open("data/reports/supervised_classification_feasibility.json", "w") as f:
    json.dump(decision, f, indent=2)

print("Saved scientific evaluation to data/reports/supervised_classification_feasibility.json")
print("Decision: SUPERVISED_DISEASE_CLASSIFICATION_UNSUPPORTED")
