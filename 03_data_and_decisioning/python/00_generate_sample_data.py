"""
00_generate_sample_data.py
--------------------------
Creates a FAKE but realistic dataset for practice, saved to ./data/:

  customers.csv : one row per customer (dimension table)
  orders.csv    : one row per order (fact table), with deliberate data-quality problems:
                  duplicate order rows, cancelled orders, a few extreme "outlier" orders
  sends.csv     : one row per message sent during the 6-week test (fact table)

The story: an online retailer ran AI Decisioning for 6 weeks.
80% of customers were in the "ai" group, 20% in a random "holdout" group
that kept getting business-as-usual (BAU) emails.

Run:  python 00_generate_sample_data.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)  # fixed seed -> same data every run
OUT = Path(__file__).parent / "data"
OUT.mkdir(exist_ok=True)

N_CUSTOMERS = 40_000
TEST_START = pd.Timestamp("2026-09-01")
TEST_END = pd.Timestamp("2026-10-12")  # 6 weeks
HISTORY_START = pd.Timestamp("2025-09-01")

# ---------------------------------------------------------------------------
# 1. customers  (SQL equivalent: CREATE TABLE customers AS SELECT ...)
# ---------------------------------------------------------------------------
customer_id = np.arange(1, N_CUSTOMERS + 1)
segment = rng.choice(["new", "repeat", "lapsed"], size=N_CUSTOMERS, p=[0.25, 0.45, 0.30])
country = rng.choice(["UK", "DE", "FR", "NL"], size=N_CUSTOMERS, p=[0.4, 0.3, 0.2, 0.1])
signup_days_ago = rng.integers(30, 1500, size=N_CUSTOMERS)
signup_date = TEST_START - pd.to_timedelta(signup_days_ago, unit="D")
group = rng.choice(["ai", "holdout"], size=N_CUSTOMERS, p=[0.8, 0.2])  # random assignment

customers = pd.DataFrame(
    {
        "customer_id": customer_id,
        "country": country,
        "segment": segment,
        "signup_date": signup_date.date,
        "group": group,
    }
)

# ---------------------------------------------------------------------------
# 2. sends during the test
# ---------------------------------------------------------------------------
AI_ACTIONS = ["new_arrivals", "free_shipping", "pct10_off", "bestsellers", "back_in_stock"]
send_rows = []
for cid, seg, grp in zip(customer_id, segment, group):
    n_sends = rng.integers(3, 10)  # 3-9 sends in 6 weeks
    days = rng.integers(0, (TEST_END - TEST_START).days, size=n_sends)
    for d in days:
        if grp == "holdout":
            action = "bau_weekly_promo"
        else:
            # the "agent" has learned some segment preferences
            if seg == "new":
                p = [0.15, 0.45, 0.15, 0.15, 0.10]
            elif seg == "lapsed":
                p = [0.10, 0.20, 0.45, 0.15, 0.10]
            else:
                p = [0.40, 0.10, 0.10, 0.25, 0.15]
            action = rng.choice(AI_ACTIONS, p=p)
        # clicks are more likely when the message matches the segment's real preference
        preferred = {"new": "free_shipping", "lapsed": "pct10_off", "repeat": "new_arrivals"}[seg]
        opened = rng.random() < 0.25
        clicked = opened and (rng.random() < (0.18 if action == preferred else 0.11))
        send_rows.append((cid, TEST_START + pd.Timedelta(days=int(d)), action, opened, clicked))

sends = pd.DataFrame(send_rows, columns=["customer_id", "send_date", "action_id", "opened", "clicked"])
sends.insert(0, "send_id", np.arange(1, len(sends) + 1))

# ---------------------------------------------------------------------------
# 3. orders: history + test period
# ---------------------------------------------------------------------------
# Baseline 6-week purchase probability by segment; the AI group gets a modest lift.
base_conv = {"new": 0.06, "repeat": 0.09, "lapsed": 0.03}
AI_RELATIVE_LIFT = 0.12  # true effect we "planted": +12% relative

order_rows = []

# historic orders (before the test) -> used for features like recency
for cid, seg in zip(customer_id, segment):
    n_hist = {"new": rng.poisson(0.5), "repeat": rng.poisson(3), "lapsed": rng.poisson(1)}[seg]
    for _ in range(n_hist):
        day = rng.integers(0, (TEST_START - HISTORY_START).days)
        order_rows.append((cid, HISTORY_START + pd.Timedelta(days=int(day)), rng.lognormal(3.8, 0.6), "complete"))

# test-period orders
for cid, seg, grp in zip(customer_id, segment, group):
    p = base_conv[seg] * (1 + AI_RELATIVE_LIFT if grp == "ai" else 1)
    if rng.random() < p:
        n_orders = 1 + rng.poisson(0.2)
        for _ in range(n_orders):
            day = rng.integers(0, (TEST_END - TEST_START).days)
            revenue = rng.lognormal(3.8, 0.6)  # median ~ EUR 45, right-skewed
            status = "cancelled" if rng.random() < 0.04 else "complete"
            order_rows.append((cid, TEST_START + pd.Timedelta(days=int(day)), revenue, status))

orders = pd.DataFrame(order_rows, columns=["customer_id", "order_date", "revenue", "status"])
orders["revenue"] = orders["revenue"].round(2)

# inject a few extreme outliers (e.g. reseller / B2B orders) in the test period
test_mask = orders["order_date"] >= TEST_START
outlier_idx = rng.choice(orders[test_mask].index, size=6, replace=False)
orders.loc[outlier_idx, "revenue"] = rng.uniform(3_000, 12_000, size=6).round(2)

orders = orders.sort_values("order_date").reset_index(drop=True)
orders.insert(0, "order_id", np.arange(100_001, 100_001 + len(orders)))

# inject duplicate rows (a classic pipeline bug) -> 1.5% of orders appear twice
dupes = orders.sample(frac=0.015, random_state=1)
orders = pd.concat([orders, dupes]).sort_values("order_id").reset_index(drop=True)

# ---------------------------------------------------------------------------
# save
# ---------------------------------------------------------------------------
customers.to_csv(OUT / "customers.csv", index=False)
orders.to_csv(OUT / "orders.csv", index=False)
sends.to_csv(OUT / "sends.csv", index=False)

print(f"customers: {len(customers):,} rows")
print(f"orders:    {len(orders):,} rows (includes {len(dupes)} duplicate rows on purpose)")
print(f"sends:     {len(sends):,} rows")
print(f"Saved to {OUT.resolve()}")
