# physics_engine.py

from config import DENSITY_WATER_KG_M3, GRAVITY_M_S2, HYDRO_PLANTS

def calculate_theoretical_power(plant_key: str, flow_rate_m3s: float, current_head_m: float) -> dict:
    """
    Calcula la potencia teórica generable basada en física de fluidos:
    P (Watts) = eta * rho * g * Q * H
    """
    if plant_key not in HYDRO_PLANTS:
        raise ValueError(f"Planta {plant_key} no registrada en la configuración.")
    
    plant_info = HYDRO_PLANTS[plant_key]
    eta = plant_info["efficiency_factor"]
    
    # Potencia en Watts -> Megawatts (MW)
    power_watts = eta * DENSITY_WATER_KG_M3 * GRAVITY_M_S2 * flow_rate_m3s * current_head_m
    power_mw = power_watts / 1e6
    
    # Capacidad máxima permitida físicamente según la ficha técnica
    capacity_limit = plant_info["nominal_capacity_mw"]
    estimated_power = min(power_mw, capacity_limit)
    
    # Estimación de cuantas turbinas estarían operando activamente
    avg_power_per_turbine = capacity_limit / plant_info["turbines_count"]
    estimated_active_turbines = round(estimated_power / avg_power_per_turbine, 1)
    
    return {
        "plant_name": plant_info["name"],
        "calculated_power_mw": round(estimated_power, 2),
        "nominal_capacity_mw": capacity_limit,
        "capacity_factor_pct": round((estimated_power / capacity_limit) * 100, 2),
        "estimated_active_turbines": min(estimated_active_turbines, plant_info["turbines_count"]),
        "total_turbines": plant_info["turbines_count"]
    }

def detect_operational_anomaly(calculated_power_mw: float, reported_power_mw: float, tolerance_pct: float = 15.0) -> dict:
    """
    Compara la generación reportada vs. la potencia física teórica calculada vía satélite.
    """
    diff_mw = reported_power_mw - calculated_power_mw
    diff_pct = (diff_mw / calculated_power_mw) * 100 if calculated_power_mw > 0 else 0
    
    has_anomaly = abs(diff_pct) > tolerance_pct
    
    status = "NORMAL"
    description = "La producción reportada coincide con la capacidad física disponible."
    
    if has_anomaly:
        if diff_pct < -tolerance_pct:
            status = "SUBGENERACION / POSIBLE FALLA MECANICA"
            description = (
                f"La central reporta {reported_power_mw} MW, pero hay agua y caída física para generar "
                f"{calculated_power_mw} MW. Posible apagado no programado o falla de turbinas."
            )
        else:
            status = "SOBREDECLARACION INCONSISTENTE"
            description = "La generación reportada supera el límite físicamente posible para el nivel y caudal actual."
            
    return {
        "status": status,
        "calculated_power_mw": calculated_power_mw,
        "reported_power_mw": reported_power_mw,
        "difference_mw": round(diff_mw, 2),
        "discrepancy_pct": round(diff_pct, 2),
        "description": description
    }