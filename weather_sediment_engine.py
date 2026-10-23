# weather_sediment_engine.py
import requests

def get_basin_rainfall(lat: float, lon: float) -> dict:
    """
    Consulta lluvias acumuladas en la cuenca mediante API de clima abierto (Open-Meteo)
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_sum&timezone=auto"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            daily_rain = data.get("daily", {}).get("precipitation_sum", [0])[0]
            return {"precipitation_mm": daily_rain, "status": "OK"}
    except Exception as e:
        pass
    # Valor de respaldo simulado si no hay conexión
    return {"precipitation_mm": 12.5, "status": "SIMULATED"}

def calculate_ndti_sediment_index(red_band: float, green_band: float) -> dict:
    """
    Calcula el Índice de Turbidez y Sedimentos por Diferencia Normalizada (NDTI):
    NDTI = (Red - Green) / (Red + Green)
    """
    if (red_band + green_band) == 0:
        return {"ndti": 0.0, "risk_level": "DESCONOCIDO"}
    
    ndti = (red_band - green_band) / (red_band + green_band)
    
    if ndti > 0.2:
        risk = "ALTO RIESGO DE SEDIMENTOS (Erosión en turbinas)"
    elif ndti > 0.0:
        risk = "MODERADO (Monitorear desarenadores)"
    else:
        risk = "BAJO (Agua clara)"
        
    return {
        "ndti_value": round(ndti, 3),
        "sediment_risk": risk
    }