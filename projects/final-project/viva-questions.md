# Final Project — Viva Questions

Asked individually after the presentation (2–4 questions per member,
focused on the member's own components). "What to listen for" notes are
for the examiner; students see only the questions.

---

## A. Problem & data (CLO-1)

1. Restate your research question in one sentence. Why is it answerable
   with your data?
   *Listen for:* a specific question; no claims the data can't support.
2. Where is your data from, and what is its license? Why does the license
   matter for a graded project?
   *Listen for:* source + license named; awareness of reuse/attribution.
3. How did you fetch the data, and how is it cached? What happens if you
   run your code offline tomorrow?
   *Listen for:* cache path, freshness rule, offline behavior.
4. What is the difference between your target variable and your features?
   *Listen for:* roles defined correctly with their own columns.

## B. Cleaning (CLO-1)

5. Show one cleaning decision you made. Why did you drop rather than fill
   (or vice versa)?
   *Listen for:* a *reason*, not "it was easier".
6. How did you handle duplicates, and why on that subset of columns?
   *Listen for:* subset choice justified (e.g., email vs. all columns).
7. What dtype mistakes did you find, and how did you fix them?
   *Listen for:* stringy numbers, object date columns, `astype` on NaN.
8. How do you know your cleaning didn't lose data you needed?
   *Listen for:* row counts logged before/after; missingness re-checked.

## C. EDA & visualization (CLO-1)

9. What is one pattern you found in EDA that surprised you? What evidence
   (number/figure) supports it?
   *Listen for:* claim → evidence → figure reference.
10. Why is correlation not causation? Apply that to your own data.
    *Listen for:* a confounder or direction-of-effect caveat.
11. Why did you choose that chart type for that question?
    *Listen for:* chart-question fit (trend → line, distribution →
    histogram, etc.).

## D. Modeling (CLO-2)

12. What is your model trying to predict or find? Supervised or
    unsupervised, and why?
    *Listen for:* labels vs. no labels correctly identified.
13. What is a train/test split for, and where did your test set come from?
    *Listen for:* unseen data; no leakage.
14. What is your metric, and why that one over accuracy/MAE?
    *Listen for:* metric matched to problem (e.g., recall for rare class).
15. What was your baseline, and how much better is your model?
    *Listen for:* exact comparison numbers.
16. Could your model be overfitting? How would you know?
    *Listen for:* train vs. test gap; depth/regularization controls.
17. Why do you scale features before k-NN but not before a decision tree?
    *Listen for:* distances vs. per-feature thresholds.

## E. Streamlit app (CLO-1)

18. Walk us through your app: what does each widget control?
    *Listen for:* every widget demonstrably changes output.
19. Why did you use `@st.cache_data` on the load function?
    *Listen for:* avoids refetch on every rerun; speed + API politeness.
20. What happens if the API is down when the app starts?
    *Listen for:* cache fallback or graceful message.
21. Your app shows a chart. What would a manager misread in it, and what
    did you do to prevent that?
    *Listen for:* labeling, sample size, truncated axes awareness.

## F. AI-assisted & optional components (CLO-3)

22. What AI assistance did you use, and how did you verify the output?
    *Listen for:* tool + prompt + verification protocol (Session 25).
23. Why is "the AI said so" not an acceptable justification in this
    course?
    *Listen for:* hallucination risk; verification duty.
24. (If PandasAI/Ollama used) What exactly left your machine when you used
    it, and why was that safe?
    *Listen for:* aggregates only; local model; privacy reasoning.
25. (If agent used) In your agent loop, who executes the tool and why is
    that a safety property?
    *Listen for:* model proposes, code executes; registry guard.
26. (If n8n used) How do you know your automation didn't duplicate data?
    *Listen for:* idempotency by key.

## G. Reproducibility & ethics (CLO-3)

27. What makes your project reproducible, and how did you verify it?
    *Listen for:* pins, seeds, Restart & Run All, fresh-env run.
28. What is one limitation of your data, and how does it limit your
    conclusion?
    *Listen for:* honest, specific limitation.
29. Could your analysis mislead someone? Give the scenario.
    *Listen for:* threats-to-validity thinking.
30. If a stakeholder asked you to deploy your model tomorrow, what would
    you check first?
    *Listen for:* per-group performance, more data, monitoring.

## H. Project-management questions

31. What did each teammate own, and what did you learn from a
    disagreement?
    *Listen for:* real collaboration; resolution.
32. If you had one more week, what's the single most valuable thing you'd
    do?
    *Listen for:* prioritized, concrete, not "make it prettier".