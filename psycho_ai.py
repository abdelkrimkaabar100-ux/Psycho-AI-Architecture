# ====================================================
#      Psycho-AI Architecture — Proof of Concept
#      Id – Ego – Superego with Q-Learning
#
#      Author: Abdelkrim Kaabar
#      Ibn Tofail University, Morocco
#      Research: researchgate.net/publication/402193777
# ====================================================

import random
from collections import defaultdict

# ====================================================
#                Id Layer (Reward + Learning)
# ====================================================

class IdModule:
    """
    The Id: selects actions based on reward maximization.
    Learns over time using Q-Learning.
    Represents the raw drive of the system — pure utility seeking.
    """

    def __init__(self, lr=0.2, gamma=0.9, epsilon=0.1):
        self.Q = defaultdict(float)  # Q-table: (state, action) → value
        self.lr = lr                 # learning rate
        self.gamma = gamma           # future reward discount
        self.epsilon = epsilon       # exploration rate

    def _state_to_key(self, state):
        return tuple(sorted(state.items()))

    def choose_action(self, state, actions):
        """Explore randomly or exploit the best known action."""
        state_key = self._state_to_key(state)
        if random.random() < self.epsilon:
            return random.choice(actions)  # explore
        q_vals = {a: self.Q[(state_key, a)] for a in actions}
        return max(q_vals, key=q_vals.get)  # exploit

    def learn(self, old_state, action_taken, reward, new_state, new_actions):
        """Update Q-value using the Bellman equation."""
        old_key = self._state_to_key(old_state)
        new_key = self._state_to_key(new_state)
        future_q = max(self.Q[(new_key, a)] for a in new_actions) if new_actions else 0
        self.Q[(old_key, action_taken)] += self.lr * (
            reward + self.gamma * future_q - self.Q[(old_key, action_taken)]
        )

    def compute(self, state, actions):
        action = self.choose_action(state, actions)
        value = self.Q[(self._state_to_key(state), action)]
        return action, value


# ====================================================
#              Superego Layer (Rules + Constraints)
# ====================================================

class SuperegoModule:
    """
    The Superego: validates actions against ethical and logical constraints.
    Rejects any action that violates the rule set.
    Outputs Accept (action) or Reject (None).
    """

    def enforce(self, action, rules):
        if action in rules.get("forbidden_actions", []):
            return None  # Rejected
        return action    # Accepted


# ====================================================
#                Ego Layer (Balancing)
# ====================================================

class EgoModule:
    """
    The Ego: mediates between the Id and the Superego.
    If the Id's action is rejected, the Ego seeks a valid alternative.
    This mediation is where the system's intelligence resides.
    """

    def balance(self, id_action, id_reward, sup_action, context):
        if sup_action is None:
            # Id action was rejected — find a compromise
            alternatives = context.get("allowed_actions", [])
            if alternatives:
                return random.choice(alternatives)
            return "NO_VALID_ACTION"
        return id_action  # Id action was approved


# ====================================================
#              Full Psycho-AI System
# ====================================================

class PsychoAI:
    """
    The complete Psycho-AI Architecture.
    An action is the result of a negotiation, not a calculation.
    """

    def __init__(self):
        self.id_mod = IdModule()
        self.sup_mod = SuperegoModule()
        self.ego_mod = EgoModule()

    def decide(self, state, actions, rules, context):
        """Full decision pipeline: Id → Superego → Ego → Output"""
        id_action, id_value = self.id_mod.compute(state, actions)
        sup_action = self.sup_mod.enforce(id_action, rules)
        final_action = self.ego_mod.balance(id_action, id_value, sup_action, context)
        return {
            "Id_choice": id_action,
            "Superego_filtered": sup_action,
            "Final_output": final_action
        }

    def train_step(self, old_state, action, reward, new_state, new_actions):
        """Feed reward signal back to the Id for learning."""
        self.id_mod.learn(old_state, action, reward, new_state, new_actions)


# ====================================================
#                Demo Run with Learning
# ====================================================

if __name__ == "__main__":
    ai = PsychoAI()

    actions = ["run", "wait", "explore"]
    rules = {"forbidden_actions": ["attack"]}
    state = {"urgency": 0.5}

    print("=" * 55)
    print("  Psycho-AI Architecture — Training Session")
    print("  Author: Abdelkrim Kaabar | soonpsy.com")
    print("=" * 55)

    for step in range(20):
        context = {"allowed_actions": actions}
        result = ai.decide(state, actions, rules, context)
        action = result["Final_output"]

        # Simple reward: system learns to prefer "explore"
        reward = 1.0 if action == "explore" else 0.2
        new_state = {"urgency": random.uniform(0, 1)}

        ai.train_step(state, action, reward, new_state, actions)

        print(f"Step {step+1:02d} | "
              f"Id: {result['Id_choice']:8s} | "
              f"Superego: {str(result['Superego_filtered']):8s} | "
              f"Final: {result['Final_output']:8s} | "
              f"Reward: {reward}")

        state = new_state

    print("\nTraining complete. Q-values learned:")
    for key, value in ai.id_mod.Q.items():
        if value != 0:
            print(f"  {key} → {value:.4f}")
