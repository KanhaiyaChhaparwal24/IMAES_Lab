"""
AI401 — Expert Systems Lab
Experiment 7: Logical and Probabilistic Reasoning
Roll No: U23AI103

Exercises:
1. Propositional Logic truth table
2. First-Order Logic derivation
3. Probability of events
4. Conditional probability
5. Bayes' theorem
6. Visualization with Matplotlib
"""

import matplotlib.pyplot as plt

# ============================================================
# 1. PROPOSITIONAL LOGIC
# Rule: If it rains, then the road is wet.
#       P -> Q
# ============================================================

def implication(p, q):
    return (not p) or q

def propositional_logic():
    rows = []
    for rains in [False, True]:
        for wet in [False, True]:
            rows.append((rains, wet, implication(rains, wet)))

    print("=" * 70)
    print("1. PROPOSITIONAL LOGIC")
    print("=" * 70)
    print("Rule: If it rains, then the road is wet.  (P -> Q)")
    print("\nRains(P) | Wet(Q) | P -> Q")
    print("-" * 30)
    for p, q, r in rows:
        print(f"{str(p):8} | {str(q):6} | {str(r):6}")
    print("\nObservation: implication is false only when it rains but the road is not wet.")
    return rows


# ============================================================
# 2. FIRST-ORDER LOGIC
# All humans are mortal.
# Socrates is a human.
# Therefore Socrates is mortal.
# ============================================================

def fol_reasoning():
    humans = {"Socrates"}
    mortal = set()

    rule = "Human(x) -> Mortal(x)"

    for person in humans:
        if person in humans:
            mortal.add(person)

    result = "Mortal(Socrates)" in {f"Mortal({x})" for x in mortal}

    print("\n" + "=" * 70)
    print("2. FIRST-ORDER LOGIC")
    print("=" * 70)
    print("Facts:")
    print("  Human(Socrates)")
    print("Rule:")
    print("  ∀x Human(x) -> Mortal(x)")
    print("Derived:")
    print("  Mortal(Socrates)" if result else "  Cannot derive Mortal(Socrates)")
    return result


# ============================================================
# 3 & 4. PROBABILITY AND CONDITIONAL PROBABILITY
#
# Dataset:
# 100 students
# A = student passed
# B = student attended
#
# Passed & attended = 70
# Passed & did not attend = 10
# Failed & attended = 10
# Failed & did not attend = 10
# ============================================================

TOTAL = 100
PASSED_ATTENDED = 70
PASSED_NOT_ATTENDED = 10
FAILED_ATTENDED = 10
FAILED_NOT_ATTENDED = 10

def probability_experiment():
    passed = PASSED_ATTENDED + PASSED_NOT_ATTENDED
    attended = PASSED_ATTENDED + FAILED_ATTENDED

    p_passed = passed / TOTAL
    p_attended = attended / TOTAL

    p_passed_and_attended = PASSED_ATTENDED / TOTAL
    p_passed_or_attended = p_passed + p_attended - p_passed_and_attended

    p_passed_given_attended = PASSED_ATTENDED / attended
    p_attended_given_passed = PASSED_ATTENDED / passed

    print("\n" + "=" * 70)
    print("3 & 4. PROBABILITY AND CONDITIONAL PROBABILITY")
    print("=" * 70)
    print("Dataset:")
    print("  Passed & attended       =", PASSED_ATTENDED)
    print("  Passed & not attended   =", PASSED_NOT_ATTENDED)
    print("  Failed & attended       =", FAILED_ATTENDED)
    print("  Failed & not attended   =", FAILED_NOT_ATTENDED)

    print("\nIndividual probabilities:")
    print(f"  P(Passed)   = {passed}/{TOTAL} = {p_passed:.2f}")
    print(f"  P(Attended) = {attended}/{TOTAL} = {p_attended:.2f}")

    print("\nJoint probability:")
    print(f"  P(Passed AND Attended) = {PASSED_ATTENDED}/{TOTAL} = {p_passed_and_attended:.2f}")

    print("\nUnion probability:")
    print(f"  P(Passed OR Attended) = P(Passed)+P(Attended)-P(Both)")
    print(f"                        = {p_passed:.2f}+{p_attended:.2f}-{p_passed_and_attended:.2f}")
    print(f"                        = {p_passed_or_attended:.2f}")

    print("\nConditional probabilities:")
    print(f"  P(Passed | Attended) = {PASSED_ATTENDED}/{attended} = {p_passed_given_attended:.2f}")
    print(f"  P(Attended | Passed) = {PASSED_ATTENDED}/{passed} = {p_attended_given_passed:.2f}")

    return {
        "P(Passed)": p_passed,
        "P(Attended)": p_attended,
        "P(Passed AND Attended)": p_passed_and_attended,
        "P(Passed OR Attended)": p_passed_or_attended,
        "P(Passed | Attended)": p_passed_given_attended,
        "P(Attended | Passed)": p_attended_given_passed,
    }


# ============================================================
# 5. BAYES' THEOREM
#
# Disease prevalence = 1%
# Sensitivity P(Positive | Disease) = 95%
# False positive rate P(Positive | No Disease) = 5%
#
# P(D|+) = P(+|D)P(D) / P(+)
# ============================================================

def bayes_example():
    p_disease = 0.01
    p_positive_given_disease = 0.95
    p_positive_given_no_disease = 0.05
    p_no_disease = 1 - p_disease

    p_positive = (
        p_positive_given_disease * p_disease
        + p_positive_given_no_disease * p_no_disease
    )

    posterior = (
        p_positive_given_disease * p_disease / p_positive
    )

    print("\n" + "=" * 70)
    print("5. BAYES' THEOREM")
    print("=" * 70)
    print("P(Disease) = 0.01")
    print("P(Positive | Disease) = 0.95")
    print("P(Positive | No Disease) = 0.05")

    print(f"\nP(Positive) = (0.95)(0.01) + (0.05)(0.99)")
    print(f"            = {p_positive:.4f}")

    print(f"\nP(Disease | Positive) = (0.95 × 0.01) / {p_positive:.4f}")
    print(f"                      = {posterior:.4f}")
    print(f"                      = {posterior * 100:.2f}%")

    return posterior


# ============================================================
# 6. VISUALIZATION
# Plot calculated probabilities and show effect of modifying
# the prior disease probability.
# ============================================================

def visualization(original_posterior):
    priors = [0.01, 0.02, 0.05, 0.10]
    sensitivity = 0.95
    false_positive = 0.05

    posteriors = []
    for prior in priors:
        positive = sensitivity * prior + false_positive * (1 - prior)
        post = sensitivity * prior / positive
        posteriors.append(post)

    labels = [f"{p*100:.0f}%" for p in priors]

    plt.figure(figsize=(8, 5))
    plt.plot(labels, [x * 100 for x in posteriors], marker="o")
    plt.xlabel("Disease prior probability")
    plt.ylabel("P(Disease | Positive) (%)")
    plt.title("Bayesian Diagnosis: Effect of Prior Probability")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("/mnt/data/LAB_7_U23AI103_probability_plot.png", dpi=150)
    plt.close()

    print("\n" + "=" * 70)
    print("6. VISUALIZATION")
    print("=" * 70)
    print("Prior disease probability -> Posterior disease probability after positive test")
    for p, post in zip(priors, posteriors):
        print(f"  {p*100:5.1f}% -> {post*100:6.2f}%")

    print("\nOriginal input: prior = 1%")
    print(f"Original posterior = {original_posterior*100:.2f}%")
    print("The graph shows that changing the prior probability changes the posterior probability.")

    return priors, posteriors


def main():
    propositional_logic()
    fol_reasoning()
    probs = probability_experiment()
    posterior = bayes_example()
    visualization(posterior)

    print("\n" + "=" * 70)
    print("FINAL OBSERVATIONS")
    print("=" * 70)
    print("1. Propositional logic can verify an implication using a truth table.")
    print("2. First-Order Logic can derive Mortal(Socrates) from Human(Socrates) and the rule Human(x)->Mortal(x).")
    print("3. Probability measures how likely an event is.")
    print("4. Joint probability measures two events happening together.")
    print("5. Union probability measures the chance that at least one of two events occurs.")
    print("6. Conditional probability changes the probability after additional information is known.")
    print("7. Bayes' theorem updates a prior belief using evidence.")
    print("8. Changing the prior probability changes the posterior probability, as shown in the graph.")


if __name__ == "__main__":
    main()
