"""Reusable engine calculation helpers for S2-Engine.

All SI units unless noted. Results are [calculated] estimates.
"""

import math


def displacement_single(bore_m, stroke_m):
    """Swept volume of one cylinder (m^3)."""
    return math.pi / 4.0 * bore_m**2 * stroke_m


def total_displacement(bore_m, stroke_m, n_cyl):
    """Total displacement (m^3)."""
    return displacement_single(bore_m, stroke_m) * n_cyl


def compression_ratio(vs_m3, vc_m3):
    """CR = (Vs + Vc)/Vc."""
    return (vs_m3 + vc_m3) / vc_m3


def otto_efficiency(cr, gamma=1.4):
    """Ideal Otto thermal efficiency."""
    return 1.0 - 1.0 / (cr ** (gamma - 1.0))


def brake_power_from_bmeP(bmep_pa, vd_m3, n_rpm):
    """Brake power (W) for 4-stroke from BMEP."""
    return bmep_pa * vd_m3 * n_rpm / (2 * 60)


def torque_from_power(bp_w, n_rpm):
    """Torque (N·m) from brake power (W) and rpm."""
    return bp_w * 60.0 / (2 * math.pi * n_rpm)


def mean_piston_speed(stroke_m, n_rpm):
    """Mean piston speed (m/s) for 4-stroke."""
    return 2.0 * stroke_m * n_rpm / 60.0


def fuel_mass_flow(bp_w, eta_b, lhv_j_per_kg):
    """Fuel mass flow (kg/s)."""
    return bp_w / (eta_b * lhv_j_per_kg)


def bsfc_g_per_kwh(mdot_f_kg_s, bp_w):
    """BSFC in g/kWh."""
    if bp_w == 0:
        return float("inf")
    return (mdot_f_kg_s * 3600.0 * 1e6) / bp_w


def heat_input_rate(mdot_f_kg_s, lhv_j_per_kg):
    return mdot_f_kg_s * lhv_j_per_kg


if __name__ == "__main__":
    # Worked example: 2.0L 4-cyl, 86x86 mm
    B = 0.086
    S = 0.086
    n = 4
    Vd = total_displacement(B, S, n)
    print(f"Displacement: {Vd*1e6:.1f} cc")
    Vs_cyl = displacement_single(B, S)
    Vc = 45e-6  # 45 cc clearance
    cr = compression_ratio(Vs_cyl, Vc)
    print(f"Compression ratio: {cr:.2f}")
    print(f"Otto efficiency (ideal): {otto_efficiency(cr)*100:.1f}%")
    print(f"Mean piston speed @6000rpm: {mean_piston_speed(S, 6000):.1f} m/s")
    bmep = 10e5  # 10 bar
    bp = brake_power_from_bmeP(bmep, Vd, 5000)
    print(f"Brake power @5000rpm, 10bar BMEP: {bp/1000:.1f} kW ({bp/745.7:.1f} hp)")
    print(f"Torque: {torque_from_power(bp, 5000):.1f} N·m")
    # Ethanol LHV ~26.8 MJ/kg
    mdot = fuel_mass_flow(bp, 0.32, 26.8e6)
    print(f"Fuel mass flow: {mdot*3600:.2f} kg/h")
    print(f"BSFC: {bsfc_g_per_kwh(mdot, bp):.1f} g/kWh")