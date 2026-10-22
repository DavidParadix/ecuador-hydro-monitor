# satellite_fetcher.py

import datetime
from config import HYDRO_PLANTS

def fetch_reservoir_satellite_data(plant_key: str) -> dict:
    """
    Simulación de ingesta desde satélites Copernicus Sentinel-1/2 o Landsat-8.
    En la versión conectada a API descargará las imágenes ráster NDWI en tiempo real.
    """
    plant = HYDRO_PLANTS.get(plant_key)
    if not plant:
        return {}
    
    # Mock data para estructurar el flujo de datos inicial de la arquitectura
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Ejemplo de valores simulados de telemetría remota
    mock_satellite_metrics = {
        "mazar": {"water_area_km2": 8.45, "water_level_m": 2140.2, "estimated_flow_m3s": 110.0, "current_head_m": 142.0},
        "paute_molino": {"water_area_km2": 1.20, "water_level_m": 1980.0, "estimated_flow_m3s": 120.0, "current_head_m": 620.0},
        "coca_codo_sinclair": {"water_area_km2": 0.85, "water_level_m": 1220.0, "estimated_flow_m3s": 290.0, "current_head_m": 580.0}
    }
    
    metrics = mock_satellite_metrics.get(plant_key, {"estimated_flow_m3s": 0.0, "current_head_m": 0.0})
    
    return {
        "plant_key": plant_key,
        "timestamp": timestamp,
        "coordinates": {"lat": plant["lat"], "lon": plant["lon"]},
        "satellite_source": "Copernicus Sentinel-2 L2A",
        "reservoir_metrics": metrics
    }