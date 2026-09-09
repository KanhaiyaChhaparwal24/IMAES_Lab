"""
Experiment 4: Forward Chaining Inference Engine — ZOOKEEPER
Roll No : U23AI103
Course  : AI401 — Intelligent Multi-Agent and Expert Systems, Semester VII
"""

# ─────────────────────────────────────────────────────────────────────────────
# KNOWLEDGE BASE  —  12 production rules
# ─────────────────────────────────────────────────────────────────────────────

RULES = [
    # Class rules
    {"id": "R1",  "ifs": ["has_hair"],                                              "then": "is_mammal"},
    {"id": "R2",  "ifs": ["gives_milk"],                                            "then": "is_mammal"},
    {"id": "R3",  "ifs": ["has_feathers"],                                          "then": "is_bird"},
    # Specialisation rules
    {"id": "R4",  "ifs": ["is_mammal", "has_claws", "has_pointed_teeth",
                           "has_forward_eyes"],                                      "then": "is_carnivore"},
    {"id": "R5",  "ifs": ["is_mammal", "eats_meat"],                               "then": "is_carnivore"},
    # Animal identification rules
    {"id": "R6",  "ifs": ["is_mammal", "is_carnivore",
                           "has_tawny_color", "has_dark_spots"],                    "then": "is_cheetah"},
    {"id": "R7",  "ifs": ["is_mammal", "is_carnivore",
                           "has_tawny_color", "has_black_stripes"],                 "then": "is_tiger"},
    {"id": "R8",  "ifs": ["is_mammal", "has_long_neck",
                           "has_long_legs",  "has_dark_spots"],                     "then": "is_giraffe"},
    {"id": "R9",  "ifs": ["is_mammal", "has_black_stripes"],                       "then": "is_zebra"},
    {"id": "R10", "ifs": ["is_bird", "does_not_fly",
                           "has_long_neck", "has_long_legs"],                       "then": "is_ostrich"},
    {"id": "R11", "ifs": ["is_bird", "does_not_fly",
                           "swims", "is_black_and_white"],                          "then": "is_penguin"},
    {"id": "R12", "ifs": ["is_bird", "flies_well"],                                "then": "is_albatross"},
]

ANIMAL_FACTS = {
    "is_cheetah", "is_tiger", "is_giraffe", "is_zebra",
    "is_ostrich", "is_penguin", "is_albatross",
}


# ─────────────────────────────────────────────────────────────────────────────
# CORE ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def match(rules, wm):
    """Return conflict set: rules whose conditions are met and conclusion is new."""
    return [r for r in rules
            if all(c in wm for c in r["ifs"]) and r["then"] not in wm]


def forward_chain(initial_facts, rules=RULES, fire_all=False, verbose=True):
    """
    Run the forward chaining cycle.
    fire_all=False → fire the FIRST rule in the conflict set (rule-order priority).
    fire_all=True  → fire ALL rules in the conflict set each cycle (Exercise 3).
    Returns (final_wm, firing_sequence, identified_animals).
    """
    wm = set(initial_facts)
    fired = []

    if verbose:
        print(f"Initial WM : {sorted(wm)}\n")

    cycle = 1
    while True:
        cs = match(rules, wm)
        if not cs:
            break

        if fire_all:
            # Exercise 3: fire every applicable rule this cycle
            ids = [r["id"] for r in cs]
            if verbose:
                print(f"Cycle {cycle}: fire ALL {ids}")
            for r in cs:
                wm.add(r["then"])
                fired.append(r["id"])
        else:
            # Default: fire first rule
            rule = cs[0]
            wm.add(rule["then"])
            fired.append(rule["id"])
            if verbose:
                print(f"Cycle {cycle}: fire {rule['id']:<4}  +{rule['then']}")
                print(f"          Conflict set : {[r['id'] for r in cs]}")
        cycle += 1

    animals = sorted(wm & ANIMAL_FACTS)
    if verbose:
        print(f"\nFiring sequence    : {' -> '.join(fired)}")
        print(f"Final WM           : {sorted(wm)}")
        print(f"Animal identified  : {animals if animals else 'None'}")
        if not animals:
            classes = sorted(f for f in wm if f.startswith("is_"))
            print(f"Most specific class: {classes}")
    return wm, fired, animals


# ─────────────────────────────────────────────────────────────────────────────
# BASE CASE — cheetah
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 60)
print("BASE CASE: cheetah identification")
print("=" * 60)
forward_chain({
    "has_hair", "gives_milk",
    "has_claws", "has_pointed_teeth", "has_forward_eyes",
    "has_tawny_color", "has_dark_spots",
})

# ─────────────────────────────────────────────────────────────────────────────
# EXERCISE 1 — tiger, giraffe, zebra
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("EXERCISE 1a: tiger")
print("=" * 60)
forward_chain({
    "has_hair",
    "has_claws", "has_pointed_teeth", "has_forward_eyes",
    "has_tawny_color", "has_black_stripes",
})

print("\n" + "=" * 60)
print("EXERCISE 1b: giraffe  (long neck, long legs, dark spots)")
print("=" * 60)
forward_chain({
    "has_hair",
    "has_long_neck", "has_long_legs", "has_dark_spots",
})

print("\n" + "=" * 60)
print("EXERCISE 1c: zebra  (black stripes, not carnivore)")
print("=" * 60)
forward_chain({
    "gives_milk",
    "has_black_stripes",
})

# ─────────────────────────────────────────────────────────────────────────────
# EXERCISE 2 — no identification; report most specific class
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("EXERCISE 2: facts satisfy no animal rule — report best class")
print("=" * 60)
forward_chain({
    "has_hair", "gives_milk",
})

# ─────────────────────────────────────────────────────────────────────────────
# EXERCISE 3 — fire ALL rules per cycle; compare sequences
# ─────────────────────────────────────────────────────────────────────────────

CHEETAH_FACTS = {
    "has_hair", "gives_milk",
    "has_claws", "has_pointed_teeth", "has_forward_eyes",
    "has_tawny_color", "has_dark_spots",
}

print("\n" + "=" * 60)
print("EXERCISE 3a: fire FIRST rule per cycle (default)")
print("=" * 60)
_, seq1, _ = forward_chain(CHEETAH_FACTS, fire_all=False)

print("\n" + "=" * 60)
print("EXERCISE 3b: fire ALL rules per cycle")
print("=" * 60)
_, seq2, _ = forward_chain(CHEETAH_FACTS, fire_all=True)

print("\n── Comparison ──")
print(f"  First-rule sequence : {' -> '.join(seq1)}")
print(f"  All-rules  sequence : {' -> '.join(seq2)}")
print(f"  Same result? {'Yes' if set(seq1)==set(seq2) else 'No — order differs'}")
print("  R2 fires in all-rules mode because R1+R2 are both applicable in cycle 1.")
print("  In first-rule mode R2 is pre-empted by R1 reaching 'is_mammal' first.")
