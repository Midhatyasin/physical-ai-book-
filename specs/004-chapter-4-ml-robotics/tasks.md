# Testable Tasks: Chapter 4 - Machine Learning for Robotics

## Task 1: Neural Network Basics

**Status**: pending | **Priority**: P1

### Description
Implement a neural network from scratch using PyTorch for a simple robotics regression task.

### Test Cases
- [ ] Network initializes without errors
- [ ] Forward pass produces expected output shape
- [ ] Training loop decreases loss over epochs
- [ ] Model generalizes to test set (MSE < threshold)

### Code Reference
```python
class RoboticsMLP(nn.Module):
    def __init__(self, input_dim=10, hidden_dims=[128, 64], output_dim=2):
        super().__init__()
        layers = []
        prev_dim = input_dim
        for h_dim in hidden_dims:
            layers.extend([nn.Linear(prev_dim, h_dim), nn.ReLU()])
            prev_dim = h_dim
        layers.append(nn.Linear(prev_dim, output_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)
```

---

## Task 2: DQN Implementation

**Status**: pending | **Priority**: P1

### Description
Implement Deep Q-Network for discrete control tasks (CartPole).

### Test Cases
- [ ] Agent trains to solve CartPole (avg reward > 450)
- [ ] Epsilon decay works correctly
- [ ] Target network updates periodically
- [ ] Experience replay buffer functions

### Code Reference
```python
class DQNAgent:
    def __init__(self, state_dim, action_dim, lr=3e-4, gamma=0.99):
        self.q_network = QNetwork(state_dim, action_dim)
        self.target_network = QNetwork(state_dim, action_dim)
        self.optimizer = Adam(self.q_network.parameters(), lr=lr)
        self.gamma = gamma
        self.epsilon = 1.0
```

---

## Task 3: PPO Implementation

**Status**: pending | **Priority**: P1

### Description
Implement Proximal Policy Optimization for continuous control.

### Test Cases
- [ ] PPO agent solves HalfCheetah-v4
- [ ] Clipped surrogate objective prevents large updates
- [ ] GAE advantage calculation is correct
- [ ] Entropy bonus encourages exploration

### Code Reference
```python
class PPOAgent:
    def __init__(self, state_dim, action_dim, clip_epsilon=0.2, lr=3e-4):
        self.policy = GaussianPolicy(state_dim, action_dim)
        self.value = ValueNetwork(state_dim)
        self.clip_epsilon = clip_epsilon
```

---

## Task 4: Behavior Cloning

**Status**: pending | **Priority**: P2

### Description
Implement behavior cloning from expert demonstrations.

### Test Cases
- [ ] Model imitates expert behavior with < 5% deviation
- [ ] Training converges on demonstration data
- [ ] Evaluation shows improvement over random policy

---

## Task 5: Transfer Learning Demo

**Status**: pending | **Priority**: P2

### Description
Demonstrate sim2real transfer with domain randomization.

### Test Cases
- [ ] Model trained in sim transfers to real with < 10% performance drop
- [ ] Domain randomization improves robustness
