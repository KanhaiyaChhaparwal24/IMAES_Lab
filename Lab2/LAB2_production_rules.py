"""
Experiment 2: Production Rules and the Match Phase
Roll No: U23AI103
"""

import time

# ─────────────────────────────────────────────────────────────
# SECTION 1: Rule Base and Working Memory
# ─────────────────────────────────────────────────────────────

# Each rule: id, list of IF-conditions, THEN-conclusion
RULES = [
    {"id": "R1", "conditions": ["symptom_fever", "symptom_cough"],          "conclusion": "suspect_flu"},
    {"id": "R2", "conditions": ["suspect_flu", "symptom_sore_throat"],       "conclusion": "diagnose_flu"},
    {"id": "R3", "conditions": ["diagnose_flu"],                             "conclusion": "prescribe_antiviral"},
    {"id": "R4", "conditions": ["symptom_fever", "symptom_rash"],            "conclusion": "suspect_infection"},
    {"id": "R5", "conditions": ["symptom_cough", "symptom_shortness_of_breath"], "conclusion": "suspect_pneumonia"},
    {"id": "R6", "conditions": ["suspect_pneumonia"],                        "conclusion": "order_chest_xray"},
]

# Working memory: set of currently known facts
working_memory = {"symptom_fever", "symptom_cough", "symptom_sore_throat"}


# ─────────────────────────────────────────────────────────────
# SECTION 2: Match Phase (Core Algorithm)
# ─────────────────────────────────────────────────────────────

def match(rules, wm):
    """
    Returns the conflict set: rules whose conditions are ALL in WM
    and whose conclusion is NOT already in WM (refractoriness check).
    """
    conflict_set = []
    for rule in rules:
        conditions_met = all(cond in wm for cond in rule["conditions"])
        not_refractory = rule["conclusion"] not in wm
        if conditions_met and not_refractory:
            conflict_set.append(rule)
    return conflict_set


def display_conflict_set(cs, wm):
    print(f"\nWorking Memory : {sorted(wm)}")
    print(f"Conflict Set   : {[r['id'] for r in cs]}")
    for rule in cs:
        print(f"  {rule['id']}: IF {rule['conditions']} -> {rule['conclusion']}")


# ─────────────────────────────────────────────────────────────
# SECTION 3: Exercise 1 — Add facts one at a time
# ─────────────────────────────────────────────────────────────

print("=" * 60)
print("EXERCISE 1: Adding facts one at a time")
print("=" * 60)

wm_ex1 = set()
facts_to_add = [
    "symptom_fever",
    "symptom_cough",
    "symptom_sore_throat",
    "suspect_flu",       # simulating a fact derived earlier
]

for fact in facts_to_add:
    wm_ex1.add(fact)
    cs = match(RULES, wm_ex1)
    print(f"\n[+] Added: {fact}")
    display_conflict_set(cs, wm_ex1)


# ─────────────────────────────────────────────────────────────
# SECTION 4: Exercise 2 — Negated conditions (NOT)
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("EXERCISE 2: Negated conditions (NOT)")
print("=" * 60)

NEG_RULES = [
    {
        "id": "N1",
        "conditions": ["fever"],
        "negations": [],
        "conclusion": "start_assessment",
    },
    {
        "id": "N2",
        "conditions": ["fever"],
        "negations": ["antibiotics_taken"],   # NOT antibiotics_taken
        "conclusion": "prescribe_antibiotics",
    },
    {
        "id": "N3",
        "conditions": ["fever", "antibiotics_taken"],
        "negations": ["allergy_penicillin"],  # NOT allergy_penicillin
        "conclusion": "continue_amoxicillin",
    },
    {
        "id": "N4",
        "conditions": ["fever"],
        "negations": ["on_treatment"],        # NOT on_treatment
        "conclusion": "escalate_care",
    },
]


def match_with_negation(rules, wm):
    """Extended matcher: supports positive AND negated conditions."""
    conflict_set = []
    for rule in rules:
        pos_met = all(c in wm for c in rule["conditions"])
        neg_met = all(c not in wm for c in rule.get("negations", []))
        not_refractory = rule["conclusion"] not in wm
        if pos_met and neg_met and not_refractory:
            conflict_set.append(rule)
    return conflict_set


scenarios = [
    {"label": "Only fever",                   "wm": {"fever"}},
    {"label": "fever + antibiotics_taken",    "wm": {"fever", "antibiotics_taken"}},
    {"label": "fever + antibiotics + allergy","wm": {"fever", "antibiotics_taken", "allergy_penicillin"}},
    {"label": "fever + on_treatment",         "wm": {"fever", "on_treatment"}},
]

for s in scenarios:
    cs = match_with_negation(NEG_RULES, s["wm"])
    print(f"\nScenario: {s['label']}")
    print(f"  WM             : {sorted(s['wm'])}")
    print(f"  Conflict Set   : {[r['id'] for r in cs]}")
    for r in cs:
        negs = [f"NOT {n}" for n in r.get("negations", [])]
        cond_str = " AND ".join(r["conditions"] + negs)
        print(f"    {r['id']}: IF {cond_str} -> {r['conclusion']}")


# ─────────────────────────────────────────────────────────────
# SECTION 5: Exercise 3 — Match time vs scale (RETE motivation)
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("EXERCISE 3: Match time vs rule-base size")
print("=" * 60)


def generate_rules(n):
    """Auto-generate n rules with 2-3 conditions each."""
    rules = []
    for i in range(n):
        num_conds = 2 + (i % 2)
        conds = [f"fact_{(i * j + j) % max(n, 10)}" for j in range(num_conds)]
        rules.append({"id": f"R{i}", "conditions": conds, "conclusion": f"conc_{i}"})
    return rules


def naive_match(rules, wm):
    return [r for r in rules if all(c in wm for c in r["conditions"]) and r["conclusion"] not in wm]


wm_bench = {f"fact_{i}" for i in range(0, 20, 2)}   # 10 facts
sizes = [10, 100, 500, 1000]

print(f"\n{'Rules':>8} | {'Avg time (ms)':>14} | {'Checks':>10} | {'Matched':>8}")
print("-" * 50)

for n in sizes:
    rules = generate_rules(n)
    avg_conditions = sum(len(r["conditions"]) for r in rules) / len(rules)
    total_checks = n * avg_conditions

    trials = 5
    times = []
    for _ in range(trials):
        t0 = time.perf_counter()
        for _ in range(100):            # 100 match cycles
            naive_match(rules, wm_bench)
        times.append((time.perf_counter() - t0) * 1000)

    avg_ms = sum(times) / trials / 100  # per cycle
    matched = len(naive_match(rules, wm_bench))
    print(f"{n:>8} | {avg_ms:>14.4f} | {int(total_checks):>10} | {matched:>8}")

print("""
Observation:
  Match time grows linearly with rule count — O(R × C) per cycle.
  RETE compiles rules into a discrimination network and recomputes
  only affected nodes when WM changes, reducing incremental cost
  from O(R × C) to approximately O(delta_facts × affected_nodes).
""")
