#!/usr/bin/env python3
"""
Auction-Based Task Allocation for Multi-Robot Systems.
Uses sealed-bid auctions for robots to bid on tasks.
"""

import numpy as np
import math
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum
import random


class AuctionState(Enum):
    """State of the auction system."""
    IDLE = "idle"
    AUCTION_RUNNING = "auction_running"
    ALLOCATION_COMPLETE = "allocation_complete"


@dataclass
class Task:
    """Represents a task to be allocated."""
    task_id: int
    x: float  # Location X
    y: float  # Location Y
    priority: int = 0  # Higher = more important
    deadline: float = float('inf')  # Time deadline
    required_capability: str = "none"  # Required robot capability
    estimated_duration: float = 1.0  # Estimated time to complete
    reward: float = 10.0  # Reward for completing

    def __lt__(self, other):
        """Compare by priority for sorting."""
        return self.priority > other.priority  # Higher priority first


@dataclass
class Robot:
    """Represents a robot in the system."""
    robot_id: int
    x: float
    y: float
    capabilities: List[str] = field(default_factory=list)
    max_tasks: int = 3  # Maximum concurrent tasks
    speed: float = 1.0  # Movement speed

    def estimate_cost(self, task: Task) -> float:
        """
        Estimate cost to complete a task.

        Args:
            task: The task to estimate cost for

        Returns:
            Estimated cost (time + distance)
        """
        # Distance to task
        distance = math.sqrt((task.x - self.x)**2 + (task.y - self.y)**2)

        # Cost is travel time plus task duration
        travel_time = distance / self.speed
        cost = travel_time + task.estimated_duration

        # Capability penalty
        if task.required_capability != "none":
            if task.required_capability not in self.capabilities:
                cost *= 10  # Very expensive if cannot perform

        return cost

    def can_complete(self, task: Task) -> bool:
        """Check if robot can complete the task."""
        if task.required_capability != "none":
            return task.required_capability in self.capabilities
        return True


@dataclass
class Bid:
    """Represents a robot's bid on a task."""
    robot_id: int
    task_id: int
    cost: float
    value: float  # Reward - cost
    timestamp: float = 0.0


class AuctionAllocator:
    """Auction-based task allocation system."""

    def __init__(self, robots: List[Robot], auction_timeout: float = 5.0):
        """
        Initialize auction allocator.

        Args:
            robots: List of available robots
            auction_timeout: Maximum time for auction to complete
        """
        self.robots = robots
        self.auction_timeout = auction_timeout
        self.current_auction = None
        self.assignments: Dict[int, int] = {}  # task_id -> robot_id
        self.auction_state = AuctionState.IDLE

    def run_auction(self, tasks: List[Task]) -> Dict[int, int]:
        """
        Run auction to allocate tasks.

        Args:
            tasks: List of tasks to allocate

        Returns:
            Dictionary mapping task_id to robot_id
        """
        self.auction_state = AuctionState.AUCTION_RUNNING
        self.assignments = {}

        # Sort tasks by priority
        sorted_tasks = sorted(tasks)

        # Each task goes through auction
        for task in sorted_tasks:
            winner = self._auction_single_task(task)
            if winner is not None:
                self.assignments[task.task_id] = winner

        self.auction_state = AuctionState.ALLOCATION_COMPLETE
        return self.assignments

    def _auction_single_task(self, task: Task) -> Optional[int]:
        """
        Run auction for a single task.

        Args:
            task: Task to auction

        Returns:
            ID of winning robot, or None
        """
        bids = []

        # Collect bids from all capable robots
        for robot in self.robots:
            if robot.can_complete(task):
                cost = robot.estimate_cost(task)
                # Value = reward - cost (lower cost = higher value)
                value = task.reward - cost
                bid = Bid(
                    robot_id=robot.robot_id,
                    task_id=task.task_id,
                    cost=cost,
                    value=value
                )
                bids.append(bid)

        if not bids:
            return None  # No capable robots

        # Find winner (highest value)
        bids.sort(key=lambda b: b.value, reverse=True)
        winner = bids[0]

        return winner.robot_id

    def get_assignment_for_task(self, task_id: int) -> Optional[Robot]:
        """Get the robot assigned to a specific task."""
        robot_id = self.assignments.get(task_id)
        if robot_id is None:
            return None

        for robot in self.robots:
            if robot.robot_id == robot_id:
                return robot
        return None


class MarketBasedAllocator:
    """Market-based task allocation with negotiation."""

    def __init__(self, robots: List[Robot]):
        self.robots = robots
        self.task_history = []
        self.performance_metrics = {}

    def allocate_tasks(self, tasks: List[Task]) -> Dict[int, int]:
        """
        Allocate tasks using market-based approach.

        Args:
            tasks: List of tasks to allocate

        Returns:
            Mapping of task_id to robot_id
        """
        assignments = {}

        # Calculate task utilities
        for task in sorted(tasks, key=lambda t: t.priority, reverse=True):
            best_robot = None
            best_utility = float('-inf')

            for robot in self.robots:
                if not robot.can_complete(task):
                    continue

                cost = robot.estimate_cost(task)
                # Utility = reward / cost (efficiency)
                utility = task.reward / cost if cost > 0 else float('inf')

                # Consider robot's current workload
                current_tasks = sum(1 for t_id, r_id in assignments.items()
                                   if r_id == robot.robot_id)
                workload_factor = 1.0 / (1.0 + current_tasks * 0.1)

                utility *= workload_factor

                if utility > best_utility:
                    best_utility = utility
                    best_robot = robot

            if best_robot is not None:
                assignments[task.task_id] = best_robot.robot_id

        return assignments


if __name__ == "__main__":
    print("Auction-Based Task Allocation")
    print("=" * 50)

    # Create robots with different capabilities
    robots = [
        Robot(robot_id=0, x=0, y=0, capabilities=["navigation", "grasping"],
              speed=1.0),
        Robot(robot_id=1, x=5, y=5, capabilities=["navigation", "vision"],
              speed=1.2),
        Robot(robot_id=2, x=10, y=0, capabilities=["grasping", "lifting"],
              speed=0.8),
        Robot(robot_id=3, x=5, y=10, capabilities=["navigation", "grasping", "vision"],
              speed=1.0),
    ]

    # Create tasks
    tasks = [
        Task(task_id=0, x=2, y=3, priority=3, required_capability="grasping",
             reward=15.0),
        Task(task_id=1, x=8, y=7, priority=2, required_capability="vision",
             reward=12.0),
        Task(task_id=2, x=1, y=9, priority=1, required_capability="none",
             reward=8.0),
        Task(task_id=3, x=12, y=2, priority=3, required_capability="lifting",
             reward=20.0),
    ]

    # Run auction allocation
    allocator = AuctionAllocator(robots)
    assignments = allocator.run_auction(tasks)

    print("\nAuction Results:")
    print("-" * 40)
    for task_id, robot_id in assignments.items():
        task = next(t for t in tasks if t.task_id == task_id)
        robot = next(r for r in robots if r.robot_id == robot_id)
        print(f"Task {task_id} at ({task.x}, {task.y})")
        print(f"  -> Assigned to Robot {robot_id} at ({robot.x}, {robot.y})")
        print(f"  -> Estimated cost: {robot.estimate_cost(task):.2f}")
