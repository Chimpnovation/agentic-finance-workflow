# Agentic Finance Workflow

A small, transparent prototype showing how specialized agents can prepare a finance lead for human review.

## V2 workflow

**Lead → Intake Agent → Verification Agent → AI Underwriting-Prep Agent → Human Review**

- **Intake Agent** checks whether required information is present.
- **Verification Agent** checks simulated ID and bank-verification signals.
- **AI Underwriting-Prep Agent** uses an OpenAI model to summarize the fictional case, surface observations and prepare questions.
- **Human Review** remains responsible for any actual credit decision.

The AI agent is deliberately prevented from approving or declining credit, assigning a credit score, or setting lending terms.

## Why this project exists

The project explores how agentic systems can reduce repetitive operational work in asset finance while preserving human oversight for consequential decisions.

V1 used deterministic Python only. V2 introduces a real model-powered agent while keeping deterministic intake, verification and arithmetic outside the model.

## Run V2 locally

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your-key-here"
python app.py
```

Never commit your API key. The repository's `.gitignore` excludes `.env`.

You can optionally choose another compatible model:

```bash
export OPENAI_MODEL="gpt-5-mini"
```

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
AI Underwriting-Prep Agent
      |
      v
 HUMAN REVIEW
```

## Safety / scope

This is an educational prototype using fictional data. It does **not** approve or deny loans and should not be used for real underwriting decisions.

## Next versions

- unstructured lead intake
- document extraction
- tool calling
- audit trail and agent observability
- human-in-the-loop web interface
- multi-agent orchestration
