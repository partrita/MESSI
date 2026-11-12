# Installation

[Pixi](https://pixi.sh/) manages Python 3.12 and all dependencies for this
repository (see `pixi.toml`). Head inference, selection, and CPU metrics do not
require DPLM, ESMFold2, NetMHCIIpan, or a scheduler.

## Install

```bash
pixi install
```

This installs the **default** environment (CUDA 12.8, GPU) with base and test
dependencies. To install a specific environment:

```bash
pixi install -e cpu             # CPU-only (PyTorch CPU wheels)
pixi install -e generation-cuda # Generation/inverse-folding (CUDA)
pixi install -e generation-cpu  # Generation/inverse-folding (CPU)
```

## Environments

| Environment | Purpose | PyTorch |
|---|---|---|
| `default`, `cuda` | Head inference, selection, CPU metrics (GPU) | CUDA 12.8 |
| `cpu` | Head inference, selection, CPU metrics (CPU-only) | CPU |
| `generation-cuda` | DPLM/inverse-folding generation (base + generation deps + `torch-scatter`) | CUDA 12.8 |
| `generation-cpu` | DPLM/inverse-folding generation (CPU) | CPU |

CPU and CUDA wheels are provided by separate environments; do not mix them.

## Run commands

Run tools inside the managed environment with `pixi run` (uses `default`, GPU):

```bash
pixi run python deimmunize.py --help
pixi run python deimmunize.py --structure input.pdb --chain A --allele DRB1_1501 --num-designs 8 --out-dir results/
```

Target a specific environment with `-e <env>`, or open an interactive shell:

```bash
pixi run -e cpu python deimmunize.py ...
pixi shell            # default (GPU)
pixi shell -e cpu
```

<details>
<summary>Manual pip/venv alternative</summary>

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
```

For CUDA 12.8, substitute the wheel index
`https://download.pytorch.org/whl/cu128` in the PyTorch command.

</details>

## Generation

The modified DPLM source is under `inverse_folding/dplm/`. It requires the
checkpoint's ByProt experiment configuration and corresponding model weights;
a standalone checkpoint without its configuration is insufficient. Keep their
relative layout and provide the checkpoint through the CLI.

Use the generation environments (include base, generation dependencies, and
`torch-scatter` matched to the PyTorch build):

```bash
pixi install -e generation-cuda   # GPU
pixi install -e generation-cpu    # CPU

pixi run -e generation-cuda python <generation-script> ...
```

The runtime loads the bundled ByProt and OpenFold Python sources. It does not
require the old cluster-specific editable installs. See the
[inverse-folding artifact layout](artifacts.md#inverse-folding-checkpoint).
The generation backend is validated separately from the CPU Head environment.

<details>
<summary>Manual pip alternative</summary>

```bash
python -m pip install -r requirements-generation.txt
python -m pip install torch-scatter -f https://data.pyg.org/whl/torch-2.7.0+cpu.html
# CUDA 12.8: https://data.pyg.org/whl/torch-2.7.0+cu128.html
```

</details>

## Structure Backends

ESMFold2 uses an isolated worker. Supply its site-packages directory through
`--esmfold2-site-packages`; do not install its `esm` package over the generation
environment's `fair-esm`. Select `--refold-model esmfold2_live` for live refinement,
or `esmfold2` with `--refold-cache-dir` to evaluate an existing normalized cache.

Protenix and AlphaFold3 are optional external installations. Their precompute
CLIs accept interpreter/wrapper paths and inputs explicitly. Use the respective
upstream installation and weight-access instructions. NetMHCIIpan and Rosetta
are also external tools; supply their executable paths only when requested.

## Tests

```bash
pixi run test                        # default (GPU) environment
pixi run -e cpu test                 # CPU-only environment
# or manually: pixi run python -m pytest tests -q
```

To smoke-check generation imports (after installing a generation environment):

```bash
pixi run -e generation-cuda check-generation-imports
# or: pixi run -e generation-cpu check-generation-imports
```

All paths and sharding options are supplied through Python CLIs. No SLURM
launcher, cluster module command, or local binary shim is required for Head use.
