# Music tagging and text–audio retrieval

Two notebook experiments by Manuel Castillo, developed for Machine Learning for Music at Universitat Pompeu Fabra:

- [Music tagging](notebooks/01_music_tagging.ipynb): an MLP predicts 50 MagnaTagATune tags from frozen audio embeddings.
- [Text–audio retrieval](notebooks/02_text_audio_retrieval.ipynb): linear, MLP and transformer projection heads align frozen audio and text embeddings. Training uses MusicCaps; evaluation uses Song Describer.

## Recorded results

These values come from saved outputs in the original notebooks. The edited notebooks have **not been retrained**. [Results, source cells and limitations](docs/results.md) explain the evaluation protocol.

| Experiment | Recorded result |
| --- | --- |
| Tagging: best validation checkpoint | Test micro average precision: **0.403904** |
| Tagging: prior baseline | Test micro average precision: **0.107657** |
| Retrieval comparison: linear head | Song Describer audio→text R@10: **0.073727** |
| Retrieval comparison: MLP head | Song Describer audio→text R@10: **0.076408** |
| Retrieval comparison: transformer head | Song Describer audio→text R@10: **0.050938** |

The tagging split is clip-level, without song or artist grouping. Retrieval uses exact paired-row matches, not all captions belonging to a track. The head comparison is one run per architecture, without uncertainty estimates.

## Run

Use Python 3.11 in a separate environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m ipykernel install --prefix .venv --name music-experiments --display-name "Python 3 (music experiments)"
```

For the tagging notebook, prepare MagnaTagATune locally and set its directory:

```bash
export MTAT_ROOT="/absolute/path/to/magnatagatune"
jupyter lab
```

Open a notebook, select the environment's kernel and run its cells in order. The retrieval notebook does not need `MTAT_ROOT`; its dataset cells download from Hugging Face. Model-loading cells also download pretrained weights.

[Data setup](docs/data.md) describes the expected layout and sources. Audio, datasets, checkpoints, caches and notebook outputs are excluded from this repository. New runs write to `artifacts/`.

The dependency file pins several versions visible in the original installation logs; it is not a complete environment lock. Package installation and full training have not been verified during curation. FFmpeg is an optional fallback for the tagging audio loader.

## Validation

```bash
python scripts/validate_notebooks.py
python -m unittest discover -s tests -v
```

These check notebook structure, Python syntax, publication hygiene and cache/row-mapping helpers. They do not download data, train models or verify model quality. To validate execution, use a fresh kernel and empty `artifacts/` directory, run both notebooks top to bottom, then inspect the new summaries and skipped-audio counts.

## Origin

This selection comes from [ml-for-sound-and-music](https://github.com/manueleco/ml-for-sound-and-music), commit `14a1cf8b66d57727c6216e40907ef2f22dcad085`. [Provenance](results/provenance.json) records source paths and hashes. [Curation notes](docs/curation.md) list edits and validation limits.

The pretrained audio model is loaded through [OMAR-RQ](https://github.com/MTG/omar-rq); the text encoder is `sentence-transformers/all-mpnet-base-v2`. Course context and external models/datasets are credited in [data.md](docs/data.md). No new license grant is attached to the coursework; third-party code, data and model weights retain their own terms.
