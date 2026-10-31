# 01: Python for People Who Already Know SQL

## The big picture

In data work, "Python" mostly means three libraries:

| Library | What it is | SQL analogy |
|---|---|---|
| **pandas** | Tables in memory ("DataFrames") | A BigQuery table / query result you can keep transforming |
| **numpy** | Fast maths on arrays | Math functions |
| **scipy.stats** / **statsmodels** | Statistical tests (t-test, chi-square) | No SQL equivalent. This is why Python is needed |

Other names you may hear: **matplotlib / seaborn / plotly** (charts), **scikit-learn** (ML models), **Jupyter notebook** (where analysts write Python in cells, like BigQuery's console with output under each cell).

### When do consultants use SQL vs Python?
- **SQL**: pull, filter, join, aggregate big data *inside the warehouse*.
- **Python**: take the (smaller) result and do what SQL is bad at: statistical tests, simulations, cleaning messy values, prototyping models, charts.

Typical workflow:
```python
from google.cloud import bigquery
client = bigquery.Client()
df = client.query("SELECT ... FROM project.dataset.orders ...").to_dataframe()
# ...now analyse df in pandas
```

---

## Reading Python: 10 rules of syntax

```python
import pandas as pd            # load a library and give it a short name
df = pd.read_csv("orders.csv") # variable = value. No types needed
df.head()                      # .method() calls a function on an object
df["revenue"]                  # select one column (a "Series")
df[["customer_id", "revenue"]] # select several columns (note double brackets)
# this is a comment             # like -- in SQL
def lift(t, c):                # define a function
    return (t - c) / c         # indentation = code block (no BEGIN/END)
for x in [1, 2, 3]:            # loop over a list
    print(x)
```

Key ideas: **indentation matters**, `True/False/None` are like `TRUE/FALSE/NULL`, `==` compares and `=` assigns, `&` and `|` mean AND/OR inside pandas filters (wrap each condition in brackets).

---

## SQL → pandas translation table

Assume a table `orders(order_id, customer_id, order_date, channel, revenue)`.

| SQL (BigQuery) | pandas |
|---|---|
| `SELECT * FROM orders LIMIT 5` | `orders.head(5)` |
| `SELECT customer_id, revenue FROM orders` | `orders[["customer_id", "revenue"]]` |
| `WHERE revenue > 100` | `orders[orders["revenue"] > 100]` |
| `WHERE revenue > 100 AND channel = 'email'` | `orders[(orders["revenue"] > 100) & (orders["channel"] == "email")]` |
| `WHERE channel IN ('email','push')` | `orders[orders["channel"].isin(["email", "push"])]` |
| `WHERE revenue IS NULL` | `orders[orders["revenue"].isna()]` |
| `ORDER BY revenue DESC` | `orders.sort_values("revenue", ascending=False)` |
| `SELECT DISTINCT channel` | `orders["channel"].unique()` |
| `COUNT(*)` | `len(orders)` |
| `GROUP BY channel` with `SUM(revenue)` | `orders.groupby("channel")["revenue"].sum()` |
| `GROUP BY` with several aggregates | `orders.groupby("channel").agg(n=("order_id","count"), rev=("revenue","sum"), aov=("revenue","mean"))` |
| `COUNT(DISTINCT customer_id)` | `orders["customer_id"].nunique()` |
| `HAVING SUM(revenue) > 1000` | `g = orders.groupby("customer_id")["revenue"].sum(); g[g > 1000]` |
| `LEFT JOIN customers USING (customer_id)` | `orders.merge(customers, on="customer_id", how="left")` |
| `CASE WHEN revenue > 100 THEN 'high' ELSE 'low' END AS tier` | `orders["tier"] = np.where(orders["revenue"] > 100, "high", "low")` |
| `COALESCE(revenue, 0)` | `orders["revenue"].fillna(0)` |
| `DATE_TRUNC(order_date, WEEK)` | `orders["order_date"].dt.to_period("W")` |
| `DATE_DIFF(CURRENT_DATE(), order_date, DAY)` | `(pd.Timestamp.today() - orders["order_date"]).dt.days` |
| `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date)` | `orders.sort_values("order_date").groupby("customer_id").cumcount() + 1` |
| `SUM(revenue) OVER (PARTITION BY customer_id)` | `orders.groupby("customer_id")["revenue"].transform("sum")` |
| `UNION ALL` | `pd.concat([df1, df2])` |
| `APPROX_QUANTILES(revenue, 4)` | `orders["revenue"].quantile([0.25, 0.5, 0.75])` |
| Dedup: `QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY updated_at DESC) = 1` | `orders.sort_values("updated_at").drop_duplicates("order_id", keep="last")` |

---

## What "cleaning data in Python" looks like

```python
df["email"] = df["email"].str.strip().str.lower()        # normalise text
df["order_date"] = pd.to_datetime(df["order_date"])      # parse dates
df = df.drop_duplicates(subset="order_id")               # remove duplicate orders
df = df[df["revenue"] >= 0]                              # drop negative revenue (refunds handled separately)
df["revenue"] = df["revenue"].fillna(0)                  # fill missing values
df.info()                                                # column types & null counts
df.describe()                                            # min/max/mean/quartiles per column
```

## What "testing a decisioning strategy" looks like

```python
from scipy import stats
treat = df[df["group"] == "ai"]["converted"]
ctrl  = df[df["group"] == "holdout"]["converted"]
print(treat.mean(), ctrl.mean())                    # conversion rates
print(stats.ttest_ind(treat, ctrl, equal_var=False)) # is the difference significant?
```

👉 Now run `python/01_pandas_vs_sql.py`. Every pandas line in it has the matching SQL in a comment.

## Interview tip
They said "comfortable **reading** Python." If shown code, narrate it like this: *"This loads the sends table, filters to the last 30 days, groups by variant, computes conversion rate, then runs a Welch t-test between AI and holdout."* Reading out loud with business meaning beats syntax perfection.
