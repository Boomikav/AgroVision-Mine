import json

with open('data/reports/clustering_report_v2.json', 'r') as f:
    c = json.load(f)

print('=== CLUSTERING MULTI-K EVALUATION ===')
for r in c.get('multi_k_evaluation', []):
    print(f"K={r['k']}: Silhouette={r['silhouette_score']:.4f}, DB={r['davies_bouldin_index']:.4f}, CH={r.get('calinski_harabasz_score', 0):.2f}")

print('\n=== K=2 SOLUTION ===')
k2 = c.get('k2_solution', {})
print(f"Silhouette: {k2.get('silhouette_score')}, DB: {k2.get('davies_bouldin_index')}, CH: {k2.get('calinski_harabasz_score')}, Sizes: {k2.get('cluster_sizes')}")

print('\n=== K=4 SOLUTION ===')
k4 = c.get('k4_solution', {})
print(f"Silhouette: {k4.get('silhouette_score')}, DB: {k4.get('davies_bouldin_index')}, CH: {k4.get('calinski_harabasz_score')}, Sizes: {k4.get('cluster_sizes')}")

print('\n=== PCA VARIANCE ===')
print(f"PC1: {c.get('pca_explained_variance_ratio')[0]:.4f} ({c.get('pca_explained_variance_ratio')[0]*100:.2f}%)")
print(f"PC2: {c.get('pca_explained_variance_ratio')[1]:.4f} ({c.get('pca_explained_variance_ratio')[1]*100:.2f}%)")
print(f"Total: {c.get('pca_total_variance_explained'):.4f} ({c.get('pca_total_variance_explained')*100:.2f}%)")

with open('data/reports/association_rules_report_v2.json', 'r') as f:
    a = json.load(f)

print('\n=== ASSOCIATION RULES ===')
print('Mode A (Visual only):', a.get('visual_feature_rules_summary', {}).get('total_rules_generated'))
print('Mode A itemsets:', a.get('visual_feature_rules_summary', {}).get('total_frequent_itemsets'))
print('Mode A baseline thresholds:', a.get('visual_feature_rules_summary', {}).get('baseline_support'), a.get('visual_feature_rules_summary', {}).get('baseline_confidence'))

with open('data/reports/supervised_classification_feasibility.json', 'r') as f:
    s = json.load(f)

print('\n=== SUPERVISED CLASSIFICATION FEASIBILITY ===')
print('Verdict:', s.get('scientific_verdict'))
print('Total specimens:', s.get('dataset_total_specimens'))
print('Single condition crops:', s.get('single_condition_crops'))
print('Rare disease classes (<20):', s.get('rare_disease_classes_below_20'))
