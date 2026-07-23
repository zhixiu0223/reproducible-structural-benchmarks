"""
Independent 12-DOF direct stiffness cross-check for Frame 1, used only to
verify that the FRAME3DD / OpenSeesPy / suanPan / CalculiX models were not
all sharing a common setup mistake. Single element per member (no
subdivision), first-order (linear, no P-Delta), imperfect geometry
(H/500 = 180/500 = 0.36 in global sway at the eave nodes, matching every
other tool's model and the original release's tabulated imperfect
coordinates -- an earlier version of this script used perfect geometry,
which reproduces a spurious ~3.7% gap against the LA benchmark that is
unrelated to, and coincidentally close in size to, the CalculiX shear-
deformation gap discussed in the paper; see git history for that version).

Run with E=29000 to reproduce the initial, too-low mismatch referenced in
the paper's evidence chain step (3). Run with E=23200 (0.8 * 29000, the
AISC DAM reduced stiffness) to confirm the corrected value, which should
match the published LA benchmark (node 9: 1.04501 in) to within numerical
precision.
"""
import numpy as np
import sys

E = float(sys.argv[1]) if len(sys.argv) > 1 else 29000.0

Icol, Abeam_col = 722.0, 20.0     # W14X68
Ibeam, Abeam = 510.0, 10.3        # W18X35
L_col, L_beam = 180.0, 360.0

def frame_elem_stiff(E, A, I, L):
    k = np.zeros((6, 6))
    EA_L, EI = E * A / L, E * I
    k[0, 0] = EA_L; k[0, 3] = -EA_L
    k[3, 0] = -EA_L; k[3, 3] = EA_L
    k[1, 1] = 12*EI/L**3; k[1, 2] = 6*EI/L**2; k[1, 4] = -12*EI/L**3; k[1, 5] = 6*EI/L**2
    k[2, 1] = 6*EI/L**2;  k[2, 2] = 4*EI/L;    k[2, 4] = -6*EI/L**2;  k[2, 5] = 2*EI/L
    k[4, 1] = -12*EI/L**3; k[4, 2] = -6*EI/L**2; k[4, 4] = 12*EI/L**3; k[4, 5] = -6*EI/L**2
    k[5, 1] = 6*EI/L**2;  k[5, 2] = 2*EI/L;    k[5, 4] = -6*EI/L**2;  k[5, 5] = 4*EI/L
    return k

def T_matrix(cx, cy):
    T = np.zeros((6, 6))
    R = np.array([[cx, cy, 0], [-cy, cx, 0], [0, 0, 1]])
    T[0:3, 0:3] = R; T[3:6, 3:6] = R
    return T

nodes = {1: (0, 0), 2: (360, 0), 9: (0.36, 180), 13: (360.36, 180)}  # H/500 sway imperfection
dof_map = {1: [0, 1, 2], 2: [3, 4, 5], 9: [6, 7, 8], 13: [9, 10, 11]}
K = np.zeros((12, 12))
elems = [(1, 9, Abeam_col, Icol, L_col), (2, 13, Abeam_col, Icol, L_col), (9, 13, Abeam, Ibeam, L_beam)]

for (ni, nj, A, I, L) in elems:
    xi, yi = nodes[ni]; xj, yj = nodes[nj]
    Lc = np.hypot(xj - xi, yj - yi)
    cx, cy = (xj - xi) / Lc, (yj - yi) / Lc
    k_global = T_matrix(cx, cy).T @ frame_elem_stiff(E, A, I, L) @ T_matrix(cx, cy)
    dofs = dof_map[ni] + dof_map[nj]
    for a in range(6):
        for b in range(6):
            K[dofs[a], dofs[b]] += k_global[a, b]

fixed = dof_map[1] + dof_map[2]
free = [d for d in range(12) if d not in fixed]
F = np.zeros(12)
F[dof_map[9][0]] = 34.849
F[dof_map[9][1]] = -348.49
F[dof_map[13][1]] = -348.49

u = np.linalg.solve(K[np.ix_(free, free)], F[free])
result = dict(zip(free, u))
print(f"E = {E} ksi")
print(f"Node 9  X-disp = {result[dof_map[9][0]]:.6f} in")
print(f"Node 13 X-disp = {result[dof_map[13][0]]:.6f} in")
