"""
01_pandas_vs_sql.py
-------------------
Every pandas step below has the BigQuery SQL that does the same thing in a comment.
Read top to bottom. Run it and compare the printed output with the code.

Prerequisite: python 00_generate_sample_data.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

pd.set_option("display.width", 120)
DATA = Path(__file__).parent / "data"


def section(title):
    print("\n" + "=" * 80 + f"\n{title}\n" + "=" * 80)


# --- Load ------------------------------------------------------------------
# SQL: tables already exist in the warehouse. In Python we load them into memory.
customers = pd.read_csv(DATA / "customers.csv")
orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
sends = pd.read_csv(DATA / "sends.csv", parse_dates=["send_date"])

section("1. Look at the data")
# SQL: SELECT * FROM orders LIMIT 5
print(orders.head(5))
# SQL: no direct equivalent. Shows column types and non-null counts
orders.info()

section("2. Data quality: duplicates")
# SQL: SELECT order_id, COUNT(*) c FROM orders GROUP BY 1 HAVING c > 1
dup_counts = orders.groupby("order_id").size()
print("order_ids appearing more than once:", (dup_counts > 1).sum())

# SQL: SELECT DISTINCT * FROM orders     (or QUALIFY ROW_NUMBER() ... = 1)
orders = orders.drop_duplicates(subset="order_id", keep="first")
print("rows after dedup:", len(orders))

section("3. Filter (WHERE)")
TEST_START, TEST_END = pd.Timestamp("2026-09-01"), pd.Timestamp("2026-10-12")
# SQL: SELECT * FROM orders
#      WHERE status = 'complete' AND order_date >= '2026-09-01' AND order_date < '2026-10-12'
test_orders = orders[
    (orders["status"] == "complete")
    & (orders["order_date"] >= TEST_START)
    & (orders["order_date"] < TEST_END)
]
print("completed orders in test window:", len(test_orders))

section("4. Aggregate (GROUP BY)")
# SQL: SELECT status, COUNT(*) AS n, SUM(revenue) AS rev, AVG(revenue) AS aov
#      FROM orders GROUP BY status
print(
    orders.groupby("status").agg(
        n=("order_id", "count"), rev=("revenue", "sum"), aov=("revenue", "mean")
    ).round(2)
)

section("5. Join (LEFT JOIN) + CASE WHEN")
# SQL: SELECT o.*, c.segment, c.group
#      FROM test_orders o LEFT JOIN customers c USING (customer_id)
test_orders = test_orders.merge(customers[["customer_id", "segment", "group"]], on="customer_id", how="left")
# SQL: CASE WHEN revenue >= 100 THEN 'high' ELSE 'standard' END AS value_tier
test_orders["value_tier"] = np.where(test_orders["revenue"] >= 100, "high", "standard")
print(test_orders.head())

section("6. One row per customer: the analysis table")
# SQL:
#   WITH cust_orders AS (
#     SELECT customer_id, COUNT(*) AS n_orders, SUM(revenue) AS revenue
#     FROM test_orders GROUP BY customer_id)
#   SELECT c.customer_id, c.segment, c.group,
#          COALESCE(n_orders, 0) AS n_orders,
#          COALESCE(revenue, 0) AS revenue,
#          COALESCE(n_orders, 0) > 0 AS converted
#   FROM customers c LEFT JOIN cust_orders USING (customer_id)
cust_orders = (
    test_orders.groupby("customer_id")
    .agg(n_orders=("order_id", "count"), revenue=("revenue", "sum"))
    .reset_index()
)
analysis = customers.merge(cust_orders, on="customer_id", how="left")
analysis[["n_orders", "revenue"]] = analysis[["n_orders", "revenue"]].fillna(0)
analysis["converted"] = analysis["n_orders"] > 0
print(analysis.head())

section("7. Conversion rate by group (the headline A/B metric)")
# SQL: SELECT `group`, COUNT(*) users, AVG(CAST(converted AS INT64)) conv_rate,
#             AVG(revenue) rev_per_user
#      FROM analysis GROUP BY 1
summary = analysis.groupby("group").agg(
    users=("customer_id", "count"),
    conv_rate=("converted", "mean"),
    rev_per_user=("revenue", "mean"),
)
print(summary.round(4))
lift = summary.loc["ai", "conv_rate"] / summary.loc["holdout", "conv_rate"] - 1
print(f"\nRelative conversion lift AI vs holdout: {lift:+.1%}")
print("-> Is that real or noise? That's what 02_ab_test_analysis.py answers.")

section("8. Window function: order sequence per customer")
# SQL: ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS order_seq
orders = orders.sort_values(["customer_id", "order_date"])
orders["order_seq"] = orders.groupby("customer_id").cumcount() + 1
print(orders[["customer_id", "order_date", "order_seq"]].head(8))

section("9. Pivot: AI action performance by segment")
# SQL: SELECT c.segment, s.action_id, AVG(CAST(s.clicked AS INT64)) AS ctr
#      FROM sends s JOIN customers c USING (customer_id) GROUP BY 1, 2
s = sends.merge(customers[["customer_id", "segment"]], on="customer_id")
pivot = s.pivot_table(index="action_id", columns="segment", values="clicked", aggfunc="mean")
print((pivot * 100).round(2).astype(str) + "%")
print("\n(How often each action was chosen per segment, i.e. what the agent 'learned'):")
print(pd.crosstab(s["action_id"], s["segment"], normalize="columns").round(2))

# save the analysis table for the next script
analysis.to_csv(DATA / "analysis_table.csv", index=False)
print(f"\nSaved {DATA / 'analysis_table.csv'}")
