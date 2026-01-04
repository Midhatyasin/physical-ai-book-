#!/usr/bin/env python3
"""
PID Controller for Robot Motor Control.
"""

import numpy as np


class PIDController:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0, output_limits=(-10, 10)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.output_limits = output_limits
        self._integral = 0.0
        self._last_error = 0.0

    def compute(self, setpoint, measurement, dt=0.01):
        error = setpoint - measurement
        P = self.kp * error
        self._integral += error * dt
        I = self.ki * self._integral
        D = self.kd * (error - self._last_error) / dt
        self._last_error = error
        output = P + I + D
        return np.clip(output, *self.output_limits)

    def reset(self):
        self._integral = 0.0
        self._last_error = 0.0


class MotorSimulator:
    def __init__(self, J=0.01, b=0.1, K=0.01, R=1.0):
        self.J, self.b, self.K, self.R = J, b, K, R
        self.velocity = 0.0
        self.position = 0.0

    def step(self, voltage, dt=0.01):
        current = voltage / self.R
        acceleration = (self.K * current - self.b * self.velocity) / self.J
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        return self.velocity, self.position


if __name__ == "__main__":
    motor = MotorSimulator()
    pid = PIDController(kp=0.5, ki=0.1, kd=0.1)

    print("PID Motor Control Demo")
    for t in range(100):
        vel, _ = motor.step(pid.compute(5.0, vel if 'vel' in dir() else 0))

    print(f"Final velocity: {vel:.2f} rad/s")
