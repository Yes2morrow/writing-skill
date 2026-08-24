# Benchmark analysis — v1.0.0

## Design

- 12 synthetic imitation papers: six Chinese and six English.
- 30 paired passages per paper: 360 pairs and 720 edited paragraphs.
- Six labeled section contexts, 60 pairs each.
- Ten language-risk types, 36 pairs each: paired escalation, manufactured contrast, ceremonial framing, navigation markers, inflated lexicon, vague action, uniform openings, terminology instability, hedge preservation, and legitimate contrast.
- Each pair contains a source semantic contract, an ordinary control edit, and a skill-guided edit.
- Thirty-six cases were selected with a fixed seed across language and section and randomized as A/B for independent blind review.

The eight-case pilot remains only a regression fixture. It is not included in release claims.

## Results

Automated diagnostics over all 360 pairs:

- skill edit lower risk: 204;
- tie: 156;
- skill edit higher risk: 0;
- mean treatment-minus-control configured risk: −5.1 points.

The large tie count is intentional. It includes passages that preserve warranted contrast, hedging, or already acceptable wording; the skill should not edit merely to appear active.

Independent blind language review over 36 stratified cases, before the final narrow scope repair:

- skill mean: 97.03/100;
- control mean: 71.08/100;
- mean difference: +25.94 points;
- relative difference against control mean: +36.5%;
- skill win/tie/loss: 29/7/0.

The reviewer found nine skill passages that omitted an exact site or institution even though they retained the sample limit. This violated the zero-drift release gate. The generator and invariants were changed to require an exact `scope_anchor` in every treatment. A targeted independent re-audit of all nine failures then found 0 remaining drift cases. The full blind set was not rescored after that repair, so this report does not infer a revised mean.

## What the numbers mean

The blind result supports a large improvement on this deliberately difficult synthetic set. It does not establish the same effect on real manuscripts. The automated score measures configured patterns, not AI authorship, originality, argument quality, or publication readiness.

## Self-optimization record

1. **Pilot overfit:** an eight-case marker-heavy test produced 100% risk reduction. Response: demoted it to a smoke test and built 360 paired cases.
2. **False-positive risk:** a justified `不是……而是……` contrast was penalized too strongly. Response: capped a lone contrast as a low-risk cue and added a unit test.
3. **Semantic-contract failure:** first large-corpus blind review found both variants drifting because source contracts omitted comparison and modality. Response: made source contracts risk-specific and regenerated the corpus.
4. **Scope loss:** second blind review found nine treatment passages dropping exact sites. Response: introduced `scope_anchor`, enforced it across 360 cases, and independently re-audited the failures.

## Remaining limitations

- Synthetic paragraphs use controlled facts and cannot reproduce all variation in published prose.
- One independent evaluator scored the blind sample; no inter-rater reliability is claimed.
- Section labels broaden coverage, but the benchmark isolates paragraph-level language rather than evaluating whole-paper coherence, consistent with this skill's scope.
- A future minor release should add author-owned and pre-LLM holdout text, preserve the frozen v1 corpus, and recruit at least two blind reviewers.
