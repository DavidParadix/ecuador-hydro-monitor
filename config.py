# config.py

# Coordenadas geográficas y parámetros nominales de las centrales
HYDRO_PLANTS = {
    "mazar": {
        "name": "Embalse Mazar (Complejo Paute)",
        "lat": -2.6325,
        "lon": -78.6180,
        "nominal_capacity_mw": 170.0,
        "turbines_count": 2,
        "max_hydraulic_head_m": 158.0,  # Altura de caída nominal
        "efficiency_factor": 0.90       # Eficiencia general (turbina + generador)
    },
    "paute_molino": {
        "name": "Central Paute-Molino",
        "lat": -2.5760,
        "lon": -78.5550,
        "nominal_capacity_mw": 1100.0,
        "turbines_count": 10,
        "max_hydraulic_head_m": 660.0,
        "efficiency_factor": 0.91
    },
    "coca_codo_sinclair": {
        "name": "Central Coca Codo Sinclair",
        "lat": -0.1008,
        "lon": -77.6833,
        "nominal_capacity_mw": 1500.0,
        "turbines_count": 8,
        "max_hydraulic_head_m": 620.0,
        "efficiency_factor": 0.88
    }
}

# Constantes físicas
DENSITY_WATER_KG_M3 = 1000.0  # ρ (kg/m³)
GRAVITY_M_S2 = 9.81           # g (m/s²)