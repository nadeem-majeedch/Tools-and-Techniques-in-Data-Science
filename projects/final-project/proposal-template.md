# Project Proposal

**Team:** `<names>` **Date:** `<date>` · Due W13 S26 · One page max

---

## 1. Question (one sentence)

> We will find out: **<question, answerable with data>**.

## 2. Audience & decision

- Who cares: **<stakeholder>**
- The decision our answer would inform: **<decision>**

## 3. Dataset

| Field | Answer |
|---|---|
| Source | <name / URL / API> |
| License | <license, e.g., CC0 / CC BY 4.0> |
| Retrieval | <keyless API call / download URL / seaborn built-in> |
| Shape (verified) | <rows × columns — actually loaded it> |
| Verified loads? | ✅ / ❌ (must be ✅ before submission) |

## 4. Framing

- Target variable: **<column>**
- Candidate features: **<columns>**
- Type: supervised/unsupervised · regression/classification/clustering

## 5. Success metric (one checkable number)

> Success = **<e.g., test MAE ≤ X or CV accuracy ≥ Y>**

## 6. Planned pipeline (3–4 bullets)

1. Acquire + cache (`data_loader.py`).
2. Clean + EDA (cleaning log, 3 figures).
3. Model + evaluation (baseline comparison).
4. Streamlit app (widgets: <list>).

## 7. Top risks & mitigations

| Risk | Mitigation |
|---|---|
| <e.g., data too small / imbalanced> | <stratified splits / different question> |
| <metric too optimistic> | <baseline + CV> |
| <time> | <scope cut list> |

## 8. Threats to validity (4–6 sentences)

Under what conditions would your conclusion be wrong? Name at least one
data problem (missingness, sampling bias) and one modeling problem
(overfitting, leakage). This paragraph becomes part of the final report.

---

*Approved: ____________ (instructor)*