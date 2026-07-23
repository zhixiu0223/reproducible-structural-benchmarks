import openseespy.opensees as ops

ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 3)

nodes = {
    1:(0,0), 2:(420,0), 3:(840,0), 4:(1260,0),
    5:(0.108,54), 6:(420.108,54), 7:(840.108,54), 8:(1260.108,54),
    9:(0.216,108), 10:(420.216,108), 11:(840.216,108), 12:(1260.216,108),
    13:(0.324,162), 14:(420.324,162), 15:(840.324,162), 16:(1260.324,162),
    17:(0.432,216), 18:(105.432,216), 19:(210.432,216), 20:(315.432,216),
    21:(420.432,216), 22:(525.432,216), 23:(630.432,216), 24:(735.432,216),
    25:(840.432,216), 26:(945.432,216), 27:(1050.432,216), 28:(1155.432,216),
    29:(1260.432,216),
}
for n,(x,y) in nodes.items():
    ops.node(n, x, y)

# duplicate "hinge" nodes for pin releases at node 17 and node 29 (beam ends)
ops.node(1017, *nodes[17])
ops.node(1029, *nodes[29])
ops.equalDOF(17, 1017, 1, 2)   # tie Ux, Uy only -> rotation free (pin)
ops.equalDOF(29, 1029, 1, 2)

# base fixities: node1,4 pinned (ZRot free); node2,3 fixed
ops.fix(1, 1,1,0)
ops.fix(2, 1,1,1)
ops.fix(3, 1,1,1)
ops.fix(4, 1,1,0)

# W27X84 (Sec1): A=24.8, Izz=2850
# W10X49 (Sec2): A=14.4, Izz=272
E_nom = 23200.0
E_dam = 23200.0

ops.geomTransf('Corotational', 1)

col_elems = [
    (1,1,5,E_dam),(2,5,9,E_dam),(3,9,13,E_dam),(4,13,17,E_dam),
    (5,2,6,E_nom),(6,6,10,E_nom),(7,10,14,E_nom),(8,14,21,E_nom),
    (9,3,7,E_nom),(10,7,11,E_nom),(11,11,15,E_nom),(12,15,25,E_nom),
    (13,4,8,E_dam),(14,8,12,E_dam),(15,12,16,E_dam),(16,16,29,E_dam),
]
for (eid,ni,nj,E) in col_elems:
    ops.element('elasticBeamColumn', eid, ni, nj, 14.4, E, 272.0, 1)

beam_elems_mid = [(18,18,19),(19,19,20),(20,20,21),(21,21,22),(22,22,23),
                   (23,23,24),(24,24,25),(25,25,26),(26,26,27),(27,27,28)]
for (eid,ni,nj) in beam_elems_mid:
    ops.element('elasticBeamColumn', eid, ni, nj, 24.8, E_nom, 2850.0, 1)
# end beam segments use the hinge-duplicate nodes
ops.element('elasticBeamColumn', 17, 1017, 18, 24.8, E_nom, 2850.0, 1)
ops.element('elasticBeamColumn', 28, 28, 1029, 24.8, E_nom, 2850.0, 1)

ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)
loads = {17:-926.5, 18:-56.149,19:-56.149,20:-56.149,21:-56.149,22:-56.149,
         23:-56.149,24:-56.149,25:-56.149,26:-56.149,27:-56.149,28:-56.149,29:-926.5}
for n,P in loads.items():
    ops.load(n, 0.0, P, 0.0)

ops.system('BandGeneral')
ops.numberer('RCM')
ops.constraints('Transformation')
ops.test('NormDispIncr', 1.0e-10, 100)
ops.algorithm('Newton')
ops.integrator('LoadControl', 0.05)
ops.analysis('Static')

ok = 0
for i in range(20):
    ok = ops.analyze(1)
    if ok != 0:
        print("FAILED at step", i)
        break

if ok == 0:
    for n in [17,21,25,29]:
        print(f"Node {n} X-disp = {ops.nodeDisp(n,1):.6f} in")
else:
    print("Analysis did not converge")
