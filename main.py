# main.py
import json
import csv
import datetime
from config import HYDRO_PLANTS
from satellite_gis_fetcher import fetch_real_satellite_water_index
from physics_engine import calculate_theoretical_power, detect_operational_anomaly
from weather_sediment_engine import get_basin_rainfall, calculate_ndti_sediment_index

def run_hydro_audit():
    print("=" * 60)
    print("🛰️ AUDITORÍA SATELITAL GIS E HIDROLÓGICA - ECUADOR")
    print("   (Teledetección Real: Sentinel-2 + Física de Fluidos)")
    print("=" * 60)
    
    audit_results = []
    csv_rows = []
    
    # Reportes oficiales de referencia (CENACE / CELEC)
    official_reports = {
        "mazar": {"reported_power_mw": 0.0},
        "paute_molino": {"reported_power_mw": 520.0},
        "sopladora": {"reported_power_mw": 360.0},
        "coca_codo_sinclair": {"reported_power_mw": 850.0}
    }
    
    for plant_key, plant_data in HYDRO_PLANTS.items():
        print(f"\n🔍 Analizando central: {plant_data['name']}...")
        
        # 1. Extracción real / procesamiento ráster GIS
        gis_data = fetch_real_satellite_water_index(plant_key)
        
        # 2. Clima y Sedimentos
        weather = get_basin_rainfall(plant_data["lat"], plant_data["lon"])
        sediment = calculate_ndti_sediment_index(red_band=0.24, green_band=0.17)
        
        # 3. Variables físicas extraídas por teledetección
        flow_q = gis_data["derived_flow_m3s"]
        head_h = plant_data.get("max_hydraulic_head_m", 150.0) * 0.9  # Altura útil estimada
        
        # 4. Cálculo de Potencia Teórica
        power_calc = calculate_theoretical_power(plant_key, flow_q, head_h)
        
        # 5. Auditoría vs Reporte Oficial
        reported_mw = official_reports.get(plant_key, {}).get("reported_power_mw", 0.0)
        anomaly_check = detect_operational_anomaly(power_calc["calculated_power_mw"], reported_mw)
        
        plant_report = {
            "plant_key": plant_key,
            "plant_name": plant_data["name"],
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "gis_satellite_data": gis_data,
            "basin_rainfall_mm": weather["precipitation_mm"],
            "sediment_analysis": sediment,
            "physical_model": power_calc,
            "audit_anomaly": anomaly_check
        }
        audit_results.append(plant_report)
        
        csv_rows.append({
            "Plant_Key": plant_key,
            "Plant_Name": plant_data["name"],
            "Cota_msnm": gis_data["derived_water_level_msnm"],
            "Caudal_m3s": flow_q,
            "Precipitacion_mm": weather["precipitation_mm"],
            "Riesgo_Sedimentos": sediment["sediment_risk"],
            "Potencia_Calculada_MW": power_calc["calculated_power_mw"],
            "Reporte_Oficial_MW": reported_mw,
            "Estado_Auditoria": anomaly_check["status"]
        })
        
        print(f"   • Cota Derivada: {gis_data['derived_water_level_msnm']} msnm | Caudal: {flow_q} m³/s")
        print(f"   • Potencia Física Teórica: {power_calc['calculated_power_mw']} MW | Oficial: {reported_mw} MW")
        print(f"   • Estado: [{anomaly_check['status']}]")
        print("-" * 60)
        
    # Guardar reportes
    with open("audit_report.json", "w", encoding="utf-8") as f:
        json.dump(audit_results, f, indent=4, ensure_ascii=False)
        
    with open("ecuador_hydro_audit.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Plant_Key", "Plant_Name", "Cota_msnm", "Caudal_m3s", "Precipitacion_mm", "Riesgo_Sedimentos", "Potencia_Calculada_MW", "Reporte_Oficial_MW", "Estado_Auditoria"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_rows:
            writer.writerow(row)
            
    print("\n✅ Archivos 'audit_report.json' y 'ecuador_hydro_audit.csv' actualizados con motor GIS.")

if __name__ == "__main__":
    run_hydro_audit()