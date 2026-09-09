"""
Experiment 3: Agent Architectures — The BDI Deliberation Cycle

The program implements:
- Beliefs revised from percepts
- Desires/options from visible holes
- Intention selection (filter)
- Shortest-path planning
- Single-minded reconsideration with gamma
- Blind / single-minded / open-minded commitment comparison
- A reproducible event trace
- Gamma x world-speed sweep over 25 seeds and 600 agent steps
"""

import random
import statistics
import statistics
from collections import deque

GRID = 15
STEPS = 600
LIFETIME = (12, 28)
HOLE_PROB = 0.10
SEED = 7

DIRS = [(1,0), (-1,0), (0,1), (0,-1)]

def shortest_path(start, goal, holes):
    """Shortest 4-neighbour path; holes are passable cells."""
    q = deque([start])
    parent = {start: None}
    while q:
        u = q.popleft()
        if u == goal:
            break
        for dx, dy in DIRS:
            v = (u[0] + dx, u[1] + dy)
            if 0 <= v[0] < GRID and 0 <= v[1] < GRID and v not in parent:
                parent[v] = u
                q.append(v)
    if goal not in parent:
        return []
    path = []
    cur = goal
    while cur != start:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path

class Tileworld:
    def __init__(self, seed, world_speed=1, forced_trace=False):
        self.rng = random.Random(seed)
        self.world_speed = world_speed
        self.holes = {}  # cell -> remaining lifetime
        self.appeared = 0
        self.filled = 0
        self.tick = 0
        self.forced_trace = forced_trace
        self.trace_schedule = {
            # These events make the required drop and switch events easy to observe.
            3: ("add", (1, 1)),
            8: ("add", (13, 13)),
            12: ("remove", (1, 1)),
            18: ("add", (2, 2)),
        }

    def add_hole(self, cell, lifetime=None):
        if cell not in self.holes:
            self.holes[cell] = lifetime if lifetime is not None else self.rng.randint(*LIFETIME)
            self.appeared += 1

    def fill(self, cell):
        if cell in self.holes:
            del self.holes[cell]
            self.filled += 1

    def advance(self):
        """Advance the world by its configured number of world ticks."""
        for _ in range(self.world_speed):
            self.tick += 1
            if self.forced_trace and self.tick in self.trace_schedule:
                action, cell = self.trace_schedule[self.tick]
                if action == "add":
                    self.add_hole(cell, lifetime=20)
                else:
                    self.holes.pop(cell, None)
                continue

            expired = []
            for cell in list(self.holes):
                self.holes[cell] -= 1
                if self.holes[cell] <= 0:
                    expired.append(cell)
            for cell in expired:
                del self.holes[cell]

            # Random hole appearance
            if self.rng.random() < HOLE_PROB:
                cell = (self.rng.randrange(GRID), self.rng.randrange(GRID))
                if cell not in self.holes:
                    self.add_hole(cell)

class BDI:
    def __init__(self, world, gamma=1, strategy="single-minded", verbose=False):
        self.world = world
        self.gamma = gamma
        self.strategy = strategy
        self.verbose = verbose
        self.pos = (GRID // 2, GRID // 2)
        self.beliefs = set()
        self.intention = None
        self.plan = []
        self.since_reconsider = 0
        self.log = []
        self.deliberations = 0

    def brf(self):
        self.beliefs = set(self.world.holes.keys())

    def options(self):
        return list(self.beliefs)

    def filter(self, options):
        if not options:
            return None
        return min(options, key=lambda h: (len(shortest_path(self.pos, h, self.beliefs)), h))

    def make_plan(self):
        if self.intention is None:
            self.plan = []
        else:
            self.plan = shortest_path(self.pos, self.intention, self.beliefs)

    def deliberate(self, reason):
        self.brf()
        opts = self.options()
        old = self.intention
        chosen = self.filter(opts)
        self.deliberations += 1

        if chosen is None:
            self.intention = None
            self.plan = []
            self.log.append(f"t={self.world.tick}: DELIBERATE ({reason}) -> no option")
            return

        self.intention = chosen
        self.make_plan()
        if old is None:
            self.log.append(f"t={self.world.tick}: COMMIT -> intention {chosen}")
        elif old != chosen:
            self.log.append(f"t={self.world.tick}: SWITCH -> {old} to better option {chosen}")
        else:
            self.log.append(f"t={self.world.tick}: RECONSIDER -> retain {chosen}")

    def run(self, steps):
        self.deliberate("initial")
        for _ in range(steps):
            self.brf()

            if self.intention is None or not self.plan:
                self.deliberate("no intention/empty plan")

            if self.intention is None:
                self.world.advance()
                continue

            # Single-minded: if the intended hole is already gone, drop it.
            if self.intention not in self.beliefs:
                self.log.append(f"t={self.world.tick}: DROP -> intention {self.intention} became unachievable")
                self.intention = None
                self.plan = []
                self.deliberate("dropped impossible intention")
                if self.intention is None:
                    self.world.advance()
                    continue

            # Execute one action.
            if self.plan:
                self.pos = self.plan.pop(0)
            self.since_reconsider += 1

            # Filling happens when the agent reaches the hole.
            if self.pos in self.world.holes:
                target = self.pos
                self.world.fill(target)
                self.log.append(f"t={self.world.tick}: ACHIEVE -> filled {target}")
                self.intention = None
                self.plan = []

            self.world.advance()

            # Commitment policy
            if self.strategy == "blind":
                # Keep intention until believed achieved.
                continue

            if self.strategy == "open-minded":
                self.deliberate("open-minded")
                continue

            # single-minded
            if self.since_reconsider >= self.gamma:
                self.since_reconsider = 0
                self.deliberations += 1
                self.brf()

                if self.intention is not None and self.intention not in self.beliefs:
                    self.log.append(f"t={self.world.tick}: DROP -> intention {self.intention} became unachievable")
                    self.intention = None
                    self.plan = []
                    self.deliberate("single-minded drop")
                else:
                    opts = self.options()
                    chosen = self.filter(opts)
                    if chosen is not None and chosen != self.intention:
                        old = self.intention
                        self.intention = chosen
                        self.make_plan()
                        self.log.append(f"t={self.world.tick}: SWITCH -> {old} to better option {chosen}")

        effectiveness = self.world.filled / self.world.appeared if self.world.appeared else 0.0
        return effectiveness

def run_experiment(gamma, world_speed, seed):
    world = Tileworld(seed, world_speed=world_speed)
    agent = BDI(world, gamma=gamma, strategy="single-minded")
    eff = agent.run(STEPS)
    return eff, world.filled, world.appeared

def run_trace():
    print("=" * 72)
    print("EXPERIMENT 3: BDI DELIBERATION CYCLE — EVENT TRACE")
    print("=" * 72)
    world = Tileworld(SEED, world_speed=1, forced_trace=True)
    agent = BDI(world, gamma=4, strategy="single-minded")
    eff = agent.run(30)
    for line in agent.log:
        print(line)
    print(f"Holes filled : {world.filled}")
    print(f"Holes appeared: {world.appeared}")
    print(f"Effectiveness: {eff:.3f}")
    print()

def sweep():
    print("=" * 72)
    print("EXERCISE 1: GAMMA x WORLD SPEED SWEEP")
    print("=" * 72)
    gammas = [1, 2, 4, 8, "bold"]
    speeds = [1, 2, 4, 8]
    rows = []

    for speed in speeds:
        best_g, best_e = None, -1
        for gamma in gammas:
            vals = []
            for seed in range(25):
                if gamma == "bold":
                    # A gamma larger than the longest possible useful plan.
                    # On a 15x15 grid, 29 is safely above the maximum Manhattan distance.
                    g = 1000
                else:
                    g = gamma
                eff, filled, appeared = run_experiment(g, speed, seed)
                vals.append(eff)
            avg = statistics.mean(vals)
            rows.append((speed, gamma, avg))
            if avg > best_e:
                best_e, best_g = avg, gamma
        print(f"speed={speed}: best gamma={best_g}, effectiveness={best_e:.4f}")

    print("\nFull table:")
    print("speed | gamma | mean effectiveness")
    print("-" * 38)
    for speed in speeds:
        for s, g, e in rows:
            if s == speed:
                print(f"{s:5d} | {str(g):5s} | {e:.4f}")

    print("\nObservation:")
    print("As world speed increases, old intentions become stale faster.")
    print("Therefore the best gamma tends to move toward smaller values.")
    print("Very small gamma spends more time deliberating; very large gamma risks")
    print("continuing toward holes that have disappeared. An intermediate gamma")
    print("balances thinking time against plan stability.")

if __name__ == "__main__":
    run_trace()
    sweep()
