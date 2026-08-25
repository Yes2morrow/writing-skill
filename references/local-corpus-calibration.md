# Local-corpus language calibration

## Corpus and limits

Version 1.1 profiles 205 local PDFs from `top-journal-classics-manual-download` and `wenxian`. PDFium recovered at least 1,800 characters from the first ten pages of 85 documents: 68 Chinese and 17 English. Full text is not stored; the benchmark retains document-level and aggregate metrics only. Visual checks covered English double-column journal pages, a Chinese double-column technical paper, and a Chinese image-rich architectural essay.

The corpus is a calibration reference, not proof of human authorship or a universal style norm. OCR availability, two-column text order, historical journal conventions, discipline, and passage type all affect the metrics. Use document medians and qualitative tendencies; do not imitate a paper mechanically.

## Comparison with the held-out no-skill corpus

The held-out baseline contains ten fictional papers and 300 paragraphs, balanced across Chinese and English. Relative to local-document medians:

| Feature per 10,000 non-space characters | Chinese no-skill / local | English no-skill / local |
|---|---:|---:|
| all configured formulaic cues | 390.81 / 41.05 | 127.51 / 20.15 |
| inflated lexicon | 46.13 / 8.88 | 14.44 / 0.22 |
| navigation markers | 26.36 / 4.21 | 9.62 / 0.48 |
| vague-action frames | 19.77 / 0.97 | 4.81 / 0.44 |
| empty transitions | 19.77 / 0.00 | 2.41 / 0.00 |
| explicit overclaims | 19.77 / 0.00 | 4.81 / 0.48 |

Median sentence-length variation was lower in the no-skill papers: CV 0.446 versus 0.999 in Chinese and 0.443 versus 0.820 in English. This supports purposeful syntactic variation, not random alternation or a fixed sentence-length target.

## Decisions supported by the comparison

1. Diagnose clusters. A single conventional phrase also appears in published prose; multiple formulaic categories recurring together are more informative.
2. Do not optimize direct-verb counts. The synthetic baseline repeats `研究记录/发现/测得` and still sounds mechanical. Check whether the subject, action, and object vary with the actual content.
3. Treat abstract shells, modifier queues, echo conclusions, empty transitions, and claim–disclaimer mismatch as first-class revision targets.
4. Keep stable technical terms even when repetition lowers superficial lexical variety.
5. Use numerical, citation, and parenthetical anchors only when supplied by the source. Their prevalence in publications does not authorize adding them.
6. Preserve legitimate long sentences and conventional transitions when they express real hierarchy or relation. Zero marker density is not a quality target.

Rebuild this profile with `scripts/profile_local_literature.py`, compare a baseline with `scripts/compare_language_profiles.py`, and record changes in a new version rather than overwriting the frozen result.
