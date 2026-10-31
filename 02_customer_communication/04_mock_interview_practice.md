# 04: Mock Interview: Customer Communication Round

## What this round probably looks like

Likely formats (prepare for all):
1. **Role play**: the interviewer plays a customer (CRM lead, CMO, data engineer). You run a discovery or design session.
2. **Present a scenario**: "A customer's results are flat after 4 weeks. Walk me through the conversation."
3. **Behavioural**: "Tell me about a time you handled a difficult stakeholder."
4. **Explain a concept**: "Explain reinforcement learning to a marketer."

---

## Behavioural questions: use STAR+L

**S**ituation → **T**ask → **A**ction (most time here, use "I" not "we") → **R**esult (a number) → **L**earning

Prepare **five stories** from your experience that you can adapt:

| # | Theme | Your story (fill in) |
|---|---|---|
| 1 | Difficult stakeholder / disagreement | |
| 2 | Project delivered under pressure / risk escalated | |
| 3 | Used data to change someone's mind | |
| 4 | Explained something technical to a non-technical audience | |
| 5 | A failure and what you learned | |

Common questions:
- Tell me about a time you managed a technical project with a customer.
- Describe a time a customer disagreed with your recommendation.
- How do you prioritise when several stakeholders want different things?
- Tell me about a campaign or test that failed. What did you do?
- How have you used data to influence a marketing decision?
- Why Hightouch? Why this role?

---

## Role play 1: Discovery call

**Interviewer brief (for Claude to play):**
> You are Maria, Head of CRM at "Nordwear", a European online fashion retailer (3M email subscribers, Braze, BigQuery). Your weekly promo email drives 40% of CRM revenue but open rates are down. Your team of 4 spends most of the week building segments. You're interested but sceptical about AI. You've been burned by a personalisation vendor before. Share information only when asked good questions.

**Your goal (candidate):** in 20 minutes, understand the business, programme, data, tech, and organisation (B-P-D-T-O), identify a first use case, and agree on next steps.

**Scorecard:**
| Criterion | 1–5 |
|---|---|
| Opened with clear agenda and objective | |
| Asked open, then specific questions | |
| Quantified the pain (numbers) | |
| Uncovered the past vendor bad experience and addressed it | |
| Covered all of B-P-D-T-O | |
| Played back understanding | |
| Proposed a sensible first use case with reasoning | |
| Closed with next steps, owners, dates | |
| Tone: calm, curious, advisor not salesperson | |

## Role play 2: The flat-results readout

**Interviewer brief:**
> You are Tom, VP Marketing at a meal-kit subscription company. 5 weeks after launch, AI Decisioning shows +2% conversion vs holdout, p = 0.21. Your CFO is asking whether to renew. You're impatient and want a yes/no.

**What a strong candidate does:**
- Explains p = 0.21 in plain English ("the +2% could easily be noise. We can't call it yet.")
- Doesn't over-claim or panic
- Diagnoses: volume? content variety? reward choice? contamination from manual campaigns?
- Proposes concrete actions (add content variants, extend the test, check power) and a decision date
- Gives Tom something to tell the CFO

## Role play 3: Explain it to three audiences

Explain AI Decisioning in 60 seconds each to a CMO, a CRM executive, and a data engineer. (See `01_role_and_concepts/02_one_to_one_campaigns.md`.)

---

## How to practise with Claude

Copy-paste:
> "Act as a senior Strategy Consultant at Hightouch who is interviewing me. Run role play [1/2/3] from `02_customer_communication/04_mock_interview_practice.md`. Stay in character and don't help me during the role play. Afterwards, score me on the scorecard, quote my weakest sentences, and rewrite them the way a senior consultant would say them."

Then save the transcript in `04_practice_log/` using the template there.
