# Evaluation and self-optimization protocol

Use paired, content-matched evaluation. The aim is better academic language and reduced formulaic risk without semantic drift, not authorship detection.

## A/B setup

For each source passage, create **A — control**, an ordinary language edit without this skill, and **B — treatment**, an independent language edit using the skill.

Do not revise A into B during formal evaluation; leakage makes the comparison optimistic. A release benchmark should contain at least 300 paired passages, with balanced Chinese and English coverage and explicit no-change cases. Blind-review a stratified sample of at least 10% (and no fewer than 36 passages) spanning abstracts and body prose, theoretical and empirical registers, language-risk categories, and passages where a reasonable editor should make no change.

## Blind substantive rubric (100 points)

Two reviewers should see randomized, unlabeled texts. Score each dimension 1–5, then multiply by the weight.

| Dimension | Weight | Anchor for 5 |
|---|---:|---|
| Semantic fidelity | 5 | propositions, scope, polarity, modality, and evidence strength unchanged |
| Lexical precision | 4 | exact, economical wording; technical terms remain stable |
| Syntax and readability | 4 | grammatical relations are clear; density is controlled without flattening |
| Cohesion and transitions | 2 | relations are legible without excessive signposting |
| Rhythm and authorial voice | 3 | purposeful variation; source voice is not homogenized |
| Formulaic-style control | 2 | little ceremonial framing, inflated diction, or template repetition |

Score = sum(rating × weight). Record reviewer rationale and adjudicate disagreements greater than one rating point.

## Automated diagnostics

Run:

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONNOUSERSITE='1'
& 'G:\skills\.venv\Scripts\python.exe' scripts/style_audit.py path\to\draft.md --format markdown
& 'G:\skills\.venv\Scripts\python.exe' scripts/evaluate_benchmark.py benchmark\cases.jsonl --format markdown
```

The audit reports formulaic-pattern density, repetition, sentence/paragraph variation, specificity proxies, citation markers, and a bounded risk score. A lower formulaic-risk score is desirable, but no threshold proves human authorship or publication quality.

## Acceptance gates

A release candidate passes only if:

1. no semantic drift, invented content, or citation changes appear;
2. mean blind language score for B exceeds A by at least 8/100;
3. B wins or ties in at least 90% of blind cases, wins at least 60% of non-ties, and loses none by more than 5 points;
4. median formulaic-risk density falls by at least 30%;
5. gains remain when lexical marker points are removed from the automated score;
6. a reviewer confirms that revisions did not erase meaning, warranted uncertainty, terminology, or author voice.

Treat these as project acceptance criteria, not universal psychometric cutoffs.

## Self-optimization loop

1. Freeze prompts, evidence packets, and evaluator instructions for the release.
2. Run A/B drafts and blind review.
3. Classify failures by cause: semantic drift, diction, syntax, transition, rhythm/voice, terminology, or surface formula.
4. Change the narrowest instruction or diagnostic that addresses repeated failures. Do not add universal bans from one example.
5. Re-run the frozen benchmark and a new holdout set.
6. Reject changes that improve detector-facing metrics while lowering language scores or semantic fidelity.
7. Record results and rationale under the next semantic version.

Report mean and median paired deltas, win/tie/loss counts, and individual cases. With small samples, describe uncertainty plainly; do not use false precision.
