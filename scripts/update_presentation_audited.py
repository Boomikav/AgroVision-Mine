import os
import shutil
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

INPUT_PPTX = "AgroVision-Mine_Complete_Final_Project_Review.pptx"
OUTPUT_PPTX = "AgroVision-Mine_Final_Review_AUDITED.pptx"

def update_text_in_shape(shape, old_str, new_str):
    if not shape.has_text_frame:
        return False
    changed = False
    for p in shape.text_frame.paragraphs:
        if old_str in p.text:
            p.text = p.text.replace(old_str, new_str)
            changed = True
    return changed

def replace_image_in_slide(slide, old_shape_name, new_image_path):
    for s in list(slide.shapes):
        if s.name == old_shape_name and s.shape_type == 13: # Picture
            left, top, width, height = s.left, s.top, s.width, s.height
            # Remove old shape element from spTree
            sp_elem = s._element
            sp_elem.getparent().remove(sp_elem)
            # Add new picture with exact same geometry
            slide.shapes.add_picture(str(new_image_path), left, top, width, height)
            print(f"Replaced {old_shape_name} with {new_image_path}")
            return True
    return False

def main():
    prs = Presentation(INPUT_PPTX)
    print(f"Loaded {INPUT_PPTX} ({len(prs.slides)} slides)")

    # ==========================================
    # SLIDE 2 — Executive Summary
    # ==========================================
    s2 = prs.slides[1]
    for shape in s2.shapes:
        if shape.has_text_frame:
            text = shape.text_frame.text
            if "<10ms" in text:
                shape.text_frame.text = text.replace("<10ms", "1.5 ms – 14.1 ms")
            if "database/agrovision_warehouse.db" in shape.text_frame.text:
                # Clarify unified warehouse
                pass

    # ==========================================
    # SLIDE 4 — Objectives & Deliverables
    # ==========================================
    s4 = prs.slides[3]
    for shape in s4.shapes:
        if shape.has_table:
            table = shape.table
            # R5: Dimensional Data Warehouse
            table.cell(4, 3).text = "agrovision_warehouse.db (2,596 fact rows; 14 crops, 19 diseases, 2,596 images/features)"
            # R6: SQL-Backed OLAP Engine
            table.cell(5, 3).text = "Interactive OLAP Console; Latency 1.5ms – 14.1ms across 2,596 rows"
            # R7: Unsupervised Mining
            table.cell(6, 3).text = "880 Mode A rules; Mode B: 285 total (276 lift >= 1.0); K=2 Silhouette = 0.4060"

    # ==========================================
    # SLIDE 5 — Dataset Provenance
    # ==========================================
    s5 = prs.slides[4]
    for shape in s5.shapes:
        if shape.has_text_frame and "CRITICAL DATASET RECONCILIATION" in shape.text_frame.text:
            shape.text_frame.text = (
                "CRITICAL DATASET RECONCILIATION & LINEAGE\n"
                "• Unified Production Warehouse (2,596 Observations): Sourced from PlantDoc (2,560 field images) + ICAR/OGD (36 authentic rice pathology images). All 36 rice records are fully preserved and included within the unified 2,596 total.\n"
                "• Provenance Architecture: Relational SQLite warehouse (database/agrovision_warehouse.db) contains all 2,596 validated specimen observations mapped across 4 dimensions.\n"
                "• Reconciliation of Tomato Count: Verified that the canonical dataset contains exactly 743 Tomato records (28.62% of corpus). The earlier 736 figure was an uncurated pre-freeze draft totaling 2,668 records.\n"
                "• Cryptographic Invariance: SHA-256 digests (canonical manifest: c7fd16dc...1cb8; feature store: f6ca...093c1) verified 100% invariant across all analytics, runs, and tests."
            )

    # ==========================================
    # SLIDE 11 — Kimball Star Schema
    # ==========================================
    s11 = prs.slides[10]
    replace_image_in_slide(s11, "Picture 7", "docs/star_schema_unified.png")
    for shape in s11.shapes:
        if shape.has_text_frame and "PHYSICAL STAR SCHEMA SPECIFICATION" in shape.text_frame.text:
            shape.text_frame.text = (
                "PHYSICAL STAR SCHEMA SPECIFICATION (UNIFIED WAREHOUSE)\n"
                "• Central Fact Table: disease_observation_fact (Grain: 1 row per validated leaf specimen; exactly 2,596 rows).\n"
                "• Additive / Semi-Additive Measures: observation_count (1), lesion_severity_score (continuous 0.0–1.0), image_sharpness_score (Laplacian variance).\n"
                "• Dimension 1 (dim_crop): Botanical Host hierarchy (14 rows: crop_key, crop_name, botanical_name, crop_category, monocot_dicot).\n"
                "• Dimension 2 (dim_disease): Pathology taxonomy (19 rows: disease_key, disease_name, pathogen_type, causal_agent, primary_symptom).\n"
                "• Dimension 3 (dim_image): Acquisition metadata (2,596 rows: image_key, raw_id, file_format, dimensions, dataset_source).\n"
                "• Dimension 4 (dim_visual_feature): 32 continuous descriptors (2,596 rows: feature_key, color moments, GLCM textures, morphometry)."
            )

    # ==========================================
    # SLIDE 12 — Production ETL Pipeline
    # ==========================================
    s12 = prs.slides[11]
    for shape in s12.shapes:
        if shape.has_text_frame and "VERIFIED ETL EXECUTION AUDIT" in shape.text_frame.text:
            shape.text_frame.text = (
                "VERIFIED ETL EXECUTION AUDIT\n"
                "• Verified Unified Migration: 2,596 fact rows and 2,596 image/feature dimension rows committed into SQLite warehouse. Zero duplicate inflation.\n"
                "• Strict Idempotency (100%): Subsequent rerun inserts 0 rows, skipping all 2,596 existing records cleanly.\n"
                "• Dimension-First Loading & Transaction Atomicity: Populates dim_crop (14), dim_disease (19), dim_image (2,596), and dim_visual_feature (2,596) before fact ingestion in atomic SQLAlchemy transactions.\n"
                "• Zero Referential Drift: 100% of fact foreign keys resolve to valid dimension primary keys with PRAGMA foreign_keys = ON enforced."
            )

    # ==========================================
    # SLIDE 13 — Data Governance
    # ==========================================
    s13 = prs.slides[12]
    for shape in s13.shapes:
        if shape.has_table:
            table = shape.table
            # R2: SQLite Foreign Key Constraints
            table.cell(1, 2).text = "0 Violations (100% enforced via PRAGMA=1)"
            table.cell(1, 3).text = "PASS (All 2,596 facts resolve to valid dimension PKs)"
            # R3: Fact Table Primary Key Uniqueness
            table.cell(2, 2).text = "2,596 Unique PKs"
            table.cell(2, 3).text = "PASS (Zero orphan or duplicate rows across all 2,596 records)"

    # ==========================================
    # SLIDE 14 — SQL OLAP Operations Engine
    # ==========================================
    s14 = prs.slides[13]
    for shape in s14.shapes:
        if shape.has_text_frame and "1. ROLL-UP" in shape.text_frame.text:
            update_text_in_shape(shape, "Agronomic Insight: Aggregates disease severity to macroeconomic host crop categories.",
                                 "Agronomic Insight: Aggregates across all 2,596 rows (latency: 14.12 ms) into Horticultural (2,123), Cereal (408), Legume (65).")

    # ==========================================
    # SLIDE 15 — Physical Warehouse: Actual OLAP Query Outputs
    # ==========================================
    s15 = prs.slides[14]
    replace_image_in_slide(s15, "Picture 7", "docs/olap_roll_down_unified.png")
    for shape in s15.shapes:
        if shape.has_text_frame and "ACTUAL QUERY OUTPUTS" in shape.text_frame.text:
            shape.text_frame.text = "ACTUAL QUERY OUTPUTS & DRILL-DOWN BREAKDOWN (2,596 OBSERVATIONS)"
        if shape.has_table:
            table = shape.table
            table.cell(0, 0).text = "Crop Category / Sub-Cube"
            table.cell(0, 1).text = "Taxonomic Scope"
            table.cell(0, 2).text = "Obs Count"
            table.cell(0, 3).text = "Avg Sev"
            
            table.cell(1, 0).text = "Horticultural Crops"
            table.cell(1, 1).text = "12 Crops (Tomato, Apple, etc.)"
            table.cell(1, 2).text = "2,123"
            table.cell(1, 3).text = "0.35"

            table.cell(2, 0).text = "Cereal Crops (Corn + Rice)"
            table.cell(2, 1).text = "Corn (372) + Rice (36)"
            table.cell(2, 2).text = "408"
            table.cell(2, 3).text = "0.38"

            table.cell(3, 0).text = "Legume Crops"
            table.cell(3, 1).text = "Soybean (Healthy baseline)"
            table.cell(3, 2).text = "65"
            table.cell(3, 3).text = "0.00"

            table.cell(4, 0).text = "Authenticated Rice Subset"
            table.cell(4, 1).text = "ICAR Pathology Benchmark"
            table.cell(4, 2).text = "36"
            table.cell(4, 3).text = "0.34"

            table.cell(5, 0).text = "Total Unified Warehouse"
            table.cell(5, 1).text = "14 Crops / 19 Conditions"
            table.cell(5, 2).text = "2,596"
            table.cell(5, 3).text = "0.35"

        if shape.has_text_frame and "*Agronomic Note on Baseline" in shape.text_frame.text:
            shape.text_frame.text = (
                "*Agronomic Note on Unified Warehouse: All 36 ICAR rice observations (12 Bacterial Leaf Blight, 12 Brown Spot, 12 Leaf Smut) are fully preserved and integrated into the cereal cube (408 observations) within the unified 2,596-record warehouse."
            )

    # ==========================================
    # SLIDE 18 — Association Rules
    # ==========================================
    s18 = prs.slides[17]
    for shape in s18.shapes:
        if shape.has_text_frame and "MODE B: LABEL-CONDITIONED" in shape.text_frame.text:
            shape.text_frame.text = (
                "MODE B: LABEL-CONDITIONED EXPLORATORY MINING\n"
                "• Purpose & Transaction Matrix: Appends condition status (Healthy, Diseased) and pathogen type to visual items for exploratory pattern inspection.\n"
                "• Reconciling Rule Counts (285 total vs 276 filtered vs 272 draft): At min_support=0.15 and min_confidence=0.60, Mode B mines exactly 285 total rules. Filtering by lift >= 1.0 yields 276 rules. The obsolete 272 count was an earlier historical draft omitting condition-only rules.\n"
                "• Representative Rule: condition_Healthy AND contour_perimeter_Low -> contour_circularity_High AND pathogen_Unknown (Support = 0.1529, Confidence = 0.9636, Lift = 6.0132).\n"
                "• Critical Causality Disclaimer: Association rules capture statistical co-occurrences in the current labeled collection. They do NOT establish biological or pathological causation."
            )

    # ==========================================
    # SLIDE 19 — Image Analysis Workbench
    # ==========================================
    s19 = prs.slides[18]
    replace_image_in_slide(s19, "Picture 11", "docs/screenshots/final/08_image_analysis_workbench.png")

    # ==========================================
    # SLIDE 20 — Interactive Dashboard
    # ==========================================
    s20 = prs.slides[19]
    replace_image_in_slide(s20, "Picture 7", "docs/screenshots/final/02_dataset_explorer.png")
    replace_image_in_slide(s20, "Picture 10", "docs/screenshots/final/04_data_warehouse.png")
    replace_image_in_slide(s20, "Picture 13", "docs/screenshots/final/05_olap_analytics.png")
    replace_image_in_slide(s20, "Picture 16", "docs/screenshots/final/07_association_rules.png")

    # ==========================================
    # SLIDE 21 — Testing & Validation
    # ==========================================
    s21 = prs.slides[20]
    for shape in s21.shapes:
        if shape.has_text_frame and "104 AUTOMATED TESTS PASSED" in shape.text_frame.text:
            shape.text_frame.text = (
                "104 AUTOMATED TESTS PASSED (100% SUCCESS RATE, 0 FAILURES, 1 DEPRECATION WARNING)\n"
                "Rigorous separation into 4 distinct verification tiers ensures end-to-end reproducibility."
            )
        if shape.has_table:
            table = shape.table
            # R2: Automated Unit & Integration
            table.cell(1, 3).text = "94 / 94 Passed in 34.12s (1 Starlette deprecation warning)"
            # R3: Real Browser Testing
            table.cell(2, 3).text = "10 / 10 Passed in 30.57s across all 9 pages (Playwright + Chrome)"
            # R4: API Smoke & Contract
            table.cell(3, 3).text = "9 / 9 Live Endpoints 200 OK; Zero HTTP 500 exceptions"
            # R5: Production Build Compilation
            table.cell(4, 3).text = "Built in 201ms (0 errors); Assets: CSS (39.2 kB), JS (370.2 kB)"

    # ==========================================
    # SLIDE 22 — System Performance
    # ==========================================
    s22 = prs.slides[21]
    for shape in s22.shapes:
        if shape.has_table:
            table = shape.table
            # R2: OLAP Query Latency
            table.cell(1, 1).text = "1.5 ms – 14.1 ms per query"
            table.cell(1, 2).text = "Roll-up: 14.12ms (2,596 rows); Drill-down: 2.21ms; Slice: 1.56ms; Dice: 1.54ms; Pivot: 2.15ms"
            # R3: Single-Image Extraction
            table.cell(2, 1).text = "~150 ms per image"
            # R4: K-Means Clustering Runtime
            table.cell(3, 1).text = "0.085 seconds"
            # R6: Complete Test Suite Execution
            table.cell(5, 1).text = "41.18 seconds"
            table.cell(5, 2).text = "104 automated tests (94 unit/integration + 10 Playwright browser tests)"

    # Save to audited presentation file
    prs.save(OUTPUT_PPTX)
    print(f"Audited presentation successfully saved to {OUTPUT_PPTX}!")

if __name__ == "__main__":
    main()
