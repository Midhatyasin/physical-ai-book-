# Testable Tasks: Chapter 5 - RL Deep Dive

## Task 1: SAC Implementation

**Status**: pending | **Priority**: P1

### Description
Implement Soft Actor-Critic for continuous control tasks.

### Test Cases
- [ ] SAC solves HalfCheetah-v4 in < 1M steps
- [ ] Entropy coefficient is automatically tuned
- [ ] Twin Q-networks reduce overestimation
- [ ] Target entropy is set correctly

### Code Reference
```python
class SACAgent:
    def __init__(self, state_dim, action_dim, lr=3e-4, gamma=0.99):
        self.policy = SquashedGaussianPolicy(state_dim, action_dim)
        self.q1 = QNetwork(state_dim, action_dim)
        self.q2 = QNetwork(state_dim, action_dim)
        self.log_alpha = torch.zeros(1, requires_grad=True)
```

---

## Task 2: TD3 Implementation

**Status**: pending | **Priority**: P1

### Description
Implement Twin Delayed DDPG for continuous control.

### Test Cases
- [ ] TD3 solves Hopper-v4 faster than DDPG
- [ ] Clipped double Q prevents overestimation
- [ ] Delayed policy updates improve stability
- [ ] Target policy noise prevents Q-value exploitation

---

## Task 3: DreamerV3 World Model

**Status**: pending | **Priority**: P2

### Description
Implement DreamerV3 world model and model-based planning.

### Test Cases
- [ ] World model learns latent dynamics accurately
- [ ] Imagination rollout predicts rewards
- [ ] Model-based planning improves sample efficiency

---

## Task 4: QMIX for Multi-Agent RL

**Status**: pending | **Priority**: P2

### Description
Implement QMIX for cooperative multi-agent tasks.

### Test Cases
- [ ] QMIX solves the Matrix Game
- [ ] Monotonic value decomposition works
- [ ] Centralized training with decentralized execution

---

## Task 5: Offline RL with CQL

**Status**: pending | **Priority**: P2

### Description
Implement Conservative Q-Learning for offline RL.

### Test Cases
- [ ] CQL learns from fixed dataset without online interaction
- [ ] Out-of-distribution actions are properly penalized
    - Performance matches or exceeds behavioral cloning
