# 02: Discovery & Design Sessions

The JD says: *"Run design sessions with customers to decide on and document use case requirements."* This is the core skill they will test.

---

## Part A: Discovery (understanding the customer)

### The 5 areas to cover (memorise as **B-P-D-T-O**)

| Area | What you want to learn | Example questions |
|---|---|---|
| **B: Business** | Goals, KPIs, what leadership cares about | "What are the top 2–3 business goals for CRM this year?" "How does leadership measure CRM success today?" "If this project wins, what changes for you personally?" |
| **P: Programme** | Current campaigns, calendar, testing, pain points | "Walk me through how the weekly promo email gets made." "How many A/B tests do you run a month? What happens to the results?" "Where does your team spend the most time?" |
| **D: Data** | What's available, quality, freshness, identity | "Where does purchase data live, and how fresh is it?" "Can you join email engagement to orders by a common customer ID?" "Any known data quality issues?" |
| **T: Tech** | Stack, channels, integrations, constraints | "Which ESP/CEM do you use?" "Which warehouse?" "Any legal/consent constraints by market?" |
| **O: Organisation** | Who decides, who executes, who blocks | "Who needs to sign off on a new use case?" "Who owns the content library?" "Who in data can help us?" |

### Good questioning technique

1. **Open → narrow**: "Tell me about your lifecycle programme" → "Which journey drives the most revenue?" → "What's its conversion rate today?"
2. **Ask for examples**: "Can you show me the last email you sent?"
3. **Quantify**: "Roughly how many?" "What does 'low' mean in numbers?"
4. **Find the pain**: "What's the most frustrating part of that?"
5. **Ask about the ideal**: "If this works perfectly, what does it look like in 6 months?"
6. **Play back**: "So, to summarise what I'm hearing..."

---

## Part B: The design session (deciding the use case)

### Session agenda (60–90 min)

| Time | Block | Output |
|---|---|---|
| 5 min | Objectives & agenda | Agreement on what we decide today |
| 10 min | Recap of discovery | Shared understanding |
| 15 min | Use case prioritisation | One chosen use case |
| 30 min | Use case design (canvas below) | Filled canvas |
| 10 min | Risks & dependencies | Risk list with owners |
| 5 min | Next steps | Action items, dates |

### Prioritising use cases: Impact × Feasibility

```
          High impact
               │
   Big bets    │   ⭐ START HERE
  (phase 2)    │   (high impact, easy)
───────────────┼──────────────── Feasibility →
   Avoid       │   Quick wins
               │   (low impact, easy)
          Low impact
```

**Impact** = audience size × frequency × revenue at stake.
**Feasibility** = data ready? content available? stakeholder buy-in? enough volume to learn?

> Senior tip: the best *first* use case is high-volume, frequent (fast learning), has a clear conversion metric, and is owned by an enthusiastic team. **The first use case is about proving value and earning trust, not about solving the hardest problem.**

### 📋 The Use Case Design Canvas

| Section | Questions | Example: weekly promo email |
|---|---|---|
| **Use case name** | | Promo email optimisation – UK |
| **Business objective** | What business outcome? | Grow CRM-driven revenue without increasing unsubscribes |
| **Primary KPI (reward)** | What will the agent optimise? Over what window? | Purchase within 7 days of send |
| **Secondary / guardrail metrics** | What must not get worse? | Unsubscribe rate, spam complaints, discount cost |
| **Audience** | Who's eligible? Exclusions? | UK email-opted-in, purchased or engaged in last 365 days; exclude customers with open service tickets |
| **Actions (levers)** | What can the agent choose? | 8 message themes, 3 offers (none / free shipping / 10%), send day, 4 send windows, frequency 0–3/week |
| **Content needed** | Who creates it, by when? | CRM team: 8 templates by week 3 |
| **Guardrails** | Business rules | Max 3 emails/week; no discount to customers who bought full price in last 30 days |
| **Data inputs** | Features & events | Customer profile, orders, email engagement, browse events. Daily refresh |
| **Measurement plan** | Holdout size, duration, success threshold | 10% holdout of BAU; 6 weeks; success = significant lift in purchase rate |
| **Stakeholders** | RACI | CRM lead (A), CRM exec (R), Data eng (C), Hightouch consultant (R) |
| **Risks** | | Late order data; small content library; overlapping manual campaigns |
| **Timeline** | | Data ready wk 2 → content wk 3 → QA wk 4 → go-live wk 5 → readout wk 11 |

---

## Part C: After go-live: the insights review

Run weekly or bi-weekly. Structure:

1. **Headline**: lift vs. holdout so far, and confidence level
2. **What the agent is learning**: top actions, segment patterns
3. **Recommendations**: content to retire or add, guardrails to relax, new use case ideas
4. **Risks/issues**: data delays, volume, contamination
5. **Decisions needed**

> Example opening: *"Week 4 headline: the AI group is converting 6% higher than holdout. It's trending positive but not yet statistically conclusive. We expect a clear read in two more weeks. The most interesting learning: first-time buyers respond strongly to free shipping, while repeat buyers respond to new-arrival messaging with no discount. That suggests a margin opportunity. Let's talk about it."*

---

## Practice exercise

Pick a brand you know (e.g. a fashion retailer, food delivery app, or streaming service). Fill in the Use Case Design Canvas for it from scratch, then ask Claude to play the customer and challenge every section.
