import matplotlib.pyplot as plt
import numpy as np

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=300)
fig.patch.set_facecolor('#F7F6EF')

# Left: Roll-up across all 2,596 rows
cats = ['Horticultural', 'Cereal', 'Legume']
counts = [2123, 408, 65]
colors = ['#175D44', '#34765B', '#8DA68E']

bars1 = ax1.bar(cats, counts, color=colors, width=0.55, edgecolor='#0F1F18', linewidth=1)
ax1.set_facecolor('#FFFFFF')
ax1.set_title('1. Roll-Up: 2,596 Facts by Category', fontsize=11, fontweight='bold', color='#175D44', pad=12)
ax1.set_ylabel('Observation Count', fontsize=9, color='#0F1F18')
ax1.set_ylim(0, 2400)
ax1.grid(axis='y', linestyle='--', alpha=0.3, color='#BFC9C2')
for bar in bars1:
    yval = bar.get_height()
    pct = (yval / 2596) * 100
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 50, f"{yval:,}\n({pct:.1f}%)", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#0F1F18')

# Right: Drill-down on Cereals (408 Obs: Corn 372 + Rice 36)
cereal_diseases = [
    'Corn: NLB', 'Corn: Rust', 'Corn: GLS',
    'Rice: BLB', 'Rice: BrownSpot', 'Rice: Smut'
]
cereal_counts = [190, 116, 66, 12, 12, 12]
cereal_colors = ['#2E7D32', '#388E3C', '#4CAF50', '#F57F17', '#FB8C00', '#FFA726']

bars2 = ax2.bar(cereal_diseases, cereal_counts, color=cereal_colors, width=0.6, edgecolor='#0F1F18', linewidth=1)
ax2.set_facecolor('#FFFFFF')
ax2.set_title('2. Drill-Down: Cereal Cube (408 Obs)', fontsize=11, fontweight='bold', color='#175D44', pad=12)
ax2.set_ylabel('Observation Count', fontsize=9, color='#0F1F18')
ax2.set_ylim(0, 220)
ax2.grid(axis='y', linestyle='--', alpha=0.3, color='#BFC9C2')
plt.setp(ax2.get_xticklabels(), rotation=25, ha='right', fontsize=8)
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 5, f"{yval}", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0F1F18')

plt.tight_layout()
plt.savefig('docs/olap_roll_down_unified.png', bbox_inches='tight', facecolor=fig.get_facecolor(), dpi=300)
plt.close()
print("Saved docs/olap_roll_down_unified.png successfully!")
