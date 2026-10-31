# 02: Statistics for A/B Testing, from Zero

> Senior consultant's note: "You don't need to derive formulas in the interview. You need to (1) pick the right test, (2) interpret the output correctly, (3) spot the traps, and (4) explain it to a marketer in one sentence. This file is organised around those four skills."

All numbers below are verified by `python/02_ab_test_analysis.py`.

---

## 1. Why statistics at all? Noise.

Flip a fair coin 100 times. You'll rarely get exactly 50 heads. 46 or 55 is normal. That randomness is **noise**.

Same with campaigns: if the AI group converts at 5.6% and holdout at 5.0%, is the AI better, or did we just get "lucky coin flips"? **Statistics tells you how surprising your result is if there were really no difference.**

---

## 2. Hypotheses

- **Null hypothesis (H0):** no difference. AI conversion = holdout conversion.
- **Alternative (H1):** there is a difference.

We never "prove" H1. We check whether the data is **too surprising to believe H0**.

---

## 3. The p-value: what it really means

> **p-value = if there were truly NO difference, the probability of seeing a difference at least as big as the one we observed, purely by chance.**

- p = 0.03 → "If AI had zero effect, we'd see a gap this big only 3% of the time. That's unlikely, so we reject H0." → **statistically significant** (when α = 0.05).
- p = 0.30 → "A gap this big happens 30% of the time from noise alone. We can't conclude anything."

### ❌ Common wrong interpretations (interviewers test these!)
| Wrong | Why |
|---|---|
| "p = 0.03 means there's a 97% chance the AI is better" | No. p is calculated *assuming* H0 is true. It isn't the probability that H1 is true |
| "p = 0.30 means there's no effect" | No. It means **not enough evidence**. Absence of evidence ≠ evidence of absence (the test may be underpowered) |
| "p = 0.001 means the effect is big" | No. With huge samples, tiny effects get tiny p-values. **Significance ≠ importance.** Always look at effect size |

### One-sentence version for a marketer
> "The p-value tells us how likely it is that we'd see this result by luck alone. Under 5% and we treat the lift as real."

---

## 4. Which test do I use? (the decision table)

| Your metric | Example | Test |
|---|---|---|
| **Proportion / rate** (yes/no per user) | Conversion rate, click rate, unsubscribe rate | **Chi-square test** or **two-proportion z-test** (same answer for 2 groups) |
| **Average of a continuous number** | Revenue per user, order value, sessions | **t-test** (use **Welch's** version) |
| **Continuous but very skewed / outliers** | Revenue with a few huge orders | **Mann-Whitney U** or **bootstrap**, or cap outliers then t-test |
| **Counts across more than 2 groups/categories** | Conversion across 4 message variants | **Chi-square** (r × c table) |
| **Same users before and after** | Spend before vs after for the same people | **Paired t-test** |

Memory hook: **"Chi for counts, t for means."**

---

## 5. Chi-square test (for conversion rates): worked example

| Group | Users | Converted | Not converted | Conv. rate |
|---|---|---|---|---|
| AI (treatment) | 10,000 | 560 | 9,440 | 5.6% |
| Holdout (control) | 10,000 | 500 | 9,500 | 5.0% |

**Intuition:** chi-square compares **observed** counts to the counts we'd **expect** if both groups converted at the same overall rate.

- Overall rate = 1,060 / 20,000 = 5.3%
- Expected conversions per group = 10,000 × 5.3% = 530
- Observed: 560 and 500. Each is 30 away from expected.

Formula: χ² = Σ (Observed − Expected)² / Expected over all 4 cells
= 30²/530 + 30²/530 + 30²/9470 + 30²/9470 ≈ **3.59**

With 1 degree of freedom, the critical value at α = 0.05 is **3.84**. 3.59 < 3.84 → **p ≈ 0.058 → NOT significant at 5%.**

🎯 **Interesting!** A +12% relative lift (5.0% → 5.6%) with 10k users per group is *not* conclusive. This is a classic interview trap: **big-looking lifts on modest samples are often noise.**

The two-proportion z-test gives the same result: z = 0.006 / 0.00317 = 1.89, and z² = 3.59 = χ². p = 0.058.

```python
from scipy import stats
table = [[560, 9440], [500, 9500]]
chi2, p, dof, expected = stats.chi2_contingency(table, correction=False)
# chi2 = 3.59, p = 0.058
```
(`correction=False` turns off Yates' correction. With large samples it barely matters. Just be consistent.)

---

## 6. t-test (for averages like revenue per user)

**Question:** is the mean revenue per user different between AI and holdout?

The t-statistic is basically a **signal-to-noise ratio**:

```
        difference in means              (signal)
t = ─────────────────────────────── = ─────────
     standard error of the difference     (noise)

standard error = sqrt( s1²/n1 + s2²/n2 )      (s = standard deviation, n = sample size)
```

- Bigger difference → bigger t
- More variability (s) → smaller t (noisier)
- More users (n) → smaller standard error → bigger t

Rule of thumb: |t| > ~2 → p < 0.05 for large samples.

**Welch's t-test** (`equal_var=False`) doesn't assume both groups have the same variance. Use it by default.

```python
stats.ttest_ind(ai_revenue, holdout_revenue, equal_var=False)
```

⚠️ Revenue per user is **mostly zeros** (non-buyers) plus a **long right tail** (a few big spenders). The t-test still works with large samples (thanks to the Central Limit Theorem), but outliers inflate variance and can hide or fake an effect. See section 9.

---

## 7. Confidence intervals: often better than p-values

A **95% confidence interval** gives a range of plausible values for the true difference.

For our example: difference = +0.6 percentage points, 95% CI ≈ **[−0.02 pp, +1.22 pp]**.

- The interval **includes 0** → not significant (consistent with p = 0.058).
- It's mostly positive → "the effect is likely positive, but we can't rule out zero yet."

Formula: diff ± 1.96 × SE.

**Why consultants like CIs:** they show **size and uncertainty together**. To a VP:
> "Our best estimate is +0.6 points of conversion, and the true value is very likely somewhere between zero and +1.2 points. Two more weeks of data will narrow that."

---

## 8. Errors, power, sample size, MDE

|  | Reality: no effect | Reality: real effect |
|---|---|---|
| **Test says significant** | ❌ **Type I error** (false positive), rate = α (5%) | ✅ |
| **Test says not significant** | ✅ | ❌ **Type II error** (false negative), rate = β |

- **Power = 1 − β** = chance of detecting an effect that's really there. Standard target: **80%**.
- **MDE (Minimum Detectable Effect)** = the smallest lift your test can reliably detect at the chosen power.

### Sample size for conversion tests (formula to recognise, not memorise)

```
n per group ≈ (z_α/2 + z_β)² × [p1(1−p1) + p2(1−p2)] / (p2 − p1)²
            = (1.96 + 0.84)² × [...] / (difference)²
```

Example: baseline 5.0%, want to detect a 10% relative lift (→ 5.5%), α = 0.05, power 80%:

n ≈ 7.85 × (0.0475 + 0.0520) / 0.005² ≈ **31,200 users per group**.

**Key intuitions (say these in the interview):**
- Halving the MDE needs **~4× the sample** (difference is squared).
- Lower baseline conversion → more sample needed.
- **Holdout size matters**: with a 10% holdout, the *holdout* is usually the bottleneck. A 10% holdout of 200k = 20k, which may only detect fairly large lifts.

---

## 9. Outliers & IQR

### IQR method (the standard "box plot" rule)
1. Q1 = 25th percentile, Q3 = 75th percentile
2. **IQR = Q3 − Q1** (the spread of the middle 50%)
3. Lower fence = Q1 − 1.5 × IQR. Upper fence = Q3 + 1.5 × IQR
4. Anything outside the fences is flagged as an outlier

Example order values: 20, 25, 30, 32, 35, 38, 40, 45, 50, **400**
- Q1 = 30.5, Q3 = 43.75 → IQR = 13.25
- Upper fence = 43.75 + 1.5 × 13.25 = **63.6** → **400 is an outlier**
- Mean with 400 = 71.5. Mean without = 35. **One order doubles the mean.** The median (36.5) barely moves.

### Other methods
- **Z-score**: flag |value − mean| / std > 3. Weakness: the outlier itself inflates mean and std, so it's less robust than IQR.
- **Percentile capping (winsorising)**: cap revenue at the 99th percentile. Very common in A/B testing.

### What to DO with outliers (the senior answer)
> "First, **investigate**, don't just delete. Is it a data error (test order, duplicate, currency bug), a B2B/reseller order, or a genuine big spender? Remove errors. For genuine extremes, I'd **cap at the 99th percentile** (winsorise) so one customer can't swing the result, and apply the **same rule to both groups**, decided **before** looking at results. I'd also report the median or a non-parametric test as a robustness check."

👉 Run `python/03_outliers_iqr.py`.

---

## 10. Pitfalls that make you sound senior

| Pitfall | What it is | Fix |
|---|---|---|
| **Peeking** | Checking daily and stopping when p < 0.05. False-positive rate balloons well above 5% | Pre-set sample size and duration, or use sequential testing methods |
| **Multiple comparisons** | Test 20 metrics/segments → ~1 will be "significant" by chance | Pick 1 primary metric upfront; Bonferroni (α / number of tests) or treat as exploratory |
| **SRM (sample ratio mismatch)** | Planned 90/10, got 88/12 → randomisation or tracking bug | Chi-square test on group sizes. Investigate before trusting results |
| **Novelty effect** | Early lift fades | Run at least 2 full business cycles (e.g. 2+ weeks) |
| **Seasonality** | Black Friday week ≠ normal week | Compare groups over the *same* period (randomised holdout handles this) |
| **Contamination** | Holdout users also receive the AI messages, or manual blasts hit both | Strict exclusions. Check overlap with SQL |
| **Simpson's paradox** | Trend in each segment reverses when combined, because of mix differences | Check segment mix is balanced; stratify |
| **Wrong unit** | Randomise by user but analyse by send → sends aren't independent | Analyse at the randomisation unit (user) |
| **Significant but tiny** | p = 0.001 for +0.05% lift | Report effect size and business value |

---

## 11. How this connects to AI Decisioning

- Inside the agent, **bandits** allocate traffic adaptively. You don't run classic t-tests between arms there, because traffic isn't split evenly or randomly over time.
- **Between AI and holdout**, assignment is random and fixed → **classic tests apply**. This is where you use chi-square / t-test / CIs to prove incremental value.
- Typical readout metrics: conversion rate (chi-square / z-test), revenue per recipient (Welch t-test, capped), unsubscribe rate (chi-square, as a guardrail).

## 12. Interpretation template (use this in the interview)

> "AI group converted at **X%** vs holdout **Y%**, a relative lift of **Z%**. The 95% confidence interval for the difference is **[a, b]**, and p = **p**. [So it's significant / not yet conclusive.] Business impact: at current volume this is **€N per month**. Checks: sample ratio matches plan, no outlier distortion, guardrail metrics stable. Recommendation: **[scale / keep running until date / change content]**."
