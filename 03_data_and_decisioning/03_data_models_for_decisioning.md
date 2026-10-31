# 03: Data Models for AI Decisioning

The JD: *"how customers, products, transactions and outcomes are organised and connected, making sure the right inputs are available, metrics are consistent, and the AI-driven decisions can be trusted and scaled."*

---

## 1. The core entities

```
                 ┌──────────────┐
                 │  customers   │  1 row per customer (dimension)
                 │ customer_id* │
                 └──────┬───────┘
        ┌───────────────┼──────────────────┬──────────────────┐
        ▼               ▼                  ▼                  ▼
 ┌─────────────┐ ┌──────────────┐  ┌───────────────┐  ┌────────────────┐
 │   orders    │ │    events    │  │   decisions   │  │   outcomes     │
 │ order_id*   │ │ event_id*    │  │ decision_id*  │  │ (engagement:   │
 │ customer_id │ │ customer_id  │  │ customer_id   │  │  opens, clicks,│
 │ order_ts    │ │ event_type   │  │ decision_ts   │  │  unsubscribes) │
 │ revenue     │ │ event_ts     │  │ action_id     │  │ decision_id    │
 └──────┬──────┘ │ product_id   │  │ group (ai/    │  │ event_type     │
        ▼        └──────────────┘  │   holdout)    │  │ event_ts       │
 ┌─────────────┐                   └──────┬────────┘  └────────────────┘
 │ order_items │                          ▼
 │ order_id    │                   ┌──────────────┐
 │ product_id ─┼──▶ products       │   actions    │  (the content library:
 │ qty, price  │    (dimension)    │  action_id*  │   message, offer, time)
 └─────────────┘                   └──────────────┘
```
`*` = primary key

| Table | Grain (1 row = ...) | Type | Used for |
|---|---|---|---|
| customers | one customer | dimension | Audience, features (country, signup date, consent) |
| products | one product | dimension | Category affinity, recommendations |
| orders | one order | fact | **Reward** (conversion, revenue), RFM features |
| order_items | one product line in an order | fact | Category affinity, margin |
| events | one behavioural event (view, add-to-cart, app open) | fact | Engagement features |
| actions | one content option | dimension | What the agent can choose |
| decisions / sends | one decision for one customer | fact | What was sent, to whom, when, which group |
| outcomes | one engagement event tied to a send | fact | Opens, clicks, unsubscribes |

## 2. Always ask about the grain first

The #1 SQL bug in marketing analytics is **joining at the wrong grain** → row fan-out → inflated revenue.

```sql
-- ❌ WRONG: orders joined to order_items duplicates order revenue once per item
SELECT SUM(o.revenue)
FROM orders o
JOIN order_items i USING (order_id);

-- ✅ RIGHT: aggregate to the same grain before joining
WITH items AS (
  SELECT order_id, COUNT(*) AS n_items
  FROM order_items GROUP BY order_id
)
SELECT SUM(o.revenue)
FROM orders o LEFT JOIN items USING (order_id);
```

## 3. The feature table (inputs to the AI)

One row per customer, refreshed daily, using only information available **as of** the decision time.

```sql
-- BigQuery: customer feature snapshot as of a given date
DECLARE as_of DATE DEFAULT CURRENT_DATE();

WITH ord AS (
  SELECT
    customer_id,
    DATE_DIFF(as_of, MAX(DATE(order_ts)), DAY)                        AS days_since_last_order,
    COUNTIF(DATE(order_ts) >= DATE_SUB(as_of, INTERVAL 365 DAY))       AS orders_365d,
    SUM(IF(DATE(order_ts) >= DATE_SUB(as_of, INTERVAL 365 DAY), revenue, 0)) AS revenue_365d,
    AVG(revenue)                                                       AS avg_order_value
  FROM `proj.crm.orders`
  WHERE DATE(order_ts) < as_of            -- no future data (prevents leakage)
    AND status != 'cancelled'
  GROUP BY customer_id
),
eng AS (
  SELECT
    customer_id,
    COUNTIF(event_type = 'email_click' AND DATE(event_ts) >= DATE_SUB(as_of, INTERVAL 30 DAY)) AS clicks_30d,
    COUNTIF(event_type = 'email_open'  AND DATE(event_ts) >= DATE_SUB(as_of, INTERVAL 30 DAY)) AS opens_30d
  FROM `proj.crm.events`
  WHERE DATE(event_ts) < as_of
  GROUP BY customer_id
)
SELECT
  c.customer_id,
  c.country,
  DATE_DIFF(as_of, DATE(c.signup_ts), DAY) AS tenure_days,
  COALESCE(o.days_since_last_order, 9999)  AS days_since_last_order,
  COALESCE(o.orders_365d, 0)               AS orders_365d,
  COALESCE(o.revenue_365d, 0)              AS revenue_365d,
  COALESCE(e.clicks_30d, 0)                AS clicks_30d,
  COALESCE(e.opens_30d, 0)                 AS opens_30d
FROM `proj.crm.customers` c
LEFT JOIN ord o USING (customer_id)
LEFT JOIN eng e USING (customer_id)
WHERE c.email_opt_in = TRUE;
```

## 4. The reward (outcome) definition

Define it precisely. **Consistency** means the agent, the dashboard, and the customer's finance team all use the same definition.

```sql
-- Reward: did the customer purchase within 7 days after the decision?
SELECT
  d.decision_id,
  d.customer_id,
  d.group_name,              -- 'ai' or 'holdout'
  d.action_id,
  COUNT(o.order_id) > 0        AS converted_7d,
  COALESCE(SUM(o.revenue), 0)  AS revenue_7d
FROM `proj.crm.decisions` d
LEFT JOIN `proj.crm.orders` o
  ON  o.customer_id = d.customer_id
  AND o.order_ts >  d.decision_ts
  AND o.order_ts <= TIMESTAMP_ADD(d.decision_ts, INTERVAL 7 DAY)
  AND o.status != 'cancelled'
GROUP BY 1, 2, 3, 4;
```

Questions to settle with the customer:
- Window: 3, 7, or 14 days? (Longer means more complete, but slower feedback for learning.)
- Gross or net of returns? Include tax/shipping?
- Any order, or only in specific channels (online vs store)?
- What if a customer gets two messages in the window? (Attribution overlap.)

## 5. Data quality checks you should run (and talk about)

```sql
-- 1. Primary key uniqueness
SELECT order_id, COUNT(*) c FROM `proj.crm.orders` GROUP BY 1 HAVING c > 1;

-- 2. Match rate: can sends be joined to customers?
SELECT COUNTIF(c.customer_id IS NULL) / COUNT(*) AS unmatched_share
FROM `proj.crm.decisions` d LEFT JOIN `proj.crm.customers` c USING (customer_id);

-- 3. Freshness: when did data last arrive?
SELECT MAX(order_ts) AS latest_order FROM `proj.crm.orders`;

-- 4. Nulls and impossible values
SELECT COUNTIF(revenue IS NULL) AS null_rev, COUNTIF(revenue < 0) AS neg_rev,
       COUNTIF(order_ts > CURRENT_TIMESTAMP()) AS future_ts
FROM `proj.crm.orders`;

-- 5. Sample ratio check: is the holdout the planned size?
SELECT group_name, COUNT(DISTINCT customer_id) n,
       COUNT(DISTINCT customer_id) / SUM(COUNT(DISTINCT customer_id)) OVER () share
FROM `proj.crm.decisions` GROUP BY 1;

-- 6. Contamination: holdout customers who received AI sends
SELECT COUNT(*) AS customers_in_both_groups
FROM (
  SELECT customer_id
  FROM `proj.crm.decisions`
  GROUP BY customer_id
  HAVING COUNT(DISTINCT group_name) > 1
);
```

## 6. Trust & scale checklist

| Dimension | Question |
|---|---|
| **Completeness** | Are all relevant customers, orders, and events present? |
| **Identity** | Is one person one ID across ESP, web, app, and orders? |
| **Freshness** | Does data arrive before the next daily decision run? |
| **Consistency** | Same definitions of "conversion" and "revenue" everywhere? |
| **No leakage** | Features only use information from before decision time? |
| **Randomisation** | Holdout assigned randomly and stable over time? |
| **Governance** | Consent, opt-outs, and GDPR deletion respected? |
| **Scalability** | Can the same model support the next use case (SMS, new market) without rebuilding? |

## Practice
Take a dataset you know from BigQuery and write down: each table's grain, its primary key, how it joins to the others, and three data quality risks. Then write the reward query for "purchase within 7 days of an email."
