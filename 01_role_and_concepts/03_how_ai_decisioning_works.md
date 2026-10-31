# 03: How AI Decisioning Works (Without the Maths First)

> Note: this explains the *general* techniques behind products like Hightouch AI Decisioning (reinforcement learning, contextual bandits). Hightouch's exact internals aren't public. In the interview, talk about concepts confidently, and ask them how their implementation works. Asking is a strength, not a weakness.

---

## 1. Start from what you know: the A/B test

You have two subject lines. You send A to 50% and B to 50% for two weeks. B wins. You send B to everyone.

**Three problems with this:**
1. **Waste during the test**: half your audience got the worse version for two weeks.
2. **Slow**: one question per test. Testing 12 subject lines × 4 offers × 6 send times = 288 combinations is impossible this way.
3. **One-size-fits-all**: B is best *on average*, but some people prefer A.

## 2. Multi-armed bandits: fix problems 1 and 2

Picture a row of slot machines ("one-armed bandits"), each with an unknown payout rate. You want to win the most money. You face a trade-off:

- **Explore**: try machines you're unsure about, to learn.
- **Exploit**: play the machine that looks best so far, to earn.

A **bandit algorithm** balances both automatically. It sends more traffic to variants that are performing well, while still testing others a little.

| | A/B test | Bandit |
|---|---|---|
| Traffic split | Fixed 50/50 until the end | Shifts toward winners as evidence arrives |
| Goal | Learn which is best (then act) | Earn the most *while* learning |
| Cost during test | High (half get the loser) | Lower ("regret" is minimised) |
| Many variants | Very slow | Handles many |

Common algorithms (know the names and the intuition):
- **Epsilon-greedy**: 90% of the time pick the current best, 10% pick at random.
- **Thompson sampling**: keep a probability distribution of "how good is each option." For each decision, draw a random sample from each and pick the highest. Uncertain options sometimes draw high, so they get explored naturally.
- **UCB (Upper Confidence Bound)**: pick the option with the highest "optimistic estimate" (average + uncertainty bonus).

👉 Run `03_data_and_decisioning/python/04_bandit_simulation.py` to see a bandit beat an A/B test.

## 3. Contextual bandits: fix problem 3 (this is the 1:1 part)

A plain bandit finds the best option **overall**. A **contextual bandit** finds the best option **given what we know about this person** (the *context*, or *features*):

```
context (Anna: 34, buys new arrivals, opens Sunday nights, low discount sensitivity)
   → model predicts expected reward for each action
   → "New arrivals email, Sunday 8pm" has highest predicted reward → send it
   → observe outcome (she clicked and bought) → update the model
```

## 4. Reinforcement learning (RL): the broader family

Reinforcement learning = an **agent** takes **actions** in an **environment**, receives **rewards**, and learns a **policy** (a strategy) that maximises total reward over time.

| RL term | Marketing translation |
|---|---|
| Agent | The AI Decisioning agent for one use case |
| State / context | Everything we know about the customer right now |
| Action | Send message X at time T on channel C (or don't send) |
| Reward | Click, purchase, revenue, retention, minus penalties (e.g. unsubscribe) |
| Policy | The learned rule: "for customers like this, do that" |
| Exploration | Occasionally trying non-obvious actions to keep learning |

Full RL also considers that **today's action changes tomorrow's state** (e.g. sending too much now causes fatigue later). That's why frequency and sequences matter.

## 5. The reward is the most important design decision

The agent will optimise **exactly** what you tell it to. A badly chosen reward creates bad behaviour:

| Reward chosen | What can go wrong |
|---|---|
| Opens | Clickbait subject lines. Apple Mail Privacy Protection inflates opens anyway |
| Clicks | Clicks without purchases |
| Purchases | Ignores order value; may push discounts too much |
| Revenue | Pushes discounts to people who would have paid full price → margin loss |
| Revenue minus discount cost minus unsubscribe penalty | Better, but needs good data |

**Consultant move:** always ask *"what does the CFO count as success?"* and work back to a reward that's measurable, attributable (e.g. a 7-day window), and frequent enough to learn from.

## 6. Holdouts: how you prove it works

The agent's own reporting shows which actions did best *relative to each other*. But the business question is: **"Is AI Decisioning better than what we did before?"**

So you keep a **holdout (control) group**, a random slice (say 10%) of customers who keep getting the business-as-usual (BAU) campaigns. Then:

```
Lift = (conversion rate of AI group − conversion rate of holdout) / conversion rate of holdout
```

And you use **statistics** (t-test / chi-square / confidence intervals) to check whether the lift is real or noise. This is where the A/B testing knowledge comes back. **Bandits don't replace statistics. They replace manual test design.**

## 7. Explainability: "shows marketers what was sent, why, and how it performed"

Marketers won't trust a black box. Typical insights:
- Distribution of actions sent (which messages, which times)
- Performance by action and by segment (e.g. "free shipping beats 15% off for first-time buyers")
- Feature importance (which customer signals drive decisions)
- Lift vs. holdout over time

**Your job:** turn those into recommendations. *"The agent almost never picks Offer C. Let's retire it and brief the creative team on two new variants in the free-shipping style that's winning."*

## 8. Things that make AI Decisioning fail (talk about these to sound senior)

1. **Not enough volume**: a small audience with rare conversions means slow learning.
2. **Too little content variety**: if all 5 messages are nearly identical, there's nothing to learn.
3. **Bad or late data**: events arrive 3 days late, IDs don't match between ESP and warehouse.
4. **Wrong reward**: see section 5.
5. **No holdout**: you can't prove value, and the renewal is at risk.
6. **Over-constrained guardrails**: the agent has no room to choose.
7. **Organisational**: the CRM team keeps sending manual blasts to the same people, which contaminates results.

## 60-second answer: "Why use RL instead of A/B testing?"
> "A/B testing answers one question at a time, wastes half the traffic on the losing variant while the test runs, and ends with one winner applied to everyone. Reinforcement learning, specifically contextual bandits, tests many variants at once, shifts traffic toward what's working while it learns, and makes the decision per person based on their context. You still keep a holdout group and use classic statistics to prove the overall lift against business as usual. So it's not 'no more experiments.' It's continuous experimentation at the individual level."
