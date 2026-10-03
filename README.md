# Agentic Finance Workflow

A small, transparent prototype showing how specialized agents can prepare a finance lead for human review.

## Workflow

**Lead → Intake Agent → Verification Agent → Risk-Prep Agent → Human Review**

- **Intake Agent** checks whether required information is present.
- **Verification Agent** checks simulated ID and bank-verification signals.
- **Risk-Prep Agent** calculates a simple affordability proxy, surfaces flags, and prepares the case.
- **Human Review** remains responsible for any actual credit decision.

## Why this project exists

The project explores how agentic systems can reduce repetitive operational work in asset finance while preserving human oversight for consequential decisions.

This first version deliberately uses deterministic Python rather than an LLM API. That makes the workflow easy to inspect, test, and understand. Individual agents can later be replaced by model-powered agents without changing the overall architecture.

## Run it

Requires Python 3.10+ and no external packages.

```bash
python app.py
```

The program reads `data/sample_lead.json` and prints the structured workflow result.

## Example architecture

```text
Customer / Lead
      |
      v
 Intake Agent
      |
      v
Verification Agent
      |
      v
 Risk-Prep Agent
      |
      v
 HUMAN REVIEW
```

## Safety / scope

This is an educational prototype using fictional data. It does **not** approve or deny loans and should not be used for real underwriting decisions.

## Next versions

- LLM-powered intake from unstructured messages
- document extraction
- tool calling
- audit trail and agent observability
- human-in-the-loop web interface
- multi-agent orchestration
