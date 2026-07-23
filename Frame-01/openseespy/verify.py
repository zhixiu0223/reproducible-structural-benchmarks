"""
Run Frame 1 (OpenSeesPy, corotational, second-order) and automatically
compare against the published WC benchmark. Requires: pip install -r
../../requirements.txt (run from repo root).
"""
import openseespy.opensees as ops

PUBLISHED = {
    "UX9":  1.19082,
    "UX13": 1.16382,
    "M1":   2427.99,
}

def run():
    ops.wipe()
    ops.model('basic', '-ndm', 2, '-ndf', 3)
    nodes = {
        1: (0, 0), 2: (360, 0),
        3: (0.09, 45), 4: (360.09, 45),
        5: (0.18, 90), 6: (360.18, 90),
        7: (0.27, 135), 8: (360.27, 135),
        9: (0.36, 180), 10: (60.36, 180),
        11: (120.36, 180), 12: (240.36, 180), 13: (360.36, 180),
    }
    # NOTE: nodes 10-12 here are placeholders for beam subdivision; the
    # exact intermediate spacing does not affect results for a straight
    # prismatic member. See Frame-01/openseespy/frame1.py for the
    # original subdivision used in the paper's reported run.
    for n, (x, y) in nodes.items():
        ops.node(n, x, y)
    ops.fix(1, 1, 1, 1); ops.fix(2, 1, 1, 1)

    E = 23200.0  # 0.8 * 29000, AISC DAM reduced stiffness (see known-pitfalls.md)
    ops.geomTransf('Corotational', 1)
    col = [(1,1,3),(2,3,5),(3,5,7),(4,7,9),(9,2,4),(10,4,6),(11,6,8),(12,8,13)]
    beam = [(5,9,10),(6,10,11),(7,11,12),(8,12,13)]
    for (e,i,j) in col:
        ops.element('elasticBeamColumn', e, i, j, 20.0, E, 722.0, 1)
    for (e,i,j) in beam:
        ops.element('elasticBeamColumn', e, i, j, 10.3, E, 510.0, 1)

    ops.timeSeries('Linear', 1)
    ops.pattern('Plain', 1, 1)
    ops.load(9, 34.849, -348.49, 0.0)
    ops.load(13, 0.0, -348.49, 0.0)

    ops.system('BandGeneral'); ops.numberer('RCM'); ops.constraints('Plain')
    ops.test('NormDispIncr', 1e-10, 50); ops.algorithm('Newton')
    ops.integrator('LoadControl', 0.1); ops.analysis('Static')
    for _ in range(10):
        if ops.analyze(1) != 0:
            raise RuntimeError("analysis failed to converge")

    ux9 = ops.nodeDisp(9, 1)
    ux13 = ops.nodeDisp(13, 1)
    m1 = ops.eleForce(1)[2]
    return {"UX9": ux9, "UX13": ux13, "M1": m1}

def main():
    mine = run()
    print(f"{'quantity':<8} {'published':>12} {'mine':>12} {'error %':>10}")
    all_pass = True
    for k, pub in PUBLISHED.items():
        m = mine[k]
        err = 100 * (m - pub) / pub
        status = "PASS" if abs(err) < 1.0 else "CHECK"
        if abs(err) >= 1.0:
            all_pass = False
        print(f"{k:<8} {pub:>12.4f} {m:>12.4f} {err:>9.2f}%  {status}")
    print()
    print("Frame-01 WC:", "PASS (all within 1%)" if all_pass else "CHECK (see above)")

if __name__ == "__main__":
    main()
