# Bird Flock Boid Simulation 🐦

This is a small Python project that simulates the flocking behavior of birds using simple rules. Each moving dot on the screen represents a “boid” that tries to move in a realistic way by following basic principles like avoiding collisions, matching the direction of nearby boids, and staying close to the group.

---

# What it does

The program creates a bunch of boids moving around in a window. Each boid:
1. Tries not to get too close to others (separation)
2. Adjusts its direction to match nearby boids (alignment)
3. Moves toward the center of nearby boids (cohesion)

Even though the rules are simple, when combined they produce lifelike, smooth flocking behavior.

---

# How it works

Each boid keeps track of its position, velocity, and acceleration.
For every frame:
It looks around to find other boids within a certain distance (its neighborhood).
It calculates how to steer based on the three main rules.
It updates its movement accordingly.

All the math behind the scenes just handles basic vector operations—adding, subtracting, normalizing, and limiting the movement speed.

---

# Requirements

You only need:
Python 3
The Pygame library
To install Pygame, run this in your terminal:
```bash
pip install pygame
```
---

# Try changing these values

At the top of the code, there are some constants you can adjust to change how the boids behave:

NUM_BOIDS = 50
desired_separation = 50
NEIGHBOR_RADIUS = 200
MAX_SPEED = 2
MAX_FORCE = 1

You can experiment with them to make the flock tighter, looser, or faster.

---

# Future ideas

Add a predator that chases the flock
Introduce obstacles or barriers
Use colors or trails to make the movement more visual
Add keyboard controls to increase or decrease speed

---

# Credits

The concept is based on Craig Reynolds’ original Boids model (1986).
This version was written in Python by Alok (IISER Bhopal) using Pygame.


