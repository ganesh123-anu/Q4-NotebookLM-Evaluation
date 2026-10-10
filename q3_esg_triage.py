import os
import json
from google import genai

# ============================================================
# Q3(a) - ESG Message Triage using an API-based LLM
# ============================================================

# Gemini API client
# GEMINI_API_KEY must already be stored as an environment variable.
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


# ============================================================
# REVISED PROMPT TEMPLATE
# ============================================================

prompt_template = """
You are an ESG Operations Message Triage Assistant.

Your task is to classify an employee's ESG-related operational message.

Analyse ONLY the information contained in the employee message.
Do not invent facts, people, impacts, locations, or events.

Return ONLY one valid JSON object.
Do not use Markdown.
Do not use ```json code fences.
Do not include explanations outside the JSON object.

Use exactly these fields:

{
  "issue_category": "",
  "urgency": "",
  "sentiment": "",
  "followup_required": "",
  "recommended_team": "",
  "escalation_reason": "",
  "data_sensitivity_risk": "",
  "brief_summary": ""
}

Allowed values for issue_category:
- ENVIRONMENTAL_WATER
- ENVIRONMENTAL_ENERGY
- ENVIRONMENTAL_WASTE
- SUSTAINABLE_PROCUREMENT
- ACCESSIBILITY
- GOVERNANCE
- OTHER

Allowed values for urgency:
- LOW
- MEDIUM
- HIGH
- CRITICAL

Allowed values for sentiment:
- POSITIVE
- NEUTRAL
- NEGATIVE

Allowed values for followup_required:
- Y
- N

Allowed values for data_sensitivity_risk:
- LOW
- MEDIUM
- HIGH

Urgency rules:
- LOW = minor issue with limited immediate impact.
- MEDIUM = normal operational issue requiring follow-up.
- HIGH = significant ESG or operational issue requiring prompt attention.
- CRITICAL = immediate safety, major environmental, accessibility, or operational risk.

Escalation rules:
- HIGH and CRITICAL issues require escalation.
- LOW and MEDIUM issues normally require standard follow-up unless the message provides evidence of a greater risk.
- Explain the escalation decision briefly.

Recommended team:
Select the most appropriate organisational team based only on the issue described.

Data sensitivity:
Assess whether the message contains sensitive personal, confidential, security-related, or other protected information.
Do not assume sensitive information when it is not present.

Brief summary:
Provide one concise sentence summarising the reported issue.

Employee message:
"""


# ============================================================
# REALISTIC ESG TEST MESSAGES
# ============================================================

messages = [
    "There is a water leak in Building C that has been running all morning.",

    "The recycling bins are contaminated again and no one seems to be checking them.",

    "The air conditioning is running overnight in an empty office."
]


# ============================================================
# OUTPUT STORAGE
# ============================================================

results = []

successful_outputs = 0
failed_outputs = 0


# ============================================================
# RUN EACH MESSAGE THROUGH THE API-BASED LLM
# ============================================================

for i, message in enumerate(messages, start=1):

    prompt = prompt_template + "\n" + message

    print("\n" + "=" * 70)
    print(f"MESSAGE {i}")
    print("=" * 70)

    print(message)

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        raw_output = response.text.strip()

        print("\nLLM OUTPUT:")
        print(raw_output)

        # ----------------------------------------------------
        # Validate that the LLM returned valid JSON
        # ----------------------------------------------------

        try:
            parsed_output = json.loads(raw_output)

            # Check required fields
            required_fields = [
                "issue_category",
                "urgency",
                "sentiment",
                "followup_required",
                "recommended_team",
                "escalation_reason",
                "data_sensitivity_risk",
                "brief_summary"
            ]

            missing_fields = [
                field for field in required_fields
                if field not in parsed_output
            ]

            if missing_fields:
                print("\nWARNING: JSON is missing required fields:")
                print(missing_fields)

                validation_status = "INVALID_JSON_STRUCTURE"

            else:
                validation_status = "VALID"

            results.append({
                "message_id": i,
                "employee_message": message,
                "llm_output": parsed_output,
                "validation_status": validation_status
            })

            successful_outputs += 1

        except json.JSONDecodeError:

            print("\nWARNING: The LLM output was not valid JSON.")

            results.append({
                "message_id": i,
                "employee_message": message,
                "llm_output": raw_output,
                "validation_status": "INVALID_JSON"
            })

            failed_outputs += 1

    except Exception as e:

        print("\nLLM OUTPUT:")
        print("API request failed for this message.")

        print(f"Error: {e}")

        results.append({
            "message_id": i,
            "employee_message": message,
            "llm_output": None,
            "validation_status": "API_ERROR",
            "error": str(e)
        })

        failed_outputs += 1

        print("\nThe program will continue with the next ESG message.")


# ============================================================
# SAVE RESULTS FOR ASSESSMENT EVIDENCE
# ============================================================

output_file = "q3_llm_results.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(
        {
            "assessment_question": "Q3(a)",
            "model": "gemini-3.6-flash",
            "purpose": "ESG message triage",
            "prompt_template": prompt_template,
            "results": results
        },
        file,
        indent=2,
        ensure_ascii=False
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("EXPERIMENT SUMMARY")
print("=" * 70)

print(f"Total ESG messages tested: {len(messages)}")
print(f"Successful LLM outputs: {successful_outputs}")
print(f"Failed/invalid outputs: {failed_outputs}")

print(f"\nResults saved to: {output_file}")