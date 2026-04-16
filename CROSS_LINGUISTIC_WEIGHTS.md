# Cross-Linguistic Construction Similarity: Weighting Rationale

## Theoretical Foundation

In construction grammar, constructions are **form-meaning pairings**. For this analysis, all comparative concepts are treated as equally important, without privileging one CC type over another.

## Equal CC-Type Importance

This approach assigns the same weight to each comparative concept type:
- `cxn`
- `str`
- `sem`
- `inf`

That means the similarity score reflects the raw overlap of comparative concepts and their type profile without pre-imposing a hierarchical bias.

---

## Why Equal Weighting?

### Transparent baseline

Equal weights are the least theory-laden choice. They allow the data to drive similarity patterns rather than a prior preference for certain CC types.

### Useful for exploratory cross-linguistic work

When comparing constructions across languages, this is a strong baseline because:
- it treats all concept types as equally informative,
- it avoids privileging construction type or structure over semantics,
- it supports direct comparison of network structure under the assumption of uniform importance.

---

## Current Configuration

The code now uses:

```python
CC_TYPE_WEIGHTS = {
    'cxn': 1.0,
    'str': 1.0,
    'sem': 1.0,
    'inf': 1.0,
}
```

This means every comparative concept contributes equally to the weighted similarity score.

---

## Alternative Weighting Schemes

### Option A: Equal Weights (Baseline)
```python
CC_TYPE_WEIGHTS = {'cxn': 1.0, 'sem': 1.0, 'str': 1.0, 'inf': 1.0}
```
**Use:** When you want all comparative concepts to count the same.

### Option B: Form-Focused
```python
CC_TYPE_WEIGHTS = {'cxn': 1.0, 'sem': 0.8, 'str': 0.6, 'inf': 0.4}
```
**Use:** When construction and structure are assumed slightly more stable than semantics.

### Option C: Meaning-Focused
```python
CC_TYPE_WEIGHTS = {'cxn': 0.6, 'sem': 2.0, 'str': 0.7, 'inf': 0.4}
```
**Use:** When semantic similarity is prioritized.

### Option D: Formal Patterns Only
```python
CC_TYPE_WEIGHTS = {'cxn': 1.5, 'sem': 0.1, 'str': 2.0, 'inf': 0.1}
```
**Use:** When morphosyntax is the main focus.
```

---

## Recommended for This Analysis

Use the equal-weight baseline:

```python
CC_TYPE_WEIGHTS = {
    'cxn': 1.0,
    'str': 1.0,
    'sem': 1.0,
    'inf': 1.0,
}
```

**Why this is recommended:**
- It avoids introducing bias among CC types.
- It treats each comparative concept as equally relevant.
- It is a robust starting point for exploratory cross-linguistic network analysis.

---

## Testing and Validation

To validate the equal-weight scheme:

1. Compare resulting clusters to manually expected construction groups.
2. Check whether constructions with similar CC overlap appear near each other.
3. Compare with alternative weightings to see whether equal weights produce qualitatively different groupings.
4. Use the result as a reference baseline for future weighting experiments.

---

## Implementation Note

The current code in `compute_similarity.py` now uses equal CC-type weights. If you want to test a different scheme later, update `SimilarityConfig.CC_TYPE_WEIGHTS` accordingly.
