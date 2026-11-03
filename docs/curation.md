# Curation notes

Curated on 2026-11-03 from the source commit and file hashes in [provenance.json](../results/provenance.json). The original repository and local files were left unchanged.

## Included

- Two notebooks with the original model architectures and main experiment workflows.
- Historical metrics extracted from saved outputs, with source cell indices.
- Setup instructions, dataset references and evaluation limitations.
- Cache identity helpers, small regression tests and a notebook validation script.

## Removed from this selection

- Embedded audio, images, widget metadata and all execution outputs in the edited notebooks.
- Personal Drive links, machine-specific paths and styled HTML headings.
- Assignment/reference notebooks, Word/PDF reports, HTML exports, backups, datasets, model weights and caches.
- Duplicate helper definitions, automatic pip installation inside notebooks, interactive file pickers and optional external-audio demos.
- The UMAP/clustering and tiny-overfit exploration sections. The main classification and retrieval comparisons remain.
- Unfinished discussion prompts and claims about scalability, reproducibility or environmental benefits not established by the saved results.

## Code changes

- **Tagging evaluation:** load the best validation checkpoint before the first test evaluation and result export. Keep both historical test values documented.
- **Output isolation:** each execution writes to its own run directory. The tagging notebook no longer automatically resumes an old checkpoint.
- **Tagging cache:** include ordered clip IDs, labels, extraction settings and a user-controlled data revision. Validate cached labels/IDs. Crops are seeded per track; this differs from the original global random sequence.
- **Audio failures:** the tagging loader raises after all decoding attempts fail rather than substituting silence. Unexpected embedding dimensions also raise instead of being truncated or padded.
- **Retrieval cache:** include dataset fingerprints and encoder/configuration identities. Record skipped rows. Map demo results through the stored source-row indices.
- **Retrieval tracking:** save extraction and training summaries separately, and stop tracking if the main training loop raises. Emissions tracking is optional and defaults to off in both notebooks.
- **Environment:** centralize dependencies and replace deprecated CUDA GradScaler calls with the current equivalent for the pinned PyTorch version.

These edits can change a future run's results. Historical tables are not relabeled as results of the edited code.

## Verification boundary

Notebook schema, code syntax, local documentation links, output removal, and cache/row-mapping behavior can be checked without ML downloads. Verified during curation: both notebook schemas, all 37 Python code cells, local documentation links, and all five unit tests passed. Source hashes match the unchanged original files. The validation script and unit tests cover this boundary.

Full dependency installation, encoder loading, dataset decoding, training and end-to-end execution were not performed during curation. A fresh-kernel run of both notebooks is still needed to verify the complete workflow. Historical model and dataset revisions are incomplete, so exact reproduction is not promised.
