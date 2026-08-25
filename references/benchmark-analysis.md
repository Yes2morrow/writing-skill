# Benchmark analysis

## v1.1.0 local-corpus and no-skill holdout

### Design

- Discovered 205 local scholarly PDFs and extracted a bounded first-ten-page sample with PDFium.
- Retained 85 documents above the 1,800-character threshold: 68 Chinese and 17 English. Excluded 117 with insufficient text layers and three PDFium failures.
- Visually checked representative English double-column journal pages, a Chinese double-column technical paper, and a Chinese image-rich architectural essay before interpreting extraction metrics.
- Generated ten additional fictional no-skill papers: five Chinese and five English, 30 paragraphs each, for 300 held-out paragraphs across 15 language-habit categories.
- Preserved only copyright-safe aggregate and document metrics from the local publications; no extracted full text is committed.

### Local comparison

Median configured formulaic-cue density per 10,000 non-space characters was 390.81 for Chinese no-skill papers versus 41.05 for local Chinese publications, and 127.51 versus 20.15 in English. The largest recurring gaps involved inflated lexicon, excessive navigation, vague-action frames, empty transitions, abstract shells, and overclaiming.

Sentence-length CV was 0.446 for Chinese no-skill papers versus 0.999 locally, and 0.443 versus 0.820 in English. The direction supports content-led rhythm and syntactic variation; it does not justify random sentence-length changes or a universal target.

Direct-verb frequency was not accepted as a standalone quality signal. The no-skill corpus often repeated `研究记录/发现/测得` or `the study recorded/identified/measured`, demonstrating that a high verb count can coexist with mechanical sentence frames.

### Held-out automated check

The 300 source contracts were used as conservative skill-reference edits against independently generated no-skill passages. Configured formulaic risk was lower in 228 cases, tied in 72, and higher in none. Mean treatment-minus-control risk was −7.0 points; median relative reduction among the reported case distribution was 100%.

The frozen v1 corpus was also rerun under the expanded v1.1 diagnostics: 222 lower-risk treatments, 138 ties, no losses, and a −5.5-point mean delta. Its v1.0 score remains preserved below because the diagnostic definition changed in this minor release.

This is a deterministic diagnostic check, not an independent human language score. The source contracts are deliberately concise, so the estimate is optimistic for formulaic-marker removal and cannot establish publication-quality improvement. The v1.0 blind review remains the human-scored evidence; no new blind human score is claimed for v1.1.

### Changes supported by failures

1. Added first-class instructions for abstract shells, stacked modifiers, echo conclusions, empty transitions, claim–disclaimer mismatch, and terminological costume changes.
2. Added a prose-finish ladder that separates grammatical correction, specification, information contour, cadence, textural verb choice, and restraint.
3. Rejected direct-verb counts as a proxy for mature prose; the skill now checks the specificity and recurrence of subject–action–object frames.
4. Retained qualified use of conventional contrasts and long sentences because local publications also contain them. Zero marker density remains an invalid target.
5. Fixed numeric-anchor detection for digits adjacent to Chinese characters and added regression tests.

### v1.1 limitations

- Extractable local English material is smaller than the Chinese sample.
- PDF reading order can distort sentence metrics despite medians and visual checks.
- Local publications vary by year, genre, and editorial convention; they are a calibration set, not a style template.
- The holdout's facts and bad-language patterns are synthetic. Future evaluation should add author-owned drafts and at least two blind reviewers.

## v1.0.0 synthetic paired benchmark

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
