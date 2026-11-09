# T1 zero-data starter: a first valid Task 1 submission, built on synthetic data

A community tutorial for the [Virtual Embryo Challenge](https://virtualembryo.ai/challenge), Task 1. It is not affiliated with or endorsed by the organisers.

## What it is
A single script, also shipped as a Colab or Jupyter notebook, that takes you from nothing to a scored, validated T1 prediction **without registering or downloading the ~1.2 GB release**:

1. It generates a **synthetic** dataset in the documented T1 layout: E8.5 and E9.5 for training, E10.5 as the target.
   - The format is `.h5ad` with `.X` float32 log1p(1e4) CSR and `obs["celltype"]`.
   - Cell-type composition turns over between stages, which mimics the documented difficulty, not the biology.
   - It can optionally run on the real public 32,285-gene `T1__val.genes.txt` panel, which is public metadata, as a full-width format test.
2. It runs two baselines: `copy_last` (the official floor) and `composition_shift` (log-linear extrapolation of cell-type proportions plus a damped per-type shift).
3. It validates each prediction against the documented contract and demonstrates the **two silent killers**:
   - **Wrong gene order** is rejected even when the genes themselves are right.
   - **Raw counts or the wrong normalisation** pass the format check but score wrongly. The starter warns via the implied library size.
4. It scores both predictions with the **official `veckit` metric functions** and the documented skill map and T1 weights (25/25/30/20). The anchors are computed on the synthetic target exactly as documented (floor = copy_last, ceiling = half against half).

## Why it helps participants
- You can build and debug your loader, writer, validator and scoring loop before registering, and in the time it takes the download to finish.
- It is a CPU-only starting point that fits Colab.
- It complements veckit PR #4 (synthetic **T2** conformance checks); this is the T1 counterpart.

## How to run
```bash
uv sync && uv run python t1_starter.py --out synthetic_t1          # or: pip install anndata scipy pandas veckit==0.1.2
uv run python t1_starter.py --genes-file T1__val.genes.txt --cells 1200   # full-width public panel
uv run pytest -q
```
For Colab, open `t1_starter.ipynb`. Its first code cell installs the dependencies. The notebook is generated from the script by `python make_notebook.py`, and a test keeps the two in sync.

Observed output (2026-11-03, CPU, 2,000 synthetic genes, 1,500 cells per stage; about 13 s and 0.7 GB RSS):
```
  method             valid  headline |     de_score de_direction        mmd_u    variogram
  copy_last           True     50.00 |        50.00        50.00        50.00        50.00
  composition_shift   True     63.90 |        81.73        71.80        71.35        20.58
Silent killers:
  raw counts     -> valid=True warnings=['implied library size ... expected ~1e4 ...']
  shuffled genes -> valid=False errors=['var_names: right genes, WRONG ORDER (rejected just the same)']
```
On the full 32,285-gene public panel with 1,200 cells per stage, the run takes about 81 s and 2.6 GB RSS, and both predictions validate.

**Synthetic scores say nothing about the real board.** We wrote the generator, so a composition-aware baseline is expected to do well on it. Note also that its variogram term falls below the floor even here, which mirrors what happens to simple shift baselines on the real board.

## Tests (`pytest -q`)
The tests check that:

- `copy_last` scores exactly 50;
- `composition_shift` scores above 55 on the synthetic data;
- both predictions validate and are float32 `.h5ad` files;
- the two silent killers are caught;
- the generated data is marked SYNTHETIC;
- the skill map's anchor points are correct;
- the notebook is in sync with the script.

## Data and AI disclosure
- It uses **no challenge data**. Every cell is generated. The only real input is the optional public gene-name list.
- It was written with AI assistance (Claude Code, by Anthropic) and reviewed and filed by a human.
- `veckit` is the organisers' MIT-licensed scorer.
- Licence: MIT.
