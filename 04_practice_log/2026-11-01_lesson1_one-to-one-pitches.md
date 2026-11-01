# Mock session: Lesson 1, explaining 1:1 campaigns to three audiences

- **Date:** 2026-11-01
- **Type:** Customer communication
- **Scenario:** Explain a 1:1 campaign to the CMO, CRM manager and data engineer of a kitchen store in Ireland
- **Material:** `01_role_and_concepts/01_what_the_job_is.md`, `01_role_and_concepts/02_one_to_one_campaigns.md`

## Transcript (key excerpts)

### Exercise 1: CMO (30 seconds)

**Attempt 1 (5/10)**
> 1:1 campaign is going to improve the conversion value by segmenting the tailored message to different customers. With the presets but sending them accordingly can encourage more revenue, providing smaller discounts by tests.

**Attempt 2 (7/10)**
> Today you set up your yearly calendar and seasonal campaigns in advance with general segmentation. With our AI decisioning products, you will be able to set up 1:1 campaign that sending the best message to each individual with tailored deals. In this case, revenue will increase because customers who tend to buy certain categories will get the recommended items which fits their interests. Less discount is offered because those already have high interest will not receive discounts while the other customers interest will be pushed. At the same time, royalty messages can be sent to those constant buyers with strategies to reach higher retention. We can held a A/B test with holdout groups to prove the lift with the AI-driven campaigns.

**Attempt 3 (8.5/10, passed)**
> Today you are planning your Calendar and seasonal campaigns in advance. With AI-decisioning, you will be able to send the right message to the right person at the suitable time. For example, your halloween kitchen ware promotion will be sent to regular halloween item buyers for the season while boosting new customers with discounts. We'd expect revenue grow by creating intentions, reducing discount amounts and improving retention. We can prove it with holdout.

### Exercise 2: CRM manager (60 seconds)

**Attempt 1 (7/10)**
> Today you spend time on building segments for the weekly email and set up A/B tests weekly, while the open rate, engagement rate can still be low in different segmented groups. With AI-decisioning, you will be saving time on setting the segmentation as the AI-agents will according to customers' interests and engagement activities to send the right message to them at the best timing to boost purchases. You will get time to focus on setting the content library, goals and guardrails. With the help of AI, you will be able to set best offers and ideas to customers and set guardrails to ensure they are engaged without over-mailed. It will help you to reach a better interaction with customers through the CRM system.

**Attempt 2 (8/10, passed)**
> Right now, you spend time on building segments for the weekly email and set up A/B tests weekly, while the engagement rate can vary in different segmented groups. With AI-decisioning, messages will be sent to customers accordingly with their interests and engagement activities at the best timing to boost purchases. You will get time to focus on setting the content library, goals and guardrails. For example, you can create specific content for those who have been browsing Christmas kitchenware more than three times but not making any purchases with discounts to boost purchases. You will be able to read the insights from what the agent learned about customers and share those to your CMO. Which part of your weekly routine is the most repeatable and time consuming one that you want it to be replaced by AI agent?

### Exercise 3: Data engineer kickoff (60 seconds)

**Attempt 1 (6.5/10)**
> Hightouch is a customer data platform that help your marketing team to build a comprehensive marketing campaign by reading directly from your BigQuery with read tables. The agent need to track all activities and orders related to each customer so as to provide 1:1 campaign to each customer. The data sets will not be changed and we will match the metrics that we need with the unique customer id to joint them together, with orders, revenue, last_attribute_platform, top purchase categories. We would like to see if you have the base for this information, we would also love to see if you have any concern that we can tackle together.

## Scorecard

| Criterion | Score (1–5) | Comment |
|---|---|---|
| Structure (adapting to the audience) | 4 | Used the 4-step structures well by the second attempt each time |
| Understanding of 1:1 vs. segments | 3 | Improved, but still slips into hand-written rules ("browsed 3+ times → discount") |
| Business language (CMO) | 4 | Leads with revenue and margin; avoids over-promising after the "guarantee" discussion |
| Technical language (data engineer) | 3 | Right ideas (read-only, `customer_id` join) but opened with marketing language |
| Partnering tone and closing questions | 4 | Good habit of ending with a question; watch words like "replaced" |
| Concision | 3 | First attempts run long; tightened well on retries |

## My 3 weakest moments → senior rewrite

1. **I said:** "…by segmenting the tailored message to different customers."
   **Better:** "…by choosing the best message for **each individual customer**." (Segments are the old way; 1:1 goes beyond them.)
2. **I said:** "…create specific content for those who have been browsing Christmas kitchenware more than three times… with discounts."
   **Better:** "Create a Christmas gift-guide email and a 10%-off version. **The agent works out who needs the discount.**" (The human decides what's possible; the agent decides who gets what, and when.)
3. **I said:** "Hightouch is a customer data platform that helps your marketing team build a comprehensive marketing campaign…" (to a data engineer)
   **Better:** "Hightouch connects to BigQuery with read-only access, so nothing is copied out and your tables aren't changed. To start, we need three things linked by `customer_id`: customers, orders and Braze engagement."

## Concepts clarified during the session

- **CMO** = Chief Marketing Officer; cares about revenue, margin, ROI and proof.
- **No guarantees:** promise an honest way to measure the lift, not the lift itself (→ Scenario 8 in `02_customer_communication/03`).
- **Long tables vs. feature table:** each event or order is a new *row*, not a new column. SQL `GROUP BY customer_id` builds a daily feature table with one row per customer.
- **Raw tables are append-only:** history is never lost; the feature table is a daily summary and can be kept as snapshots.
- **The agent is an ML model, not a chatbot:** it reads numbers, not text, so there are no token costs.
- **Braze is an ESP / engagement platform, not a CDP.** Data flows in a loop: sources → warehouse → Hightouch → Braze → engagement back to the warehouse.
- **Journey gaps** (consent, cross-device, ads): the holdout measures the effect without needing attribution (→ Scenario 9).
- **Data engineers can't sign off on the budget, but they can block the project.** Partner with them, don't instruct them.
- **Read-only access:** Hightouch can read every number in the source tables but cannot change or delete them.

## What to practise next

- [ ] Retry Exercise 3 (data engineer) using: read-only → 3 minimum tables → feature table in a separate dataset → "good enough" → specific question + offer of help
- [ ] Practise saying "the agent decides who gets what" without describing segment rules
- [ ] Lesson 2: `01_role_and_concepts/03` + `04`, explaining "why RL instead of A/B tests" in 60 seconds
