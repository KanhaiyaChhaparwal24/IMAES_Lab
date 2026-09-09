"""
LAB5 — Backward Chaining Inference Engine
Roll No : U23AI103
Course  : AI401 — Intelligent Multi-Agent and Expert Systems, Semester VII
Experiment: 5 — Goal-Driven Reasoning for Car-Fault Diagnosis
"""

# ─────────────────────────────────────────────
# KNOWLEDGE BASE
# Each rule: { 'id', 'hypothesis', 'conditions', 'description' }
# ─────────────────────────────────────────────
RULES = [
    {
        'id': 'R1',
        'hypothesis': 'flat_battery',
        'label': 'flat battery',
        'conditions': ['battery_flat', 'lights_dim'],
        'description': 'A flat battery causes dim lights and failure to start.',
    },
    {
        'id': 'R2',
        'hypothesis': 'bad_connection',
        'label': 'bad connection',
        'conditions': ['battery_ok', 'connections_loose'],
        'description': 'Battery is fine but a loose connection prevents proper current flow.',
    },
    {
        'id': 'R3',
        'hypothesis': 'out_of_fuel',
        'label': 'out of fuel',
        'conditions': ['fuel_empty', 'engine_cranks'],
        'description': 'Tank is empty; the engine cranks but never fires.',
    },
    # Exercise 1 — Starter motor fault
    {
        'id': 'R4',
        'hypothesis': 'starter_motor_fault',
        'label': 'starter motor fault',
        'conditions': ['clicking_sound', 'engine_not_cranking'],
        'description': 'A single click with no crank points to a faulty starter motor.',
    },
]

# Human-friendly questions for each fact
QUESTIONS = {
    'battery_flat':       'Is the battery flat (voltmeter reads below 12 V)?',
    'lights_dim':         'Are the headlights dim or flickering?',
    'battery_ok':         'Is the battery charged and showing a good voltage (12 V+)?',
    'connections_loose':  'Are any battery or ignition connections loose or corroded?',
    'fuel_empty':         'Is the fuel tank empty (fuel gauge on E)?',
    'engine_cranks':      'Does the engine crank (turn over) when you turn the key?',
    'clicking_sound':     'Do you hear a single loud click when you turn the key?',
    'engine_not_cranking':'Does the engine completely fail to crank at all?',
}


# ─────────────────────────────────────────────
# BACKWARD CHAINING ENGINE
# ─────────────────────────────────────────────
def ask_fact(fact, hypothesis_label, rule):
    """
    Ask the user about a single fact.
    Supports 'yes', 'no', and 'why'.
    Returns True (yes) or False (no).
    """
    question = QUESTIONS.get(fact, f'Is {fact} true?')
    while True:
        answer = input(f'  Q: {question}   (yes/no/why): ').strip().lower()
        if answer in ('yes', 'y'):
            return True
        elif answer in ('no', 'n'):
            return False
        elif answer == 'why':
            print(f'\n  WHY: Asking about [{fact.replace("_", " ")}]')
            print(f'       to prove   : [{hypothesis_label}]')
            print(f'       Rule {rule["id"]}    : {rule["description"]}\n')
        else:
            print('  Please answer yes, no, or why.')


def backward_chain(rules):
    """
    Try each hypothesis in order (Exercise 2 — order matters).
    Return the first hypothesis that succeeds, or None.
    """
    fact_cache = {}          # Fact caching — answered once, reused
    facts_asked = []         # Track order of facts queried

    for rule in rules:
        print(f'\n-- Trying: [{rule["label"]}] --')
        hypothesis_proved = True

        for fact in rule['conditions']:
            # Use cached answer if available (no re-ask)
            if fact in fact_cache:
                result = fact_cache[fact]
                print(f'  (cached) {fact.replace("_", " ")}: {"yes" if result else "no"}')
            else:
                result = ask_fact(fact, rule['label'], rule)
                fact_cache[fact] = result
                facts_asked.append(fact)

            # Short-circuit — if any condition fails, skip rest of this rule
            if not result:
                hypothesis_proved = False
                break

        if hypothesis_proved:
            return rule, facts_asked

    return None, facts_asked


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print('=' * 55)
    print('  CAR FAULT DIAGNOSIS — Backward Chaining Engine')
    print('=' * 55)
    print('Answer each question with:  yes / no / why')
    print('  why  →  shows the rule driving the current question')
    print('-' * 55)

    # ── Exercise 2: Change hypothesis order here to observe different question sequences ──
    # Default order: R1 → R2 → R3 → R4
    # Try swapping, e.g., start with R2 to see battery_ok asked first.
    ordered_rules = RULES  # swap to e.g. [RULES[1], RULES[0], RULES[2], RULES[3]]

    matched_rule, facts_asked = backward_chain(ordered_rules)

    print('\n' + '=' * 55)
    if matched_rule:
        print(f'  DIAGNOSIS  : {matched_rule["label"].upper()}')
        print(f'  Rule fired : {matched_rule["id"]}')
        print(f'  Facts asked: {facts_asked}')
    else:
        print('  DIAGNOSIS  : UNKNOWN FAULT')
        print('  No hypothesis could be proved with the given answers.')
        print(f'  Facts asked: {facts_asked}')
    print('=' * 55)


if __name__ == '__main__':
    main()
