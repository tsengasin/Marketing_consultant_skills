# 02: What Is a 1:1 Campaign?

## Plain-English definition

A **1:1 (one-to-one) campaign** treats **each customer as their own audience**. Instead of one message going to a whole segment, every person can get a different combination of:

- **Content**: which message, offer, product, subject line, or creative
- **Timing**: which day and which hour
- **Frequency**: how many messages this week (sometimes zero)
- **Channel**: email, push, SMS, in-app

The combination is chosen to maximise a business goal (e.g. purchase) *for that individual*.

---

## The evolution: batch → segment → 1:1

Imagine a fashion retailer launching a summer sale.

### Level 1: Batch and blast
> Everyone gets "Summer Sale – 20% off everything!" on Tuesday at 10am.

### Level 2: Segmented
> - Women's shoppers → "Summer dresses 20% off"
> - Men's shoppers → "Summer shirts 20% off"
> - Lapsed customers → "We miss you – 25% off"
>
> All sent Tuesday 10am. The marketer wrote the rules by hand.

### Level 3: Personalised content inside a segment
> Same as level 2, but product recommendations inside the email change per person (dynamic content blocks).
> Still one send time and one offer strategy per segment.

### Level 4: True 1:1 (AI Decisioning)
> For **Anna**: the agent learned she opens emails on Sunday evenings, ignores discount messaging, and clicks on "new arrivals". → **Sunday 8pm, "New in: linen collection", no discount.**
>
> For **Ben**: he only buys on promotion and checks email at lunch. → **Wednesday 12:30, "20% off shirts – 48 hours only".**
>
> For **Chloe**: she's received 4 emails this week and engagement is dropping. → **Send nothing.** (Not sending is also a decision.)

Nobody wrote rules for Anna, Ben, or Chloe. The marketer supplied:
1. A **library of options** (messages, offers, send-time windows)
2. A **goal** (e.g. maximise purchases in 7 days)
3. **Guardrails** (max 3 emails per week, no discounts above 25%, brand rules)

The agent decides the rest and **learns from what happens**.

---

## Why marketers want this

| Pain today | 1:1 benefit |
|---|---|
| A/B tests take weeks and only answer one question | Many variants are tested continuously and simultaneously |
| A test "winner" is applied to everyone, even people who preferred the loser | Each person gets what works for them |
| Segments are coarse and maintained by hand | Decisions use all available signals per person |
| Over-mailing causes unsubscribes | Frequency is optimised per person; sometimes the answer is "don't send" |
| Hard to explain what worked | Reporting shows what was sent, why, and how it performed |

### The key insight to say in interviews
> "A classic A/B test gives you the **best average answer**. But no customer is average. If Variant A wins 55/45, the 45% who preferred B are getting a worse experience forever. 1:1 decisioning finds the best answer **per person**."

---

## What 1:1 is NOT

- ❌ Just putting `{first_name}` in the subject line (that's basic personalisation)
- ❌ Product recommendations alone (that's one component)
- ❌ Writing a different email for every person (the content library is still finite. The *selection* is 1:1)
- ❌ Magic. It needs good data, enough content variety, enough volume to learn, and a clear goal

---

## The building blocks you'll discuss with customers

| Block | Question to ask | Example |
|---|---|---|
| **Goal / reward** | What does success mean? | Purchase within 7 days of send; revenue; subscription renewal |
| **Action space** | What can the agent choose between? | 12 subject lines × 4 offers × 6 send windows |
| **Audience** | Who's eligible? | Opted-in, active in last 180 days, not in a complaint flow |
| **Features / signals** | What does the agent know about each person? | Recency, frequency, monetary value, category affinity, device, engagement history |
| **Guardrails** | What must never happen? | Max 1 message per day; no discount to full-price loyalists; legal exclusions |
| **Holdout** | How will we prove it works? | 10% of eligible customers get business-as-usual (BAU) campaigns |
| **Cadence** | How often are decisions made? | Daily |

---

## Typical first use cases (good examples for interviews)

1. **Promotional email optimisation**: replace the weekly blast with daily 1:1 decisions on message + time.
2. **Win-back / reactivation**: which incentive (if any) brings lapsed customers back?
3. **Onboarding**: which sequence of messages gets new sign-ups to a first purchase?
4. **Cross-sell**: which product category to promote next.
5. **Subscription retention**: which save message to show before churn.
6. **Discount optimisation**: give the *smallest* incentive needed, protecting margin.

## Practice prompt
Explain a 1:1 campaign to:
1. A CMO (30 seconds, business outcomes only)
2. A CRM manager (60 seconds, how their day changes)
3. A data engineer (60 seconds, what data is needed)
