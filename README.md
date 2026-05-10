# Simspractice - Physics Simulations

A collection of Python-based physics simulations exploring classical mechanics, gravitational dynamics, and general relativity using numerical integration and visualization.

## Overview

This project implements various physics simulations to visualize and understand gravitational phenomena and relativistic effects. Simulations are rendered using Pygame for real-time visualization and Matplotlib for detailed analysis.

## Project Structure

### Gravitational Simulations

**freefallorbit.py**
- Newtonian gravitational N-body simulation
- Simulates orbital dynamics and free-fall trajectories
- Models planetary/object interactions under gravity
- Real-time 2D visualization using Pygame

**simusinggr.py**
- Advanced gravitational simulation with spacetime deformation
- Introduces wave propagation through a 2D spacetime grid
- Visualizes how massive objects distort spacetime
- Combines classical gravity with relativistic wave effects

**freefallsim.py**
- Basic projectile motion and free-fall simulation
- Demonstrates motion under constant gravitational acceleration
- Tests collision and bouncing behavior
- Useful for validation of physics calculations

### Light Bending & General Relativity

**lightbending1.py**
- Initial implementation of light bending near massive objects
- Explores photon trajectories in Schwarzschild geometry
- Incomplete implementation (noted in source comments)

**lightbending2.py**
- Advanced light bending simulation using General Relativity
- Implements Schwarzschild metric for photon trajectory calculation
- Black hole visualization with event horizon
- Uses effective potential formulation for accurate light path prediction
- Real-time rendering of light rays bending around black holes

**GRsimpletest.py**
- Test/validation file for General Relativity implementations
- Used for debugging and verifying GR equation correctness

### rebound.py
- Integration with Rebound N-body dynamics library
- Provides alternative numerical integration methods
- Used for validating simulation accuracy

## Dependencies

- **numpy** - Numerical computations and linear algebra
- **matplotlib** - Data visualization and plotting
- **pygame-ce** - Real-time 2D graphics and visualization engine

## Installation

```bash
pip install -r requirements.txt
```

## Key Features

- **Real-time Visualization**: Interactive Pygame-based graphics for orbit and light path visualization
- **Accurate Physics**: Implements proper gravitational force calculations and relativistic effects
- **Schwarzschild Geometry**: Models light bending in strong gravitational fields
- **N-Body Dynamics**: Simulate multiple interacting gravitational bodies
- **Spacetime Deformation**: Visualize how mass curves spacetime

## Physics Constants

The simulations use accurate physical constants:
- Gravitational constant (G): 6.67430×10⁻¹¹ m³·kg⁻¹·s⁻²
- Speed of light (c): 299,792,458 m/s

## Running the Simulations

```bash
# Gravitational simulation
python freefallorbit.py

# Advanced spacetime simulation
python simusinggr.py

# Light bending around black hole
python lightbending2.py

# Projectile motion
python freefallsim.py
```

## Notes

- Some simulations are noted as incomplete or not fully physically accurate (see source code comments)
- Integration methods can be improved in certain modules
- Schwarzschild light bending uses effective potential formulation suitable for far-field photons
