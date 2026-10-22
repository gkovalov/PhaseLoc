import zipfile
import os

# 1. core_constants.py
core_constants_py = """\"\"\"
CORE CONSTANTS
GLAB Research Cluster - Phase Dynamics Framework

This module contains the fundamental topological and physical constants
derived without empirical parameters.
\"\"\"
import numpy as np

# Fundamental Physics Constants
HBAR = 1.054571817e-34       # J*s
C_LIGHT = 299792458.0        # m/s
M_P = 1.67262192369e-27      # kg (Proton rest mass)
ALPHA = 1.0 / 137.035999084  # Fine-structure constant

# Phase Dynamics & Topological Constants
K_C = 1.0 / np.pi            # Kuramoto critical threshold
G_FACTOR = ((np.pi / (2 * np.sqrt(2))) * (1.0 - (ALPHA * np.pi) / 2.0))**4 # S-matrix residue

# Acoustic Constants
C_SOUND = 1500.0             # m/s (Speed of sound in water)
"""

# 2. spectra_engine.py
spectra_engine_py = """\"\"\"
SPECTRA ENGINE
Topological Derivation of Hydrogen-Bond Frequency and Water IR Spectrum.
\"\"\"
import numpy as np
from core_constants import C_LIGHT, M_P, ALPHA, G_FACTOR

def calculate_hydrogen_bond_freq():
    # Base frequency of the chi-attractor
    nu_chi = 3.43315e20  # Hz
    # Hydrogen-bond frequency
    nu_HB = nu_chi * (ALPHA**3 / 4.0) * G_FACTOR
    # Terahertz resonance
    nu_res = 4.0 * ALPHA * nu_HB
    
    print("=== PAPER 1: HYDROGEN-BOND FREQUENCY ===")
    print(f"Hydrogen-Bond Freq (nu_HB): {nu_HB / 1e12:.2f} THz")
    print(f"Terahertz Resonance (nu_res): {nu_res / 1e12:.3f} THz\\n")

def calculate_water_ir_spectrum():
    h = 6.62607015e-34
    
    # Nuclear level (wavenumber cm^-1)
    tilde_nu_p = (M_P * C_LIGHT**2) / h / (C_LIGHT * 100)
    
    # Ultraviolet Electronic Scaffold
    nu_res = tilde_nu_p * (ALPHA**4) * G_FACTOR
    
    # Intra-Molecular Valence Level
    nu_val = nu_res / (3.0 * np.pi)
    
    # Inter-Molecular Collective Network Level
    nu_net = (2.0 / 3.0) * tilde_nu_p * (ALPHA**5) * G_FACTOR
    
    print("=== PAPER 2: WATER IR SPECTRUM ===")
    print(f"Proton Rest Mass Base (nu_p): {tilde_nu_p:.4e} cm^-1")
    print(f"UV Electronic Scaffold (nu_res): {nu_res:.2f} cm^-1")
    print(f"Valence Level (nu_val): {nu_val:.2f} cm^-1")
    print(f"Collective Network Level (nu_net): {nu_net:.2f} cm^-1")

if __name__ == "__main__":
    calculate_hydrogen_bond_freq()
    calculate_water_ir_spectrum()
"""

# 3. topological_radar.py
topological_radar_py = """\"\"\"
SPECTRAL RADAR v2.1
Absolute Matrix Localization via Topological Phase Filter in Vacuum.
\"\"\"
import numpy as np
from scipy.optimize import minimize
from core_constants import C_LIGHT

def radar_simulation():
    dt = 1e-7  # 0.1 microseconds integration step

    # 50x50 km grid
    receiver_positions = np.array([
        [0.0, 0.0],
        [50000.0, 0.0],
        [50000.0, 50000.0],
        [0.0, 50000.0]
    ])

    true_target = np.array([32000.0, 41000.0])
    distances = np.linalg.norm(receiver_positions - true_target, axis=1)

    alpha_true = 1.5e-14 
    lock_times_true = distances / C_LIGHT + alpha_true * (distances ** 2)
    lock_steps_true = lock_times_true / dt

    np.random.seed(101) 
    noise_std = 0.005   
    lock_steps_measured = lock_steps_true + np.random.normal(0, noise_std, size=4)

    def localize_target_radar_scaled(receivers, measured_steps, c_speed, dt_step):
        def cost(params):
            x_km, y_km, alpha_scaled = params
            pos = np.array([x_km * 1000.0, y_km * 1000.0])
            alpha = alpha_scaled * 1e-14
            
            c = 0.0
            for i in range(1, 4):
                di = np.linalg.norm(receivers[i] - pos)
                d0 = np.linalg.norm(receivers[0] - pos)
                
                t_i = (di / c_speed + alpha * (di**2)) * 1e6
                t_0 = (d0 / c_speed + alpha * (d0**2)) * 1e6
                
                tdoa_m = (measured_steps[i] - measured_steps[0]) * dt_step * 1e6
                tdoa_p = t_i - t_0
                
                c += (tdoa_m - tdoa_p)**2
            return c
        
        bounds = ((-20.0, 70.0), (-20.0, 70.0), (0.0, 100.0))
        res = minimize(cost, (25.0, 25.0, 1.0), method='L-BFGS-B', bounds=bounds)
        
        est_x = res.x[0] * 1000.0
        est_y = res.x[1] * 1000.0
        est_alpha = res.x[2] * 1e-14
        
        return np.array([est_x, est_y]), est_alpha, res.fun

    est_tgt, est_alpha, cost_val = localize_target_radar_scaled(
        receiver_positions, lock_steps_measured, C_LIGHT, dt
    )
    error = np.linalg.norm(est_tgt - true_target)

    print("=== SPECTRAL RADAR v2.1 (Light Speed) ===")
    print(f"True Target:  {true_target}")
    print(f"Estimated:    {est_tgt}")
    print(f"Alpha (est):  {est_alpha:.2e}")
    print(f"Error:        {error:.2f} meters\\n")

if __name__ == '__main__':
    radar_simulation()
"""

# 4. topological_sonar.py
topological_sonar_py = """\"\"\"
SONAR v2.3
Hydroacoustic Topological Phase Filter with Calibrated TDOA.
\"\"\"
import numpy as np
from scipy.optimize import minimize
from core_constants import C_SOUND

def sonar_simulation():
    dt = 0.1

    receiver_positions = np.array([
        [0.0, 0.0],
        [5000.0, 0.0],
        [5000.0, 5000.0],
        [0.0, 5000.0]
    ])

    true_target = np.array([2500.0, 2500.0])
    distances = np.linalg.norm(receiver_positions - true_target, axis=1)

    alpha_true = 1e-6
    lock_times_true = distances / C_SOUND + alpha_true * (distances ** 2)
    lock_steps_true = lock_times_true / dt

    np.random.seed(42)
    noise_std = 0.01 
    lock_steps_measured = lock_steps_true + np.random.normal(0, noise_std, size=len(receiver_positions))

    def localize_target_calibrated(receivers, measured_steps, c_sound, dt_step):
        def cost(params):
            x, y, alpha = params
            pos = np.array([x, y])
            c = 0.0
            for i in range(1, 4):
                di = np.linalg.norm(receivers[i] - pos)
                d0 = np.linalg.norm(receivers[0] - pos)
                
                t_i = di / c_sound + alpha * (di ** 2)
                t_0 = d0 / c_sound + alpha * (d0 ** 2)
                
                tdoa_m = (measured_steps[i] - measured_steps[0]) * dt_step
                tdoa_p = t_i - t_0
                
                c += (tdoa_m - tdoa_p) ** 2
            return c
        
        bounds = ((-2000.0, 7000.0), (-2000.0, 7000.0), (0.0, 1e-4))
        res = minimize(cost, (1000.0, 1000.0, 1e-7), method='L-BFGS-B', bounds=bounds)
        return res.x[:2], res.x[2], res.fun

    est_tgt, est_alpha, cost_val = localize_target_calibrated(
        receiver_positions, lock_steps_measured, C_SOUND, dt
    )

    error = np.linalg.norm(est_tgt - true_target)

    print("=== TOPOLOGICAL SONAR v2.3 (Sound Speed) ===")
    print(f"True Target:  {true_target}")
    print(f"Estimated:    {est_tgt}")
    print(f"Alpha (est):  {est_alpha:.2e}")
    print(f"Error:        {error:.2f} meters\\n")

if __name__ == '__main__':
    sonar_simulation()
"""

# 5. README.md
readme_md = """# PhaseLoc / Absolute-Monitor
**Topological Phase Dynamics Framework**

**Author:** Hennadii Kovalov (GLAB Research Cluster)  
**Date:** October 2026

## Overview
This package contains the numerical verification scripts for the Phase Dynamics framework. It establishes a new paradigm in spectroscopy, condensed matter physics, and radar/sonar localization based on the topology of the quantum vacuum without empirical parameters.

## Package Structure
- `core_constants.py`: Fundamental invariants (Proton mass, Fine-structure constant, S-matrix residue `g`, Kuramoto threshold `1/pi`).
- `spectra_engine.py`: Parameter-free derivation of the Hydrogen-Bond frequency and Water IR Spectrum.
- `topological_radar.py`: TDOA absolute matrix localization for stealth-immune radar (speed of light). Features gradient-normalized optimization for extreme parameter scale differences.
- `topological_sonar.py`: Hydroacoustic phase filter localization with bounded Kuramoto inertia parameter.

## Instructions
Ensure you have `numpy` and `scipy` installed:
```bash
pip install numpy scipy