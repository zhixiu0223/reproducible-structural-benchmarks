# reproducible-structural-benchmarks

Public benchmark datasets in structural engineering are increasingly
released with open data (see the Ziemian & Ziemian frames below). But a
public dataset being available is not the same as it being independently
reproducible: this repo's own experience with Frame 1 is that the released
data alone was *not* sufficient to reproduce the published numbers, and the
gap was easy to mistake for a modeling error rather than a missing
methodological detail (see `issues/known-pitfalls.md`). This repo exists to
make that reproduction process, including the mistakes made along the way,
checkable by anyone -- not just asserted.

## This is a challenge, not a claim.

I independently reproduced published steel-frame second-order analysis
benchmarks (Ziemian & Ziemian, 2021, *Data in Brief* / *JCSR*) using four
open-source FEM tools. I found that the released data alone is *not*
sufficient to reproduce the published numbers -- a standard AISC Direct
Analysis Method stiffness reduction (0.8E), well documented in AISC 360
itself but absent from this specific released dataset's own description,
has to be identified from a companion paper and applied, and the released
Excel data even contains a same-named-but-unreduced decoy material entry.

**Please do not trust my results.** What I actually want is for you to try to
break them:

## Quick start (works in most sandboxes, including AI agents)

```
pip install -r requirements.txt
python Frame-01/openseespy/verify.py
```

This is deliberately the easy path: this repo's own dev environment can
build and run all four tools (see `BUILD.md`), but AI-agent blind-test
attempts against this repo have shown a wide range of actual execution
capability -- one agent (Grok) independently installed and ran the
OpenSeesPy path with a real solver; several others (DeepSeek, Qwen,
Gemini) could only produce a manual/hand-calculated Python check without
an actual FEM solver; one (ChatGPT) proposed strategy repeatedly but never
executed anything. OpenSeesPy's pip-installable wheel appears to be the
most portable *real solver* path across agents that can execute code at
all -- not a universal ceiling every sandbox hits, just the best
default starting point given that spread. See
`issues/known_issues.md`, "External validation", for the itemized
breakdown per agent.

## Advanced: independent solver cross-validation

If you have FRAME3DD, suanPan, and/or CalculiX available (see `BUILD.md`
for exact build steps), the corresponding scripts in each frame's
subfolder let you cross-check the same benchmark across four independent
implementations, which is the paper's actual central claim -- the
OpenSeesPy-only quick start above is a fast sanity check, not a
substitute for that cross-validation.

1. Build your own independent model of one of the frames below (from the
   original public dataset, not from my scripts).
2. Try to reproduce the published benchmark numbers.
3. See if you get the same ~20-25% low result I got on a first attempt, and
   whether you find the same explanation (or a different one).
4. If anything in my evidence chain, my code, or my conclusions looks wrong,
   **please open an issue.** Finding a real problem is the useful outcome
   here, not a thumbs-up.

## What's in this repo

- `reproduction-report/draft.md` -- the current draft write-up (ReScience C
  format), including the full evidence chain for the stiffness-reduction
  finding.
- `Frame-01/`, `Frame-04/`, `Frame-09/` -- per-frame reproduction scripts,
  one subfolder per independent tool (OpenSeesPy, FRAME3DD, suanPan,
  CalculiX). Each script is runnable standalone against the original
  released dataset.
- `Frame-01/REPRODUCIBILITY_CHECKLIST.md` -- step-by-step checklist to
  independently reproduce Frame 1 without reading the full report first.
- `benchmark-data/` -- pointers to the original released dataset (not
  redistributed here; see below).
- `issues/known_issues.md` -- gaps I already know about. Check here first
  so you don't waste time re-finding something I've already flagged.
- `issues/known-pitfalls.md` -- lookup table of specific mistakes to expect
  while reproducing, keyed by symptom.
- `.github/ISSUE_TEMPLATE/` -- use "Reproduction result" to report a match
  *or* a mismatch; both are useful.
- `requirements.txt`, `BUILD.md` -- exact Python/tool versions and build
  commands actually used (FRAME3DD built from source, suanPan pre-built
  release binary, CalculiX via `apt`, OpenSeesPy via `pip`).
- `Frame-01/openseespy/verify.py` -- runs the model and prints a
  published-vs-mine-vs-error% table automatically (PASS/CHECK).
- `Frame-01/openseespy/sensitivity_study.py` -- sweeps the stiffness
  reduction factor from 0.70E to 1.00E and confirms 0.80E is the actual
  error-minimizing value, not just "close enough."

**Not yet done:** a single `setup.sh` / Dockerfile that builds all four
tools in one command, and CI that runs `verify.py` automatically on every
push. Deliberately deferred rather than skipped -- see
`issues/known_issues.md` for the reasoning (mainly: the tool mix here is
unusually heavy -- a compiled-from-source FRAME3DD, a large suanPan
binary, and CalculiX -- and getting a Dockerfile right for all four before
this repo has had any real external feedback risks a lot of maintenance
overhead on infrastructure for a project whose scope might still change).
Contributions welcome.

## Original data (not redistributed here)

Ziemian, C.W., Ziemian, R.D. (2021). Benchmark Frames for Structural
Analysis. Mendeley Data, v1. https://doi.org/10.17632/39sjhchwtx.1
(CC BY 4.0). Download the "Description of Frames" PDF and "FEA Model
Details" Excel file directly from that link if you want to build your own
model from scratch, independent of anything in this repo.

## Status

Draft. Not yet submitted anywhere. Frame 1 is the most thoroughly checked
(four tools, both first- and second-order comparisons). Frame 4 and Frame 9
are partial (see `issues/known_issues.md`).
