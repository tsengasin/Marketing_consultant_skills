# 04: Data & Decisioning Interview Question Bank

Cover the answer, say yours out loud, then compare. ⭐ = very likely to be asked.

---

## A. Statistics & A/B testing

**⭐ A1. What is a p-value? Explain it to a marketer.**
> If there were truly no difference between the groups, the p-value is the chance we'd see a gap at least this big from random noise alone. For a marketer: "It's how likely this result is a fluke. Under 5% and we treat the lift as real." It is *not* the probability the treatment works.

**⭐ A2. AI group converts at 5.6%, holdout 5.0%, 10,000 users each. Is it significant?**
> Overall rate 5.3%. SE of the difference ≈ √(0.053 × 0.947 × 2/10,000) ≈ 0.32 pp. z ≈ 0.6 / 0.32 ≈ 1.9 → p ≈ 0.058. Just *not* significant at 5%. The 95% CI is roughly −0.02 to +1.2 pp. It's promising, but we need more data. (A sample size calculation says ~31k per group to reliably detect a 10% relative lift from 5%.)

**⭐ A3. When do you use a t-test vs. a chi-square test?**
> Chi-square (or a z-test for two proportions) for **rates/counts**: conversion, click, unsubscribe. t-test for **means of continuous metrics**: revenue per user, AOV. "Chi for counts, t for means." I'd use Welch's t-test since it doesn't assume equal variances.

**A4. What are Type I and Type II errors?**
> Type I: false positive. We declare a winner that isn't real (rate = α, usually 5%). Type II: false negative. We miss a real effect (rate = β; power = 1 − β, usually 80%).

**⭐ A5. What is statistical power and why does it matter for a holdout?**
> The probability of detecting a real effect. A small holdout means low power, so even a real lift can come out "not significant." Before launch I'd calculate the minimum detectable effect for the planned holdout size, and agree with the customer on whether that's acceptable.

**A6. How do you determine sample size?**
> Inputs: baseline rate, minimum detectable effect, α (0.05), power (0.8). n per group ≈ 7.85 × [p1(1−p1) + p2(1−p2)] / (p2 − p1)². Halving the MDE quadruples the sample.

**⭐ A7. How do you handle outliers in revenue?**
> Investigate first (errors, duplicates, B2B orders, genuine VIPs). Remove errors. Cap genuine extremes at e.g. the 99th percentile, with the same rule for both groups, decided before seeing results. Check robustness with the median or Mann-Whitney. Detection: the IQR rule (outside Q1 − 1.5·IQR or Q3 + 1.5·IQR). For skewed money data, apply it on log scale.

**A8. What is the IQR?**
> Q3 − Q1, the range of the middle 50% of the data. Robust to extremes, unlike standard deviation.

**⭐ A9. The customer checks the dashboard daily and wants to stop as soon as p < 0.05. Problem?**
> Yes: peeking. Every look is another chance for noise to cross the threshold, so the real false-positive rate climbs well above 5%. Fix: agree on duration and sample size upfront, or use a sequential testing method designed for continuous monitoring.

**A10. You test 15 segments and one shows a significant lift. Do you trust it?**
> Not by itself. With 15 tests at α = 0.05, we'd expect ~0.75 false positives by chance. Treat it as a hypothesis, apply a correction (Bonferroni: 0.05 / 15), or validate it in a follow-up test.

**A11. What is a sample ratio mismatch?**
> The observed split differs from the plan (e.g. 88/12 instead of 90/10). A chi-square goodness-of-fit test flags it. It usually indicates a bug in assignment or tracking, so results can't be trusted until it's explained.

**A12. Statistically significant vs. practically significant?**
> With millions of users, a +0.01% lift can be "significant" but worthless. Always report effect size, a confidence interval, and business value (€).

**A13. What is a confidence interval?**
> A range of plausible values for the true effect. If we repeated the experiment many times, 95% of the intervals built this way would contain the true value. If it excludes 0, the result is significant at 5%.

**A14. Results show a lift overall, but within every segment the AI is worse. How?**
> Simpson's paradox: the groups have a different segment mix. Check randomisation and balance, and analyse stratified by segment.

## B. Bandits, RL, AI Decisioning

**⭐ B1. Why use reinforcement learning instead of A/B testing?**
> See `01_role_and_concepts/03`: many variants at once, traffic shifts to winners while learning (less waste), and decisions are per person (contextual). Still keep a holdout for proving incremental value.

**⭐ B2. What is the explore/exploit trade-off?**
> Exploit = use the best-known option to earn now. Explore = try uncertain options to learn. Too much exploit and you can lock onto a false winner. Too much explore and you waste sends. Bandits (e.g. Thompson sampling) balance it automatically.

**B3. What is a contextual bandit?**
> A bandit that uses features about the person (recency, segment, engagement) to choose the best action *for them*, not just the best on average.

**⭐ B4. How would you choose the reward for a promo email use case?**
> Start from the business goal. Purchase within N days is usually better than opens or clicks (opens are inflated by Apple MPP, clicks don't equal revenue). Consider revenue or margin, and penalties for unsubscribes. Balance completeness (longer window) against learning speed (shorter window). Make it consistent with how finance measures success.

**⭐ B5. How do you measure whether AI Decisioning is working?**
> A random, stable holdout getting BAU. Primary metric (e.g. conversion or revenue per recipient) compared with chi-square / Welch t-test and confidence intervals. Guardrails: unsubscribes, complaints, discount cost. Plus an SRM check and a contamination check.

**B6. Customer: "the agent sends Offer C to almost nobody." Is that a problem?**
> Probably not. It suggests Offer C underperforms for everyone, which is a useful insight. Recommend retiring or reworking it and adding new content so the agent has fresh options. Check that it's not caused by a guardrail or eligibility bug.

**B7. Why can't you just run a t-test between two arms inside the bandit?**
> Traffic is allocated adaptively, not randomly and evenly over time. Arms get different volumes at different times and to different contexts, which biases naive comparisons. Use the randomised holdout for causal claims, and treat arm-level stats as directional.

**B8. What is the cold-start problem?**
> New customers or new messages have no history. Handle it with exploration, priors, using features (contextual) rather than individual history, or sensible defaults.

## C. Data modelling & SQL

**⭐ C1. What data would you need for an AI Decisioning use case?**
> Customer table (ID, consent, attributes), orders (reward), engagement events (opens, clicks, browse), sends/decisions log (what was sent, when, group), content/action catalogue, products. All joinable on a consistent customer ID, refreshed before each decision run.

**⭐ C2. Revenue looks 30% too high after your join. Why?**
> Probably fan-out: joining orders to a many-row table (order items, or sends) duplicates revenue. Check the grain, aggregate before joining, and verify primary key uniqueness.

**C3. What is data leakage?**
> Using information that wasn't available at decision time (e.g. a feature computed with orders after the send). The model looks great offline and fails live. Always compute features "as of" the decision timestamp.

**⭐ C4. Write SQL: conversion rate within 7 days of send, by group.**
```sql
WITH reward AS (
  SELECT d.customer_id, d.group_name,
         LOGICAL_OR(o.order_id IS NOT NULL) AS converted
  FROM decisions d
  LEFT JOIN orders o
    ON o.customer_id = d.customer_id
   AND o.order_ts > d.decision_ts
   AND o.order_ts <= TIMESTAMP_ADD(d.decision_ts, INTERVAL 7 DAY)
  GROUP BY 1, 2
)
SELECT group_name, COUNT(*) AS users, AVG(IF(converted, 1, 0)) AS conv_rate
FROM reward GROUP BY 1;
```
*(Here the grain is customer: a customer counts as converted if any send was followed by an order within 7 days.)*

**C5. Write SQL: deduplicate an orders table keeping the latest version.**
```sql
SELECT * FROM orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY updated_at DESC) = 1;
```

**C6. What does "metrics are consistent" mean in practice?**
> One definition of conversion, revenue (gross/net, tax, returns), and attribution window, used by the agent's reward, the Hightouch reporting, and the customer's BI. Document it in the use case canvas.

## D. Python reading

**⭐ D1. Explain this code:**
```python
df = sends.merge(orders, on="customer_id", how="left")
df["converted"] = df["order_ts"].between(df["send_ts"], df["send_ts"] + pd.Timedelta(days=7))
res = df.groupby(["group", "send_id"])["converted"].max().groupby("group").mean()
stats.chi2_contingency(pd.crosstab(df_cust["group"], df_cust["converted"]))
```
> Left-joins sends to orders by customer. Flags whether each order happened within 7 days after the send. Collapses to one row per send (did *any* order convert it?), then averages by group to get the conversion rate per send. Finally runs a chi-square test on a group × converted contingency table. I'd check the join doesn't fan out more than intended, and that the analysis unit matches the randomisation unit (customer, not send).

## E. Case question (likely format)

**⭐ E1. "A retailer ran AI Decisioning for 6 weeks: +4% conversion vs. holdout, p = 0.42. The CMO asks if it worked. Walk me through it."**
Structure your answer:
1. **Interpret**: +4% is the best estimate, but p = 0.42 and a CI spanning zero mean we can't distinguish it from noise. Not "it failed", but "not proven yet."
2. **Diagnose power**: what lift could this holdout detect? (e.g. with 8k holdout users at 6.5% baseline, only ~18%+ lifts.) Likely underpowered.
3. **Check validity**: SRM, contamination, data freshness, outliers, reward definition.
4. **Check learning**: is the agent converging? Enough content variety? Over-tight guardrails?
5. **Recommend**: extend the test / increase holdout or volume / add content / use revenue per recipient (capped) as the primary metric. Set a decision date.
6. **Communicate**: one-line message for the CMO.

👉 This exact scenario is in `python/02_ab_test_analysis.py`. Run it and practise the readout.
