# Architecture Plan: Chapter 5 - RL Deep Dive

## 1. Scope and Dependencies

### In Scope
- Advanced actor-critic methods (SAC, TD3)
- Model-based RL (PlaNet, Dreamer)
- Multi-agent RL (QMIX, MAPPO)
- Hierarchical RL
- Offline RL

### Out of Scope
- Basic RL concepts (covered in Chapter 4)
- Hardware deployment (Chapter 8)
- Ethics (Chapter 9)

### External Dependencies
- PyTorch 2.0+
- DM-Control Suite
- PyMJCF (for MuJoCo environments)

## 2. Key Decisions and Rationale

| Decision | Options | Chosen | Rationale |
|----------|---------|--------|-----------|
| Continuous Control Suite | DM-Control vs MuJoCo | DM-Control | Python-native, well-documented |
| MARL Framework | PettingZoo vs RLlib | PettingZoo | Simpler for learning |
| Model-Based RL | PlaNet vs Dreamer | DreamerV3 | State-of-the-art performance |

## 3. Interfaces and API Contracts

### SAC Agent
```python
class SACAgent:
    def __init__(self, state_dim: int, action_dim: int, config: Dict)
    def select_action(self, state: np.ndarray, deterministic: bool = False) -> np.ndarray
    def update(self, batch: ReplayBuffer) -> Dict
```

### World Model
```python
class WorldModel(nn.Module):
    def __init__(self, obs_dim: int, action_dim: int, latent_dim: int)
    def forward(self, obs: Tensor, action: Tensor) -> Tuple[Tensor, Tensor, Tensor]
```

## 4. Chapter Structure

1. Advanced Actor-Critic Methods (SAC, TD3)
2. Model-Based Reinforcement Learning
3. Multi-Agent Reinforcement Learning
4. Hierarchical Reinforcement Learning
5. Offline Reinforcement Learning
