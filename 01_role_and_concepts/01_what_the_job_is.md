# 01: What This Job Actually Is

## The one-sentence version

> You are the person who makes a customer's AI Decisioning deployment **succeed in business terms**. You turn "we bought an AI product" into "our CRM revenue went up 12% and we can prove it."

The job title includes "Strategy" and the role sits in **Forward Deployed Engineering**. Both words tell you something:

- **Strategy**: you decide *what* to optimise and *why* (use cases, goals, success metrics).
- **Forward Deployed**: you sit close to the customer and get your hands on their data. You are not a slide-only consultant.

---

## Where Hightouch fits in a martech stack

```
 ┌──────────────────────┐     ┌───────────────────────┐     ┌─────────────────────┐
 │  Data warehouse      │     │  Hightouch            │     │  Delivery tools     │
 │  (BigQuery,          │ ──▶ │  - Composable CDP     │ ──▶ │  (Braze, Iterable,  │
 │   Snowflake,         │     │  - Audiences          │     │   Salesforce MC,    │
 │   Databricks)        │     │  - AI Decisioning     │     │   Klaviyo, ad       │
 │  customers, orders,  │ ◀── │    (agents choose     │     │   platforms, app)   │
 │  events, products    │     │     who/what/when)    │     │                     │
 └──────────────────────┘     └───────────────────────┘     └─────────────────────┘
          ▲                                                            │
          └──────────── outcomes (opens, clicks, purchases) ───────────┘
```

**Composable CDP** means Hightouch doesn't copy all your data into its own database. It reads directly from the warehouse the customer already owns. That's why **SQL and data models** matter so much in this role: the AI's inputs come straight from the customer's warehouse tables.

**AI Decisioning** sits on top. For each individual customer, an agent decides:
- **What** to send (which message, offer, product, or creative)
- **When** to send it (send time, day of week)
- **How often** (frequency)
- **Through which channel** (email, push, SMS), depending on the setup

It learns from outcomes (clicks, conversions) using reinforcement learning, so the decisions improve over time.

---

## Today vs. the world Hightouch is selling

| Traditional CRM marketing | AI Decisioning |
|---|---|
| Calendar planned weeks ahead | Decisions made daily, per person |
| Segments ("women 25–34 who bought in last 90 days") | Individuals (1:1) |
| One A/B test at a time, 2–4 weeks each | Many variants tested continuously |
| A winner is picked and sent to everyone | Each person gets what works *for them* |
| 3–5 people and dozens of steps per campaign | Marketers set goals and guardrails, agents execute |
| "Did the campaign work?" | "What did we send, to whom, why, and what was the lift vs. holdout?" |

---

## The lifecycle of a use case (what you own end to end)

| Phase | What you do | Skills used |
|---|---|---|
| **1. Discovery** | Understand the business, the goals, the current CRM programme, the data, the tech stack | Questioning, listening, business acumen |
| **2. Use case design** | Run design sessions: pick the use case (e.g. "replace the weekly promo blast"), define the KPI, the actions the agent can take, guardrails, and the holdout | Facilitation, structured thinking |
| **3. Data readiness** | Check the warehouse: are customers, events, and conversions available, clean, and joined correctly? Build or validate feature tables | SQL, data modelling, Python |
| **4. Configuration & QA** | Set up the agent: action space (messages/offers), reward (e.g. purchase within 7 days), constraints (max 3 emails per week) | Product knowledge, attention to detail |
| **5. Go-live** | Launch with a control group, monitor early signals, catch data issues fast | Project management, risk management |
| **6. Measure & insights** | Compare treatment vs. holdout, read what the agent learned ("Segment X responds to free shipping, not % off") | Statistics, Python, storytelling |
| **7. Expand** | Recommend the next use cases and new content to add. Feed learnings back to product and ML engineers | Strategy, roadmap influence |

---

## A typical week (realistic picture)

- **Mon**: Weekly check-in with a retailer's CRM team. Walk through the agent's insights dashboard. Recommend retiring two underperforming subject lines.
- **Tue**: SQL session. A new customer's order table has duplicate `order_id`s from refunds. Write a dedup query and raise it as a data risk.
- **Wed**: Design session with a subscription brand. Use case: "win-back for lapsed subscribers." Define reward, actions, guardrails, and holdout size.
- **Thu**: Python notebook. Measure 6-week lift vs. holdout for an existing customer. Build a slide for their VP.
- **Fri**: Sync with ML engineers. Customers keep asking for "explain why person X got message Y". Write up the feedback for the roadmap.

---

## What the interviewers are really testing

| They ask about... | They are really checking... |
|---|---|
| Martech / lifecycle experience | Can you speak the marketer's language (CRM, journeys, segments, ESPs, frequency caps)? |
| Customer communication | Can you lead a room, simplify complex ideas, handle pushback, and stay calm? |
| SQL | Can you independently investigate a customer's data? |
| Python | Can you *read* and lightly modify analysis code? (You don't need to be a software engineer.) |
| A/B testing / stats | Can you tell real lift from noise, and explain it to a non-technical VP? |
| Data models | Do you understand how customers, products, transactions, and outcomes connect, and what breaks AI decisions? |

## Your 60-second pitch (draft, personalise this)

> "I come from lifecycle marketing and martech, so I know how CRM teams really work: the calendar, the segments, the endless A/B tests. I'm strong in SQL in BigQuery, and I've used it to [your example: build audiences / analyse campaign performance]. What excites me about AI Decisioning is that it removes the biggest bottleneck I've seen in CRM, which is manual testing at segment level. My job would be to help customers pick use cases that move a real KPI, make sure their data is ready, and prove the lift in a way their leadership trusts."
