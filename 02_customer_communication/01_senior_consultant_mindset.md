# 01: Think and Talk Like a Senior Consultant

*Written in the voice of a senior consultant coaching a new hire.*

---

> "Here's the thing nobody tells you in your first month: customers don't remember your analysis. They remember whether you made them **feel in control** and whether you made them **look good to their boss**. Everything below serves those two things."

## Rule 1: Answer first, then explain (the Pyramid Principle)

Junior consultants tell the story in the order they discovered it. Seniors lead with the conclusion.

**❌ Junior:**
> "So we pulled the data from the last six weeks, and we looked at the holdout group, and there were some data quality issues in week two which we fixed, and then when we compared conversion rates we found that..."

**✅ Senior:**
> "The short answer: AI Decisioning is driving **8% more purchases** than your BAU campaigns, and we're confident it's real. Three things behind that: [1]... [2]... [3]... Want me to go into any of them?"

**Structure:** *Answer → 3 supporting points → evidence on request.*

## Rule 2: SCQA for anything persuasive

- **Situation**: what everyone agrees on
- **Complication**: what changed or what's wrong
- **Question**: the question that raises
- **Answer**: your recommendation

> **S:** "Your weekly promo email is your biggest revenue driver in CRM."
> **C:** "But open rates have dropped 15% this year, and unsubscribes are rising. Same message, same time, to everyone."
> **Q:** "So how do we keep the revenue but stop burning out the list?"
> **A:** "Start with that email as the first AI Decisioning use case: let the agent choose message and send time per person, with a 10% holdout so we can prove the lift in 6 weeks."

## Rule 3: Always land the "so what"

Every number needs a business consequence.

| Without "so what" | With "so what" |
|---|---|
| "Click rate went from 2.1% to 2.4%." | "Click rate is up 14%. At your volume that's roughly 30k extra visits a week to the site." |
| "Offer C is rarely chosen." | "Offer C is rarely chosen, so it's not working for anyone. Let's replace it and give the agent something new to learn from." |

## Rule 4: Discover before you prescribe

The fastest way to lose credibility is to recommend a solution before you understand the problem. In the first meeting, aim to **talk 30% and listen 70%**.

> "Before I suggest anything, can I understand how the weekly campaign gets built today, from idea to send?"

## Rule 5: Make complexity simple, but never dumb it down

Use analogies the audience owns.

- **To a CMO:** "Think of it as running hundreds of A/B tests at once, and instead of picking one winner for everyone, each customer gets their own winner."
- **To a CRM manager:** "You still own the content and the rules. The agent takes over the *who gets what, when* part you currently do with segments and calendars."
- **To a data engineer:** "It's a contextual bandit. Features come from a customer-level table in your warehouse, rewards from the orders table joined on customer ID within a 7-day window."

## Rule 6: Bad news early, with a plan

> "I want to flag a risk early: about 20% of your email sends can't be matched to a customer ID in the warehouse. That means the agent can't learn from those people. Here's what I suggest: [plan]. Here's the impact if we don't: [impact]. I need [person] to [action] by [date]."

**Formula:** *Issue → Impact → Proposal → Ask (with owner and date)*

## Rule 7: Own the next step

Never end a meeting without:
1. A recap of what was decided
2. Action items with **owners and dates**
3. When you'll talk next

> "To recap: we're going with win-back as use case one, reward is purchase within 14 days, 10% holdout. I'll send the data requirements doc by Thursday. Sarah, could your team confirm the event table access by next Tuesday? I'll book the design review for the 14th."

## Rule 8: Say "I don't know" like a senior

> ❌ "Umm, I'm not sure, maybe..."
> ✅ "Good question. I don't want to guess on that. I'll confirm with our ML team and come back to you by Friday."

## Rule 9: Tone

- **Calm and confident**, not salesy. You're an advisor, not a vendor.
- **"We"** language: "What we're going to prove together..."
- **Curious**: "Help me understand..." / "What's driving that?"
- **Direct but kind**: "I'd push back on that a little, because..."
- **Empathetic** to the CRM team, whose jobs are changing: "This frees your team from building 40 segments a week so they can focus on creative and strategy."

## Phrase bank

| Situation | Phrase |
|---|---|
| Open a meeting | "The goal for today is X. By the end I'd like us to have decided Y. Does that work?" |
| Probe deeper | "Can you walk me through an example?" / "What happens today when...?" |
| Clarify | "So if I understood correctly, the main concern is X. Is that right?" |
| Disagree | "I see why you'd want that. My concern is X. What if we tried Y instead?" |
| Redirect scope creep | "That's a great idea for phase two. Let me capture it so we don't lose it, and keep today focused on X." |
| Handle silence | Wait three seconds. Then: "What's going through your mind?" |
| Close | "What would make you confident to sign off on this?" |
