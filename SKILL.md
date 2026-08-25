---
name: academic-architecture-digital-media-writing
description: Copyedit Chinese or English academic prose in architecture and digital-media fields for precise, natural, discipline-appropriate language with low formulaic AI-style risk. Use when polishing wording, syntax, rhythm, transitions, register, or authorial voice while preserving meaning; do not use it to redesign article structure, repair research logic, or create evidence.
---

# Academic Architecture and Digital-Media Writing

Polish academic language without silently rewriting the paper's argument.

## Scope boundary

- Edit diction, syntax, sentence rhythm, cohesion markers, register, terminology consistency, concision, and formulaic AI-like phrasing.
- Do not reorganize sections, redesign argument structure, supply missing logic, add evidence, or change the research contribution. Flag such issues briefly as out of scope when they block safe copyediting.
- Never invent or alter a source, quotation, page number, method, result, building fact, or causal relation.
- Preserve the author's position and productive idiosyncrasy. Do not homogenize prose merely to make it sound academic.
- Do not claim to identify human or AI authorship. Diagnose formulaic tendencies and scholarly weaknesses only.
- Preserve epistemic force: do not upgrade `may` to `shows`, correlation to cause, or an interpretation to a fact.

## Working sequence

1. Establish the language, intended register, target venue if known, citation style to preserve, and whether the user wants tracked explanations or clean copy.
2. Read [references/anti-formulaic-style.md](references/anti-formulaic-style.md). For bilingual or discipline-sensitive wording, also read [references/language-calibration.md](references/language-calibration.md). When the request includes polishing, elegance, or `文辞美化`, read [references/prose-finish.md](references/prose-finish.md).
3. Freeze the semantic payload: propositions, evidence strength, technical terms, citations, numbers, scope, and paragraph order. Make only language-level changes unless the user separately authorizes substantive editing.
4. Revise in passes: formulaic clusters → abstract shells and modifier stacks → agency and verb choice → evidential calibration → transitions → information contour and sentence rhythm → terminology consistency.
5. Compare source and edit for semantic drift. Restore any qualification, ambiguity, or authorial emphasis lost during polishing.
6. For substantial work, run `scripts/style_audit.py`; treat its output as prompts for inspection, not verdicts.
7. For comparison, benchmarking, or self-improvement, follow [references/evaluation-protocol.md](references/evaluation-protocol.md). Do not tune to a single detector or phrase list.

## Language standard

- Prefer the most exact ordinary verb over ornamental nominalizations or inflated academic diction.
- Keep established disciplinary terms; do not replace them simply to increase lexical variety.
- Use transitions only when they name a real relation. Sentence order can often carry continuity without `此外` or `moreover`.
- Vary length and syntax in response to information density, not for cosmetic randomness.
- Retain deliberate repetition when it stabilizes a concept; remove accidental repetition and recycled framing.
- Keep authorial stance visible and calibrated, including first person where the venue permits it.

## Formulaic contrast rule

Default-avoid `不是……而是……`, `并非……而是……`, `not X but Y`, and `rather than merely` when they manufacture drama, erase overlap, or recur. Replace them with the actual relation: degree, sequence, coexistence, mechanism, scope, or correction. Retain a contrast only when X and Y are genuinely incompatible and the distinction advances the argument.

## Delivery

Return the requested clean text or tracked changes. For substantial edits, add a short language audit: recurring patterns changed, terminology decisions, and any passages left untouched because editing would alter meaning. Do not append generic praise or an authorship/detector verdict.

## References

- Research basis and limitations: [references/evidence-base.md](references/evidence-base.md)
- Benchmark findings: [references/benchmark-analysis.md](references/benchmark-analysis.md)
- Local-corpus calibration: [references/local-corpus-calibration.md](references/local-corpus-calibration.md)
- Release and optimization policy: [references/versioning.md](references/versioning.md)
