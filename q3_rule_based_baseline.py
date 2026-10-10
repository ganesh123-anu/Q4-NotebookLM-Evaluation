import json
import csv

# ============================================================
# Q3(b) - Rule-Based Baseline for ESG Message Classification
# ============================================================

# Same ESG messages used in Q3(a)
messages = [
    "There is a water leak in Building C that has been running all morning.",
    "The recycling bins are contaminated again and no one seems to be checking them.",
    "The air conditioning is running overnight in an empty office."
]


# ============================================================
# RULE-BASED CLASSIFIER
# ============================================================

def classify_message(message):

    text = message.lower()

    # --------------------------------------------------------
    # Issue category rules
    # --------------------------------------------------------

    if any(word in text for word in [
        "water leak",
        "water leaking",
        "pipe leak",
        "tap is leaking",
        "water wastage"
    ]):
        issue_category = "ENVIRONMENTAL_WATER"
        recommended_team = "Facilities Management"

    elif any(word in text for word in [
        "recycling",
        "recycling bins",
        "waste",
        "bins",
        "contaminated"
    ]):
        issue_category = "ENVIRONMENTAL_WASTE"
        recommended_team = "Facilities Management"

    elif any(word in text for word in [
        "air conditioning",
        "air conditioner",
        "ac ",
        "electricity",
        "energy",
        "lights",
        "running overnight"
    ]):
        issue_category = "ENVIRONMENTAL_ENERGY"
        recommended_team = "Facilities Management"

    else:
        issue_category = "OTHER"
        recommended_team = "General ESG Support"

    # --------------------------------------------------------
    # Urgency rules
    # --------------------------------------------------------

    if any(word in text for word in [
        "critical",
        "emergency",
        "immediate danger"
    ]):
        urgency = "CRITICAL"

    elif any(word in text for word in [
        "running all morning",
        "major leak",
        "urgent",
        "high priority"
    ]):
        urgency = "HIGH"

    elif any(word in text for word in [
        "again",
        "recurring",
        "not checking",
        "no one seems to be checking"
    ]):
        urgency = "MEDIUM"

    else:
        urgency = "LOW"

    # --------------------------------------------------------
    # Sentiment rules
    # --------------------------------------------------------

    if any(word in text for word in [
        "problem",
        "issue",
        "leak",
        "contaminated",
        "waste",
        "blocked",
        "no one",
        "running overnight"
    ]):
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    # --------------------------------------------------------
    # Follow-up rule
    # --------------------------------------------------------

    followup_required = "Y"

    # --------------------------------------------------------
    # Escalation rule
    # --------------------------------------------------------

    if urgency in ["HIGH", "CRITICAL"]:
        escalation_reason = (
            "Escalation required because the issue has high or critical urgency."
        )
    else:
        escalation_reason = (
            "No immediate escalation required; standard operational follow-up is sufficient."
        )

    # --------------------------------------------------------
    # Data sensitivity rule
    # --------------------------------------------------------

    data_sensitivity_risk = "LOW"

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    brief_summary = message

    return {
        "issue_category": issue_category,
        "urgency": urgency,
        "sentiment": sentiment,
        "followup_required": followup_required,
        "recommended_team": recommended_team,
        "escalation_reason": escalation_reason,
        "data_sensitivity_risk": data_sensitivity_risk,
        "brief_summary": brief_summary
    }


# ============================================================
# RUN BASELINE
# ============================================================

results = []

print("=" * 70)
print("Q3(b) RULE-BASED ESG BASELINE")
print("=" * 70)

for i, message in enumerate(messages, start=1):

    classification = classify_message(message)

    result = {
        "message_id": i,
        "employee_message": message,
        "baseline_output": classification
    }

    results.append(result)

    print("\n" + "=" * 70)
    print(f"MESSAGE {i}")
    print("=" * 70)

    print(message)

    print("\nRULE-BASED OUTPUT:")
    print(json.dumps(classification, indent=2))


# ============================================================
# SAVE JSON RESULTS
# ============================================================

json_file = "q3_rule_based_results.json"

with open(json_file, "w", encoding="utf-8") as file:
    json.dump(
        {
            "assessment_question": "Q3(b)",
            "method": "Rule-based baseline",
            "results": results
        },
        file,
        indent=2,
        ensure_ascii=False
    )


# ============================================================
# CREATE CSV FOR COMPARISON
# ============================================================

csv_file = "q3_rule_based_results.csv"

with open(csv_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Message ID",
        "Issue Category",
        "Urgency",
        "Sentiment",
        "Follow-up Required",
        "Recommended Team",
        "Data Sensitivity Risk"
    ])

    for result in results:

        output = result["baseline_output"]

        writer.writerow([
            result["message_id"],
            output["issue_category"],
            output["urgency"],
            output["sentiment"],
            output["followup_required"],
            output["recommended_team"],
            output["data_sensitivity_risk"]
        ])


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("BASELINE EXPERIMENT COMPLETE")
print("=" * 70)

print(f"JSON results saved to: {json_file}")
print(f"CSV results saved to:  {csv_file}")