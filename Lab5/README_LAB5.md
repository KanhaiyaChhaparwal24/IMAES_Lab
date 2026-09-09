# LAB5 — Backward Chaining Inference Engine

**Roll No:** U23AI103

---

## How to Run

```bash
python3 LAB5_backward_chaining.py
```

Answer each prompt with `yes`, `no`, or `why`.  
`why` prints the rule currently driving the question.

---

## Knowledge Base (4 rules)

| Rule | Hypothesis          | Conditions                             |
| ---- | ------------------- | -------------------------------------- |
| R1   | flat_battery        | battery_flat AND lights_dim            |
| R2   | bad_connection      | battery_ok AND connections_loose       |
| R3   | out_of_fuel         | fuel_empty AND engine_cranks           |
| R4   | starter_motor_fault | clicking_sound AND engine_not_cranking |

---

## Sample Sessions

### Base case — Flat battery

```
-- Trying: [flat battery] --
  Q: Is the battery flat (voltmeter reads below 12 V)?   A: yes
  Q: Are the headlights dim or flickering?               A: yes

  DIAGNOSIS  : FLAT BATTERY
  Rule fired : R1
  Facts asked: ['battery_flat', 'lights_dim']
```

### Exercise 1 — Starter motor fault

```
-- Trying: [flat battery] --      Q: battery_flat?         A: no
-- Trying: [bad connection] --    Q: battery_ok?           A: no
-- Trying: [out of fuel] --       Q: fuel_empty?           A: no
-- Trying: [starter motor fault] --
  Q: Do you hear a single click?                          A: yes
  Q: Does the engine fail to crank at all?                A: yes

  DIAGNOSIS  : STARTER MOTOR FAULT
  Rule fired : R4
  Facts asked: ['battery_flat','battery_ok','fuel_empty','clicking_sound','engine_not_cranking']
```

### Exercise 2 — Reordered hypotheses (bad_connection tried first)

```
-- Trying: [bad connection] --    Q: battery_ok?           A: no  (fails → skip)
-- Trying: [flat battery] --      Q: battery_flat?         A: yes
                                  Q: lights_dim?           A: yes

  DIAGNOSIS  : FLAT BATTERY
  Facts asked: ['battery_ok', 'battery_flat', 'lights_dim']
  Observation: battery_ok is now asked FIRST, changing question order.
```

### Exercise 3 — WHY option

```
-- Trying: [flat battery] --
  Q: Is the battery flat?    A: why

  WHY: Asking about [battery flat]
       to prove: [flat battery]
       Rule R1: A flat battery causes dim lights and failure to start.

  Q: Is the battery flat?    A: yes
  Q: Are the headlights dim? A: yes

  DIAGNOSIS  : FLAT BATTERY
```

---

## Key Observations

1. **Goal-driven** — only facts needed to prove the current hypothesis are asked; irrelevant facts are never queried.
2. **Short-circuit** — if the first condition of a hypothesis fails, remaining conditions are skipped immediately.
3. **Hypothesis order matters** — whichever hypothesis is listed first is tried first, changing which questions the user sees.
4. **WHY transparency** — the `why` option shows exactly which rule is driving the question and what it is trying to prove.
5. **Fact caching** — a fact answered once is reused across hypotheses without re-asking.
