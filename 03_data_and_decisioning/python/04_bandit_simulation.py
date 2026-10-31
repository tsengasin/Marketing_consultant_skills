"""
04_bandit_simulation.py
-----------------------
Why AI Decisioning uses bandits / RL instead of classic A/B tests, as a simulation.

Five email variants with TRUE (unknown to us) conversion rates.
We have 50,000 sends. Compare three strategies:

  1. A/B/n test : split evenly for the first 20,000 sends, then send the winner
  2. Epsilon-greedy : 90% send the current best, 10% explore at random
  3. Thompson sampling : sample from a Beta distribution for each variant, pick the highest

Then a mini CONTEXTUAL example: different segments prefer different variants.

No data files needed. Run: python 04_bandit_simulation.py
"""

import numpy as np

rng = np.random.default_rng(7)

VARIANTS = ["new_arrivals", "free_shipping", "pct10_off", "bestsellers", "back_in_stock"]
TRUE_RATES = np.array([0.040, 0.052, 0.047, 0.035, 0.030])  # free_shipping is truly best
N = 50_000
K = len(VARIANTS)


def run_ab_test(test_size=20_000):
    conversions, chosen = 0, np.zeros(K, int)
    succ, trials = np.zeros(K), np.zeros(K)
    for t in range(N):
        if t < test_size:
            a = t % K                      # equal split during the test
        else:
            a = int(np.argmax(succ / trials))  # then exploit the observed winner
        r = rng.random() < TRUE_RATES[a]
        if t < test_size:
            succ[a] += r
            trials[a] += 1
        conversions += r
        chosen[a] += 1
    return conversions, chosen


def run_epsilon_greedy(eps=0.10):
    succ, trials = np.zeros(K), np.zeros(K)
    conversions, chosen = 0, np.zeros(K, int)
    for t in range(N):
        if t < K or rng.random() < eps:
            a = t % K if t < K else rng.integers(K)   # explore
        else:
            a = int(np.argmax(succ / trials))         # exploit
        r = rng.random() < TRUE_RATES[a]
        succ[a] += r
        trials[a] += 1
        conversions += r
        chosen[a] += 1
    return conversions, chosen


def run_thompson():
    # Beta(1 + successes, 1 + failures) = our belief about each variant's conversion rate
    alpha, beta = np.ones(K), np.ones(K)
    conversions, chosen = 0, np.zeros(K, int)
    for _ in range(N):
        samples = rng.beta(alpha, beta)  # one random draw per variant from our belief
        a = int(np.argmax(samples))      # uncertain variants sometimes draw high -> natural exploration
        r = rng.random() < TRUE_RATES[a]
        alpha[a] += r
        beta[a] += 1 - r
        conversions += r
        chosen[a] += 1
    return conversions, chosen


best_possible = N * TRUE_RATES.max()
print("True rates (unknown to the algorithms):", ", ".join(f"{v}={r:.1%}" for v, r in zip(VARIANTS, TRUE_RATES)))
print(f"If we magically knew the best variant from day 1: ~{best_possible:,.0f} conversions\n")
print(f"{'Strategy':<20}{'Conversions':>12}{'Regret':>10}   Share of sends per variant")
for name, fn in [("A/B/n test", run_ab_test), ("Epsilon-greedy", run_epsilon_greedy), ("Thompson sampling", run_thompson)]:
    conv, chosen = fn()
    shares = "  ".join(f"{v[:8]}={c / N:.0%}" for v, c in zip(VARIANTS, chosen))
    print(f"{name:<20}{conv:>12,}{best_possible - conv:>10,.0f}   {shares}")

print("""
How to read this:
  * Regret = conversions lost vs. always sending the best variant.
  * The A/B test spends 20,000 sends split evenly, so 80% of them go to worse variants.
  * Bandits shift traffic to the winner as evidence builds up, so they earn more WHILE learning.
  (Results vary a little run to run. Randomness is the whole point.)
""")

# -----------------------------------------------------------------------------
print("=" * 80)
print("CONTEXTUAL example: the best message depends on the customer")
print("=" * 80)
SEGMENTS = ["new", "repeat", "lapsed"]
# rows = segment, cols = variant
SEG_RATES = np.array([
    [0.030, 0.070, 0.045, 0.040, 0.020],  # new: free shipping wins
    [0.065, 0.040, 0.035, 0.050, 0.045],  # repeat: new arrivals wins
    [0.015, 0.030, 0.050, 0.020, 0.025],  # lapsed: discount wins
])
SEG_MIX = [0.3, 0.4, 0.3]


def run(contextual: bool):
    a_ = np.ones((3, K)) if contextual else np.ones((1, K))
    b_ = np.ones_like(a_)
    conv = 0
    for _ in range(N):
        s = rng.choice(3, p=SEG_MIX)
        row = s if contextual else 0
        a = int(np.argmax(rng.beta(a_[row], b_[row])))
        r = rng.random() < SEG_RATES[s, a]
        a_[row, a] += r
        b_[row, a] += 1 - r
        conv += r
    return conv, a_ / (a_ + b_)


conv_plain, _ = run(contextual=False)
conv_ctx, est = run(contextual=True)
oracle = N * sum(m * SEG_RATES[i].max() for i, m in enumerate(SEG_MIX))
print(f"One-size-fits-all bandit : {conv_plain:,} conversions")
print(f"Contextual bandit (1:1)  : {conv_ctx:,} conversions")
print(f"Perfect per-segment      : ~{oracle:,.0f}")
print("\nWhat the contextual agent learned (best variant per segment):")
for i, seg in enumerate(SEGMENTS):
    print(f"  {seg:<7} -> {VARIANTS[int(np.argmax(est[i]))]}")
print("""
This is the core of a 1:1 campaign: no single 'winner' exists. The agent learns the winner
FOR EACH KIND OF CUSTOMER, and that per-segment pattern is exactly the kind of insight
you'd present to the marketing team.
""")
