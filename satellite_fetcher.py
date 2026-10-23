import datetime
from config import HYDRO_PLANTS

def fetch_reservoir_satellite_data(plant_key: str) -> dict:
    plant = HYDRO_PLANTS.get(plant_key)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    mock_satellite_metrics = {
        "mazar": {"water_area_km2": 8.45, "water_level_m": 2140.2, "estimated_flow_m3s": 110.0, "current_head_m": 142.0},
        "paute_molino": {"water_area_km2": 1.20, "water_level_m": 1980.0, "estimated_flow_m3s": 105.0, "current_head_m": 620.0},
        "sopladora": {"water_area_km2": 0.95, "water_level_m": 1310.0, "estimated_flow_m3s": 130.0, "current_head_m": 340.0},
        "coca_codo_sinclair": {"water_area_km2": 0.85, "water_level_m": 1220.0, "estimated_flow_m3s": 180.0, "current_head_m": 580.0}
    }
    metrics = mock_satellite_metrics.get(plant_key, {"estimated_flow_m3s": 0.0, "current_head_m": 0.0})
    
    return {
        "plant_key": plant_key,
        "timestamp": timestamp,
        "coordinates": {"lat": plant["lat"], "lon": plant["lon"]},
        "satellite_source": "Copernicus Sentinel-2 / Landsat-8",
        "reservoir_metrics": metrics
    }