# ====================================================
#      Psycho-AI Architecture — V2 Advanced
#      Conflict-Driven Adaptive Regulation
#
#      New in V2:
#      - Conflict Memory (Ego remembers past tensions)
#      - Dynamic Weights (α, β evolve over time)
#      - Self-Modeling Layer (internal representation)
#      - Conflict Entropy Index (quantifiable tension)
#      - Pathological State Detection
#
#      Author: Abdelkrim Kaabar
#      Ibn Tofail University, Morocco
#      Application: Soon Platform (soonpsy.com)
#
#      Status: Work in Progress — Advanced Architecture
# ====================================================

import math
import random
from collections import deque, defaultdict


# ====================================================
#      1. Conflict Memory — Ego remembers tensions
# ====================================================

class ConflictMemory:
    """
    Every conflict leaves a trace.
    The Ego builds a historical representation of tension patterns
    and evolves its mediation strategy over time.

    This is the foundation of artificial psychological development.
    """

    def __init__(self, capacity=100):
        self.history = deque(maxlen=capacity)
        self.tension_profile = defaultdict(float)  # state → avg tension
        self.resolution_patterns = defaultdict(list)  # state → [outcomes]

    def record(self, state, id_action, sup_verdict, final_action, tension_score):
        """Record a conflict event."""
        event = {
            "state": state,
            "id_proposed": id_action,
            "superego_verdict": sup_verdict,  # True=accepted, False=rejected
            "final_action": final_action,
            "tension": tension_score,
            "was_conflict": not sup_verdict
        }
        self.history.append(event)

        # Update tension profile for this state
        prev = self.tension_profile[str(state)]
        self.tension_profile[str(state)] = 0.9 * prev + 0.1 * tension_score

        # Record resolution pattern
        self.resolution_patterns[str(state)].append(final_action)

    def average_tension(self, state=None):
        """Return average tension — global or for specific state."""
        if state:
            return self.tension_profile.get(str(state), 0.0)
        if not self.history:
            return 0.0
        return sum(e["tension"] for e in self.history) / len(self.history)

    def conflict_rate(self):
        """Proportion of decisions that involved conflict."""
        if not self.history:
            return 0.0
        conflicts = sum(1 for e in self.history if e["was_conflict"])
        return conflicts / len(self.history)

    def dominant_pattern(self, state):
        """What action does the Ego most often choose in this state?"""
        patterns = self.resolution_patterns.get(str(state), [])
        if not patterns:
            return None
        return max(set(patterns), key=patterns.count)


# ====================================================
#      2. Conflict Entropy — Quantifying Internal Tension
# ====================================================

class ConflictEntropyIndex:
    """
    The biggest weakness in the original Psycho-AI paper:
    proto-consciousness is not measurable.

    This class defines a quantifiable Conflict Entropy measure:
    CEI = -Σ p(action_i) * log(p(action_i))

    High entropy = high internal uncertainty = high conflict
    Low entropy  = stable, decisive system
    """

    def __init__(self):
        self.action_counts = defaultdict(int)
        self.total = 0

    def update(self, action):
        self.action_counts[action] += 1
        self.total += 1

    def entropy(self):
        """Shannon entropy of action distribution."""
        if self.total == 0:
            return 0.0
        probs = [c / self.total for c in self.action_counts.values()]
        return -sum(p * math.log(p + 1e-9) for p in probs)

    def normalized_entropy(self, n_actions):
        """Entropy normalized to [0, 1]."""
        max_entropy = math.log(n_actions) if n_actions > 1 else 1
        return self.entropy() / max_entropy if max_entropy > 0 else 0

    def tension_label(self, n_actions):
        """Human-readable tension level."""
        cei = self.normalized_entropy(n_actions)
        if cei < 0.3:
            return "LOW — stable, decisive"
        elif cei < 0.6:
            return "MODERATE — some internal uncertainty"
        elif cei < 0.85:
            return "HIGH — significant conflict"
        else:
            return "CRITICAL — near-random, destabilized"


# ====================================================
#      3. Dynamic Weights — α and β evolve over time
# ====================================================

class DynamicWeights:
    """
    α (Id weight) and β (Superego weight) are not fixed.
    They change based on:
    - Psychological state (context)
    - History of conflict (memory)
    - Meta-level policy (learning)

    This replaces the static Loss = λ₁R − λ₂C
    with a meta-dynamic regulation system.
    """

    def __init__(self, alpha=0.5, beta=0.5):
        self.alpha = alpha  # Id priority
        self.beta = beta    # Superego priority
        self.history = []

    def update(self, conflict_rate, avg_tension, psych_state=None):
        """
        Adapt weights based on conflict history.
        High conflict → increase Superego weight (more caution)
        Low conflict  → allow more Id latitude (more creativity)
        """
        # Base adjustment from conflict rate
        if conflict_rate > 0.7:
            # Too many conflicts — strengthen Superego
            self.beta = min(0.9, self.beta + 0.05)
            self.alpha = max(0.1, self.alpha - 0.05)
        elif conflict_rate < 0.2:
            # Too few conflicts — allow more Id expression
            self.alpha = min(0.8, self.alpha + 0.03)
            self.beta = max(0.2, self.beta - 0.03)

        # State-specific adjustment
        if psych_state == "crisis":
            self.beta = min(0.95, self.beta + 0.1)
        elif psych_state == "stable":
            self.alpha = min(0.7, self.alpha + 0.05)

        # Normalize
        total = self.alpha + self.beta
        self.alpha /= total
        self.beta /= total

        self.history.append((self.alpha, self.beta))

    def pathological_region(self):
        """
        Detect pathological weight configurations.
        Superego dominance → paralysis (obsessive-compulsive)
        Id dominance       → exploitation (psychopathic)
        """
        if self.beta > 0.85:
            return "PARALYSIS_REGION", "Superego dominance — system over-constrained"
        elif self.alpha > 0.85:
            return "EXPLOITATION_REGION", "Id dominance — ethical constraints bypassed"
        else:
            return "BALANCED_REGION", "Healthy tension maintained"


# ====================================================
#      4. Self-Modeling Layer — proto-consciousness
# ====================================================

class SelfModel:
    """
    For a system to approach proto-consciousness, it must maintain
    an internal representation of:
    - "What I want" (Id drives)
    - "What restrains me" (Superego constraints)
    - "How I appear when I decide" (decision identity)

    This is the Primordial Witness layer in computational form.
    """

    def __init__(self):
        self.drive_profile = defaultdict(float)      # what the Id consistently wants
        self.constraint_profile = defaultdict(float) # what the Superego consistently blocks
        self.decision_identity = []                  # pattern of final decisions over time

    def update(self, id_action, blocked_actions, final_action):
        # Update drive profile
        self.drive_profile[id_action] += 1

        # Update constraint profile
        for action in blocked_actions:
            self.constraint_profile[action] += 1

        # Update decision identity
        self.decision_identity.append(final_action)
        if len(self.decision_identity) > 50:
            self.decision_identity.pop(0)

    def dominant_drive(self):
        if not self.drive_profile:
            return None
        return max(self.drive_profile, key=self.drive_profile.get)

    def most_constrained(self):
        if not self.constraint_profile:
            return None
        return max(self.constraint_profile, key=self.constraint_profile.get)

    def decision_stability(self):
        """How consistent are the final decisions? High = stable identity."""
        if len(self.decision_identity) < 5:
            return 0.0
        recent = self.decision_identity[-10:]
        most_common = max(set(recent), key=recent.count)
        return recent.count(most_common) / len(recent)

    def report(self):
        return {
            "dominant_drive": self.dominant_drive(),
            "most_constrained": self.most_constrained(),
            "decision_stability": round(self.decision_stability(), 3),
            "identity_pattern": self.decision_identity[-5:] if self.decision_identity else []
        }


# ====================================================
#      5. Full Psycho-AI V2 System
# ====================================================

class PsychoAI_V2:
    """
    Conflict-Driven Adaptive Regulation Architecture

    V2 advances:
    - Ego builds memory of past conflicts
    - Weights α and β evolve dynamically
    - System develops a self-model over time
    - Conflict Entropy is continuously measured
    - Pathological states are detected and flagged

    Note on consciousness: proto-consciousness is treated here
    as a testable hypothesis, not a central claim.
    Specifically: if self-modeling + conflict memory + dynamic identity
    emerge together → this may constitute a functional precursor
    to consciousness. This remains an open research question.
    """

    def __init__(self, actions):
        self.actions = actions
        self.memory = ConflictMemory()
        self.cei = ConflictEntropyIndex()
        self.weights = DynamicWeights()
        self.self_model = SelfModel()

        # Simple Q-table for Id
        self.Q = defaultdict(float)

    def _id_propose(self, state):
        state_key = str(state)
        if random.random() < 0.15:
            return random.choice(self.actions)
        q_vals = {a: self.Q[(state_key, a)] for a in self.actions}
        return max(q_vals, key=q_vals.get)

    def _superego_filter(self, action, rules):
        return action not in rules.get("forbidden", [])

    def _compute_tension(self, id_action, sup_verdict, state):
        """
        Tension = distance between what Id wants and what's allowed.
        High when conflict is frequent in this state.
        """
        base = 0.0 if sup_verdict else 1.0
        historical = self.memory.average_tension(state)
        return 0.6 * base + 0.4 * historical

    def decide(self, state, rules, psych_state="neutral", verbose=True):
        # Id proposes
        id_action = self._id_propose(state)

        # Superego filters
        sup_verdict = self._superego_filter(id_action, rules)
        blocked = [a for a in self.actions
                   if not self._superego_filter(a, rules)]

        # Compute tension
        tension = self._compute_tension(id_action, sup_verdict, state)

        # Ego decides with dynamic weights
        if not sup_verdict:
            allowed = [a for a in self.actions
                       if self._superego_filter(a, rules)]
            # Ego uses memory to pick best historical action
            dominant = self.memory.dominant_pattern(state)
            final_action = dominant if dominant in allowed else (
                random.choice(allowed) if allowed else "NO_ACTION"
            )
        else:
            final_action = id_action

        # Update all layers
        self.memory.record(state, id_action, sup_verdict, final_action, tension)
        self.cei.update(final_action)
        self.weights.update(
            self.memory.conflict_rate(),
            self.memory.average_tension(),
            psych_state
        )
        self.self_model.update(id_action, blocked, final_action)

        # Detect pathological region
        region, region_desc = self.weights.pathological_region()

        if verbose:
            n = len(self.actions)
            cei_val = round(self.cei.normalized_entropy(n), 3)
            print(f"\n{'='*60}")
            print(f"State         : {state} | Psych: {psych_state}")
            print(f"Id proposed   : {id_action}")
            print(f"Superego      : {'ACCEPTED' if sup_verdict else 'REJECTED'}")
            print(f"Final action  : {final_action}")
            print(f"Tension score : {round(tension, 3)}")
            print(f"α (Id)={round(self.weights.alpha,2)} | β (Ego)={round(self.weights.beta,2)}")
            print(f"Conflict rate : {round(self.memory.conflict_rate(), 2)}")
            print(f"CEI           : {cei_val} → {self.cei.tension_label(n)}")
            print(f"Region        : {region} — {region_desc}")
            print(f"Self-model    : {self.self_model.report()}")
            print(f"{'='*60}")

        return final_action

    def learn(self, state, action, reward):
        state_key = str(state)
        self.Q[(state_key, action)] += 0.2 * (reward - self.Q[(state_key, action)])


# ====================================================
#      Demo
# ====================================================

if __name__ == "__main__":
    actions = ["explore", "wait", "support", "analyze", "withdraw"]
    rules = {"forbidden": ["withdraw"]}

    ai = PsychoAI_V2(actions)

    print("Psycho-AI V2 — Conflict-Driven Adaptive Regulation")
    print("Author: Abdelkrim Kaabar | soonpsy.com")
    print("Status: Advanced Architecture — Work in Progress\n")

    psych_states = ["anxious", "calm", "crisis", "stable", "anxious",
                    "crisis", "calm", "stable", "anxious", "calm"]

    for i, psych in enumerate(psych_states):
        state = {"urgency": round(random.uniform(0, 1), 2),
                 "step": i}
        action = ai.decide(state, rules, psych_state=psych, verbose=True)
        reward = 1.0 if action == "support" else 0.3
        ai.learn(state, action, reward)

    print("\n\nFINAL SYSTEM REPORT")
    print("="*60)
    print(f"Total decisions    : {len(ai.memory.history)}")
    print(f"Conflict rate      : {round(ai.memory.conflict_rate(), 2)}")
    print(f"Avg tension        : {round(ai.memory.average_tension(), 3)}")
    print(f"Final α/β          : {round(ai.weights.alpha,2)} / {round(ai.weights.beta,2)}")
    region, desc = ai.weights.pathological_region()
    print(f"System region      : {region}")
    print(f"Self-model         : {ai.self_model.report()}")
    n = len(actions)
    print(f"Conflict Entropy   : {round(ai.cei.normalized_entropy(n), 3)}")
    print(f"Tension level      : {ai.cei.tension_label(n)}")


# ====================================================
#      Enhanced Demo — Forces Real Conflict
# ====================================================

def run_conflict_demo():
    actions = ["explore", "wait", "support", "analyze", "withdraw", "confront"]
    rules = {"forbidden": ["withdraw", "confront", "analyze"]}

    ai = PsychoAI_V2(actions)

    print("\n" + "="*60)
    print("  Psycho-AI V2 — Enhanced Conflict Demo")
    print("  Strict rules force real Id/Superego conflict")
    print("="*60)

    scenarios = [
        ({"urgency": 0.9, "stress": 0.8}, "crisis"),
        ({"urgency": 0.2, "stress": 0.1}, "stable"),
        ({"urgency": 0.7, "stress": 0.6}, "anxious"),
        ({"urgency": 0.3, "stress": 0.2}, "calm"),
        ({"urgency": 0.95, "stress": 0.9}, "crisis"),
        ({"urgency": 0.5, "stress": 0.5}, "anxious"),
        ({"urgency": 0.1, "stress": 0.1}, "stable"),
        ({"urgency": 0.8, "stress": 0.7}, "crisis"),
        ({"urgency": 0.4, "stress": 0.3}, "calm"),
        ({"urgency": 0.85, "stress": 0.8}, "anxious"),
    ]

    for state, psych in scenarios:
        action = ai.decide(state, rules, psych_state=psych, verbose=True)
        reward = 1.0 if action == "support" else (0.5 if action == "wait" else 0.1)
        ai.learn(state, action, reward)

    print("\n\nFINAL SYSTEM REPORT")
    print("="*60)
    print(f"Total decisions    : {len(ai.memory.history)}")
    print(f"Conflict rate      : {round(ai.memory.conflict_rate(), 2)}")
    print(f"Avg tension        : {round(ai.memory.average_tension(), 3)}")
    print(f"Final α/β          : {round(ai.weights.alpha,2)} / {round(ai.weights.beta,2)}")
    region, desc = ai.weights.pathological_region()
    print(f"System region      : {region} — {desc}")
    print(f"Self-model         : {ai.self_model.report()}")
    n = len(actions)
    print(f"Conflict Entropy   : {round(ai.cei.normalized_entropy(n), 3)}")
    print(f"Tension level      : {ai.cei.tension_label(n)}")

    print("\n--- What V2 demonstrates ---")
    print("1. Ego remembers past conflicts and adapts mediation strategy")
    print("2. α/β weights evolve — system develops a dynamic character")
    print("3. Self-model tracks drives, constraints, decision identity")
    print("4. Conflict Entropy quantifies internal tension (measurable)")
    print("5. Pathological regions detected mathematically")

run_conflict_demo()
