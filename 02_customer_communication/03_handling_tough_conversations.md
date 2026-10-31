# 03: Handling Tough Customer Conversations

For each scenario: what the customer says, a **weak** answer, a **strong** answer, and **why** the strong one works. Interviewers love these, so expect at least one.

General framework, **A-C-E-N**:
1. **Acknowledge**: show you heard the concern (and the emotion).
2. **Clarify**: ask a question to find the real issue.
3. **Explain / Evidence**: give your view with data or reasoning.
4. **Next step**: agree on a concrete action.

---

## Scenario 1: "The AI is a black box. I can't trust it."

**Customer (CRM Director):** "My team doesn't understand why the AI sends what it sends. I can't present this to my VP if I can't explain it."

**❌ Weak:** "Don't worry, the model is very sophisticated and it's proven to work across many customers."

**✅ Strong:**
> "That's a completely fair concern. If you can't explain it, you can't defend it, and you shouldn't have to. Can I ask what your VP typically wants to see: the *why* behind individual decisions, or proof that the overall approach is working?
>
> *(listens)*
>
> We can cover both. For the overall picture, the holdout group gives you a clean comparison: AI vs. what you'd have done anyway. For the *why*, the insights show which messages went to which kinds of customers and how each performed. For example, I can already see that lapsed customers are getting the free-shipping message far more than the discount. I'd suggest I build you a one-page summary for your VP: headline lift, the three most interesting learnings, and what we're changing next. Would a draft by Thursday help?"

**Why it works:** validates the concern, finds out what "trust" means to *this* person, uses concrete evidence, and makes the customer look good to their boss.

---

## Scenario 2: "The results are worse than BAU."

**Customer:** "We're three weeks in and the AI group is converting *lower* than the holdout. Should we stop?"

**❌ Weak:** "It's still learning, just give it more time."

**✅ Strong:**
> "I'm glad you raised it straight away. Let's look at it together rather than guess. Three things I'd check, in this order:
> 1. **Is the difference real?** At three weeks with the volume we have, the gap may still be within normal noise. I'll show you the confidence interval.
> 2. **Is something broken?** For example, are conversions being tracked equally for both groups, and is the split still 90/10 as planned?
> 3. **Is it the early exploration phase?** The agent deliberately tests options early on. We'd expect that cost to shrink each week. I'll show you the weekly trend.
>
> I'll have this analysis to you by tomorrow. If it's a real negative effect, we'll pause and fix it. I don't want you carrying risk you're not comfortable with. Can we agree on a threshold now, for example 'if we're significantly worse after week 5, we pause'?"

**Why it works:** takes it seriously, gives a structured diagnosis (stats → data bugs → expected behaviour), offers an exit rule. Shows data maturity.

---

## Scenario 3: "Our data isn't ready."

**Data engineer:** "Honestly, our orders table is a mess. Duplicates from returns, and the email IDs don't match customer IDs."

**✅ Strong:**
> "Thanks for being upfront. That saves us weeks later. Let's size it. Roughly what share of email recipients can we match to a customer ID today? *(listens: '~75%')*
>
> OK. 75% is workable for a first use case if we're clear about the gap. Here's what I'd propose: we start with the matched 75%, build a deduplicated orders view (I can draft the SQL with you), and in parallel we track the matching issue as a phase-two improvement. Would that unblock us without overloading your team?"

**Why it works:** asks for numbers, finds a pragmatic path, offers hands-on help (the "forward deployed" part).

---

## Scenario 4: Scope creep

**Customer:** "While we're at it, can the AI also handle push, SMS, and our paid social audiences?"

**✅ Strong:**
> "I love the ambition, and yes, that's where this goes. My recommendation is that we nail email first, prove the lift with a clean holdout, and use that win to expand. If we launch four channels at once, we won't know what's driving results and the risk goes up. I'll add push and SMS to our phase-two roadmap. Shall we pencil in that conversation for the week-6 readout?"

---

## Scenario 5: The worried CRM team

**CRM Manager:** "Is this going to replace my team?"

**✅ Strong:**
> "I hear that question a lot, and it's an honest one. What I see at other brands is that the work shifts rather than disappears. Your team stops spending hours building segments and scheduling sends, and spends more time on what the agent can't do: creative ideas, new offers, brand strategy, and reading the insights. Honestly, the agent is only as good as the content your team gives it. What part of your current work would you most like to get rid of?"

---

## Scenario 6: The executive who wants a number now

**VP Marketing:** "What revenue uplift will I get?"

**✅ Strong:**
> "I don't want to give you a number I can't stand behind. It depends on your volume, content variety, and baseline. What I can tell you is how we'll *measure* it: a 10% holdout, a six-week read, and a revenue-per-recipient comparison you can take to the CFO. Before that, I can model a range from your current numbers so you have a realistic expectation. Would that be useful?"

---

## Scenario 7: Conflicting stakeholders

**CRM lead wants** to optimise for revenue. **Brand lead wants** no discounts at all.

**✅ Strong (as facilitator):**
> "I think you're both protecting something important: revenue on one side, brand and margin on the other. Can we make both explicit? What if the reward is revenue, *and* we set a guardrail that discounts can go to at most 20% of customers, never to full-price loyalists? Then we report discount cost alongside revenue. Would that address both concerns?"

---

## Practice drill
For each scenario, cover the strong answer and say your own version out loud in under 90 seconds. Record yourself. Check:
- [ ] Did I acknowledge before explaining?
- [ ] Did I ask at least one question?
- [ ] Did I use a number or concrete example?
- [ ] Did I end with a next step, owner, and date?
