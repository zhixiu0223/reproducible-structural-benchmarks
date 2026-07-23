"""
Frame 1, OpenSeesPy, corotational second-order model.

This is the original script whose output is what's cited in
reproduction-report/draft.md's Results table (manual print statements,
no automatic pass/fail).

If you just want to check whether you can reproduce the published
benchmark, run `verify.py` in this same folder instead -- it runs the
same model and prints an automatic published-vs-mine-vs-error% table.
This script is kept as-is for exact traceability to the paper's reported
numbers.
"""
import openseespy.opensees as ops

ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 3)

# imperfect geometry (H/500 global sway), same as FRAME3DD run
nodes = {
    1:(0,0), 2:(360,0),
    3:(0.09,45), 4:(360.09,45),
    5:(0.18,90), 6:(360.18,90),
    7:(0.27,135), 8:(360.27,135),
    9:(0.36,180), 10:(90.36,180),
    11:(180.36,180), 12:(270.36,180), 13:(360.36,180),
}
for n,(x,y) in nodes.items():
    ops.node(n, x, y)

ops.fix(1, 1,1,1)
ops.fix(2, 1,1,1)

E = 23200.0   # AISC Direct Analysis Method reduced stiffness 0.8*29000
A_col, I_col = 20.0, 722.0    # W14X68
A_beam, I_beam = 10.3, 510.0  # W18X35

ops.geomTransf('PDelta', 1)

col_elems = [(1,1,3),(2,3,5),(3,5,7),(4,7,9),(9,2,4),(10,4,6),(11,6,8),(12,8,13)]
beam_elems = [(5,9,10),(6,10,11),(7,11,12),(8,12,13)]

for (eid,ni,nj) in col_elems:
    ops.element('elasticBeamColumn', eid, ni, nj, A_col, E, I_col, 1)
for (eid,ni,nj) in beam_elems:
    ops.element('elasticBeamColumn', eid, ni, nj, A_beam, E, I_beam, 1)

ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)
ops.load(9, 34.849, -348.49, 0.0)
ops.load(13, 0.0, -348.49, 0.0)

ops.system('BandGeneral')
ops.numberer('RCM')
ops.constraints('Plain')
ops.test('NormDispIncr', 1.0e-10, 50)
ops.algorithm('Newton')
ops.integrator('LoadControl', 0.1)
ops.analysis('Static')

ok = 0
for i in range(10):
    ok = ops.analyze(1)
    if ok != 0:
        print("FAILED at step", i)
        break

if ok == 0:
    ux9 = ops.nodeDisp(9,1)
    ux13 = ops.nodeDisp(13,1)
    print(f"Node 9  X-disp = {ux9:.6f} in")
    print(f"Node 13 X-disp = {ux13:.6f} in")
    ops.reactions()
    print("Base reactions Fy:", ops.nodeReaction(1)[1], ops.nodeReaction(2)[1])
    forces = ops.eleForce(1)
    print("Element 1 (base of left column) end forces:", forces)
    print(f"Base moment (col1, node1) = {forces[2]:.3f} kip-in")
else:
    print("Analysis did not converge")
