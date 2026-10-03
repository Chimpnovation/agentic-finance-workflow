import json
from pathlib import Path

REQUIRED = ["name", "business_name", "monthly_revenue", "monthly_payment", "bank_verified", "id_verified"]


def intake_agent(lead):
    missing = [k for k in REQUIRED if k not in lead or lead[k] in (None, "")]
    return {"agent": "intake", "complete": not missing, "missing_fields": missing, "lead": lead}


def verification_agent(state):
    lead = state["lead"]
    flags = []
    if not lead.get("id_verified", False): flags.append("ID_NOT_VERIFIED")
    if not lead.get("bank_verified", False): flags.append("BANK_NOT_VERIFIED")
    return {**state, "verification": {"passed": not flags, "flags": flags}}


def risk_prep_agent(state):
    lead = state["lead"]
    revenue = float(lead.get("monthly_revenue", 0))
    payment = float(lead.get("monthly_payment", 0))
    ratio = payment / revenue if revenue > 0 else 1.0
    flags = list(state["verification"]["flags"])
    if ratio > 0.20: flags.append("HIGH_PAYMENT_TO_REVENUE")
    if revenue < 5000: flags.append("LOW_REPORTED_REVENUE")

    if not state["complete"]:
        recommendation = "INCOMPLETE — REQUEST INFORMATION"
    elif flags:
        recommendation = "REFER TO HUMAN REVIEW"
    else:
        recommendation = "READY FOR HUMAN CREDIT REVIEW"

    return {**state, "risk_prep": {
        "payment_to_revenue": round(ratio, 3),
        "flags": flags,
        "recommendation": recommendation,
        "note": "Prototype only. No autonomous credit approval or denial."
    }}


def run_workflow(lead):
    state = intake_agent(lead)
    state = verification_agent(state)
    return risk_prep_agent(state)


if __name__ == "__main__":
    lead = json.loads(Path("data/sample_lead.json").read_text())
    print(json.dumps(run_workflow(lead), indent=2))
