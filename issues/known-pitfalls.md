# Known pitfalls

Short version of the evidence chain in `reproduction-report/draft.md`,
reorganized as a lookup table for someone who's stuck, not as a narrative.
If you hit one of these while reproducing Frame 1, this is probably why.

## Pitfall 1: unreduced stiffness (the big one)
**Symptom:** your linear result is ~20-25% lower than the published LA
benchmark, but internally consistent (equilibrium checks out, no errors).
**Cause:** the AISC Direct Analysis Method requires E* = 0.8E applied to
every member throughout the analysis. This is not stated in the "Description
of Frames" PDF. It is only findable by reading the companion JCSR paper.
**Fix:** use E = 23,200 ksi (0.8 x 29,000), not the nominal 29,000 ksi, for
every member.

## Pitfall 2: the decoy material entry
**Symptom:** you noticed the released Excel file has a material literally
named "A36 (DAM)" and used it, but still get the ~20-25% low result.
**Cause:** the released material table has *two* entries named "A36 (DAM)"
-- one at the nominal E = 29,000 ksi (unreduced, despite the name) and only
the other at the correct E = 23,200 ksi. It is easy to pick the wrong one
by name alone.
**Fix:** check the actual E value, not just the label.

## Pitfall 3: the connectivity table's own material assignment can't be
trusted at face value
**Symptom:** even after finding Pitfall 1 and 2, a mixed/selective
application of the reduction (matching whatever the connectivity table's
Material column literally says per element) still doesn't match.
**Cause:** confirmed on Frame 4 -- the connectivity table's per-element
material assignment does not correspond to what was actually used to
produce the published benchmark. The correction needs to be applied
uniformly to every member, regardless of what each element's Material
column says.
**Fix:** apply E = 23,200 ksi to every member, ignore the per-element
Material index as a guide to which members need it.

## Pitfall 4: out-of-plane singularity
**Symptom:** your solver returns a singular stiffness matrix error, or an
unconstrained mechanism warning, on an otherwise-correct 2D model.
**Cause:** most general-purpose 3D FEM tools (FRAME3DD, CalculiX) need
out-of-plane translation and both out-of-plane rotations restrained at
every node for a nominally-2D structure; this is implicit in the paper's
"fully braced out-of-plane" assumption but not encoded as an explicit
boundary condition anywhere in the released data.
**Fix:** restrain Z-translation and X/Y-rotation at every node (for a
frame lying in the X-Y plane).

## Pitfall 5: member end releases (relevant to Frame 4, not Frame 1)
**Symptom:** results don't match, model has no obvious errors, and the
frame includes leaning/gravity columns.
**Cause:** pinned beam-column connections have to be modeled explicitly;
neither FRAME3DD nor OpenSeesPy has a simple native "release" keyword for
this element type, and the workaround (duplicate coincident node + partial
constraint) is easy to get wrong.
**Fix:** see `Frame-04/openseespy/frame4_wc.py` for a worked example.

## Pitfall 6: first-order (LA) results also need the imperfect geometry
**Symptom:** your first-order (linear, no P-Delta) member moments don't
match the published LA benchmark, and -- this is the confusing part --
changing between nominal E (29,000 ksi) and DAM-reduced E (23,200 ksi)
makes *no difference at all* to the moment you get.
**Cause:** the "no difference" observation is not a bug in your code --
it's mathematically correct. In a first-order linear-elastic analysis,
member moments in a statically indeterminate frame depend only on the
*relative* EI ratios between members, not on the absolute value of E, as
long as every member is scaled by the same factor. So Pitfall 1's fix
(0.8E) genuinely cannot be the explanation for a first-order moment
mismatch. The actual cause is more mundane and easy to miss on a from-
scratch model built specifically to isolate the first-order case: the
H/500 global sway imperfection has to be included even for the first-order
benchmark, not just the second-order one. Without it, base moment comes
out to 2094.98 kip-in (independent of E); with it, 2177.81 kip-in,
matching the published LA benchmark for Frame 1 to <0.001% (independent of
E, as expected).
**Fix:** use the imperfect coordinates for every analysis type (LA, SIPC,
WC), not just the second-order ones.

---
If you hit something not on this list, please open an issue -- that's
exactly what this list is missing until someone finds it.
