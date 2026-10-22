# main.py

import json
from config import HYDRO_PLANTS
from satellite_fetcher import fetch_reservoir_satellite_data
from physics_engine import calculate_theoretical_power, detect_operational_anomaly

def run_hydro_audit():
    print("=" * 60)
    print("🛰️ AUDITORÍA SATELITAL DE HIDROELÉCTRICAS - ECUADOR")
    print("   (Monitoreo Independiente y Verificación Física)")
    print("=" * 60)
    
    audit_results = []
    
    # Datos reportados oficiales simulados (para comparar contra la física satelital)
    # En producción, estos valores se pueden extraer de boletines o APIs abiertas oficiales.
    official_reports = {
        "mazar": {"reported_power_mw": 85.0},          # Ejemplo: reporte oficial actual
        "paute_molino": {"reported_power_mw": 520.0},
        "coca_codo_sinclair": {"reported_power_mw": 850.0}
    }
    
    for plant_key in HYDRO_PLANTS.keys():
        print(f"\n🔍 Procesando datos satelitales para: {HYDRO_PLANTS[plant_key]['name']}...")
        
        # 1. Obtener datos derivados del satélite (Caudal y Altura de embalse)
        sat_data = fetch_reservoir_satellite_data(plant_key)
        metrics = sat_data["reservoir_metrics"]
        
        flow_q = metrics["estimated_flow_m3s"]
        head_h = metrics["current_head_m"]
        
        # 2. Calcular la potencia teórica con el motor físico
        power_calc = calculate_theoretical_power(plant_key, flow_q, head_h)
        
        # 3. Comparar con lo reportado oficialmente para detectar anomalías o fallas
        reported_mw = official_reports.get(plant_key, {}).get("reported_power_mw", 0.0)
        anomaly_check = detect_operational_anomaly(
            calculated_power_mw=power_calc["calculated_power_mw"],
            reported_power_mw=reported_mw
        )
        
        # 4. Consolidar el informe de la planta
        plant_report = {
            "plant_key": plant_key,
            "timestamp": sat_data["timestamp"],
            "satellite_metrics": metrics,
            "physical_model": power_calc,
            "audit_anomaly": anomaly_check
        }
        audit_results.append(plant_report)
        
        # Imprimir resumen en consola de forma clara
        print(f"   • Nivel / Caudal estimado: {metrics['water_level_m']} msnm | {flow_q} m³/s")
        print(f"   • Potencia Física Teórica: {power_calc['calculated_power_mw']} MW (Capacidad: {power_calc['nominal_capacity_mw']} MW)")
        print(f"   • Turbinas activas estimadas: {power_calc['estimated_active_turbines']} / {power_calc['total_turbines']}")
        print(f"   • Estado de Auditoría: [{anomaly_check['status']}]")
        print(f"     -> {anomaly_check['description']}")
        print("-" * 60)
        
    # Guardar resultados en un JSON limpio (que luego consumirá tu interfaz HTML/JS)
    output_filename = "audit_report.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(audit_results, f, indent=4, ensure_ascii=False)
        
    print(f"\n✅ Auditoría finalizada con éxito. Datos guardados en '{output_filename}'.")

if __name__ == "__main__":
    run_hydro_audit()