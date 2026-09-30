# Experiment 6: Fuzzy Logic and Constraint Satisfaction
# Roll No: U23AI103

from itertools import product

# ---------- Fuzzy Logic ----------

def left(x, a, b):
    if x <= a: return 1.0
    if x >= b: return 0.0
    return (b-x)/(b-a)

def right(x, a, b):
    if x <= a: return 0.0
    if x >= b: return 1.0
    return (x-a)/(b-a)

def tri(x, a, b, c):
    if x <= a or x >= c: return 0.0
    if x == b: return 1.0
    if x < b: return (x-a)/(b-a)
    return (c-x)/(c-b)

def fuzzify(att, marks):
    return {
        "attendance": {
            "low": left(att,50,70),
            "medium": tri(att,50,75,95),
            "high": right(att,75,95)},
        "marks": {
            "low": left(marks,40,60),
            "medium": tri(marks,40,65,85),
            "high": right(marks,65,85)}
    }

RULES = [
    ("low","low","poor"), ("low","medium","poor"),
    ("low","high","average"), ("medium","low","average"),
    ("medium","medium","average"), ("medium","high","good"),
    ("high","low","average"), ("high","medium","good"),
    ("high","high","excellent")
]
SCORE = {"poor":25, "average":50, "good":75, "excellent":95}

def fuzzy(att, marks, rules=RULES):
    m = fuzzify(att, marks)
    out = {}
    for a,b,c in rules:
        strength = min(m["attendance"][a], m["marks"][b])
        out[c] = max(out.get(c,0), strength)
    den = sum(out.values())
    score = sum(SCORE[k]*v for k,v in out.items())/den if den else 0
    category = "Poor" if score < 37.5 else "Average" if score < 62.5 else "Good" if score < 85 else "Excellent"
    return m, out, score, category

def exercise1():
    print("="*65)
    print("EXERCISE 1 - FUZZY STUDENT PERFORMANCE")
    print("="*65)
    cases = [
        ("Low attendance + low marks",50,35),
        ("Medium attendance + medium marks",75,65),
        ("High attendance + high marks",95,90),
        ("Low attendance + high marks",55,90),
        ("High attendance + low marks",95,45)]
    for name,a,mk in cases:
        mem, rules, score, cat = fuzzy(a,mk)
        print("\n",name)
        print(" Attendance:",a,"%  Marks:",mk,"%")
        print(" Memberships:", {k:{x:round(y,2) for x,y in v.items()} for k,v in mem.items()})
        print(" Rule strengths:", {k:round(v,2) for k,v in rules.items() if v})
        print(" Score:",round(score,2)," Category:",cat)

# ---------- CSP Timetable ----------

DAYS=["Mon","Tue","Wed"]
SLOTS=["9-10","10-11","11-12"]
COURSES=["AI","DBMS","OS","NLP"]

def idx(x):
    return DAYS.index(x[0])*3 + SLOTS.index(x[1])

def valid(t):
    if len(set(t.values())) != 4: return False
    if t["AI"][0] == t["DBMS"][0]: return False
    if idx(t["OS"]) >= idx(t["NLP"]): return False
    if t["AI"] == ("Mon","9-10"): return False
    return True

def solve(extra=False):
    domain=list(product(DAYS,SLOTS))
    for vals in product(domain, repeat=4):
        t=dict(zip(COURSES,vals))
        if extra:
            # Changed constraint: AI and DBMS may be on the same day.
            if len(set(t.values())) != 4: continue
            if idx(t["OS"]) >= idx(t["NLP"]): continue
            if t["AI"] == ("Mon","9-10"): continue
            return t
        if valid(t): return t

def exercise2():
    print("\n"+"="*65)
    print("EXERCISE 2 - TIMETABLE CSP")
    print("="*65)
    t=solve()
    for c in COURSES: print(f" {c:5} -> {t[c][0]} {t[c][1]}")
    print(" All slots unique:",len(set(t.values()))==4)
    print(" AI and DBMS different days:",t["AI"][0]!=t["DBMS"][0])
    print(" OS before NLP:",idx(t["OS"])<idx(t["NLP"]))
    print(" AI not Mon 9-10:",t["AI"]!=("Mon","9-10"))
    return t

def exercise3():
    print("\n"+"="*65)
    print("EXERCISE 3 - CHANGE RULES / CONSTRAINTS")
    print("="*65)
    modified_rules=RULES.copy()
    modified_rules[5]=("medium","high","excellent")
    _,_,old_score,old_cat=fuzzy(75,90,RULES)
    _,_,new_score,new_cat=fuzzy(75,90,modified_rules)
    print("\nFuzzy rule change:")
    print(" Original: medium attendance + high marks -> good")
    print(" Modified: medium attendance + high marks -> excellent")
    print(f" Input: attendance=75%, marks=90%")
    print(f" Original result: {old_score:.2f} ({old_cat})")
    print(f" Modified result: {new_score:.2f} ({new_cat})")
    old=solve()
    new=solve(True)
    print("\nCSP constraint change:")
    print(" Original: AI and DBMS must be on different days")
    print(" Modified: AI and DBMS may be on the same day")
    print(" Original timetable:")
    for c in COURSES: print(f"  {c:5} -> {old[c][0]} {old[c][1]}")
    print(" Modified timetable:")
    for c in COURSES: print(f"  {c:5} -> {new[c][0]} {new[c][1]}")

if __name__=="__main__":
    exercise1()
    exercise2()
    exercise3()
    print("\n"+"="*65)
    print("OBSERVATIONS")
    print("="*65)
    print("1. Fuzzy logic changes the output gradually as attendance and marks change.")
    print("2. The fuzzy rule base directly affects the final performance category.")
    print("3. The CSP accepts only timetables satisfying every constraint.")
    print("4. Changing a constraint changes the set of valid timetable solutions.")
    print("5. Fuzzy logic handles gradual/uncertain inputs; CSP handles strict restrictions.")
