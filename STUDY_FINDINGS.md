# Copilot Agency Study — Findings

**Author:** Archita Sindigi  
**Date:** June 2026  
**Context:** Microsoft Build 2026 — LIVE162 session  
**Research question:** When should you trust the agent?

---

## Setup

I ran GitHub Copilot Agent (VS Code) on 5 issues across a small Flask task API.
Before each issue, I recorded a prediction. After each, I recorded what actually happened.
The goal was not to evaluate code quality — it was to understand where human judgment
is still irreplaceable, and where it is not.

---

## Pre-Study Hypothesis

> Copilot performs better on tasks with unambiguous specs and known code patterns.
> Tasks requiring contextual reasoning or judgment will produce lower quality output
> even if technically valid.

Recorded: 5 June 2026, before running any tasks.

---

## Issue-by-Issue Findings

### Issue 1 — Bug Report (GET /tasks returns 500 on empty list)
**Prediction:** Will STRUGGLE — requires understanding of app state and initialization context  
**Actual:** Agent OUTPERFORMED expectation

The agent did not reproduce the bug. It read the code, reasoned about what could
cause a 500, initially said "this should work fine," then changed its mind. It found
a duplicate decorator introduced by our own earlier edits — a different problem than
what was reported — and correctly concluded that `jsonify([])` works fine in Flask.
The reported bug did not exist.

**HAI finding:** This is the inverse of automation bias. The agent showed appropriate
skepticism of a flawed bug report rather than complying blindly. But this raises a
harder question: should we trust that skepticism? What if it had been wrong, and the
bug did exist?

---

### Issue 2 — Feature (Add DELETE endpoint)
**Prediction:** Will SUCCEED — clear spec, standard pattern  
**Actual:** Partially correct

The agent went straight to implementation; no clarifying questions asked. The code was
clean, correct per the spec, and handled both success and not-found cases. I accepted
it. Then I tested an edge case the spec never mentioned: delete task 1, create a new
task — what ID does it get?

It got id 1. ID collision. The agent used `len(tasks) + 1` which recycles IDs after
deletion. The spec said nothing about ID uniqueness. The agent said nothing either.

**HAI finding:** The agent was 100% compliant with the spec and 100% silent about a
real-world problem the spec forgot to mention. A human junior developer might have
flagged this. The agent's confidence gave no signal that anything was uncertain.
This is automation bias in action — I nearly accepted it without checking.

---

### Issue 3 — Refactor (Extract TaskService class)
**Prediction:** Will STRUGGLE — requires understanding intent behind code structure  
**Actual:** SUCCEEDED — better than predicted

The agent produced clean, well-structured code. But it made four architectural
decisions without telling me:

1. Moved global state into class instance variables
2. Added a `get_task()` helper method not mentioned in the spec
3. Used `return None` rather than raising an exception for missing tasks
4. Used `return False` rather than raising an exception for delete failures

All four decisions were reasonable. But I did not know they were made. I would have
had to read carefully to notice — and most developers, trusting a confident-looking
output, would not.

**HAI finding:** The agent acts decisively and buries its decisions in code. Humans
inherit invisible architectural choices. The agent does not disclose what it assumed.

---

### Issue 4 — Documentation (Add API README)
**Prediction:** Will SUCCEED but with AI-flavoured language  
**Actual:** Correct on both counts

The docs were technically complete — accurate curl examples, correct status codes,
clean structure. But the language was human-empty. AI patterns spotted:

- Generic opening description ("A simple Flask REST API for managing tasks")
- Filler phrases ("in the system")
- States the obvious repeatedly
- Zero personality, zero voice
- No context for why this project exists

I rewrote the opening myself. The rewrite took five minutes and made the document
mine. The agent's version would have been indistinguishable from any other
AI-generated README.

**HAI finding:** AI documentation is technically complete but contextually empty.
A reader learns what the API does but nothing about who built it or why. In a
portfolio context, that absence of voice is itself a signal to an interviewer.
This raises an open research question: should AI writing tools detect and flag
the absence of human voice?

---

### Issue 5 — Tests (Add pytest suite)
**Prediction:** Will SUCCEED — pytest patterns are heavily represented in training data  
**Actual:** Correct

This was the most thorough approach of all five issues. The agent read three files
before writing a single line, planned a test isolation strategy using a reset fixture,
and ran pytest itself to verify tests passed. 6 tests, all passing.

But it missed:
- Empty string title `{"title": ""}`
- Double deletion of the same task
- The ID collision scenario we found manually in Issue 2

**HAI finding:** The tests pass but do not fully protect. Coverage looks complete;
protection has gaps. This connects directly to BRK208 — the session on AI testing
that argues coverage numbers are not the same as safety. The study came full circle.

Also: for the first time across all five issues, the agent asked a clarifying question.
"Would you like me to commit these tests or add a GitHub Actions workflow?"

It asked at a completion boundary, not at an ambiguity boundary. It acted through
uncertainty and paused at a fork. That pattern — initiative during, interruptibility
after — appears to be consistent behaviour, not accident.

---

## Cross-Issue Patterns

### Pattern 1 — The agent never asks clarifying questions mid-task
Across all five issues, every question came at a completion boundary. During execution,
regardless of ambiguity, the agent acted. This is a known HAI design tension:
**initiative vs. interruptibility**. Microsoft, Google, and CMU have active research on this.

Arguments for immediate action: faster, less friction, you can always undo.  
Arguments against: assumptions baked silently into code, false confidence, user does not
know what was assumed.

### Pattern 2 — Spec compliance ≠ real-world correctness
Issue 2 demonstrated this most clearly. The agent satisfied every requirement in the
spec and introduced a production bug the spec never addressed. The agent had no mechanism
to say "I notice the spec is silent on X — should I handle it?"

### Pattern 3 — Thoroughness is inconsistent
Issue 2: jumped straight to code. Issue 5: read three files, planned isolation strategy,
ran tests. Same agent, different behaviour. Whether this variation is driven by task type,
prompt length, or random sampling is unclear. If thoroughness is inconsistent, users
cannot rely on it.

### Pattern 4 — Agent decisions are invisible by default
Across Issues 2, 3, and 5, the agent made decisions beyond the spec without disclosure.
Some were correct (Issue 1 skepticism). Some introduced bugs (Issue 2 ID collision).
Some were sound but undisclosed (Issue 3 architecture). The user must read carefully
to know what was decided. Most users will not.

---

## Conclusion

My hypothesis held: Copilot performs better on tasks with unambiguous specs and known
patterns. But the more interesting finding is subtler — the agent is not just better or
worse by task type. It is **consistently non-disclosing**. It acts, it completes, it
presents. It does not flag uncertainty, does not surface assumptions, does not say
"I noticed the spec was silent on X."

That silence is the design choice with the largest human consequences. A confident-looking
output from a capable agent is precisely the condition most likely to produce automation
bias — a user who accepts without checking, inherits invisible decisions, and discovers
gaps only in production.

The gap between spec compliance and real-world correctness is not a model limitation.
It is a **human-AI interaction design problem**. It belongs to the interface, not the model.

---

## What I Would Build Next

A disclosure layer for AI coding agents: a lightweight mechanism that surfaces assumptions
made during code generation — not as warnings that interrupt flow, but as a reviewable
artifact alongside the code. Something like a git commit message, but for the agent's
reasoning. Opt-in, concise, and human-readable.

That is the HAI contribution this study points toward.

---

*This document was written by Archita Sindigi based on notes recorded during the study.
The findings reflect one developer's experience across five tasks. They are observational,
not statistically generalisable — but they are real, and they are mine.*