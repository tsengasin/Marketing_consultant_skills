"""
03_outliers_iqr.py
------------------
Outlier detection on order values: IQR fences, z-scores, percentile capping.
Shows how ONE extreme value distorts the mean, and why the median and IQR are robust.

Prerequisite: python 00_generate_sample_data.py
"""

from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data"


def section(title):
    print("\n" + "=" * 80 + f"\n{title}\n" + "=" * 80)


def iqr_fences(s: pd.Series, k: float = 1.5):
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    return q1, q3, iqr, q1 - k * iqr, q3 + k * iqr


# -----------------------------------------------------------------------------
section("1. Tiny example from the notes")
s = pd.Series([20, 25, 30, 32, 35, 38, 40, 45, 50, 400])
q1, q3, iqr, lo, hi = iqr_fences(s)
print(f"Q1={q1}  Q3={q3}  IQR={iqr}  lower fence={lo:.2f}  upper fence={hi:.2f}")
print("Outliers:", s[(s < lo) | (s > hi)].tolist())
print(f"Mean with 400: {s.mean():.1f}   mean without: {s[s < hi].mean():.1f}   median: {s.median()}")
# SQL equivalent (BigQuery):
#   SELECT APPROX_QUANTILES(revenue, 4)[OFFSET(1)] AS q1,
#          APPROX_QUANTILES(revenue, 4)[OFFSET(3)] AS q3
#   FROM orders

# -----------------------------------------------------------------------------
section("2. Real(istic) order values")
orders = pd.read_csv(DATA / "orders.csv").drop_duplicates("order_id")
orders = orders[orders["status"] == "complete"]
rev = orders["revenue"]
print(rev.describe(percentiles=[0.25, 0.5, 0.75, 0.99]).round(2))

q1, q3, iqr, lo, hi = iqr_fences(rev)
flag_iqr = (rev < lo) | (rev > hi)
print(f"\nIQR rule: fences [{lo:.2f}, {hi:.2f}] -> {flag_iqr.sum()} orders flagged ({flag_iqr.mean():.1%})")
print("Note: order values are right-skewed (lognormal), so the IQR rule flags many")
print("legitimate big baskets too. Outlier rules are a starting point for INVESTIGATION.")

# IQR on log(revenue) is often more sensible for skewed money data
import numpy as np  # noqa: E402

log_rev = np.log(rev)
q1l, q3l, iqrl, lol, hil = iqr_fences(log_rev, k=3.0)  # k=3 -> "extreme" outliers
flag_log = (log_rev < lol) | (log_rev > hil)
print(f"\nIQR on log(revenue), k=3: upper fence EUR {np.exp(hil):,.0f} -> {flag_log.sum()} orders flagged")
print(orders.loc[flag_log, ["order_id", "customer_id", "revenue"]].sort_values("revenue", ascending=False).head(10).to_string(index=False))

# -----------------------------------------------------------------------------
section("3. Z-score method (|z| > 3)")
z = (rev - rev.mean()) / rev.std()
print(f"Flagged by z-score: {(z.abs() > 3).sum()} orders")
print("Weakness: the outliers themselves inflate the mean and std, so z-scores are less robust than IQR.")

# -----------------------------------------------------------------------------
section("4. Effect on the average order value (AOV)")
cap99 = rev.quantile(0.99)
print(f"Mean (raw)               : EUR {rev.mean():.2f}")
print(f"Mean (capped at p99={cap99:.0f}) : EUR {rev.clip(upper=cap99).mean():.2f}")
print(f"Mean (extremes removed)  : EUR {rev[~flag_log].mean():.2f}")
print(f"Median                   : EUR {rev.median():.2f}")

print("""
What to say in the interview:
  1. Investigate first: data error (test/duplicate/currency), B2B/reseller, or genuine VIP?
  2. Remove clear errors. For genuine extremes, cap (winsorise) at e.g. the 99th percentile.
  3. Apply the SAME rule to treatment and control, decided BEFORE looking at results.
  4. Report a robust metric too (median, or a Mann-Whitney test) as a sanity check.
""")
