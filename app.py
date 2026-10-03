import json
import os
from pathlib import Path

from openai import OpenAI

REQUIRED = [
    "name",
    "business_name",
    "monthly_revenue",
    "monthly_payment",
    "bank_verified",
    "id_verified",
]


def intake_agent(lead):
    missing = [k for k in REQUIRED if k not in lead or lead[k] in (None, "")]
    return {"agent": "intake", "complete": not missing, "missing_fields": missing, "lead": lead}


def verification_agent(state):
    lead = state["lead"]
    flags = []
    if not lead.get("id_verified", False):
        flags.append("ID_NOT_VERIFIED")
    if not lead.get("bank_verified", False):
        flags.append("BANK_NOT_VERIFIED")
    return {**state, "verification": {"passed": not flags, "flags": flags}}


def calculate_case_metrics(state):
    lead = state["lead"]
    revenue = float(lead.get("monthly_revenue", 0))
    payment = float(lead.get("monthly_payment", 0))
    ratio = payment / revenue if revenue > 0 else 1.0
    flags = list(state["verification"]["flags"])
    if ratio > 0.20:
        flags.append("HIGH_PAYMENT_TO_REVENUE")
    if revenue < 5000:
        flags.append("LOW_REPORTED_REVENUE")
    return {
        "payment_to_revenue": round(ratio, 3),
        "flags": flags,
        "application_complete": state["complete"],
        "missing_fields": state["missing_fields"],
    }


def ai_underwriting_prep_agent(state):
    """Use an LLM to prepare a case summary for a human reviewer.

    The model may summarize and surface questions, but it is explicitly prohibited
    from approving, declining, or setting credit terms.
    """
    metrics = calculate_case_metrics(state)

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Export it locally before running the V2 workflow."
        )

    client = OpenAI()
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        instructions=(
            "You are an underwriting-preparation agent for an educational asset-finance "
            "prototype using fictional data. Prepare information for a human credit reviewer. "
            "Do NOT approve or decline credit, assign a credit score, recommend loan terms, "
            "or make a lending decision. Identify missing information, verification issues, "
            "relevant arithmetic already supplied, and questions a human reviewer should consider. "
            "Return concise JSON only with keys: case_summary, observations, questions_for_human, "
            "next_step. next_step must be either REQUEST_INFORMATION or HUMAN_REVIEW."
        ),
        input=json.dumps({"lead": state["lead"], "metrics": metrics}),
    )

    raw = response.output_text.strip()
    try:
        assessment = json.loads(raw)
    except json.JSONDecodeError:
        assessment = {
            "case_summary": raw,
            "observations": [],
            "questions_for_human": [],
            "next_step": "HUMAN_REVIEW",
        }

    return {
        **state,
        "metrics": metrics,
        "ai_underwriting_prep": assessment,
        "note": "Prototype only. A human remains responsible for any actual credit decision.",
    }


def run_workflow(lead):
    state = intake_agent(lead)
    state = verification_agent(state)
    return ai_underwriting_prep_agent(state)


if __name__ == "__main__":
    lead = json.loads(Path("data/sample_lead.json").read_text())
    print(json.dumps(run_workflow(lead), indent=2))
