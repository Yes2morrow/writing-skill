# Versioning

Use semantic versions recorded in `VERSION` and Git tags `vMAJOR.MINOR.PATCH`.

- **MAJOR:** changes core workflow, evaluation meaning, or compatibility.
- **MINOR:** adds a supported genre, language behavior, reference module, or diagnostic.
- **PATCH:** clarifies instructions or fixes a script without changing score meaning.

For every release:

1. run the skill validator and unit tests;
2. run the frozen paired benchmark and a holdout check;
3. update `references/benchmark-analysis.md` with exact results and limitations;
4. update `CHANGELOG.md` with evidence for the change;
5. update `VERSION`, commit, and tag the commit;
6. never silently change metric weights under a patch version.

Keep benchmark prompts stable within a major version. Add new cases rather than rewriting difficult cases. If a source correction changes a case materially, preserve the old result in Git history and explain the break.
