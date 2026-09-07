# Session 31 — Final Project Presentations I

**Week 16 · Session 31 · Module C · 90 min · CLO-1, CLO-2, CLO-3**

## 1. Learning objectives

By the end of this session, students demonstrate they can:
- Present a complete data science project (question → data → EDA → model → AI component → reflection) in 10 minutes.
- Communicate findings to a non-technical audience with evidence, not jargon.
- Answer questions about their own decisions (cleaning choices, model choice, limitations).
- Give and receive constructive peer feedback.

## 2. Key concepts

- **A presentation is communication, the final lifecycle stage** — the analysis only matters if people act on it.
- **Structure mirrors the lifecycle:** question → data → method → findings → limits → reflection.
- **One message per slide;** charts carry evidence, words carry the story.
- **Honesty is a feature:** stating limitations builds credibility, it doesn't lose marks.
- **Rubric-driven:** every rubric line in `../assessment-plan.md` is a slide.

## 3. Detailed lecture notes

**Session format (90 min):**
- **0–5 min:** logistics — order of teams, timing (10 min talk + 3 min Q&A), peer-feedback forms.
- **5–75 min:** presentations (~5–6 teams, depending on class size; half the teams present today, the rest Session 32).
- **75–90 min:** instructor summary, common strengths/weaknesses, final-submission reminders.

**The presentation structure (mirror the rubric).** Tell students to map every
rubric line to a slide:
1. **Question & motivation** (problem framing): why does this question matter — in one sentence a non-expert understands.
2. **Data & provenance** (acquisition): source, license, size, and *who's in it* (Session 30's representation question).
3. **Cleaning & EDA** (CLO-1): 2–3 cleaning decisions with justification; 2–3 findings with chart evidence (finding → evidence → implication from Session 15).
4. **Model** (CLO-2): what was tried (baseline first!), what won (CV, Session 22), honest metrics.
5. **AI-assisted component** (CLO-3): what the AI did, how it was verified (Sessions 25–28), what it genuinely added.
6. **Reproducibility & ethics reflection** (CLO-3): how to reproduce (Session 24), one bias/privacy consideration (Session 30).
7. **Limitations & next steps:** what you'd do with more time/data.
That's 7–9 slides — one idea each. Charts from `figures/`, numbers with units,
no code dumps (code lives in the repo, which was submitted).

**Presentation craft (10 practical rules):**
- Practice against a timer — 10 minutes is shorter than it feels; aim for 9.
- One slide = one message; the audience reads slides, they listen to *you*.
- Talk to the audience, not the screen; face the room; slow down.
- Every chart: "what does this show and why does it matter?" — don't just flash it.
- Number every finding; state limitations unprompted (it earns trust).
- Rehearse the first 30 seconds — the opening sets the tone.
- Prepare for Q&A: what would *you* ask about your own project? (Cleaning choice, model choice, "what if the data were biased?", "how would you improve it?")
- Peer feedback: one strength + one specific suggestion, written, not vague praise.
- Technical failures happen — have a PDF fallback of your slides.

**The Q&A mindset.** The goal isn't to be unimpeachable; it's to show you
*understand your own decisions*. Honest answers ("we considered X and chose Y
because...") score higher than defensive or vague ones. If you don't know,
say what you'd do to find out. This is the last demonstration of the course's
central skill: knowing what your results mean — and don't mean.

## 4. Important terminology

- **Elevator pitch** — the question + answer in under 30 seconds.
- **Finding → evidence → implication** — the structure of every claims slide.
- **Limitations** — what the analysis can't claim; stated explicitly.
- **Q&A** — question/answer period; the understanding check.
- **Peer feedback** — one strength + one suggestion per presentation.
- **Deck** — the slide set (7–9 slides recommended).
- **Rubric mapping** — each slide covers a rubric line.
- **Fallback** — a PDF copy of slides in case the projector fails.

## 5. Python examples

Preparation tooling (not for the deck itself):

```python
# A final sanity pass over every number you'll quote (no stale stats!)
import seaborn as sns
import pandas as pd

tips = sns.load_dataset("tips")
print(tips.groupby("day")["tip"].mean().round(2))     # verify: matches your slide?
print(tips.isna().sum())                               # verify: cleaning claims

# Print the repo's key facts for the provenance slide:
print("Rows:", len(tips), "| Source: seaborn (CC BY)")
```

## 6. Beginner example

```python
# The 30-second pitch template (fill in, practice out loud):
# "We asked [question]. We used [data — source, size]. We found [finding 1]
#  and [finding 2]. A [model] predicts [target] with [metric], and an
#  [AI component] helped [task], verified by [check]. The main limitation is
#  [limitation]."
```

## 7. Practical Data Science example

A model "finding slide" done right (put on the board as a template):

> **Slide title:** Tips are ~15% higher on weekends — and it's not party size.
> **Chart:** boxplot of tip% by day (from Session 14).
> **Number:** mean tip% Fri 13.2% vs Sat/Sun 15.5% (p-value-free comparison:
>   overlap of boxes noted honestly).
> **Limitation line:** small sample; smoking status not controlled.
> **Implication:** a restaurant could staff differently — but we wouldn't
>   claim causation (Session 15's rule).

## 8. In-class activity

Presentations *are* the activity (format in section 3). Presenters: arrive with
slides loaded, PDF fallback ready, and the repo open for Q&A references.
Non-presenters: complete the peer-feedback form (one strength, one suggestion,
one question) for each team; these forms count toward participation.

## 9. Lab exercise

No lab. Final deliverables to confirm before Session 32:
- Repo complete: executed notebooks, `requirements.txt`, README with "How to reproduce" (Session 24).
- Final submission due Session 32 (repo + final report/reflection + presentation).
- **Assignment 3** (due Session 30) already pushed.

## 10. Common mistakes (presentation-specific)

- Reading slides verbatim — the audience can read; you must *explain*.
- Code dumps — the repo is the code home; slides carry evidence.
- Charts without a spoken takeaway ("here's a plot…" with no "and it shows…").
- Overshooting the time — the Q&A is part of the grade; finish on time.
- Hiding limitations until asked — state them; it builds credibility.
- Overstating conclusions ("proves", "causes") — use "suggests", "is associated with".
- Ignoring the rubric when building slides — map each slide to a line.

## 11. Short assessment questions

Self-check before you present:
1. Can you state your question and answer in under 30 seconds?
2. Can you name your data's source and license without notes?
3. Can you explain *why* you made your top cleaning decision?
4. Can you state one limitation of your model unprompted?
5. Can you say exactly what AI did and how you verified it?
6. Does every slide have exactly one message?

## 12. CLO mapping

The presentation is the *communication* proof for all three CLOs: CLO-1 (data
+ EDA claims with evidence), CLO-2 (model choice defended), CLO-3 (AI component
shown, verified, and reflected on). The rubric in `../assessment-plan.md` maps
each criterion to a CLO.

## 13. Suggested homework

- Presenters from today: incorporate one piece of feedback into the final submission (due Session 32).
- Remaining teams: rehearse tonight with the timing rules; load slides early.
- Everyone: submit the final report/reflection and repo link before Session 32's deadline.
- Preview: Session 32 — remaining presentations, the final exam, and course wrap-up (what you can now do, and what's next).