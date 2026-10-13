"""
Generate High-Resolution Visual Assets for Review 1 PowerPoint Presentation.
Creates:
1. pipeline_flow.png: End-to-end multimodal pipeline
2. star_schema_erd.png: Kimball Star Schema diagram
3. feature_breakdown.png: 44-column feature store taxonomy
4. preprocessing_comparison.png: Real image + quality diagnostics
5. olap_visuals.png: Real OLAP analytical results charts
6. dashboard_composite.png: Streamlit dashboard visualization
"""
import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image

output_dir = Path("assets/presentation")
output_dir.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Pipeline Flowchart (pipeline_flow.png)
# -----------------------------------------------------------------------------
def generate_pipeline_flow():
    fig, ax = plt.subplots(figsize=(14, 2.5), dpi=300)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    stages = [
        ("Raw Imagery\n(36 Authentic Images)", "#E8F5E9", "#2E7D32"),
        ("Quality Gates\n(Diagnostics & 256x256)", "#E3F2FD", "#1565C0"),
        ("Feature Extraction\n(34 Visual Descriptors)", "#FFF8E1", "#F57F17"),
        ("Production ETL\n(Dimension-First Load)", "#EDE7F6", "#512DA8"),
        ("Star Schema DW\n(Fact: 1 Observation)", "#FCE4EC", "#C2185B"),
        ("OLAP Analytics\n(Roll-up, Drill, Slice, Dice, Pivot)", "#E0F2F1", "#00695C"),
        ("Interactive UI\n(Streamlit Dashboard)", "#EFEBE9", "#4E342E")
    ]

    n = len(stages)
    box_w = 1.45
    box_h = 1.4
    spacing = 1.95
    start_x = 0.4
    y = 0.55

    for i, (text_str, bg_col, border_col) in enumerate(stages):
        x = start_x + i * spacing
        # Draw box
        rect = patches.FancyBboxPatch(
            (x, y - box_h / 2), box_w, box_h,
            boxstyle="round,pad=0.08,rounding_size=0.15",
            facecolor=bg_col, edgecolor=border_col, linewidth=2
        )
        ax.add_patch(rect)
        # Text
        ax.text(
            x + box_w / 2, y, text_str,
            ha="center", va="center", fontsize=8.5, fontweight="bold",
            color="#212121", fontfamily="sans-serif"
        )
        # Arrow
        if i < n - 1:
            arr_start = x + box_w + 0.05
            arr_end = arr_start + (spacing - box_w) - 0.1
            ax.annotate(
                "", xy=(arr_end, y), xytext=(arr_start, y),
                arrowprops=dict(arrowstyle="-|>", color="#546E7A", lw=2.5, mutation_scale=15)
            )

    ax.set_xlim(0, start_x + (n - 1) * spacing + box_w + 0.4)
    ax.set_ylim(-0.3, 1.4)
    plt.tight_layout()
    plt.savefig(output_dir / "pipeline_flow.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("Generated pipeline_flow.png")


# -----------------------------------------------------------------------------
# 2. Star Schema ERD (star_schema_erd.png)
# -----------------------------------------------------------------------------
def generate_star_schema_erd():
    fig, ax = plt.subplots(figsize=(10, 8.0), dpi=300)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    # Center Fact
    fact_box = patches.FancyBboxPatch(
        (3.2, 2.3), 3.6, 2.8,
        boxstyle="round,pad=0.1,rounding_size=0.15",
        facecolor="#1B4332", edgecolor="#081C15", linewidth=2.5
    )
    ax.add_patch(fact_box)
    fact_text = (
        "DISEASE_OBSERVATION_FACT\n"
        "-------------------------------------\n"
        "• observation_key (PK) [INT]\n"
        "• crop_key (FK) → dim_crop\n"
        "• disease_key (FK) → dim_disease\n"
        "• image_key (FK) → dim_image\n"
        "• feature_key (FK) → dim_visual_feature\n"
        "• observation_count: 1 (Additive)\n"
        "• lesion_severity_score [0.0 - 10.0]\n"
        "• image_sharpness_score (Laplacian Var)\n"
        "• lesion_coverage_ratio [0.0 - 1.0]\n"
        "• texture_contrast_norm [0.0 - 1.0]\n"
        "• etl_batch_id, created_at\n"
        "-------------------------------------\n"
        "36 Valid Observations Loaded"
    )
    ax.text(5.0, 3.7, fact_text, ha="center", va="center", color="#FFFFFF", fontsize=7.5, fontfamily="monospace")

    # Dimensions
    dims = [
        # North: DIM_CROP
        (3.4, 5.5, 3.2, 1.4, "DIM_CROP (1 Row)", [
            "• crop_key (PK) [INT]",
            "• crop_code (UK): RICE",
            "• botanical_name: Oryza sativa",
            "• crop_category: Cereal",
            "• economic_role: Primary Staple"
        ], "#D8F3DC", "#2D6A4F", (5.0, 5.5), (5.0, 5.1)),
        # East: DIM_DISEASE
        (7.2, 2.6, 2.7, 2.2, "DIM_DISEASE (4 Rows)", [
            "• disease_key (PK) [INT]",
            "• disease_code (UK)",
            "• disease_name: 3 Active",
            "• pathogen_type: Fungal/Bact",
            "• causal_agent (Latin)",
            "• primary_symptom",
            "• HEALTHY (Control Baseline)"
        ], "#D8F3DC", "#2D6A4F", (7.2, 3.7), (6.8, 3.7)),
        # South: DIM_IMAGE
        (3.4, 0.4, 3.2, 1.5, "DIM_IMAGE (36 Rows)", [
            "• image_key (PK) [INT]",
            "• raw_id (UK), filename",
            "• raw_dim: 256x256 RGB",
            "• md5_hash (Cryptographic UK)",
            "• blur_score, phash",
            "• disk_storage_paths"
        ], "#D8F3DC", "#2D6A4F", (5.0, 1.9), (5.0, 2.3)),
        # West: DIM_VISUAL_FEATURE
        (0.1, 2.4, 2.8, 2.6, "DIM_VISUAL_FEATURE (36 Rows)", [
            "• feature_key (PK) [INT]",
            "• image_filename (UK)",
            "• 17 Color Moments (RGB/HSV)",
            "• exg_index_mean (Vegetation)",
            "• dominant_color_tone",
            "• 7 Haralick GLCM Textures",
            "• 7 Morphometric Shape Contours",
            "(34 Explainable Descriptors)"
        ], "#D8F3DC", "#2D6A4F", (2.9, 3.7), (3.2, 3.7))
    ]

    for (x, y, w, h, title, lines, bg_col, b_col, conn_start, conn_end) in dims:
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.08,rounding_size=0.12",
            facecolor=bg_col, edgecolor=b_col, linewidth=2
        )
        ax.add_patch(rect)
        content = f"{title}\n" + "-" * 28 + "\n" + "\n".join(lines)
        ax.text(x + w / 2, y + h / 2, content, ha="center", va="center", color="#1B4332", fontsize=7.0, fontfamily="monospace")

        # Connection line
        ax.annotate(
            "", xy=conn_end, xytext=conn_start,
            arrowprops=dict(arrowstyle="<->", color="#081C15", lw=2, mutation_scale=12)
        )

    # Title & Grain Badge
    ax.text(5.0, 7.7, "AgroVision-Mine Multimodal Star Schema", ha="center", va="center", fontsize=13, fontweight="bold", color="#1B4332")
    grain_badge = patches.FancyBboxPatch(
        (1.5, 7.1), 7.0, 0.38,
        boxstyle="round,pad=0.04,rounding_size=0.08",
        facecolor="#FFF3E0", edgecolor="#E65100", linewidth=1.5
    )
    ax.add_patch(grain_badge)
    ax.text(5.0, 7.29, "FACT GRAIN: Exactly ONE row per validated preprocessed multimodal image observation", ha="center", va="center", fontsize=7.8, fontweight="bold", color="#BF360C")

    ax.set_xlim(-0.2, 10.2)
    ax.set_ylim(0.0, 8.1)
    plt.tight_layout()
    plt.savefig(output_dir / "star_schema_erd.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("Generated star_schema_erd.png")


# -----------------------------------------------------------------------------
# 3. Feature Breakdown (feature_breakdown.png)
# -----------------------------------------------------------------------------
def generate_feature_breakdown():
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    categories = [
        ("Color Moments & Indices\n(17 Descriptors)", [
            "• RGB Channel Means (R, G, B)",
            "• RGB Standard Deviations",
            "• Normalized Chromaticities",
            "• HSV Hue, Saturation, Value Means",
            "• HSV Standard Deviations",
            "• Excess Green Index (ExG)",
            "• Dominant Tone Classification"
        ], "#E8F5E9", "#2E7D32"),
        ("Haralick GLCM Texture\n(7 Descriptors)", [
            "• GLCM Angular Second Moment",
            "• GLCM Texture Contrast",
            "• Normalized Contrast Disruption",
            "• Dissimilarity Measure",
            "• Homogeneity (Inverse Difference)",
            "• Haralick Texture Energy",
            "• Linear Dependency Correlation"
        ], "#E3F2FD", "#1565C0"),
        ("Morphometric Shape Contours\n(7 Descriptors)", [
            "• Otsu Threshold Lesion Detection",
            "• Valid Contour Existence Flag",
            "• Macro Lesion Area (Pixels)",
            "• Contour Boundary Perimeter",
            "• Bounding Box Aspect Ratio",
            "• Circularity / Roundness Factor",
            "• Solidity & Surface Coverage Ratio"
        ], "#FFF3E0", "#E65100"),
        ("Metadata & Lineage Fields\n(10 Identifier Columns)", [
            "• image_id (Unique Synthetic ID)",
            "• filename, raw_path, proc_path",
            "• crop_label (botanical host)",
            "• condition_label, disease_label",
            "• pest_label, is_pest (Flag)",
            "• md5_hash (Cryptographic Audit)",
            "Total Dataset: 44 Columns"
        ], "#F3E5F5", "#6A1B9A")
    ]

    card_w = 2.2
    card_h = 3.6
    spacing = 2.45
    start_x = 0.35

    for i, (title, items, bg_col, b_col) in enumerate(categories):
        x = start_x + i * spacing
        rect = patches.FancyBboxPatch(
            (x, 0.4), card_w, card_h,
            boxstyle="round,pad=0.08,rounding_size=0.12",
            facecolor=bg_col, edgecolor=b_col, linewidth=2
        )
        ax.add_patch(rect)
        # Title box
        title_box = patches.FancyBboxPatch(
            (x, 3.2), card_w, 0.8,
            boxstyle="round,pad=0.05,rounding_size=0.1",
            facecolor=b_col, edgecolor=b_col, linewidth=1
        )
        ax.add_patch(title_box)
        ax.text(x + card_w / 2, 3.6, title, ha="center", va="center", color="#FFFFFF", fontsize=8.5, fontweight="bold")

        body_text = "\n".join(items)
        ax.text(x + 0.12, 1.8, body_text, ha="left", va="center", color="#212121", fontsize=7.2, fontfamily="sans-serif", linespacing=1.6)

    ax.text(5.0, 4.4, "44-Column Feature Store: 34 Explainable Descriptors + 10 Lineage Fields", ha="center", va="center", fontsize=12, fontweight="bold", color="#1B4332")
    ax.set_xlim(0, 10.0)
    ax.set_ylim(0.2, 4.7)
    plt.tight_layout()
    plt.savefig(output_dir / "feature_breakdown.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("Generated feature_breakdown.png")


# -----------------------------------------------------------------------------
# 4. Preprocessing & Quality Gate Visuals (preprocessing_comparison.png)
# -----------------------------------------------------------------------------
def generate_preprocessing_visuals():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")

    # Sample images
    raw_img_path = Path("data/raw/rice/bacterial_leaf_blight/DSC_0365.JPG")
    proc_img_path = Path("data/processed/rice/bacterial_leaf_blight/proc_DSC_0365.png")

    if raw_img_path.exists():
        raw_img = Image.open(raw_img_path)
        axes[0].imshow(raw_img)
        axes[0].set_title(f"Raw Field Capture\n({raw_img.width}x{raw_img.height} px)", fontsize=9, fontweight="bold", color="#B71C1C")
        axes[0].axis("off")
    else:
        axes[0].text(0.5, 0.5, "Raw Image", ha="center", va="center")
        axes[0].axis("off")

    if proc_img_path.exists():
        proc_img = Image.open(proc_img_path)
        axes[1].imshow(proc_img)
        axes[1].set_title(f"Standardized & Normalized\n(256x256 px RGB, Lanczos)", fontsize=9, fontweight="bold", color="#1B5E20")
        axes[1].axis("off")
    else:
        axes[1].text(0.5, 0.5, "Processed Image", ha="center", va="center")
        axes[1].axis("off")

    # Quality Gate Summary Bar
    gates = ["Corrupted Header", "Tiny Dimensions", "MD5 Duplicate", "Extension Check"]
    results = [1, 1, 1, 1]  # all caught in test suite
    y_pos = np.arange(len(gates))

    axes[2].barh(y_pos, results, color=["#D32F2F", "#E65100", "#1976D2", "#7B1FA2"], height=0.55)
    axes[2].set_yticks(y_pos)
    axes[2].set_yticklabels(gates, fontsize=8.5, fontweight="bold")
    axes[2].set_xlabel("Diagnostic Artifacts Caught (100% Rejection)", fontsize=8)
    axes[2].set_xlim(0, 1.4)
    for i, v in enumerate(results):
        axes[2].text(v + 0.05, i, "PASSED (Rejected)", va="center", color="#2E7D32", fontsize=8, fontweight="bold")
    axes[2].set_title("Quality Gate Verification\n(Isolated in data/diagnostic_tests/)", fontsize=9, fontweight="bold", color="#1B4332")
    axes[2].spines["top"].set_visible(False)
    axes[2].spines["right"].set_visible(False)

    plt.tight_layout()
    plt.savefig(output_dir / "preprocessing_comparison.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("Generated preprocessing_comparison.png")


# -----------------------------------------------------------------------------
# 5. OLAP Analytics Visuals (olap_visuals.png)
# -----------------------------------------------------------------------------
def generate_olap_visuals():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")

    # Chart 1: Roll-up
    categories = ["Cereal\n(Rice)"]
    obs = [36]
    bars = axes[0].bar(categories, obs, color="#2D6A4F", width=0.45)
    axes[0].set_title("1. Roll-up Aggregation\n(Obs -> Crop -> Category)", fontsize=9, fontweight="bold", color="#1B4332")
    axes[0].set_ylabel("Total Observations", fontsize=8)
    axes[0].set_ylim(0, 42)
    for b in bars:
        axes[0].text(b.get_x() + b.get_width() / 2, b.get_height() + 1, f"{int(b.get_height())} Facts\nAvg Severity: 3.57", ha="center", fontsize=8, fontweight="bold")
    axes[0].spines["top"].set_visible(False)
    axes[0].spines["right"].set_visible(False)

    # Chart 2: True Drill-down
    diseases = ["Bacterial\nLeaf Blight\n(Bacterial)", "Brown Spot\n(Fungal)", "Leaf Smut\n(Fungal)"]
    counts = [12, 12, 12]
    colors = ["#1976D2", "#388E3C", "#689F38"]
    bars2 = axes[1].bar(diseases, counts, color=colors, width=0.55)
    axes[1].set_title("2. True Drill-down\n(Pathogen Type -> Disease Name)", fontsize=9, fontweight="bold", color="#1B4332")
    axes[1].set_ylim(0, 16)
    for b in bars2:
        axes[1].text(b.get_x() + b.get_width() / 2, b.get_height() + 0.5, f"{int(b.get_height())}", ha="center", fontsize=8.5, fontweight="bold")
    axes[1].spines["top"].set_visible(False)
    axes[1].spines["right"].set_visible(False)

    # Chart 3: Pivot Cross-Tabulation Matrix
    matrix = np.array([[24, 12, 0, 0]])
    im = axes[2].imshow(matrix, cmap="Greens", vmin=0, vmax=25)
    axes[2].set_xticks([0, 1, 2, 3])
    axes[2].set_xticklabels(["Fungal", "Bacterial", "Viral", "Healthy*"], fontsize=8, fontweight="bold")
    axes[2].set_yticks([0])
    axes[2].set_yticklabels(["Rice\n(Cereal)"], fontsize=8.5, fontweight="bold")
    axes[2].set_title("3. Pivot Dimension Rotation\n(Rows: Crop x Cols: Pathogen)", fontsize=9, fontweight="bold", color="#1B4332")

    for j in range(4):
        val = matrix[0, j]
        col_text = "#FFFFFF" if val > 15 else "#000000"
        axes[2].text(j, 0, f"{val}", ha="center", va="center", color=col_text, fontsize=11, fontweight="bold")
    axes[2].set_xlabel("*Healthy=0 (unpopulated control baseline)", fontsize=7, color="#555555")

    plt.tight_layout()
    plt.savefig(output_dir / "olap_visuals.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("Generated olap_visuals.png")


if __name__ == "__main__":
    generate_pipeline_flow()
    generate_star_schema_erd()
    generate_feature_breakdown()
    generate_preprocessing_visuals()
    generate_olap_visuals()
    print("All presentation visual assets generated successfully!")
