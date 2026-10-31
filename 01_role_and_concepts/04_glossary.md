# 04: Glossary (Martech + Data + ML)

## Martech / lifecycle
| Term | Meaning |
|---|---|
| **CDP** | Customer Data Platform: unified customer profiles used for marketing |
| **Composable CDP** | A CDP that runs on top of your own warehouse instead of copying data (Hightouch's model) |
| **Reverse ETL** | Moving data *from* the warehouse *to* business tools (Braze, Salesforce, ad platforms) |
| **ESP** | Email Service Provider (Braze, Iterable, Klaviyo, SFMC) |
| **CEM** | Customer Engagement Management platform (Braze, Iterable, etc.) |
| **Lifecycle marketing** | Messages tied to the customer journey: onboarding, activation, retention, win-back |
| **BAU** | Business As Usual: the current campaign approach, often the control |
| **Frequency cap** | Max messages per person per period |
| **Suppression** | Excluding people (unsubscribed, complaints, recently purchased) |
| **RFM** | Recency, Frequency, Monetary value: classic customer scoring |
| **LTV / CLV** | Customer lifetime value |
| **Churn** | Customer stops buying or cancels |
| **Attribution window** | How long after a message a conversion is credited to it (e.g. 7 days) |
| **MPP** | Apple Mail Privacy Protection: inflates open rates, so opens are an unreliable metric |

## Experimentation & statistics
| Term | Meaning |
|---|---|
| **Control / holdout** | Group that does NOT get the new treatment, used for comparison |
| **Treatment** | Group that gets the new thing |
| **Lift** | (treatment − control) / control |
| **Null hypothesis (H0)** | "There is no difference" |
| **p-value** | If there were truly no difference, the probability of seeing a result at least this extreme |
| **Significance level (α)** | Threshold for p, usually 0.05 |
| **Confidence interval** | Range of plausible values for the true effect |
| **Statistical power** | Probability of detecting a real effect (target 80%) |
| **MDE** | Minimum Detectable Effect: smallest lift the test can reliably detect |
| **t-test** | Compares **means** of two groups (e.g. revenue per user) |
| **Chi-square test** | Compares **proportions / counts** across groups (e.g. conversion rates) |
| **Z-test for proportions** | Another way to compare two conversion rates (equivalent to 2×2 chi-square) |
| **IQR** | Interquartile range = Q3 − Q1. Used to flag outliers |
| **Outlier** | Extreme value (e.g. a €20,000 B2B order in a consumer dataset) |
| **Peeking** | Checking results repeatedly and stopping when p < 0.05. Inflates false positives |
| **SRM** | Sample Ratio Mismatch: you planned 50/50 but got 53/47, which signals a bug |
| **Novelty effect** | Early lift that fades once people get used to the change |

## ML / decisioning
| Term | Meaning |
|---|---|
| **Reinforcement learning** | Learning by trial, action, and reward |
| **Multi-armed bandit** | Choose between options to maximise reward while learning |
| **Contextual bandit** | Bandit that uses customer features to pick per person |
| **Explore / exploit** | Trying uncertain options vs. using the best known one |
| **Regret** | Reward lost by not always picking the best option |
| **Thompson sampling** | Bandit method that samples from probability distributions |
| **Policy** | The decision rule the agent learned |
| **Feature** | An input signal about a customer (days since last order, etc.) |
| **Reward** | The number the agent tries to maximise |
| **Action space** | All the choices the agent can make |
| **Cold start** | New customer or new message with no history yet |
| **Uplift / incrementality** | Effect *caused* by the action, beyond what would have happened anyway |

## Data modelling
| Term | Meaning |
|---|---|
| **Grain** | What one row represents (one customer? one order? one order line?) |
| **Primary key** | Column(s) that uniquely identify a row |
| **Foreign key** | Column that links to another table's primary key |
| **Fact table** | Events / transactions (orders, sends, clicks). Many rows |
| **Dimension table** | Descriptive entities (customers, products) |
| **Star schema** | Facts in the middle, dimensions around them |
| **Identity resolution** | Matching one person across emails, devices, IDs |
| **Feature table** | One row per customer with model inputs, refreshed regularly |
| **Data leakage** | Using information from *after* the decision time to predict the outcome |
