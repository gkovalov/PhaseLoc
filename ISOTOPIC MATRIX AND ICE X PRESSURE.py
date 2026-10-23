python
# ============================================================
# ISOTOPIC MATRIX AND ICE X PRESSURE
# GLAB Research Cluster - Phase Dynamics Framework
# ============================================================
import numpy as np

# Fundamental Constants
ALPHA = 1.0 / 137.035999084
G_FACTOR = ((np.pi / (2 * np.sqrt(2))) * (1.0 - (ALPHA * np.pi) / 2.0))**4

# Masses (MeV/c^2)
M_P = 938.272088
M_D = 1875.612942
M_T = 2808.921132

# Base Network Mode (cm^-1)
NU_NET_H2O = 151.74

# Ice X Constants
LAMBDA_P = 1.321409855e-15  # m
EV = 1.602176634e-19

def isotopic_matrix():
    print("=== ISOTOPIC MATRIX ===")
    
    # D2O
    mass_ratio_d = M_D / M_P
    nu_net_d2o = NU_NET_H2O * mass_ratio_d
    print(f"D2O Network Mode: {nu_net_d2o:.2f} cm^-1 (Exp: 302-310)")
    
    # T2O
    mass_ratio_t = M_T / M_P
    nu_net_t2o = NU_NET_H2O * mass_ratio_t
    print(f"T2O Network Mode: {nu_net_t2o:.2f} cm^-1 (Blind-test)")

def ice_x_pressure():
    print("\n=== ICE X PRESSURE ===")
    
    # Proton energy in Joules
    E_p_joules = (M_P * 1e6) * EV
    
    # Core pressure
    P_core = E_p_joules / (LAMBDA_P ** 3)
    
    # Geometric factor
    geom_factor = 2.0 / (3.0 * np.pi)
    
    # Critical pressure
    P_critical = geom_factor * P_core * (ALPHA ** 11) * G_FACTOR
    
    print(f"Critical Pressure: {P_critical / 1e9:.2f} GPa (Exp: 60-62)")

if __name__ == "__main__":
    isotopic_matrix()
    ice_x_pressure()
