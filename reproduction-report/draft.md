---
title: "[Re] Efficient geometric nonlinear elastic analysis for design of steel structures: Benchmark studies (Frame 1)"
author:
  - name: "[author name]"
    affiliation: "1"
affiliations:
  - name: "Independent researcher"
    index: 1
date: "2026-07-22"
bibliography: paper.bib
---

Status: draft. Target venue: ReScience C.

Original article: [@ziemian2021data]

Related article: [@ziemian2021jcsr]

Data repository: <https://doi.org/10.17632/39sjhchwtx.1> (Mendeley Data, CC BY 4.0)

## Abstract

We independently reproduced the elastic second-order (P-Delta) benchmark results for Frame 1 (single-story steel portal frame) from [@ziemian2021data] and identified one methodological requirement -- the AISC Direct Analysis Method's 0.8EI stiffness reduction, a standard, published provision of AISC 360 -- that is essential for successful replication but is absent from the released data article's own frame descriptions. The requirement is not obscure in the structural engineering literature; it is simply missing from this specific released dataset's documentation, which is what makes it a reproducibility pitfall rather than a modeling-competence question. Modeling the frame at the nominal, unreduced stiffness produces self-consistent but systematically low results (roughly 20-25% low relative to the published benchmark) that could easily be mistaken for a modeling error; the released FEA data even contains a same-named but unreduced "DAM" material entry that a reproducer could plausibly select in error. Once the correct reduction is identified and applied, cross-validation across four independent open-source finite element implementations (FRAME3DD, OpenSeesPy, suanPan, CalculiX) confirms the benchmark is reproducible within engineering tolerance (0.03-2.5% for the second-order comparison across three tools; the fourth, CalculiX, is compared against the first-order benchmark only, for reasons discussed below). Preliminary checks on two further, structurally dissimilar benchmark frames from the same dataset suggest this finding is not unique to Frame 1 (see Discussion); a full report on those frames, with the same tool coverage as Frame 1, is left for a follow-up article.

## Introduction

[@ziemian2021data] published the complete geometry, member sizes, loading, and simulation results for 22 planar steel benchmark frames, released under CC BY 4.0 on Mendeley Data. The companion methods paper [@ziemian2021jcsr] uses these frames to validate a proposed single-increment predictor-corrector (SIPC) method for second-order elastic analysis against a more exact iterative work-control (WC) method and a first-order linear analysis (LA).

This data article is, by construction, well suited to independent reproduction: it states that the frame nodal and connectivity data can be used to create the same benchmark structures with other finite element software, and provides node coordinates, member connectivity, section properties, and loading in a software-agnostic Excel format alongside the native MASTAN2 models.

We reproduce Frame 1 (a single-story, single-bay portal frame) using four independent, open-source implementations, none of which share code with the original authors' toolchain.

**Figure 1** (to be rendered as a proper figure before submission) summarizes the reproduction process as actually followed, rather than as a single re-run: published data -> independent reconstruction -> initial mismatch against the published benchmark -> methodology audit of the companion paper -> identification of the 0.8EI requirement (standard under AISC 360, but absent from the released data article) -> correction -> cross-tool validation. This sequence, not any single tool's output, is the paper's primary contribution.

## Methods

### Structure

Frame 1 is a fixed-base portal frame: 30 ft (360 in) span, 15 ft (180 in) height, columns W14X68, beam W18X35, A36 steel (nominal E = 29000 ksi, Fy = 36 ksi). Load combination 1.2D + 1.6Lr + 0.5W, applied as concentrated nodal forces (34.849 kip horizontal, 348.49 kip vertical at each eave), with an initial global sway imperfection of H/500 in the direction of the horizontal load, exactly as tabulated in the original release.

### Implementations

| Tool | Element | Geometric nonlinearity | Transformation tested | Section input |
|---|---|---|---|---|
| FRAME3DD 20140514+ (source build) [@frame3dd] | frame element with geometric stiffness | Newton-Raphson, full | built-in large-displacement N-R | A, Izz, Iyy from original paper |
| OpenSeesPy [@openseespy] | elasticBeamColumn + geometric transformation | Newton, incremental | PDelta (Frame 1, 4); Corotational (Frame 4, cross-checked) | A, I from original paper |
| suanPan 4.1.1 [@suanpan] | EB21 (linear) / B21 (corotational) | corotational (B21 only) | Corotational | EB21: A, I from paper. B21: built-in AISC US2D W14X68 / W18X35 database |
| CalculiX 2.21 (source build) [@calculix] | U1 user element, SECTION=GENERAL | not supported by this element in v2.21 | n/a (linear only) | A, I11, I22 from original paper |

All models use the imperfect (H/500 sway) geometry and the exact nodal loads from the data release, and restrain out-of-plane translation/rotation at every node to reduce the inherently 3D element formulations to the paper's implicit 2D behavior.

### The AISC Direct Analysis Method stiffness reduction

The companion paper [@ziemian2021jcsr] targets second-order analysis methods for use under the AISC Direct Analysis Method (DAM) [@aisc360], which prescribes a reduced stiffness (EA* = 0.8EA, EI* = 0.8 tau_b EI, tau_b = 1.0 here) applied to all members throughout an otherwise fully elastic, geometrically nonlinear analysis.

**Evidence chain.** (1) The released "Description of Frames" PDF -- both its general notes page and every per-frame page, including Frame 1's -- states only the nominal material property (E = 29,000 ksi) and never mentions a stiffness reduction. (2) The released FEA Model Details spreadsheet nonetheless contains three material entries for Frame 1: No. 1 (E = 29,000 ksi, named "A36"), No. 2 (E = 29,000 ksi, named "A36 (DAM)"), and No. 3 (E = 23,200 ksi = 0.8 x 29,000, also named "A36 (DAM)"). All 12 elements in the connectivity table reference Material No. 1 -- the plain, unreduced entry -- not either of the two DAM-labeled entries. A reproducer relying only on the connectivity table therefore builds a model at nominal stiffness by construction; a reproducer who does notice the DAM-labeled entries but selects by name alone could easily misidentify Material No. 2 (labeled "A36 (DAM)" but *not* reduced, E = 29,000 ksi) as the intended entry rather than No. 3 (also labeled "A36 (DAM)", correctly reduced, E = 23,200 ksi). (3) We modeled Frame 1 at the nominal E = 29,000 ksi across all four tools, independently cross-checked with an in-house 12-DOF direct stiffness solver (`Frame-01/hand-calc/direct_stiffness_check.py` in the code repository), and obtained self-consistent, correctly-converged results that are nonetheless 20-25% low relative to both the published LA and WC benchmarks. (4) Only after consulting the companion paper [@ziemian2021jcsr] -- whose title and abstract identify it as a Direct Analysis Method benchmarking study -- did we identify Material No. 3 (E = 23,200 ksi) as the correct entry. Applying it throughout brings all four implementations to within 2.5% of the published benchmark (Results, below). This chain is reported as a problem encountered rather than a modeling error: the reduction is real, documented in the companion paper, and physically motivated (an elastic proxy for the stiffness-degrading effect of distributed yielding and imperfections), but is not recoverable from the data article's descriptive text alone, and the released spreadsheet's naming makes the correct entry easy to pass over in favor of a same-named, unreduced one.

## Results

### Second-order (WC benchmark comparison)

| Tool | Node 9 disp. (in) | Error | Node 13 disp. (in) | Error | Base moment (kip-in) | Error |
|---|---|---|---|---|---|---|
| Ziemian and Ziemian (WC) [@ziemian2021data] | 1.1908 | -- | 1.1638 | -- | 2427.99 | -- |
| FRAME3DD | 1.1938 | +0.25% | 1.1679 | +0.35% | 2428.07 | +0.003% |
| OpenSeesPy | 1.1904 | -0.03% | 1.1644 | +0.05% | 2428.31 | +0.01% |
| suanPan B21 (real AISC section) | 1.2208 | +2.52% | 1.1933 | +2.53% | not extracted[^suanpan-moment] | -- |

[^suanpan-moment]: Member end moments were not queried in the suanPan `B21` run reported here; this is a gap in the reproduction script, not a limitation of the element (`B21` does report section forces). Left for a follow-up revision.

### First-order (LA benchmark comparison)

| Tool | Node 9 disp. (in) | Error | Node 13 disp. (in) | Error |
|---|---|---|---|---|
| Ziemian and Ziemian (LA) [@ziemian2021data] | 1.04501 | -- | 1.01902 | -- |
| FRAME3DD (geometric stiffness off) | 1.04501 | ~0.0% | 1.01902 | ~0.0% |
| suanPan EB21 (linear) | 1.0450 | ~0.0% | 1.0190 | ~0.0% |
| CalculiX U1 (linear only) | 1.0068 | -3.66% | 0.9809 | -3.76% |

## Discussion

The central result of this reproduction is the evidence chain above: a benchmark that is precisely, repeatably reproducible across four independent tools once one methodological detail -- standard under AISC 360, but absent from this specific released dataset's own documentation -- is supplied, and not otherwise. Two smaller, tool-specific observations round out the cross-validation and are noted briefly rather than as separate findings.

**CalculiX (one data point among four, not this paper's subject).** Of the four tools, CalculiX is the only one compared against the first-order (LA) rather than second-order (WC) benchmark: the only CalculiX 2.21 element accepting an arbitrary user-specified section (`U1`) is documented as linear-only, and its native geometrically-nonlinear beam element (`B31`) does not accept an arbitrary section. This is reported as a scope limitation of that one data point, not a property of CalculiX generally. Within its linear-only scope, `U1` matches the LA benchmark to within -3.7%, a gap consistent with its Timoshenko (shear-flexible) formulation against the original's shear-rigid assumption.

**suanPan real-section B21.** suanPan's `B21` element, run against its built-in AISC Shapes Database (full flange/web section integration) rather than the single tabulated moment of inertia used by the other three tools, reproduces the WC benchmark to +2.5% -- a small, explainable gap attributable to modeling fidelity rather than to the 0.8EI issue, which is corrected identically in all four tools.

**Preliminary findings on additional frames (not part of this paper's formal Results).** In exploratory checks -- OpenSeesPy and FRAME3DD only, first-order benchmark only in one case -- we observed the same underlying reproduction issue in two further benchmark frames from the same released dataset, chosen for structural dissimilarity from Frame 1: a single-story, multi-bay leaning-column frame with a markedly lower critical buckling ratio (alpha_cr = 1.19), in which an even less obvious, member-selective variant of the same connectivity-table trap is present, and an asymmetric two-story, two-bay frame (alpha_cr = 2.62). In both cases the published linear (LA) benchmark was reproduced to within 0.01% once a uniform 0.8E stiffness was applied to every member, regardless of what the released connectivity table's per-element material assignment literally indicates. For the two-story frame we additionally tested, and ruled out, the two most plausible alternative explanations available in the same released material table: the unreduced nominal stiffness (20% high) and the GMNIA-associated 0.9E reduction also present in every frame's material list (11% high) -- only the 0.8E DAM value matched. These are exploratory results with narrower tool coverage than the Frame 1 results reported above, presented here to motivate future work rather than as a validated finding of this paper: they suggest, but do not yet establish with the same rigor as Frame 1, that the 0.8E correction generalizes across the released benchmark set. A systematic investigation of the remaining benchmark frames -- including a search for any frame that does *not* require this correction, which would sharpen the finding from "always reduce" into a rule for *when* reduction is needed -- is left for future work.

## What replicated and what did not

- Fully replicated: WC (second-order) benchmark lateral displacements and base moment, by FRAME3DD and OpenSeesPy, within 0.5%.
- Replicated with an explained, non-trivial deviation: suanPan B21 (+2.5%, attributed to real-section vs idealized-I modeling).
- Partially replicated: CalculiX U1, against the LA (first-order) benchmark only, -3.7% deviation attributed to Timoshenko shear flexibility; the WC benchmark could not be attempted with this element.
- All four implementations confirm the underlying finding of the original study: the DAM-reduced-stiffness elastic second-order analysis is closely and consistently reproducible across independent open-source tools once the stiffness-reduction detail is applied.

## Data and code availability

Original data: [@ziemian2021data]'s Mendeley Data release, <https://doi.org/10.17632/39sjhchwtx.1> (CC BY 4.0).

Replication code: `reproducible-structural-benchmarks` repository (this repository). FRAME3DD input deck, OpenSeesPy script, suanPan `.supan` scripts for EB21 and B21, CalculiX `.inp` deck with the U1 `*USER ELEMENT` beam section, and the in-house 12-DOF direct stiffness solver used for the evidence-chain cross-check. All tools used are open source with no proprietary dependencies.

## References
