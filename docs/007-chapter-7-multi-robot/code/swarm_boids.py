#!/usr/bin/env python3
"""
Boids Flocking Model for Swarm Robotics.
Implements separation, alignment, and cohesion behaviors.
"""

import numpy as np
import math
from dataclasses import dataclass
from typing import List, Tuple
import random


@dataclass
class Boid:
    """A single boid (bird-like agent)."""
    x: float
    y: float
    vx: float
    vy: float
    boid_id: int


class BoidsSimulation:
    """Simulation of boids flocking behavior."""

    def __init__(self, n_boids: int, width: float = 100, height: float = 100,
                 perception_radius: float = 25.0,
                 separation_weight: float = 1.5,
                 alignment_weight: float = 1.0,
                 cohesion_weight: float = 1.0,
                 max_speed: float = 3.0,
                 min_speed: float = 1.0):
        """
        Initialize boids simulation.

        Args:
            n_boids: Number of boids
            width: World width
            height: World height
            perception_radius: Distance to see other boids
            separation_weight: Weight for separation behavior
            alignment_weight: Weight for alignment behavior
            cohesion_weight: Weight for cohesion behavior
            max_speed: Maximum velocity magnitude
            min_speed: Minimum velocity magnitude
        """
        self.n_boids = n_boids
        self.width = width
        self.height = height
        self.perception_radius = perception_radius
        self.separation_weight = separation_weight
        self.alignment_weight = alignment_weight
        self.cohesion_weight = cohesion_weight
        self.max_speed = max_speed
        self.min_speed = min_speed

        # Initialize boids randomly
        self.boids = []
        for i in range(n_boids):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(min_speed, max_speed)
            boid = Boid(
                x=random.uniform(0, width),
                y=random.uniform(0, height),
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                boid_id=i
            )
            self.boids.append(boid)

    def compute_flocking_force(self, boid: Boid) -> Tuple[float, float]:
        """
        Compute the flocking force for a single boid.

        Args:
            boid: The boid to compute forces for

        Returns:
            (fx, fy) force vector
        """
        separation = np.array([0.0, 0.0])
        alignment = np.array([0.0, 0.0])
        cohesion = np.array([0.0, 0.0])
        neighbors = 0

        boid_pos = np.array([boid.x, boid.y])
        boid_vel = np.array([boid.vx, boid.vy])

        for other in self.boids:
            if other.boid_id == boid.boid_id:
                continue

            other_pos = np.array([other.x, other.y])
            other_vel = np.array([other.vx, other.vy])

            # Distance to neighbor
            diff = boid_pos - other_pos
            distance = np.linalg.norm(diff)

            if distance < self.perception_radius and distance > 0:
                # Separation: steer away from close neighbors
                separation += diff / (distance * distance)
                neighbors += 1

                # Alignment: match velocity of neighbors
                alignment += other_vel

                # Cohesion: steer toward center of neighbors
                cohesion += other_pos

        if neighbors > 0:
            separation *= 1.0 / neighbors
            alignment /= neighbors
            cohesion = cohesion / neighbors - boid_pos

        # Apply weights
        separation *= self.separation_weight
        alignment *= self.alignment_weight
        cohesion *= self.cohesion_weight

        # Combine forces
        total_force = separation + alignment + cohesion

        return total_force[0], total_force[1]

    def update(self, dt: float):
        """
        Update all boids by one time step.

        Args:
            dt: Time step
        """
        new_velocities = []

        for boid in self.boids:
            # Compute flocking force
            fx, fy = self.compute_flocking_force(boid)

            # Add boundary avoidance (soft boundaries)
            margin = 10.0
            force_x, force_y = fx, fy

            if boid.x < margin:
                force_x += (margin - boid.x) * 2
            elif boid.x > self.width - margin:
                force_x += (self.width - margin - boid.x) * 2

            if boid.y < margin:
                force_y += (margin - boid.y) * 2
            elif boid.y > self.height - margin:
                force_y += (self.height - margin - boid.y) * 2

            # Update velocity
            new_vx = boid.vx + force_x * dt
            new_vy = boid.vy + force_y * dt

            # Limit speed
            speed = math.sqrt(new_vx**2 + new_vy**2)
            if speed > self.max_speed:
                new_vx = (new_vx / speed) * self.max_speed
                new_vy = (new_vy / speed) * self.max_speed
            elif speed < self.min_speed and speed > 0:
                new_vx = (new_vx / speed) * self.min_speed
                new_vy = (new_vy / speed) * self.min_speed

            new_velocities.append((new_vx, new_vy))

        # Update positions
        for i, boid in enumerate(self.boids):
            boid.vx, boid.vy = new_velocities[i]
            boid.x += boid.vx * dt
            boid.y += boid.vy * dt

            # Wrap around boundaries (toroidal world)
            if boid.x < 0:
                boid.x = self.width
            elif boid.x > self.width:
                boid.x = 0

            if boid.y < 0:
                boid.y = self.height
            elif boid.y > self.height:
                boid.y = 0

    def compute_flocking_metrics(self) -> dict:
        """Compute metrics to measure flocking quality."""
        if len(self.boids) < 2:
            return {"avg_speed": 0, "alignment": 0, "cohesion": 0}

        # Average speed
        avg_speed = sum(math.sqrt(b.vx**2 + b.vy**2) for b in self.boids) / len(self.boids)

        # Alignment (how aligned are velocities)
        avg_vel = np.array([sum(b.vx for b in self.boids) / len(self.boids),
                           sum(b.vy for b in self.boids) / len(self.boids)])
        alignment = np.linalg.norm(avg_vel) / avg_speed if avg_speed > 0 else 0

        # Cohesion (how close are boids to center)
        center_x = sum(b.x for b in self.boids) / len(self.boids)
        center_y = sum(b.y for b in self.boids) / len(self.boids)
        avg_dist = sum(math.sqrt((b.x - center_x)**2 + (b.y - center_y)**2)
                      for b in self.boids) / len(self.boids)
        cohesion = 1.0 / (1.0 + avg_dist)

        return {
            "avg_speed": avg_speed,
            "alignment": alignment,
            "cohesion": cohesion,
            "num_boids": len(self.boids)
        }


class StigmergicSwarm:
    """Stigmergic coordination through environment."""

    def __init__(self, width: int = 50, height: int = 50,
                 evaporation_rate: float = 0.02,
                 diffusion_rate: float = 0.1):
        """
        Initialize stigmergic swarm.

        Args:
            width: Grid width
            height: Grid height
            evaporation_rate: Pheromone decay rate
            diffusion_rate: Pheromone spread rate
        """
        self.width = width
        self.height = height
        self.evaporation_rate = evaporation_rate
        self.diffusion_rate = diffusion_rate

        # Pheromone grid
        self.pheromone = np.zeros((height, width))

        # Robot positions
        self.robots = [(random.uniform(0, width), random.uniform(0, height))
                      for _ in range(10)]

    def update_pheromones(self):
        """Update pheromone grid (diffusion + evaporation)."""
        # Simple diffusion
        new_pheromone = self.pheromone.copy()

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                # Diffusion from neighbors
                avg = (self.pheromone[y-1, x] + self.pheromone[y+1, x] +
                       self.pheromone[y, x-1] + self.pheromone[y, x+1]) / 4
                new_pheromone[y, x] = (1 - self.diffusion_rate) * self.pheromone[y, x] + \
                                      self.diffusion_rate * avg

        # Evaporation
        new_pheromone *= (1 - self.evaporation_rate)
        self.pheromone = new_pheromone

    def deposit_pheromone(self, x: float, y: float, amount: float = 1.0):
        """Deposit pheromone at a location."""
        xi, yi = int(x), int(y)
        if 0 <= xi < self.width and 0 <= yi < self.height:
            self.pheromone[yi, xi] += amount


if __name__ == "__main__":
    print("Boids Flocking Simulation")
    print("=" * 50)

    # Create simulation
    sim = BoidsSimulation(n_boids=50, width=100, height=100)

    print(f"Created {sim.n_boids} boids")

    # Run simulation for several steps
    print("\nSimulating flocking behavior...")
    for step in range(10):
        sim.update(dt=0.1)

        metrics = sim.compute_flocking_metrics()
        print(f"Step {step + 1}: Speed={metrics['avg_speed']:.2f}, "
              f"Alignment={metrics['alignment']:.2f}, "
              f"Cohesion={metrics['cohesion']:.2f}")
