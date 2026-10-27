import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import time
import statistics
import pandas as pd
from src.mining.association_rules import VisualAssociationMiner

miner = VisualAssociationMiner(min_support=0.15, min_confidence=0.60)
df_disc, bin_meta = miner.load_and_discretize()

print("Loaded 2,596 transactions.")
print(f"Mode A transaction matrix: {miner.df_transactions_visual.shape} ({miner.df_transactions_visual.shape[1]} unique items)")
print(f"Mode B transaction matrix: {miner.df_transactions_labeled.shape} ({miner.df_transactions_labeled.shape[1]} unique items)")

def run_benchmark(mode, n_runs=10):
    print(f"\n==========================================")
    print(f"BENCHMARKING: {mode.upper()} (Runs = {n_runs})")
    print(f"==========================================")
    
    fp_times, ap_times = [], []
    fp_itemsets, fp_rules = None, None
    ap_itemsets, ap_rules = None, None
    
    for i in range(n_runs):
        t0 = time.perf_counter()
        cur_fp_is, cur_fp_r, _ = miner.mine_patterns(mode=mode, algorithm="fpgrowth", min_support=0.15, min_confidence=0.60)
        fp_times.append(time.perf_counter() - t0)
        if i == 0:
            fp_itemsets, fp_rules = cur_fp_is, cur_fp_r
            
        t0 = time.perf_counter()
        cur_ap_is, cur_ap_r, _ = miner.mine_patterns(mode=mode, algorithm="apriori", min_support=0.15, min_confidence=0.60)
        ap_times.append(time.perf_counter() - t0)
        if i == 0:
            ap_itemsets, ap_rules = cur_ap_is, cur_ap_r

    print(f"FP-Growth median runtime: {statistics.median(fp_times):.4f}s (min: {min(fp_times):.4f}s, max: {max(fp_times):.4f}s)")
    print(f"Apriori median runtime:   {statistics.median(ap_times):.4f}s (min: {min(ap_times):.4f}s, max: {max(ap_times):.4f}s)")
    print(f"FP-Growth frequent itemsets count: {len(fp_itemsets)}")
    print(f"Apriori frequent itemsets count:   {len(ap_itemsets)}")
    print(f"FP-Growth total rules generated:   {len(fp_rules)}")
    print(f"Apriori total rules generated:     {len(ap_rules)}")
    
    # Filter by lift >= 1.0
    fp_rules_lift1 = fp_rules[fp_rules['lift'] >= 1.0] if not fp_rules.empty else pd.DataFrame()
    ap_rules_lift1 = ap_rules[ap_rules['lift'] >= 1.0] if not ap_rules.empty else pd.DataFrame()
    print(f"Rules with lift >= 1.0: {len(fp_rules_lift1)} (FP-Growth), {len(ap_rules_lift1)} (Apriori)")

    # Parity check
    fp_is_map = {frozenset(row["itemsets"]): float(row["support"]) for _, row in fp_itemsets.iterrows()}
    ap_is_map = {frozenset(row["itemsets"]): float(row["support"]) for _, row in ap_itemsets.iterrows()}
    itemsets_match = set(fp_is_map.keys()) == set(ap_is_map.keys())
    max_is_diff = max(abs(fp_is_map[k] - ap_is_map[k]) for k in fp_is_map) if itemsets_match and fp_is_map else -1.0
    
    def r_key(row):
        return (frozenset(row["antecedents"]), frozenset(row["consequents"]))
    fp_r_map = {r_key(row): (float(row["support"]), float(row["confidence"]), float(row["lift"])) for _, row in fp_rules.iterrows()}
    ap_r_map = {r_key(row): (float(row["support"]), float(row["confidence"]), float(row["lift"])) for _, row in ap_rules.iterrows()}
    rules_match = set(fp_r_map.keys()) == set(ap_r_map.keys())
    
    max_supp_diff = max(abs(fp_r_map[k][0] - ap_r_map[k][0]) for k in fp_r_map) if rules_match and fp_r_map else -1.0
    max_conf_diff = max(abs(fp_r_map[k][1] - ap_r_map[k][1]) for k in fp_r_map) if rules_match and fp_r_map else -1.0
    max_lift_diff = max(abs(fp_r_map[k][2] - ap_r_map[k][2]) for k in fp_r_map) if rules_match and fp_r_map else -1.0

    print(f"Itemset set match: {itemsets_match}, Max Support Diff: {max_is_diff}")
    print(f"Rule set match:    {rules_match}")
    print(f"Max Rule Diff -> Supp: {max_supp_diff}, Conf: {max_conf_diff}, Lift: {max_lift_diff}")

run_benchmark("visual_only")
run_benchmark("labeled")
