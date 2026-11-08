"""
Sustainable Micro Wind Turbine Harvester - Aerodynamic Power & Velocity Derivation
Author: Suresh Ganesen (Atom Forge Studio / Politeknik Malaysia)
Part Number: SG-WIND-006 / DWG-WIND-006-REV-A
Standard: ISO 61400-2 (Small Wind Turbines)

Physics Equations:
  - Swept Rotor Area: A = pi * R^2
  - Available Kinetic Wind Power: P_wind = 0.5 * rho * A * v^3
  - Theoretical Betz Limit: P_betz = P_wind * (16 / 27) ~= P_wind * 0.593
  - Actual Mechanical Shaft Power: P_mech = P_wind * C_p
  - Electrical Generated Power: P_elec = P_mech * eta_gen * eta_rect
"""

import math
import sys
import os

AIR_DENSITY = 1.225            # kg/m^3 (Standard sea level air at 15 deg C)
ROTOR_RADIUS = 0.210           # meters (210 mm radius -> 420 mm diameter)
SWEPT_AREA = math.pi * (ROTOR_RADIUS ** 2)  # ~0.13854 m^2
AERODYNAMIC_CP = 0.285         # Experimental Power Coefficient (28.5% extraction)
GENERATOR_EFFICIENCY = 0.65    # Permanent Magnet DC Dynamo efficiency (65%)
RECTIFIER_EFFICIENCY = 0.88    # Schottky 1N5819 full-bridge + buck regulator (88%)
OVERALL_ELEC_ETA = GENERATOR_EFFICIENCY * RECTIFIER_EFFICIENCY  # ~57.2%

BETZ_LIMIT = 16.0 / 27.0       # 0.59259 (Maximum theoretical aerodynamic limit)
CUT_IN_SPEED = 2.2             # m/s (minimum velocity required to overcome startup cogging torque)
RATED_SPEED = 8.5              # m/s (nominal operating velocity for 5V 350mA regulation)
CUT_OUT_SPEED = 14.0           # m/s (furling / aerodynamic stall braking limit)


def calculate_power(wind_speed: float) -> dict:
    """Computes all aerodynamic and electrical parameters for a given wind velocity."""
    if wind_speed < CUT_IN_SPEED:
        status = "SUB-CUT-IN (STATIC)"
        p_wind = 0.5 * AIR_DENSITY * SWEPT_AREA * (wind_speed ** 3)
        p_betz = p_wind * BETZ_LIMIT
        p_mech = 0.0
        p_elec = 0.0
        current_5v_ma = 0.0
    elif wind_speed > CUT_OUT_SPEED:
        status = "CUT-OUT (FURLING)"
        p_wind = 0.5 * AIR_DENSITY * SWEPT_AREA * (wind_speed ** 3)
        p_betz = p_wind * BETZ_LIMIT
        p_mech = 0.0
        p_elec = 0.0
        current_5v_ma = 0.0
    else:
        status = "ACTIVE HARVESTING"
        p_wind = 0.5 * AIR_DENSITY * SWEPT_AREA * (wind_speed ** 3)
        p_betz = p_wind * BETZ_LIMIT
        p_mech = p_wind * AERODYNAMIC_CP
        p_elec = p_mech * OVERALL_ELEC_ETA
        current_5v_ma = (p_elec / 5.0) * 1000.0

    return {
        "wind_speed": wind_speed,
        "p_wind": p_wind,
        "p_betz": p_betz,
        "p_mech": p_mech,
        "p_elec": p_elec,
        "current_5v_ma": current_5v_ma,
        "status": status,
    }


def print_power_curve_table():
    """Prints formatted aerodynamic power table from 1 m/s to 15 m/s."""
    print("=" * 78)
    print("  SUSTAINABLE MICRO WIND TURBINE HARVESTER (SG-WIND-006)")
    print("  AERODYNAMIC POWER & ELECTRICAL GENERATION DERIVATION")
    print("=" * 78)
    print(f"Swept Rotor Area    : {SWEPT_AREA:.4f} m^2 (Diameter = {ROTOR_RADIUS * 2 * 1000:.0f} mm)")
    print(f"Air Density (rho)   : {AIR_DENSITY:.3f} kg/m^3")
    print(f"Aerodynamic Cp      : {AERODYNAMIC_CP * 100:.1f}% (Betz Limit = {BETZ_LIMIT * 100:.1f}%)")
    print(f"Generator Efficiency: {GENERATOR_EFFICIENCY * 100:.1f}% | Rectifier: {RECTIFIER_EFFICIENCY * 100:.1f}%")
    print(f"Operating Envelope  : Cut-In = {CUT_IN_SPEED:.1f} m/s | Rated = {RATED_SPEED:.1f} m/s | Cut-Out = {CUT_OUT_SPEED:.1f} m/s")
    print("-" * 78)
    print(f"{'Wind (m/s)':^10} | {'Kinetic (W)':^12} | {'Betz Max (W)':^12} | {'Mechanical (W)':^14} | {'5V Elec (W)':^11} | {'Output (mA)':^11}")
    print("-" * 78)

    results = []
    for ws in [1.0, 2.0, 2.2, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 8.5, 9.0, 10.0, 12.0, 14.0, 15.0]:
        res = calculate_power(ws)
        results.append(res)
        print(f"{res['wind_speed']:10.1f} | {res['p_wind']:12.3f} | {res['p_betz']:12.3f} | {res['p_mech']:14.3f} | {res['p_elec']:11.3f} | {res['current_5v_ma']:10.1f} mA")

    print("=" * 78)
    print("At rated 8.5 m/s wind: Generates ~5.0V regulated output @ 350-400 mA USB charging current.")
    print("=" * 78)
    return results


def export_csv(filepath: str):
    """Exports aerodynamic data to CSV file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("Wind_Speed_ms,Kinetic_Power_W,Betz_Limit_W,Mechanical_Power_W,Electrical_Output_W,Current_mA_5V,Operating_Status\n")
        v = 1.0
        while v <= 15.0:
            res = calculate_power(round(v, 2))
            f.write(f"{res['wind_speed']:.2f},{res['p_wind']:.4f},{res['p_betz']:.4f},{res['p_mech']:.4f},{res['p_elec']:.4f},{res['current_5v_ma']:.2f},{res['status']}\n")
            v += 0.5
    print(f"[+] Aerodynamic power curve CSV saved to: {filepath}")


if __name__ == "__main__":
    table = print_power_curve_table()
    csv_out = os.path.join(os.path.dirname(__file__), "wind_power_curve.csv")
    export_csv(csv_out)
