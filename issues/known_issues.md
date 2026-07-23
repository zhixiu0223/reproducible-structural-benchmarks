# Known issues / gaps

Listed here proactively so reviewers don't waste time re-discovering them.
Confirming, refuting, or extending any of these is genuinely useful.

## Frame 1
- CalculiX cross-check only covers the first-order (LA) benchmark. The only
  CalculiX 2.21 element accepting an arbitrary user-specified section (`U1`)
  is documented as linear-only; `NLGEOM` fails outright. Second-order
  comparison with CalculiX is unresolved -- possibly achievable via an
  equivalent-rectangle `B31` section, not yet attempted.
- suanPan's `B21` result uses the tool's built-in real AISC W-shape section
  database rather than the paper's single tabulated moment of inertia,
  which gives a consistent but unexplained-in-detail +2.5% offset. The exact
  source of that 2.5% (web/flange integration vs. some other difference)
  has not been decomposed.

## Frame 4
- Only OpenSeesPy and FRAME3DD have been run; suanPan and CalculiX are not
  yet attempted.
- Pin releases at the two leaning-column-to-beam connections are modeled
  with a workaround (duplicate coincident node + translational-only
  constraint for OpenSeesPy; a near-zero-stiffness stub element for
  FRAME3DD) because neither tool has a native "release" keyword for this
  element type. Both workarounds should give the same physical result, but
  this has not been independently checked against a tool with native
  release support.
- Second-order (WC) match is looser than Frame 1 (-2.2% to +3.7% across
  tools, vs <0.5% for Frame 1), attributed to this frame's much higher
  second-order amplification (alpha_cr = 1.19) making small differences in
  geometric-nonlinearity formulation more visible. This attribution is
  plausible but not independently verified.

## Frame 9
- Only the first-order (LA) benchmark has been checked, and only with
  OpenSeesPy. The 0.8E / 0.9E / 1.0E comparison was run to identify which
  stiffness value is correct, but the second-order (WC) benchmark has not
  yet been attempted for this frame with any tool.

## General
- Only 3 of the 22 released benchmark frames have been attempted. The claim
  that "0.8E, applied uniformly regardless of the connectivity table's
  literal material assignment" generalizes across the dataset is based on
  these 3 cases and has not been checked against the other 19, including
  any frame that might *not* require this correction.
- All reproduction scripts in this repo were developed with AI assistance
  (Claude). Every numerical result reported in the write-up was
  independently executed and its output checked against the published
  benchmark values by the author, but the code itself has not yet had a
  human-only, AI-free review pass.

## Resolved

- **Frame 1 hand-calc script used perfect geometry instead of imperfect
  (H/500 sway).** Found during external review of this repo: the first
  version of `Frame-01/hand-calc/direct_stiffness_check.py` omitted the
  H/500 global sway imperfection that every other tool's model includes,
  producing a spurious ~3.7% gap against the LA benchmark that was
  coincidentally close in size to the unrelated CalculiX Timoshenko-shear
  gap discussed in the paper -- a genuine risk of being misread as the same
  cause. Fixed by adding the imperfect coordinates (node 9: x=0.36 in,
  node 13: x=360.36 in) to match the imperfect geometry used everywhere
  else in the reproduction. Corrected script now matches the LA benchmark
  to <0.001%.
