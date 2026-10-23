# main.py (Actualizado con Clima y Sedimentos)
import json
import csv
import datetime
from config import HYDRO_PLANTS
from satellite_fetcher import fetch_reservoir_satellite_data
from physics_engine import calculate_theoretical_power, detect_operational_anomaly
from weather_sediment_engine import get_basin_rainfall, calculate_ndti_sediment_index

def run_hydro_audit():
    print("=" * 60)
    print("🛰️ AUDITORÍA SATELITAL E HIDROLÓGICA INTEGRAL - ECUADOR")
    print("   (Cruza: Satélite + Clima + CELEC / CENACE)")
    print("=" * 60)
    
    audit_results = []
    csv_rows = []
    
    # Datos extraídos/simulados del panel oficial de CELEC y CENACE
    official_reports = {
        "mazar": {"reported_power_mw": 0.0, "reported_cota_msnm": 2122.50},  # Mazar reporta 0 MW en captura
        "paute_molino": {"reported_power_mw": 520.0, "reported_cota_msnm": 1975.0},
        "sopladora": {"reported_power_mw": 360.0, "reported_cota_msnm": 1315.4},
        "coca_codo_sinclair": {"reported_power_mw": 850.0, "reported_cota_msnm": 1220.0}
    }
    
    for plant_key, plant_data in HYDRO_PLANTS.items():
        sat_data = fetch_reservoir_satellite_data(plant_key)
        metrics = sat_data["reservoir_metrics"]
        
        # 1. Clima y Sedimentos
        weather = get_basin_rainfall(plant_data["lat"], plant_data["lon"])
        sediment = calculate_ndti_sediment_index(red_band=0.25, green_band=0.18) # Reflexión espectral
        
        # 2. Modelo Físico
        flow_q = metrics["estimated_flow_m3s"]
        head_h = metrics["current_head_m"]
        power_calc = calculate_theoretical_power(plant_key, flow_q, head_h)
        
        # 3. Comparativa vs Reporte Oficial
        official = official_reports.get(plant_key, {})
        reported_mw = official.get("reported_power_mw", 0.0)
        anomaly_check = detect_operational_anomaly(power_calc["calculated_power_mw"], reported_mw)
        
        plant_report = {
            "plant_key": plant_key,
            "plant_name": plant_data["name"],
            "timestamp": sat_data["timestamp"],
            "basin_rainfall_mm": weather["precipitation_mm"],
            "sediment_analysis": sediment,
            "physical_model": power_calc,
            "audit_anomaly": anomaly_check
        }
        audit_results.append(plant_report)
        
        csv_rows.append({
            "Plant_Key": plant_key,
            "Plant_Name": plant_data["name"],
            "Precipitacion_mm": weather["precipitation_mm"],
            "Riesgo_Sedimentos": sediment["sediment_risk"],
            "Caudal_m3s": flow_q,
            "Potencia_Calculada_MW": power_calc["calculated_power_mw"],
            "Reporte_Oficial_MW": reported_mw,
            "Estado_Auditoria": anomaly_check["status"]
        })
        
        print(f"\n📍 {plant_data['name']}")
        print(f"   • Lluvia en cuenca: {weather['precipitation_mm']} mm | Sedimentos: {sediment['sediment_risk']}")
        print(f"   • Potencia Teórica: {power_calc['calculated_power_mw']} MW | Reportado Oficial: {reported_mw} MW")
        print(f"   • Estado: [{anomaly_check['status']}]")
        print("-" * 60)
        
    with open("audit_report.json", "w", encoding="utf-8") as f:
        json.dump(audit_results, f, indent=4, ensure_ascii=False)
        
    with open("ecuador_hydro_audit.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Plant_Key", "Plant_Name", "Precipitacion_mm", "Riesgo_Sedimentos", "Caudal_m3s", "Potencia_Calculada_MW", "Reporte_Oficial_MW", "Estado_Auditoria"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_rows:
            writer.writerow(row)
            
    print("\n✅ Auditoría con integración de Clima y Sedimentos completada con éxito.")

if __name__ == "__main__":
    run_hydro_audit()