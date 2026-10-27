"""AgroVision-Mine: Research Paper Figure Generator.
Produces publication-quality 300+ DPI figures for IEEE conference paper submission.
"""
import json
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FIG_DIR = ROOT / "research_paper" / "figures"
REPORTS_DIR = ROOT / "data" / "reports"
PRED_REP_PATH = REPORTS_DIR / "prediction" / "prediction_evaluation_report.json"
CLUSTERING_PATH = ROOT / "data" / "features" / "clustering_assignments_v2.csv"
INSPECT_DIR = REPORTS_DIR / "presentation_inspection"

# IEEE Style Settings
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 9
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['figure.titlesize'] = 12

PRIMARY_COLOR = '#175D44'   # Deep Green
SECONDARY_COLOR = '#2D6A4F' # Forest Green
ACCENT_BLUE = '#1F4E79'     # Slate Blue
ACCENT_AMBER = '#B45309'    # Amber
ALERT_RED = '#93000A'       # Red
LIGHT_BG = '#F7F6EF'


def generate_fig1_architecture():
    """Generates Figure 1: 5-Layer System Architecture Diagram."""
    fig, ax = plt.subplots(figsize=(10, 3.6), dpi=300)
    ax.axis('off')

    layers = [
        ("Layer 1: Ingestion & Quality", 
         ["PlantDoc (2,560) + ICAR (36)", "Gate 1: Magic Bytes Check", "Gate 2: Geometry (>=100px)", "Gate 3: Payload (<=15MB)", "Gate 4: MD5 Deduplication", "Gate 5: EXIF Transpose"],
         0.02, 0.17, '#E8F5E9', '#2E7D32'),
        ("Layer 2: Features & Store", 
         ["256x256 Bilinear Standardization", "19 Color Moments (RGB/HSV/ExG)", "7 Haralick GLCM Textures", "6 Contour Morphometrics", "44-Col Feature Store (2,596 rows)", "SHA-256 Immutability Check"],
         0.22, 0.17, '#E0F2F1', '#00695C'),
        ("Layer 3: Warehouse & ETL", 
         ["Kimball Star Schema in SQLite", "disease_observation_fact (2,596)", "dim_crop (14 botanical taxa)", "dim_disease (20 conditions)", "dim_image & dim_visual_feature", "PRAGMA foreign_keys = ON"],
         0.42, 0.17, '#E1F5FE', '#0277BD'),
        ("Layer 4: Analytical Engines", 
         ["ANSI SQL OLAP (Roll-up, Slice)", "Dual K-Means (K=2 primary, K=4)", "2D PCA Projection (52.1% var)", "Apriori & FP-Growth Parity", "32D Euclidean Nearest Neighbors", "Deep EfficientNet-B0 (25-class)"],
         0.62, 0.19, '#F3E5F5', '#6A1B9A'),
        ("Layer 5: Presentation Tier", 
         ["FastAPI REST Adapter (:8001)", "React 19 + TypeScript SPA", "Live Visual Workbench GUI", "Cross-Modal OOD Safeguard", "117/117 Test Suite Passing", "Zero-Mutation In-Memory Cache"],
         0.84, 0.15, '#FFF8E1', '#F57F17')
    ]

    from matplotlib.patches import FancyBboxPatch
    for title, items, left, width, bg, border in layers:
        rect = FancyBboxPatch((left, 0.05), width, 0.88, transform=ax.transAxes,
                              facecolor=bg, edgecolor=border, linewidth=1.5,
                              boxstyle="round,pad=0.015", zorder=1)
        ax.add_patch(rect)
        ax.text(left + width/2, 0.87, title, transform=ax.transAxes,
                ha='center', va='top', fontsize=8.5, fontweight='bold', color=border)
        
        y_text = 0.77
        for item in items:
            ax.text(left + 0.012, y_text, f"• {item}", transform=ax.transAxes,
                    ha='left', va='top', fontsize=6.8, color='#1A1A1A')
            y_text -= 0.11

    # Connective arrows
    arrow_positions = [0.192, 0.392, 0.592, 0.812]
    for x in arrow_positions:
        ax.annotate('', xy=(x + 0.025, 0.48), xytext=(x, 0.48), xycoords='axes fraction',
                    arrowprops=dict(facecolor=PRIMARY_COLOR, edgecolor='none', width=2.0, headwidth=6, headlength=6))

    plt.tight_layout()
    out_p = FIG_DIR / "fig1_system_architecture.png"
    plt.savefig(out_p, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_p}")


def generate_fig2_star_schema():
    """Copies the verified high-resolution star schema diagram."""
    src = INSPECT_DIR / "star_schema_diagram.png"
    dst = FIG_DIR / "fig2_star_schema.png"
    if src.exists():
        shutil.copy(src, dst)
        print(f"Copied: {dst}")
    else:
        print(f"Warning: {src} not found.")


def generate_fig3_model_tournament():
    """Generates Figure 3: Model Selection Tournament (Validation Macro-F1)."""
    models = ['Majority\nBaseline', 'RBF-SVM\n(32D)', 'Random\nForest (32D)', 'EfficientNet-B0\n(Fine-Tuned CNN)']
    val_macro_f1 = [0.58, 15.12, 17.02, 63.26]
    test_macro_f1 = [0.58, 19.01, 19.19, 60.84]

    x = np.arange(len(models))
    width = 0.35

    fig, ax = plt.subplots(figsize=(5.5, 3.2), dpi=300)
    rects1 = ax.bar(x - width/2, val_macro_f1, width, label='Validation Macro-F1 (Selection Metric)', color=SECONDARY_COLOR, edgecolor='black', linewidth=0.8)
    rects2 = ax.bar(x + width/2, test_macro_f1, width, label='Held-Out Test Macro-F1 (N=490)', color='#81C784', edgecolor='black', linewidth=0.8)

    ax.set_ylabel('Macro-F1 Score (%)', fontweight='bold')
    ax.set_title('Model Tournament: Handcrafted Baselines vs Deep CNN', fontweight='bold', pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontweight='bold')
    ax.set_ylim(0, 75)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)

    for r in rects1:
        h = r.get_height()
        ax.annotate(f'{h:.1f}%', xy=(r.get_x() + r.get_width()/2, h), xytext=(0, 2),
                    textcoords="offset points", ha='center', va='bottom', fontsize=7.5, fontweight='bold')
    for r in rects2:
        h = r.get_height()
        ax.annotate(f'{h:.1f}%', xy=(r.get_x() + r.get_width()/2, h), xytext=(0, 2),
                    textcoords="offset points", ha='center', va='bottom', fontsize=7.5, color='#1B5E20')

    plt.tight_layout()
    out_p = FIG_DIR / "fig3_model_tournament.png"
    plt.savefig(out_p, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_p}")


def generate_fig4_confusion_matrix():
    """Generates Figure 4: 25-Class Normalized Confusion Matrix on Held-Out Test Set (N=490)."""
    with open(PRED_REP_PATH) as f:
        rep = json.load(f)

    cm = np.array(rep['confusion_matrix'])
    classes = [c.replace('___', ' - ') for c in rep['classes']]
    short_classes = [c.replace('Tomato', 'Tom').replace('Bell Pepper', 'Pep').replace('Raspberry', 'Rasp').replace('Strawberry', 'Straw').replace('Blueberry', 'Blue') for c in classes]

    # Normalize by true class support (row sum)
    row_sums = cm.sum(axis=1)[:, np.newaxis]
    row_sums[row_sums == 0] = 1
    cm_norm = cm.astype('float') / row_sums

    fig, ax = plt.subplots(figsize=(7.5, 6.8), dpi=300)
    sns.heatmap(cm_norm, annot=False, cmap='Greens', ax=ax, cbar_kws={'label': 'Recall (Fraction of True Class)'},
                xticklabels=short_classes, yticklabels=short_classes)

    ax.set_title('Normalized Confusion Matrix: 25 Composite Classes (Test N = 490)', fontweight='bold', pad=12)
    ax.set_xlabel('Predicted Label', fontweight='bold', labelpad=8)
    ax.set_ylabel('Ground Truth Label', fontweight='bold', labelpad=8)
    plt.xticks(rotation=90, fontsize=6.5)
    plt.yticks(rotation=0, fontsize=6.5)

    plt.tight_layout()
    out_p = FIG_DIR / "fig4_confusion_matrix.png"
    plt.savefig(out_p, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_p}")


def generate_fig5_pca_clusters():
    """Generates Figure 5: 2D PCA Loadings & Cluster Separation."""
    df_cl = pd.read_csv(CLUSTERING_PATH)
    
    fig, ax = plt.subplots(figsize=(5.5, 3.6), dpi=300)
    
    # Plot PlantDoc cluster 0 and 1
    c0 = df_cl[(df_cl['cluster_id_k2'] == 0) & (df_cl['dataset_source'] == 'plantdoc')]
    c1 = df_cl[(df_cl['cluster_id_k2'] == 1) & (df_cl['dataset_source'] == 'plantdoc')]
    icar = df_cl[df_cl['dataset_source'] == 'icar_ogd']

    ax.scatter(c0['pca_x'], c0['pca_y'], c='#2E7D32', alpha=0.35, s=12, label='Cluster 0 (Dense Green Foliage, N=2,114)', edgecolors='none')
    ax.scatter(c1['pca_x'], c1['pca_y'], c='#C62828', alpha=0.55, s=14, label='Cluster 1 (Textured / Lesion-Heavy, N=446)', edgecolors='none')
    ax.scatter(icar['pca_x'], icar['pca_y'], c='#0277BD', marker='^', s=45, label='ICAR Rice Flatbed Scanner Shift (N=36)', edgecolors='black', linewidth=0.7, zorder=5)

    ax.set_xlabel('Principal Component 1: Foliar Luminance (38.56% Var)', fontweight='bold')
    ax.set_ylabel('Principal Component 2: Textural Contrast (13.55% Var)', fontweight='bold')
    ax.set_title('2D PCA Projection: Visual Clusters & Domain Shift (52.11% Total Var)', fontweight='bold', pad=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(frameon=True, facecolor='white', framealpha=0.92, loc='lower right', fontsize=7.5)

    plt.tight_layout()
    out_p = FIG_DIR / "fig5_pca_clusters.png"
    plt.savefig(out_p, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_p}")


def generate_fig6_per_class_f1():
    """Generates Figure 6: Per-Class F1-Score Breakdown across all 25 Classes."""
    with open(PRED_REP_PATH) as f:
        rep = json.load(f)

    pcm = rep['per_class_metrics']
    sorted_pcm = sorted(pcm, key=lambda x: x['f1_score'], reverse=True)
    labels = [x['readable_label'] for x in sorted_pcm]
    f1_scores = [x['f1_score'] * 100 for x in sorted_pcm]
    supports = [x['test_support'] for x in sorted_pcm]

    y_pos = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(6.2, 5.8), dpi=300)
    colors = [PRIMARY_COLOR if s >= 60 else (ACCENT_AMBER if s >= 40 else ALERT_RED) for s in f1_scores]
    bars = ax.barh(y_pos, f1_scores, color=colors, edgecolor='black', linewidth=0.6, height=0.7)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=7.5)
    ax.invert_yaxis()
    ax.set_xlabel('Held-Out Test F1-Score (%)', fontweight='bold')
    ax.set_title('Per-Class F1-Score Breakdown (Held-Out Test Set N = 490)', fontweight='bold', pad=10)
    ax.set_xlim(0, 105)
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    # Reference mean line
    mean_f1 = rep['evaluation_summary']['test_macro_f1'] * 100
    ax.axvline(mean_f1, color='blue', linestyle=':', linewidth=1.2, label=f'Macro-F1 Mean = {mean_f1:.1f}%')
    ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9)

    for bar, score, supp in zip(bars, f1_scores, supports):
        w = bar.get_width()
        ax.text(w + 1.2, bar.get_y() + bar.get_height()/2, f'{score:.1f}% (n={supp})',
                va='center', ha='left', fontsize=6.8, color='#1A1A1A')

    plt.tight_layout()
    out_p = FIG_DIR / "fig6_per_class_f1.png"
    plt.savefig(out_p, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_p}")


def generate_fig7_inference_workbench():
    """Generates Figure 7: Dual-case demonstration of inference and out-of-domain safeguard."""
    from PIL import Image
    apple_p = INSPECT_DIR / "crop_apple_healthy.png"
    rice_p = INSPECT_DIR / "crop_rice_rejection.png"

    if apple_p.exists() and rice_p.exists():
        im1 = Image.open(apple_p)
        im2 = Image.open(rice_p)

        # Create side-by-side or stacked image
        w1, h1 = im1.size
        w2, h2 = im2.size
        target_w = max(w1, w2)
        im1_resized = im1.resize((target_w, int(h1 * (target_w / w1))), Image.Resampling.LANCZOS)
        im2_resized = im2.resize((target_w, int(h2 * (target_w / w2))), Image.Resampling.LANCZOS)

        total_h = im1_resized.height + im2_resized.height + 40
        combined = Image.new('RGB', (target_w, total_h), (255, 255, 255))
        combined.paste(im1_resized, (0, 0))
        combined.paste(im2_resized, (0, im1_resized.height + 40))

        out_p = FIG_DIR / "fig7_inference_workbench.png"
        combined.save(out_p, dpi=(300, 300))
        print(f"Generated: {out_p}")


if __name__ == "__main__":
    print("=" * 60)
    print("GENERATING PUBLICATION-GRADE RESEARCH FIGURES")
    print("=" * 60)
    generate_fig1_architecture()
    generate_fig2_star_schema()
    generate_fig3_model_tournament()
    generate_fig4_confusion_matrix()
    generate_fig5_pca_clusters()
    generate_fig6_per_class_f1()
    generate_fig7_inference_workbench()
    print("[SUCCESS] All figures generated in:", FIG_DIR)
