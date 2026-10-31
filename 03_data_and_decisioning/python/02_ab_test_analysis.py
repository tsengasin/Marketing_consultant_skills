"""
02_ab_test_analysis.py
----------------------
A complete AI-vs-holdout readout, the way a Strategy Consultant would do it:

  Part A: textbook example (numbers from 02_statistics_for_ab_testing.md)
  Part B: sample ratio mismatch (SRM) check
  Part C: conversion rate -> chi-square / z-test + confidence interval
  Part D: revenue per user -> Welch t-test (raw vs outlier-capped) + Mann-Whitney
  Part E: power / sample size: how big must the holdout be?
  Part F: plain-English readout

Prerequisites: python 00_generate_sample_data.py && python 01_pandas_vs_sql.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

DATA = Path(__file__).parent / "data"


def section(title):
    print("\n" + "=" * 80 + f"\n{title}\n" + "=" * 80)


def two_proportion_test(conv_t, n_t, conv_c, n_c, alpha=0.05):
    """Compare two conversion rates. Returns a dict with all the numbers you'd report."""
    p_t, p_c = conv_t / n_t, conv_c / n_c
    diff = p_t - p_c

    # z-test (pooled standard error, assumes H0: same rate)
    p_pool = (conv_t + conv_c) / (n_t + n_c)
    se_pool = np.sqrt(p_pool * (1 - p_pool) * (1 / n_t + 1 / n_c))
    z = diff / se_pool
    p_value = 2 * stats.norm.sf(abs(z))  # two-sided

    # chi-square on the 2x2 table: gives the same p-value (chi2 = z^2)
    table = [[conv_t, n_t - conv_t], [conv_c, n_c - conv_c]]
    chi2, p_chi, _, _ = stats.chi2_contingency(table, correction=False)

    # 95% confidence interval for the difference (unpooled SE)
    se = np.sqrt(p_t * (1 - p_t) / n_t + p_c * (1 - p_c) / n_c)
    zcrit = stats.norm.ppf(1 - alpha / 2)
    ci = (diff - zcrit * se, diff + zcrit * se)

    return dict(p_t=p_t, p_c=p_c, diff=diff, rel_lift=diff / p_c, z=z, chi2=chi2,
                p_value=p_value, p_chi=p_chi, ci_low=ci[0], ci_high=ci[1])


def print_prop_result(r):
    print(f"Treatment rate : {r['p_t']:.2%}")
    print(f"Control rate   : {r['p_c']:.2%}")
    print(f"Difference     : {r['diff']*100:+.2f} percentage points  (relative lift {r['rel_lift']:+.1%})")
    print(f"95% CI (diff)  : [{r['ci_low']*100:+.2f} pp, {r['ci_high']*100:+.2f} pp]")
    print(f"z = {r['z']:.2f}   chi2 = {r['chi2']:.2f}   p-value = {r['p_value']:.4f} (chi-square p = {r['p_chi']:.4f})")
    verdict = "SIGNIFICANT at 5%" if r["p_value"] < 0.05 else "NOT significant at 5%: could be noise"
    print("Verdict        :", verdict)


# =============================================================================
section("PART A: Textbook example: 560/10,000 vs 500/10,000")
r = two_proportion_test(560, 10_000, 500, 10_000)
print_prop_result(r)
print("\nLesson: a +12% relative lift with 10k per group is NOT conclusive (p ~ 0.058).")

# =============================================================================
analysis = pd.read_csv(DATA / "analysis_table.csv")
ai = analysis[analysis["group"] == "ai"]
ho = analysis[analysis["group"] == "holdout"]

section("PART B: Sample Ratio Mismatch (SRM) check")
# We PLANNED 80/20. Is the observed split consistent with that?
observed = [len(ai), len(ho)]
expected = [0.8 * len(analysis), 0.2 * len(analysis)]
chi2_srm, p_srm = stats.chisquare(observed, f_exp=expected)
print(f"Observed: ai={observed[0]:,}  holdout={observed[1]:,}  (holdout share {observed[1]/len(analysis):.2%})")
print(f"SRM chi-square p-value = {p_srm:.3f}")
print("-> p > 0.01: split looks fine." if p_srm > 0.01 else "-> WARNING: SRM! Investigate assignment/tracking before trusting results.")

# =============================================================================
section("PART C: Conversion rate (binary metric -> chi-square / z-test)")
r = two_proportion_test(ai["converted"].sum(), len(ai), ho["converted"].sum(), len(ho))
print_prop_result(r)

# =============================================================================
section("PART D: Revenue per user (continuous metric -> Welch t-test)")
print("Revenue distribution (all users, incl. zeros):")
print(analysis["revenue"].describe(percentiles=[0.5, 0.9, 0.99, 0.999]).round(2))

t_raw = stats.ttest_ind(ai["revenue"], ho["revenue"], equal_var=False)
print(f"\nRAW     mean rev/user  ai={ai['revenue'].mean():.3f}  holdout={ho['revenue'].mean():.3f}"
      f"   t={t_raw.statistic:.2f}  p={t_raw.pvalue:.4f}")

# Cap (winsorise) at the 99th percentile of BUYERS, same cap for both groups, decided upfront
cap = analysis.loc[analysis["revenue"] > 0, "revenue"].quantile(0.99)
ai_cap, ho_cap = ai["revenue"].clip(upper=cap), ho["revenue"].clip(upper=cap)
t_cap = stats.ttest_ind(ai_cap, ho_cap, equal_var=False)
print(f"CAPPED  (cap = EUR {cap:,.0f})  ai={ai_cap.mean():.3f}  holdout={ho_cap.mean():.3f}"
      f"   t={t_cap.statistic:.2f}  p={t_cap.pvalue:.4f}")

# 95% CI for the capped difference in means
diff = ai_cap.mean() - ho_cap.mean()
se = np.sqrt(ai_cap.var(ddof=1) / len(ai_cap) + ho_cap.var(ddof=1) / len(ho_cap))
print(f"Capped diff = EUR {diff:+.3f} per user, 95% CI [{diff-1.96*se:+.3f}, {diff+1.96*se:+.3f}]")

# Non-parametric robustness check (doesn't care about outliers; compares distributions/ranks)
mw = stats.mannwhitneyu(ai["revenue"], ho["revenue"], alternative="two-sided")
print(f"Mann-Whitney U p-value = {mw.pvalue:.4f}")

print("\nLesson: a handful of huge orders inflate variance. Capping makes the test more sensitive,")
print("and shows whether the result depends on a few outliers. Decide the cap rule BEFORE looking.")

# Which group got the outliers?
big = analysis[analysis["revenue"] > 2000][["customer_id", "group", "revenue"]]
print("\nCustomers with > EUR 2,000 in the test window:")
print(big.to_string(index=False))

# =============================================================================
section("PART E: Power & sample size")


def n_per_group(p_base, rel_mde, alpha=0.05, power=0.8):
    p2 = p_base * (1 + rel_mde)
    za, zb = stats.norm.ppf(1 - alpha / 2), stats.norm.ppf(power)
    return (za + zb) ** 2 * (p_base * (1 - p_base) + p2 * (1 - p2)) / (p2 - p_base) ** 2


print("Users needed PER GROUP (alpha 5%, power 80%):")
for base in [0.02, 0.05, 0.10]:
    row = "  ".join(f"MDE {m:>4.0%}: {n_per_group(base, m):>9,.0f}" for m in [0.05, 0.10, 0.20])
    print(f"baseline {base:>4.0%} | {row}")
print("\nNotice: halving the MDE (10% -> 5%) needs ~4x the users.")

# What can OUR holdout detect? Solve for MDE given the holdout size (approximation, equal-group formula)
base = r["p_c"]
for mde in np.arange(0.02, 0.60, 0.01):
    if n_per_group(base, mde) <= len(ho):
        print(f"With {len(ho):,} holdout users and baseline {base:.2%}, the test reliably detects lifts of ~{mde:.0%}+ (relative)")
        break

# =============================================================================
section("PART F: Plain-English readout (say this to the customer)")
print(f"""
Over 6 weeks the AI group converted at {r['p_t']:.2%} vs {r['p_c']:.2%} in the holdout,
a {r['rel_lift']:+.1%} relative lift. The 95% confidence interval for the difference is
[{r['ci_low']*100:+.2f}, {r['ci_high']*100:+.2f}] percentage points (p = {r['p_value']:.3f}).
The group split matches the 80/20 plan. Revenue per user is {'significantly ' if t_cap.pvalue < 0.05 else 'not significantly '}different after
capping a handful of extreme orders (p = {t_cap.pvalue:.3f}).
Recommendation: {'scale to more audiences, keeping a smaller holdout for ongoing measurement.' if r['p_value'] < 0.05
                 else 'keep running. The lift is promising but not yet conclusive at this sample size.'}
""")
print("""Teaching note: 00_generate_sample_data.py planted a TRUE +12% relative lift for the AI group.
The 20% holdout (~8k users) can only reliably detect ~18%+ lifts (Part E), so the test is UNDERPOWERED:
a real effect can easily come out 'not significant'. 'Not significant' != 'no effect'.
Fixes: a bigger holdout, a longer test, or a more sensitive metric.""")
