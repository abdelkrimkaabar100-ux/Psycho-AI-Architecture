# Psycho-AI Architecture
### A Tripartite Framework for Human-State-Aware AGI

**Author:** Abdelkrim Kaabar  
**Affiliation:** Ibn Tofail University, Morocco  
**Version:** 1.0 — Proof of Concept  
**Research Paper:** [ResearchGate](https://www.researchgate.net/publication/402193777_Towards_Controlled_Internal_Conflict_A_Conceptual_Framework_for_Artificial_General_Intelligence_via_the_Psycho-_AI_Architecture)

---

## Overview

The Psycho-AI Architecture proposes that true Artificial General Intelligence cannot emerge from a monolithic optimization system. Instead, it requires a **structured internal conflict** modeled on the human psyche — specifically the Freudian tripartite model of Id, Ego, and Superego.

This repository contains a working **Proof of Concept** implementation demonstrating the core architecture with a Q-Learning-based Id module.

---

## The Three Layers

| Layer | Function | Technical Analog |
|-------|----------|-----------------|
| **Id (Reward Module)** | Maximizes utility — drives action toward highest reward | Q-Learning Agent |
| **Superego (Rules Module)** | Validates actions against ethical and logical constraints | Constraint Validator |
| **Ego (Balancing Layer)** | Mediates between Id and Superego to produce a final decision | Meta-Controller |

---

## Core Equation

The Ego seeks to minimize:

```
Final Decision = argmin [ α · |a − a_id|² + β · (1 − V_se(a)) ]
```

Where:
- `α` = weight of reward-seeking (Id priority)
- `β` = weight of rule adherence (Superego priority)
- `V_se` = Superego validation score ∈ [0, 1]

---

## Architecture Diagram

```
INPUT (state, actions, rules, context)
         │
    ┌────┴────┐
    │         │
  Id        Superego
(Reward)    (Rules)
    │         │
 Id_Action  Accept/Reject
    │         │
    └────┬────┘
         │
       Ego
  (Balancing Layer)
         │
   Final Decision
```

---

## Implementation

### Requirements
```
Python 3.7+
No external dependencies
```

### Run
```bash
python psycho_ai.py
```

### What it does
- The **Id** uses Q-Learning to select the highest-reward action
- The **Superego** filters forbidden actions
- The **Ego** resolves conflict and produces a final output
- The system **learns over time** — Q-values update with each step

---

## Roadmap

- [x] Core tripartite architecture
- [x] Q-Learning Id module
- [x] Constraint validation layer
- [ ] Integration with LLM inference pipeline
- [ ] ROS Net Load Index as upstream anchor for Ego weights (α, β)
- [ ] Deployment in Soon — AI Mental Health Platform
- [ ] Full AGI formalization

---

## Application: Soon Web App

I am striving to integrate Psycho-AI into **[Soon](https://www.soonpsy.com)** — an AI-powered mental health support platform for both humans and animals.

The core principle is simple yet essential: **the psychological state of the user must be understood before generating any response.**

In Soon, this concept extends to the LLM architecture, where multiple possible responses interact within an organized internal conflict, allowing the system to choose a response that best aligns with the user's current psychological state and future direction.

This conflict-based model could form the foundation for a new generation of Psycho-AI-based LLM models — with the potential to achieve deeper understanding where artificial intelligence has genuine comprehension and approaches Artificial General Intelligence (AGI).

By applying Psycho-AI, the model operates as **the human self operates** — not just how the brain functions.

---

## Related Work

- [Full Research Paper on ResearchGate](https://www.researchgate.net/publication/402193777)
- [Author's Website](https://abdelkrimkaabar.lovestoblog.com)
- [Soon — Web App](https://www.soonpsy.com)

---

## License

© 2026 Abdelkrim Kaabar. All rights reserved.  
This repository is shared for academic and research purposes.  
Any commercial use or derivative implementation requires written permission.

---

*"An action is the result of a negotiation, not a calculation."*  
— Psycho-AI Architecture, Kaabar (2026)
