import sys

class Junction:
    def __init__(self, junction_id, vehicle_count, average_speed, accident_count, signal_delay, pollution_index, peak_hour_traffic):
        self.junction_id = junction_id
        self.vehicle_count = vehicle_count
        self.average_speed = average_speed
        self.accident_count = accident_count
        self.signal_delay = signal_delay
        self.pollution_index = pollution_index
        self.peak_hour_traffic = peak_hour_traffic
        
        # Requirement 1: Calculate Congestion Score
        self.congestion_score = self.calculate_congestion()

    def calculate_congestion(self):
        if self.average_speed <= 0:
            return 0.0
        # Formula: (Vehicle Count * Signal Delay) / Average Speed
        return (self.vehicle_count * self.signal_delay) / self.average_speed

def main():
    # Sample Dataset
    junctions = [
        Junction("J001", 1200, 25.0, 5, 45, 180, True),
        Junction("J002", 850, 40.0, 1, 20, 95, False),
        Junction("J003", 2100, 15.0, 8, 90, 240, True),
        Junction("J004", 450, 50.0, 0, 10, 60, False),
        Junction("J005", 1600, 20.0, 4, 60, 210, True),
        Junction("J006", 1900, 18.0, 2, 75, 190, True),
        Junction("J007", 700, 35.0, 6, 30, 110, False)
    ]

    print("==================================================")
    print("      SMART CITY TRAFFIC ANALYTICS SYSTEM        ")
    print("==================================================\n")

    # Requirement 9 & 2: Sort and Rank Junctions by Congestion
    sorted_junctions = sorted(junctions, key=lambda x: x.congestion_score, reverse=True)

    print("--- 2 & 9. Junction Rankings (Sorted by Congestion Score) ---")
    for rank, j in enumerate(sorted_junctions, start=1):
        print(f"Rank {rank}: {j.junction_id} | Congestion Score: {j.congestion_score:.2f}")

    # Requirement 3: Identify Accident-Prone Areas (Accidents >= 4)
    print("\n--- 3. Accident-Prone Areas ---")
    accident_prone = [j for j in junctions if j.accident_count >= 4]
    for j in accident_prone:
        print(f"Junction: {j.junction_id} | Accident Count: {j.accident_count}")

    # Requirement 4: Display Heavily Polluted Junctions (Pollution Index > 150)
    print("\n--- 4. Heavily Polluted Junctions ---")
    polluted = [j for j in junctions if j.pollution_index > 150]
    for j in polluted:
        print(f"Junction: {j.junction_id} | Pollution Index: {j.pollution_index}")

    # Requirement 5: Calculate City Average Congestion
    total_congestion = sum(j.congestion_score for j in junctions)
    city_avg_congestion = total_congestion / len(junctions)
    print(f"\n--- 5. City Average Congestion ---")
    print(f"Average Congestion Score: {city_avg_congestion:.2f}")

    # Requirement 6: Find the Busiest Junction (Highest Vehicle Count)
    busiest_junction = max(junctions, key=lambda x: x.vehicle_count)
    print(f"\n--- 6. Busiest Junction ---")
    print(f"Junction ID: {busiest_junction.junction_id} | Vehicle Count: {busiest_junction.vehicle_count}")

    # Requirement 7 & 8: Generate Traffic Alerts and Save to File
    alerts = []
    for j in junctions:
        if j.congestion_score > 3000:
            alerts.append(f"HIGH CONGESTION ALERT: {j.junction_id} has a score of {j.congestion_score:.2f}")
        if j.accident_count >= 4:
            alerts.append(f"ACCIDENT RISK ALERT: {j.junction_id} reported {j.accident_count} accidents.")
        if j.pollution_index > 150:
            alerts.append(f"POLLUTION WARNING: {j.junction_id} Pollution Index is critical ({j.pollution_index}).")

    print("\n--- 7. Generated Traffic Alerts ---")
    for alert in alerts:
        print(f"- {alert}")

    # Requirement 8: Save Alerts to File
    file_name = "traffic_alerts.txt"
    with open(file_name, "w") as f:
        for alert in alerts:
            f.write(f"{alert}\n")
    print(f"\n--- 8. File Output ---")
    print(f"Successfully saved {len(alerts)} alert(s) to '{file_name}'.")

    # Requirement 10: Display Top 5 Congestion Points
    print("\n--- 10. Top 5 Congestion Points ---")
    for j in sorted_junctions[:5]:
        print(f"Junction ID: {j.junction_id} | Vehicles: {j.vehicle_count} | Delay: {j.signal_delay}s | Speed: {j.average_speed}km/h | Score: {j.congestion_score:.2f}")

if __name__ == "__main__":
    main()
