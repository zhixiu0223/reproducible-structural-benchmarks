# Changelog

All notable changes to this project are documented here. Format loosely
follows [Keep a Changelog](https://keepachangelog.com/).

## [v0.1.0-draft] - 2026-07-XX

### Summary

This release packages the current state of the Frame 1 reproduction of
Ziemian & Ziemian (2021)'s published second-order steel-frame benchmark:
a documented evidence chain for the AISC Direct Analysis Method's 0.8E
stiffness-reduction requirement (absent from the released data article's
own description, though standard under AISC 360), cross-validated across
four independent open-source tools, plus a one-click Colab notebook for
quick verification.

### Added

- **Four-tool cross-validation for Frame 1**: FRAME3DD and OpenSeesPy
  match the published second-order (WC) benchmark within 0.5%; suanPan
  (using its built-in real AISC section database rather than the paper's
  single tabulated I) within 2.5%; CalculiX is compared against the
  first-order (LA) benchmark only, a scope limitation of that tool's
  available element type, not a modeling failure (see
  `reproduction-report/draft.md`, Discussion).
- **Evidence chain for the 0.8E finding**: documented in
  `reproduction-report/draft.md`, Methods -- the released Excel data
  contains a decoy, same-named-but-unreduced material entry alongside the
  correct one, and the connectivity table references neither by default.
- **`known-pitfalls.md`**: six documented pitfalls, symptom-keyed, found
  across this project's own mistakes and an independent AI blind-test.
- **`Frame-01/openseespy/sensitivity_study.py`**: confirms 0.80E as the
  error-minimizing stiffness factor (not just an approximate match) by
  sweeping 0.70E-1.00E against both displacement and moment.
- **`colab/frame01_quick_reproduction.ipynb`**: zero-install Colab
  notebook mirroring `verify.py` and `sensitivity_study.py`, for reviewers
  who want a one-click check without cloning the repo.
- **External validation record** (`issues/known_issues.md`): an
  independent Claude blind-reproduction attempt and a Grok sandbox run
  both confirmed the WC benchmark match. Note: only Grok is confirmed to
  have executed a real FEA solver among the AI systems tried informally
  so far; other informal attempts either did manual hand-calculation only
  or did not execute code at all -- see that file for the itemized,
  corrected breakdown.
- `requirements.txt`, `BUILD.md`, `Frame-01/openseespy/verify.py`,
  `Frame-01/REPRODUCIBILITY_CHECKLIST.md`, `.github/ISSUE_TEMPLATE/`.

### Known gaps (not hidden -- see `issues/known_issues.md` for full detail)

- Frame 4 and Frame 9 are preliminary (narrower tool coverage than
  Frame 1), not yet part of this release's validated claims.
- Figure 1 in the report is still a text placeholder.
- Docker / CI deliberately deferred (see reasoning in known_issues.md).

### Status

Draft. Not yet submitted to ReScience C or any venue.
