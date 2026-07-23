# Build notes

Exact versions and build commands used to produce the results in
`reproduction-report/draft.md`. Not yet packaged as a one-command
`setup.sh` / Dockerfile -- see `issues/known_issues.md` for why, and for
help doing that if you want to contribute it.

## Python / OpenSeesPy / hand-calc
```
python3 --version          # 3.12.3
pip install -r requirements.txt
```

## FRAME3DD (built from source)
No pre-built binary used; compiled from the original author's repository.
```
git clone https://github.com/hpgavin/HPGnumlib.git
git clone https://github.com/hpgavin/frame3dd.git
cd frame3dd
make                        # produces ./frame3dd
```
Version banner at build time: `0.20240514+` (HPGnumlib-based Makefile
build, Dec 2025 commit).

## suanPan (pre-built release binary)
```
curl -sL "https://github.com/TLCFEM/suanPan/releases/download/suanPan-v4.1.1/suanPan-linux-amd64-openblas-avx.tar.gz" -o suanpan.tar.gz
tar -xzf suanpan.tar.gz -C suanpan_bin
LD_LIBRARY_PATH=suanpan_bin/lib suanpan_bin/bin/suanPan -f <script>.supan
```
Requires an AVX2-capable CPU for this particular build (openblas-avx
variant); if your CPU lacks AVX2, use the `-no-avx` release asset instead.

## CalculiX (Ubuntu package)
```
apt-get install -y calculix-ccx    # installs ccx 2.21
```

## Known version-sensitivity risk
Not yet checked: whether any of the numerical results in this repo are
sensitive to the exact tool version (e.g., a newer suanPan or CalculiX
release changing default behavior). If you reproduce this with different
versions and get a different result, please open an issue -- that's
useful information either way.
