"""
Sensitivity sweep: stiffness reduction factor from 0.70E to 1.00E, to show
that 0.80E is not an arbitrarily chosen value but the one that actually
minimizes error against the published WC benchmark. Requires: pip install
-r ../../requirements.txt (run from repo root).
"""
import openseespy.opensees as ops
import csv

PUBLISHED_UX9 = 1.19082
PUBLISHED_M1 = 2427.99

def run(factor):
    ops.wipe()
    ops.model('basic', '-ndm', 2, '-ndf', 3)
    nodes = {1:(0,0), 2:(360,0), 3:(0.09,45), 4:(360.09,45), 5:(0.18,90),
             6:(360.18,90), 7:(0.27,135), 8:(360.27,135), 9:(0.36,180),
             10:(60.36,180), 11:(120.36,180), 12:(240.36,180), 13:(360.36,180)}
    for n,(x,y) in nodes.items():
        ops.node(n, x, y)
    ops.fix(1,1,1,1); ops.fix(2,1,1,1)
    E = 29000.0 * factor
    ops.geomTransf('Corotational', 1)
    col = [(1,1,3),(2,3,5),(3,5,7),(4,7,9),(9,2,4),(10,4,6),(11,6,8),(12,8,13)]
    beam = [(5,9,10),(6,10,11),(7,11,12),(8,12,13)]
    for (e,i,j) in col:
        ops.element('elasticBeamColumn', e, i, j, 20.0, E, 722.0, 1)
    for (e,i,j) in beam:
        ops.element('elasticBeamColumn', e, i, j, 10.3, E, 510.0, 1)
    ops.timeSeries('Linear', 1); ops.pattern('Plain', 1, 1)
    ops.load(9, 34.849, -348.49, 0.0); ops.load(13, 0.0, -348.49, 0.0)
    ops.system('BandGeneral'); ops.numberer('RCM'); ops.constraints('Plain')
    ops.test('NormDispIncr', 1e-10, 50); ops.algorithm('Newton')
    ops.integrator('LoadControl', 0.1); ops.analysis('Static')
    for _ in range(10):
        ops.analyze(1)
    return ops.nodeDisp(9, 1), ops.eleForce(1)[2]

def main():
    rows = []
    print(f"{'factor':>8} {'E (ksi)':>10} {'UX9':>10} {'UX9 err%':>10} {'M1':>10} {'M1 err%':>10}")
    for factor in [0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]:
        ux9, m1 = run(factor)
        ux9_err = 100 * (ux9 - PUBLISHED_UX9) / PUBLISHED_UX9
        m1_err = 100 * (m1 - PUBLISHED_M1) / PUBLISHED_M1
        print(f"{factor:>8.2f} {29000*factor:>10.0f} {ux9:>10.5f} {ux9_err:>9.2f}% {m1:>10.2f} {m1_err:>9.2f}%")
        rows.append({"factor": factor, "E_ksi": 29000*factor, "UX9": ux9,
                      "UX9_error_pct": ux9_err, "M1": m1, "M1_error_pct": m1_err})

    with open("sensitivity_results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["factor","E_ksi","UX9","UX9_error_pct","M1","M1_error_pct"])
        w.writeheader(); w.writerows(rows)
    best = min(rows, key=lambda r: abs(r["UX9_error_pct"]))
    print(f"\nMinimum |UX9 error| at factor = {best['factor']} (E = {best['E_ksi']:.0f} ksi)")

if __name__ == "__main__":
    main()
