import json
import csv
import datetime
from config import HYDRO_PLANTS
from satellite_fetcher import fetch_reservoir_satellite_data
from physics_engine import calculate_theoretical_power, detect_operational_anomaly

def run_hydro_audit():
    print("=" * 60)
    print("🛰️ AUDITORÍA SATELITAL DE HIDROELÉCTRICAS - ECUADOR")
    print("   (Monitoreo Independiente y Verificación Física - CELEC / CENACE)")
    print("=" * 60)
    
    audit_results = []
    csv_rows = []
    
    official_reports = {
        "mazar": {"reported_power_mw": 85.0},
        "paute_molino": {"reported_power_mw": 520.0},
        "sopladora": {"reported_power_mw": 360.0},
        "coca_codo_sinclair": {"reported_power_mw": 850.0}
    }
    
    for plant_key, plant_data in HYDRO_PLANTS.items():
        print(f"\n🔍 Procesando datos para: {plant_data['name']}...")
        
        sat_data = fetch_reservoir_satellite_data(plant_key)
        metrics = sat_data["reservoir_metrics"]
        
        flow_q = metrics["estimated_flow_m3s"]
        head_h = metrics["current_head_m"]
        
        power_calc = calculate_theoretical_power(plant_key, flow_q, head_h)
        
        reported_mw = official_reports.get(plant_key, {}).get("reported_power_mw", 0.0)
        anomaly_check = detect_operational_anomaly(
            calculated_power_mw=power_calc["calculated_power_mw"],
            reported_power_mw=reported_mw
        )
        
        plant_report = {
            "plant_key": plant_key,
            "plant_name": plant_data["name"],
            "timestamp": sat_data["timestamp"],
            "satellite_metrics": metrics,
            "physical_model": power_calc,
            "audit_anomaly": anomaly_check
        }
        audit_results.append(plant_report)
        
        csv_rows.append({
            "Plant_Key": plant_key,
            "Plant_Name": plant_data["name"],
            "Caudal_m3s": flow_q,
            "Caida_m": head_h,
            "Potencia_Calculada_MW": power_calc["calculated_power_mw"],
            "Reporte_Oficial_MW": reported_mw,
            "Turbinas_Activas": power_calc["estimated_active_turbines"],
            "Estado_Auditoria": anomaly_check["status"]
        })
        
        print(f"   • Nivel / Caudal: {metrics['water_level_m']} msnm | {flow_q} m³/s")
        print(f"   • Potencia Física Teórica: {power_calc['calculated_power_mw']} MW")
        print(f"   • Estado: [{anomaly_check['status']}]")
        print("-" * 60)
        
    with open("audit_report.json", "w", encoding="utf-8") as f:
        json.dump(audit_results, f, indent=4, ensure_ascii=False)
        
    csv_filename = "ecuador_hydro_audit.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Plant_Key", "Plant_Name", "Caudal_m3s", "Caida_m", "Potencia_Calculada_MW", "Reporte_Oficial_MW", "Turbinas_Activas", "Estado_Auditoria"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_rows:
            writer.writerow(row)
            
    print(f"\n✅ Archivos generados con éxito: 'audit_report.json' y '{csv_filename}'.")

if __name__ == "__main__":
    run_hydro_audit()