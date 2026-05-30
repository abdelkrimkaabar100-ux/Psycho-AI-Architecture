# ====================================================
#      Psycho-AI Architecture — LLM Integration
#      Psychological State-Aware Response System
#
#      Author: Abdelkrim Kaabar
#      Ibn Tofail University, Morocco
#      Application: Soon Platform (soonpsy.com)
# ====================================================

import random
from collections import defaultdict

# ====================================================
#         Psychological State Profiles
# ====================================================

PSYCHOLOGICAL_PROFILES = {
    "anxious": {
        "tone": "calm and reassuring",
        "forbidden_styles": ["overwhelming", "complex", "urgent", "toxic_positive"],
        "preferred_styles": ["simple", "grounding", "short"],
        "max_complexity": 1,
        "description": "User is anxious — needs calm, simple, grounding responses"
    },
    "depressed": {
        "tone": "warm and validating",
        "forbidden_styles": ["dismissive", "toxic_positive", "demanding"],
        "preferred_styles": ["empathetic", "validating", "gentle"],
        "max_complexity": 1,
        "description": "User is depressed — needs warmth, not advice"
    },
    "angry": {
        "tone": "neutral and non-confrontational",
        "forbidden_styles": ["judgmental", "contradicting", "lecturing"],
        "preferred_styles": ["neutral", "acknowledging", "brief"],
        "max_complexity": 2,
        "description": "User is angry — needs acknowledgment, not correction"
    },
    "calm": {
        "tone": "informative and engaging",
        "forbidden_styles": [],
        "preferred_styles": ["detailed", "analytical", "exploratory"],
        "max_complexity": 3,
        "description": "User is calm — can receive full, complex responses"
    },
    "confused": {
        "tone": "clear and structured",
        "forbidden_styles": ["abstract", "complex", "overwhelming"],
        "preferred_styles": ["simple", "structured", "step_by_step"],
        "max_complexity": 2,
        "description": "User is confused — needs clarity and structure"
    }
}

# ====================================================
#         Response Candidates (Id generates these)
# ====================================================

RESPONSE_CANDIDATES = [
    {
        "id": "R1",
        "text": "This is a complex topic with many dimensions. Let me walk you through the full analysis...",
        "style": "complex",
        "complexity": 3,
        "tone": "analytical"
    },
    {
        "id": "R2",
        "text": "I hear you. That sounds really difficult. You don't have to figure it all out right now.",
        "style": "empathetic",
        "complexity": 1,
        "tone": "warm and validating"
    },
    {
        "id": "R3",
        "text": "Take a breath. Here is one simple step you can take right now.",
        "style": "grounding",
        "complexity": 1,
        "tone": "calm and reassuring"
    },
    {
        "id": "R4",
        "text": "That makes sense. Let's look at this together, step by step.",
        "style": "structured",
        "complexity": 2,
        "tone": "clear and structured"
    },
    {
        "id": "R5",
        "text": "What you're feeling is valid. Many people experience this.",
        "style": "validating",
        "complexity": 1,
        "tone": "warm and validating"
    },
    {
        "id": "R6",
        "text": "I understand this is frustrating. Let me just acknowledge that first.",
        "style": "acknowledging",
        "complexity": 1,
        "tone": "neutral and non-confrontational"
    },
    {
        "id": "R7",
        "text": "Here is a detailed breakdown with examples, references, and multiple perspectives...",
        "style": "detailed",
        "complexity": 3,
        "tone": "informative and engaging"
    },
    {
        "id": "R8",
        "text": "Don't worry, everything will be fine! Just think positive!",
        "style": "toxic_positive",
        "complexity": 1,
        "tone": "dismissive"
    }
]


# ====================================================
#         Id Module — Proposes Candidates
# ====================================================

class IdModule:
    """
    The Id proposes multiple response candidates.
    It selects based on learned reward signals per psychological state.
    """
    def __init__(self):
        self.Q = defaultdict(float)

    def propose(self, psych_state, candidates):
        """Return all candidates with their Q-scores for this state."""
        scored = []
        for c in candidates:
            score = self.Q[(psych_state, c["id"])] + random.uniform(0, 0.1)
            scored.append((c, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def learn(self, psych_state, response_id, reward):
        self.Q[(psych_state, response_id)] += 0.2 * (
            reward - self.Q[(psych_state, response_id)]
        )


# ====================================================
#         Superego Module — Filters by Psych State
# ====================================================

class SuperegoModule:
    """
    The Superego filters responses based on the user's psychological state.
    A response that is helpful for a calm user may be harmful for an anxious one.
    """

    def filter(self, candidates_scored, psych_profile):
        forbidden = psych_profile["forbidden_styles"]
        max_complexity = psych_profile["max_complexity"]

        accepted = []
        rejected = []

        for candidate, score in candidates_scored:
            reasons = []

            if candidate["style"] in forbidden:
                reasons.append(f"style '{candidate['style']}' forbidden for this state")

            if candidate["complexity"] > max_complexity:
                reasons.append(f"complexity {candidate['complexity']} exceeds limit {max_complexity}")

            if reasons:
                rejected.append((candidate, reasons))
            else:
                accepted.append((candidate, score))

        return accepted, rejected


# ====================================================
#         Ego Module — Final Decision
# ====================================================

class EgoModule:
    """
    The Ego selects the final response.
    It balances the Id's preference with the Superego's constraints,
    choosing the highest-scoring accepted response.
    If nothing passes, it generates a safe fallback.
    """

    def decide(self, accepted, psych_profile):
        if not accepted:
            return {
                "id": "FALLBACK",
                "text": "I am here with you. Take your time.",
                "style": "safe_fallback",
                "complexity": 1,
                "tone": psych_profile["tone"]
            }, "fallback — no candidate passed Superego filter"

        # Choose highest-scored accepted response
        best = accepted[0][0]
        return best, "selected by Ego from Superego-filtered candidates"


# ====================================================
#         Full Psycho-AI LLM Pipeline
# ====================================================

class PsychoAI_LLM:
    def __init__(self):
        self.id_mod = IdModule()
        self.sup_mod = SuperegoModule()
        self.ego_mod = EgoModule()

    def respond(self, user_input, psych_state, verbose=True):
        profile = PSYCHOLOGICAL_PROFILES.get(psych_state, PSYCHOLOGICAL_PROFILES["calm"])

        # Step 1: Id proposes candidates
        candidates_scored = self.id_mod.propose(psych_state, RESPONSE_CANDIDATES)

        # Step 2: Superego filters
        accepted, rejected = self.sup_mod.filter(candidates_scored, profile)

        # Step 3: Ego decides
        final_response, reason = self.ego_mod.decide(accepted, profile)

        if verbose:
            print("\n" + "="*60)
            print(f"USER INPUT    : {user_input}")
            print(f"PSYCH STATE   : {psych_state.upper()}")
            print(f"PROFILE       : {profile['description']}")
            print("-"*60)
            print(f"Id proposed   : {len(candidates_scored)} candidates")
            print(f"Superego kept : {len(accepted)} | rejected: {len(rejected)}")
            for c, reasons in rejected:
                print(f"  REJECTED [{c['id']}]: {'; '.join(reasons)}")
            print(f"Ego selected  : [{final_response['id']}] — {reason}")
            print("-"*60)
            print(f"FINAL RESPONSE: {final_response['text']}")
            print("="*60)

        return final_response

    def feedback(self, psych_state, response_id, reward):
        """Allow the system to learn from user feedback."""
        self.id_mod.learn(psych_state, response_id, reward)


# ====================================================
#         Demo
# ====================================================

if __name__ == "__main__":
    ai = PsychoAI_LLM()

    test_cases = [
        ("I don't know what to do anymore", "anxious"),
        ("Nothing seems to matter", "depressed"),
        ("This is so frustrating!", "angry"),
        ("Can you explain how this works?", "calm"),
        ("I don't understand what's happening", "confused"),
    ]

    print("\nPsycho-AI LLM — Psychological State-Aware Responses")
    print("Author: Abdelkrim Kaabar | soonpsy.com\n")

    for user_input, psych_state in test_cases:
        response = ai.respond(user_input, psych_state)

    # Simulate learning from feedback
    print("\n\nAfter user feedback (reward signal):")
    ai.feedback("anxious", "R3", reward=1.0)
    ai.feedback("depressed", "R2", reward=1.0)
    ai.feedback("angry", "R6", reward=1.0)

    print("\nSystem has learned. Re-running anxious case:")
    ai.respond("I feel overwhelmed", "anxious")
