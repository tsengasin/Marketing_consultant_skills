# Interview Prep: Hightouch AI Decisioning Strategy Consultant

A study kit for the **AI Decisioning Strategy Consultant** role at Hightouch (Remote, Europe).
It has three goals:

1. **Understand the job**: what a 1:1 campaign is, how AI Decisioning works, and what a consultant does day to day.
2. **Customer communication interview**: think and talk like a senior consultant.
3. **Data & decisioning interview**: SQL, Python, A/B testing statistics, and how reinforcement learning (bandits) replaces manual A/B tests.

---

## Folder map

| Folder | What's inside | Interview it serves |
|---|---|---|
| [`01_role_and_concepts/`](01_role_and_concepts/) | The job, 1:1 campaigns, how AI Decisioning works, glossary | Both. This is the foundation |
| [`02_customer_communication/`](02_customer_communication/) | Senior consultant mindset, discovery and design sessions, difficult conversations, mock interview scripts | Technical interview #1 (customer communication) |
| [`03_data_and_decisioning/`](03_data_and_decisioning/) | Python for SQL users, A/B testing stats, data models, runnable Python scripts, question bank | Technical interview #2 (data & decisioning) |
| [`04_practice_log/`](04_practice_log/) | Your mock interview transcripts, feedback, weak spots to revisit | Both |

---

## Suggested study plan (about 10 days, 1.5–2 h per day)

| Day | Read / do | Output |
|---|---|---|
| 1 | `01_role_and_concepts/01` + `02` | Explain "1:1 campaign" out loud in 60 seconds |
| 2 | `01_role_and_concepts/03` + `04` | Explain "why RL instead of A/B tests" in 60 seconds |
| 3 | `03_data_and_decisioning/01` + run `python/01_pandas_vs_sql.py` | Rewrite 3 of your own BigQuery queries in pandas |
| 4 | `03_data_and_decisioning/02`, sections 1–5 (p-value, t-test, chi-square) | Run `python/02_ab_test_analysis.py`, then explain the output |
| 5 | `03_data_and_decisioning/02`, sections 6–10 (CI, power, outliers, pitfalls) + `python/03_outliers_iqr.py` | Cheat sheet in your own words |
| 6 | `03_data_and_decisioning/03` (data models) + `python/04_bandit_simulation.py` | Sketch a data model on paper |
| 7 | `02_customer_communication/01` + `02` | Run a mock discovery session with Claude |
| 8 | `02_customer_communication/03` + `04` | Two mock "tough conversation" rounds |
| 9 | `03_data_and_decisioning/04` question bank | Answer every question out loud and log the weak ones |
| 10 | Full mock interviews (both) | Final notes in `04_practice_log/` |

## Running the Python scripts

```bash
cd 03_data_and_decisioning/python
pip install -r requirements.txt
python 00_generate_sample_data.py      # creates ./data/*.csv
python 01_pandas_vs_sql.py
python 02_ab_test_analysis.py
python 03_outliers_iqr.py
python 04_bandit_simulation.py
```

Each script is heavily commented. Read the code and the output side by side.

## How to practise with Claude

Open a session and say, for example:

- *"Act as a senior Hightouch consultant. Run a mock discovery call where you play the CRM lead at a fashion retailer. Grade me afterwards."*
- *"Give me an A/B test result and ask me to interpret it like the interviewer would."*
- *"Quiz me on the question bank in `03_data_and_decisioning/04_interview_question_bank.md`, one question at a time."*

Save the transcript and feedback in `04_practice_log/`.
