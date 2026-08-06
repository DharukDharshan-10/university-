import json
import os

# Sample dataset of faculty research projects stored as dictionaries
faculty_data = [
    {
        "Faculty_ID": "F001",
        "Faculty_Name": "Dr. Alice Smith",
        "Department": "Computer Science",
        "Publications": 15,
        "H_index": 12,
        "Project_Budget_Requested": 120000.0,
        "Industry_Collaboration_Score": 80
    },
    {
        "Faculty_ID": "F002",
        "Faculty_Name": "Dr. Bob Jones",
        "Department": "Mechanical Engineering",
        "Publications": 20,
        "H_index": 15,
        "Project_Budget_Requested": 95000.0,
        "Industry_Collaboration_Score": 70
    },
    {
        "Faculty_ID": "F003",
        "Faculty_Name": "Dr. Carol White",
        "Department": "Computer Science",
        "Publications": 25,
        "H_index": 18,
        "Project_Budget_Requested": 150000.0,
        "Industry_Collaboration_Score": 90
    },
    {
        "Faculty_ID": "F004",
        "Faculty_Name": "Dr. David Brown",
        "Department": "Electrical Engineering",
        "Publications": 8,
        "H_index": 5,
        "Project_Budget_Requested": -5000.0,  # Invalid budget test case
        "Industry_Collaboration_Score": 40
    }
]

def validate_and_clean_data(data):
    """10. Handle invalid budgets."""
    valid_data = []
    for item in data:
        try:
            budget = item["Project_Budget_Requested"]
            if budget < 0:
                raise ValueError(f"Negative budget detected for {item['Faculty_Name']}: {budget}")
            valid_data.append(item)
        except ValueError as e:
            print(f"[Data Error Validation]: {e} -> Setting budget to 0.")
            item["Project_Budget_Requested"] = 0.0
            valid_data.append(item)
    return valid_data

def calculate_research_scores(data):
    """1. Calculate research score & 2. Allocate grants."""
    for item in data:
        # Research Score Formula
        score = (0.4 * item["Publications"]) + (0.3 * item["H_index"]) + (0.3 * item["Industry_Collaboration_Score"])
        item["Research_Score"] = round(score, 2)
        
        # Simple allocation logic based on score threshold
        if item["Research_Score"] >= 40:
            item["Allocated_Grant"] = item["Project_Budget_Requested"]
        else:
            item["Allocated_Grant"] = item["Project_Budget_Requested"] * 0.5
    return data

def display_high_grants(data, threshold=100000.0):
    """3. Display faculty receiving grants above $100,000."""
    print(f"\n--- Faculty Receiving Grants Above ${threshold:,.2f} ---")
    found = False
    for item in data:
        if item["Allocated_Grant"] > threshold:
            print(f"Name: {item['Faculty_Name']} | Dept: {item['Department']} | Grant: ${item['Allocated_Grant']:,.2f}")
            found = True
    if not found:
        print("No faculty members found above this threshold.")

def max_funding_department(data):
    """4. Find the department receiving maximum funding."""
    dept_funding = {}
    for item in data:
        dept = item["Department"]
        dept_funding[dept] = dept_funding.get(dept, 0.0) + item["Allocated_Grant"]
    
    if dept_funding:
        max_dept = max(dept_funding, key=dept_funding.get)
        print(f"\n--- Department Receiving Maximum Funding ---")
        print(f"Department: {max_dept} with Total Funding of ${dept_funding[max_dept]:,.2f}")
        return max_dept
    return None

def rank_faculty(data):
    """5. Rank faculty members based on Research Score."""
    ranked_data = sorted(data, key=lambda x: x["Research_Score"], reverse=True)
    print("\n--- Faculty Rankings ---")
    for rank, item in enumerate(ranked_data, start=1):
        item["Rank"] = rank
        print(f"Rank {rank}: {item['Faculty_Name']} (Score: {item['Research_Score']})")
    return ranked_data

def calculate_average_score(data):
    """6. Calculate average research score."""
    if not data:
        return 0.0
    total_score = sum(item["Research_Score"] for item in data)
    avg_score = total_score / len(data)
    print(f"\n--- Average Research Score ---")
    print(f"Average Score: {avg_score:.2f}")
    return avg_score

def identify_top_performer(data):
    """7. Identify the top performer."""
    if not data:
        return None
    top_performer = max(data, key=lambda x: x["Research_Score"])
    print(f"\n--- Top Performer ---")
    print(f"Name: {top_performer['Faculty_Name']} ({top_performer['Department']}) with Score: {top_performer['Research_Score']}")
    return top_performer

def save_rankings_to_file(data, filename="rankings.json"):
    """8. Save the rankings to a file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"\n[System]: Rankings successfully saved to {filename}")

def read_rankings_from_file(filename="rankings.json"):
    """9. Read the rankings back."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        print(f"\n--- Reading Rankings Back From File ({filename}) ---")
        for item in data:
            print(f"Rank {item.get('Rank')}: {item['Faculty_Name']} | Score: {item['Research_Score']}")
        return data
    else:
        print(f"[System Error]: File {filename} not found.")
        return []

if __name__ == "__main__":
    print("=== University Research Grant Allocation System Execution Started ===")
    cleaned_data = validate_and_clean_data(faculty_data)
    processed_data = calculate_research_scores(cleaned_data)
    
    display_high_grants(processed_data, 100000.0)
    max_funding_department(processed_data)
    
    ranked_data = rank_faculty(processed_data)
    calculate_average_score(ranked_data)
    identify_top_performer(ranked_data)
    
    save_rankings_to_file(ranked_data)
    read_rankings_from_file()
    print("\n=== Execution Completed Successfully ===")
