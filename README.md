# MESSI

Protein deimmunization with discrete diffusion. Redesign a protein for a target
MHC-II allele while preserving structural feasibility and optional fixed residues.

## Run

Dependencies are managed with [Pixi](https://pixi.sh/). After [installing dependencies](docs/installation.md) and [setting model paths once](docs/deimmunize.md#one-time-setup):

```bash
pixi install
pixi run python deimmunize.py \
  --structure input.pdb --chain A \
  --allele DRB1_1501 --num-designs 8 \
  --out-dir results/
```

`pixi install` creates the default environment (CUDA 12.8, GPU). Use `pixi run -e cpu python ...` for a CPU-only environment, or `-e generation-cuda`/`-e generation-cpu` for generation workflows (see [installation](docs/installation.md)).

Accepts PDB/mmCIF structures and DRB1_0701, DRB1_0401 or DRB1_1501.
Selected sequences are saved to `results/designs.fasta` and
`results/generated.parquet`.

Defaults use official MESSI generation and selection, without an additional
refinement stage. `--num-designs` is the maximum number of unique feasible designs;
the pipeline never fills a shortfall by duplicating sequences or relaxing its gates.

## More Options

- [Setup, constraints, dry-run and output details](docs/deimmunize.md).
- Run `pixi run python deimmunize.py --help` for optional arguments.
- [Refinement](docs/workflows.md#head-refinement) and [evaluation](docs/workflows.md#evaluation).
- [Experiment configurations](docs/configs.md) and [all scripts](docs/scripts.md).

## License

[MIT](LICENSE). External models and bundled source retain their
[respective terms](THIRD_PARTY_NOTICES.md).
