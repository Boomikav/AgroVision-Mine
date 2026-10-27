import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set up high-res figure for Slide 11 Star Schema Diagram
fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Background
fig.patch.set_facecolor('#F7F6EF')
ax.set_facecolor('#F7F6EF')

# Colors
FACT_BG = '#24342D'
FACT_HEADER = '#175D44'
DIM_BG = '#FFFFFF'
DIM_HEADER = '#2E7D32'
BORDER_COLOR = '#A3B899'
TEXT_DARK = '#0F1F18'
TEXT_MUTED = '#404943'
ACCENT_GREEN = '#34765B'
LINE_COLOR = '#175D44'

def draw_table(ax, x, y, w, h, title, subtitle, rows, is_fact=False):
    # Shadow / border
    bg_col = FACT_BG if is_fact else DIM_BG
    hdr_col = FACT_HEADER if is_fact else DIM_HEADER
    text_hdr = '#FFFFFF'
    text_sub = '#C3EFAA' if is_fact else '#E2F5EB'
    border_col = '#175D44' if is_fact else BORDER_COLOR
    
    # Outer box
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.5",
                                  facecolor=bg_col, edgecolor=border_col, linewidth=1.8, zorder=2)
    ax.add_patch(rect)
    
    # Header box
    hdr_h = 9.0
    hdr_rect = patches.FancyBboxPatch((x, y + h - hdr_h), w, hdr_h, boxstyle="round,pad=0.3,rounding_size=1.0",
                                      facecolor=hdr_col, edgecolor=border_col, linewidth=1.2, zorder=3)
    ax.add_patch(hdr_rect)
    
    # Header text
    ax.text(x + w/2, y + h - 3.8, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=text_hdr, zorder=4)
    ax.text(x + w/2, y + h - 6.8, subtitle, ha='center', va='center', fontsize=7.5, color=text_sub, zorder=4)
    
    # Rows
    row_y = y + h - 12.0
    row_step = (h - 13.0) / max(len(rows), 1)
    for r in rows:
        col = '#E2F5EB' if is_fact else TEXT_DARK
        weight = 'bold' if ('[PK]' in r or '[FK]' in r) else 'normal'
        ax.text(x + 2.5, row_y, r, ha='left', va='center', fontsize=7.2, fontweight=weight, color=col, zorder=4)
        row_y -= row_step

# Central Fact Table
fact_rows = [
    "• observation_key INTEGER [PK]",
    "• crop_key INTEGER [FK -> dim_crop]",
    "• disease_key INTEGER [FK -> dim_disease]",
    "• image_key INTEGER [FK -> dim_image]",
    "• feature_key INTEGER [FK -> dim_visual_feature]",
    "• observation_count INTEGER (1)",
    "• lesion_severity_score FLOAT (0.0-1.0)",
    "• image_sharpness_score FLOAT (Laplacian)",
    "• created_at TIMESTAMP"
]
draw_table(ax, 31, 30, 38, 36, "disease_observation_fact", "Central Fact Table | 2,596 Rows", fact_rows, is_fact=True)

# Top Left: dim_crop
crop_rows = [
    "• crop_key INTEGER [PK]",
    "• crop_name VARCHAR(64) UNIQUE",
    "• botanical_name VARCHAR(128)",
    "• crop_category VARCHAR(64)",
    "• monocot_dicot VARCHAR(32)"
]
draw_table(ax, 3, 62, 28, 25, "dim_crop", "Botanical Hierarchy | 14 Rows", crop_rows)

# Bottom Left: dim_disease
disease_rows = [
    "• disease_key INTEGER [PK]",
    "• disease_name VARCHAR(128) UNIQUE",
    "• pathogen_type VARCHAR(64)",
    "• causal_agent VARCHAR(128)",
    "• primary_symptom VARCHAR(128)"
]
draw_table(ax, 3, 5, 28, 25, "dim_disease", "Pathology Dimension | 19 Rows", disease_rows)

# Top Right: dim_image
image_rows = [
    "• image_key INTEGER [PK]",
    "• raw_image_id VARCHAR(64) UNIQUE",
    "• filename VARCHAR(255)",
    "• file_format VARCHAR(16) (PNG/JPG)",
    "• dimensions VARCHAR(32) (256x256)",
    "• dataset_source VARCHAR(64)"
]
draw_table(ax, 69, 62, 28, 25, "dim_image", "Acquisition Metadata | 2,596 Rows", image_rows)

# Bottom Right: dim_visual_feature
feature_rows = [
    "• feature_key INTEGER [PK]",
    "• raw_image_id VARCHAR(64) UNIQUE",
    "• 19 Color Moments (RGB/HSV/Veg)",
    "• 7 Haralick GLCM Textures",
    "• 6 Morphometric Shape Contours",
    "• 32 Total Continuous Features"
]
draw_table(ax, 69, 5, 28, 25, "dim_visual_feature", "Feature Store | 2,596 Rows", feature_rows)

# Draw connecting lines with arrows
def connect(x1, y1, x2, y2, label="1:N"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=LINE_COLOR, lw=2.2, mutation_scale=14),
                zorder=1)

# dim_crop -> Fact
connect(29, 66, 33, 58)
# dim_disease -> Fact
connect(29, 25, 33, 34)
# dim_image -> Fact
connect(71, 66, 67, 58)
# dim_visual_feature -> Fact
connect(71, 25, 67, 34)

# Title overlay
ax.text(50, 95, "KIMBALL STAR SCHEMA — PHYSICAL DATA WAREHOUSE", ha='center', va='center',
        fontsize=12, fontweight='bold', color='#175D44')
ax.text(50, 91.5, "database/agrovision_warehouse.db • 2,596 Observations • PRAGMA foreign_keys = ON", ha='center', va='center',
        fontsize=8.5, color='#404943')

plt.tight_layout()
plt.savefig("docs/star_schema_unified.png", bbox_inches='tight', facecolor=fig.get_facecolor(), dpi=300)
plt.close()
print("Saved docs/star_schema_unified.png successfully!")
