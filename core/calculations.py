import math

def calculate_flexible_duct(
    duct_diameter_in: float,
    air_flow_cfm: float,
    duct_length_ft: float,
    bend_counts: dict,
    roughness_value: float,
    compression_percent: float,
    safety_factor: float,
):
    dh_ft = duct_diameter_in / 12.0
    a_duct = math.pi * (dh_ft ** 2) / 4.0
    velocity_fpm = air_flow_cfm / a_duct if a_duct > 0 else float("inf")

    re_number = 8.50 * duct_diameter_in * velocity_fpm

    try:
        f_factor = 0.25 / (
            math.log10(
                (roughness_value / (3.7 * duct_diameter_in))
                + (5.74 / (re_number ** 0.9))
            )
        ) ** 2
    except (ValueError, ZeroDivisionError):
        f_factor = 0.0

    leq = (
        bend_counts.get("45", 0) * 10
        + bend_counts.get("90", 0) * 20
        + bend_counts.get("180", 0) * 40
    )

    rho_air = 0.075
    pf = (
        (12 * f_factor * (duct_length_ft + leq)) / duct_diameter_in
    ) * rho_air * ((velocity_fpm / 1097) ** 2)

    kc = compression_percent
    pdcf = 1 + 0.58 * kc * math.exp(-0.126 * duct_diameter_in)

    total_pressure_loss = pf * pdcf * safety_factor

    details = {
        "Area (ft²)": a_duct,
        "Velocity (FPM)": velocity_fpm,
        "Reynolds Number": re_number,
        "Friction Factor (f)": f_factor,
        "Equivalent Length (ft)": leq,
        "Raw Pf (in.w.g.)": pf,
        "PDCF": pdcf,
        "Safety Factor": safety_factor,
        "Total ΔP (in.w.g.)": total_pressure_loss,
    }

    return velocity_fpm, total_pressure_loss, details
