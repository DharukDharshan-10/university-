import json
import os

# Sample dataset of IoT machines stored as dictionaries
machine_data = [
    {
        "Machine_ID": "M001",
        "Plant_Name": "Plant Alpha",
        "Operating_Hours": 200,
        "Downtime": 10,
        "Energy_Consumption": 1500.0,
        "Units_Produced": 4500,
        "Maintenance_Cost": 1200.0
    },
    {
        "Machine_ID": "M002",
        "Plant_Name": "Plant Alpha",
        "Operating_Hours": 200,
        "Downtime": 40,
        "Energy_Consumption": 1800.0,
        "Units_Produced": 2500,
        "Maintenance_Cost": 3500.0
    },
    {
        "Machine_ID": "M003",
        "Plant_Name": "Plant Beta",
        "Operating_Hours": 180,
        "Downtime": 5,
        "Energy_Consumption": 1200.0,
        "Units_Produced": 4000,
        "Maintenance_Cost": 800.0
    },
    {
        "Machine_ID": "M004",
        "Plant_Name": "Plant Beta",
        "Operating_Hours": 190,
        "Downtime": 25,
        "Energy_Consumption": 1600.0,
        "Units_Produced": 3000,
        "Maintenance_Cost": 2200.0
    }
]

def calculate_metrics(data):
    """1. Calculates machine efficiency & 2. Calculates production cost per unit."""
    for machine in data:
        effective_hours = machine["Operating_Hours"] - machine["Downtime"]
        
        # Handle zero division if operating hours equals downtime
        if effective_hours > 0:
            efficiency = machine["Units_Produced"] / effective_hours
        else:
            efficiency = 0.0
        machine["Efficiency"] = round(efficiency, 2)
        
        # Total cost can be approximated using energy and maintenance or just maintenance/energy metrics
        # Production cost per unit calculation: (Energy Cost proxy + Maintenance Cost) / Units Produced
        # Assuming an energy rate of $0.10 per unit of energy consumption
        total_cost = (machine["Energy_Consumption"] * 0.10) + machine["Maintenance_Cost"]
        if machine["Units_Produced"] > 0:
            cost_per_unit = total_cost / machine["Units_Produced"]
        else:
            cost_per_unit = 0.0
        machine["Cost_Per_Unit"] = round(cost_per_unit, 2)
        
    return data

def identify_inefficient_machines(data, threshold=15.0):
    """3. Identifies inefficient machines."""
    print(f"\n--- Inefficient Machines (Efficiency < {threshold}) ---")
    inefficient = [m for m in data if m["Efficiency"] < threshold]
    for m in inefficient:
        print(f"Machine: {m['Machine_ID']} ({m['Plant_Name']}) | Efficiency: {m['Efficiency']}")
    return inefficient

def highest_maintenance_cost_machine(data):
    """4. Finds the machine with highest maintenance cost."""
    if not data:
        return None
    highest = max(data, key=lambda x: x["Maintenance_Cost"])
    print(f"\n--- Machine with Highest Maintenance Cost ---")
    print(f"Machine ID: {highest['Machine_ID']} | Plant: {highest['Plant_Name']} | Cost: ${highest['Maintenance_Cost']:,.2f}")
    return highest

def plant_wise_efficiency(data):
    """5. Calculates plant-wise efficiency."""
    plant_stats = {}
    for m in data:
        plant = m["Plant_Name"]
        if plant not in plant_stats:
            plant_stats[plant] = {"total_efficiency": 0.0, "count": 0}
        plant_stats[plant]["total_efficiency"] += m["Efficiency"]
        plant_stats[plant]["count"] += 1
        
    print(f"\n--- Plant-Wise Average Efficiency ---")
    plant_averages = {}
    for plant, stats in plant_stats.items():
        avg = stats["total_efficiency"] / stats["count"]
        plant_averages[plant] = round(avg, 2)
        print(f"Plant: {plant} | Avg Efficiency: {plant_averages[plant]}")
    return plant_averages

def display_preventive_maintenance(data):
    """6. Displays machines requiring preventive maintenance (e.g., high downtime or high maintenance cost)."""
    print(f"\n--- Machines Requiring Preventive Maintenance ---")
    required = [m for m in data if m["Downtime"] > 20 or m["Maintenance_Cost"] > 2000.0]
    for m in required:
        print(f"Machine: {m['Machine_ID']} | Downtime: {m['Downtime']} hrs | Maint Cost: ${m['Maintenance_Cost']:,.2f}")
    return required

def sort_machines_by_efficiency(data):
    """7. Sorts machines by efficiency."""
    sorted_data = sorted(data, key=lambda x: x["Efficiency"], reverse=True)
    print(f"\n--- Machines Sorted by Efficiency (Descending) ---")
    for m in sorted_data:
        print(f"Machine: {m['Machine_ID']} | Efficiency: {m['Efficiency']}")
    return sorted_data

def generate_maintenance_report(data):
    """8. Generates a maintenance report summary."""
    report = {
        "Total_Machines": len(data),
        "Details": data
    }
    print(f"\n--- Maintenance Report Generated ---")
    return report

def save_report_to_file(report, filename="maintenance_report.json"):
    """9. Saves report to file."""
    with open(filename, 'w') as f:
        json.dump(report, f, indent=4)
    print(f"[System]: Report successfully saved to {filename}")

def read_report_from_file(filename="maintenance_report.json"):
    """10. Reads the report."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            report = json.load(f)
        print(f"\n--- Reading Report Back From File ({filename}) ---")
        print(f"Total Machines Logged: {report.get('Total_Machines')}")
        for m in report.get("Details", []):
            print(f" - {m['Machine_ID']} | Plant: {m['Plant_Name']} | Efficiency: {m['Efficiency']}")
        return report
    else:
        print(f"[System Error]: Report file {filename} not found.")
        return None

if __name__ == "__main__":
    print("=== Industrial IoT Machine Performance Monitoring Started ===")
    processed_data = calculate_metrics(machine_data)
    
    identify_inefficient_machines(processed_data)
    highest_maintenance_cost_machine(processed_data)
    plant_wise_efficiency(processed_data)
    display_preventive_maintenance(processed_data)
    
    sorted_data = sort_machines_by_efficiency(processed_data)
    report = generate_maintenance_report(sorted_data)
    
    save_report_to_file(report)
    read_report_from_file()
    print("\n=== Execution Completed Successfully ===")
