# Frame 1 reproducibility checklist

Follow this in order. Expected numbers are at the bottom -- don't look at
them until you have your own result, or the check is meaningless.

## Setup
- [ ] Download `Description Of Frames.pdf` and `FEA Model Details_All frames.xlsx`
      directly from https://doi.org/10.17632/39sjhchwtx.1 (do not reuse any
      file from this repo -- the point is an independent build)
- [ ] Read Frame 1's page in the PDF and its sheet in the Excel file

## Build (pick any one tool to start; all four are in this repo for cross-check)
- [ ] Build the geometry: 30 ft span, 15 ft height, fixed base, imperfect
      (H/500 sway) coordinates
- [ ] Assign W14X68 columns, W18X35 beam, A36 steel
- [ ] Apply the load combination 1.2D + 1.6Lr + 0.5W as concentrated nodal
      loads (see PDF for magnitudes)
- [ ] Run a first-order (linear) static analysis

## First checkpoint
- [ ] Compare your linear result to the published LA benchmark (node 9
      lateral displacement = 1.04501 in). If you get roughly 20-25% low
      (around 0.83-0.84 in), you have reproduced our first, incorrect
      attempt -- see `reproduction-report/draft.md`, Methods, "Evidence
      chain" before doing anything else.
- [ ] Read `issues/known-pitfalls.md` if you're stuck here.

## Second-order run
- [ ] Re-run with geometric nonlinearity (P-Delta) enabled, at the
      corrected stiffness
- [ ] Compare to the published WC benchmark (node 9 = 1.1908 in, node 13 =
      1.1638 in, base moment = 2427.99 kip-in)

## Report back
- [ ] Whatever you get -- matching or not -- please open a GitHub issue
      using the "Reproduction result" template. A mismatch is exactly as
      useful to us as a match.
