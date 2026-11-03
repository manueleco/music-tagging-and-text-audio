# Recorded results and limits

All numbers below were extracted from outputs already saved in the source notebooks at commit `14a1cf8b66d57727c6216e40907ef2f22dcad085`. No new training or inference was performed during curation. Cell indices refer to the original notebooks and are zero-based.

## Lab 9: music tagging

The saved split contains 8,000 training, 2,000 validation and 2,000 test clips. Embeddings have 512 features; the classifier predicts 50 tags. Configuration: 16 kHz, two-second crops, frozen `mtg-upf/clap_omarrq_mp_small_music` layer 6, MLP with a 256-unit hidden layer and dropout 0.2.

The original metric field `pr_auc_micro` is computed with scikit-learn's `average_precision_score`. It is **average precision (AP)**, not trapezoidal area under a precision–recall curve.

| Evaluation | Micro AP | Micro ROC-AUC | Source |
| --- | ---: | ---: | --- |
| Best checkpoint, validation | 0.419856 | 0.893990 | Cell 38 |
| Best checkpoint, test | 0.403904 | 0.893734 | Cell 38 |
| Prior baseline, test | 0.107657 | 0.683760 | Cell 38 |
| Random baseline, test | 0.052564 | 0.494203 | Cell 38 |
| Last training state, test | 0.384031 | 0.887372 | Cell 31 |

**Why two test values?** Cell 31 evaluates the model left in memory after training. Cell 38 explicitly loads `best_model.pt`, selected by validation micro AP. The edited notebook now loads that checkpoint before its first test evaluation and JSON export. The lower historical value is retained here rather than discarded.

Evidence: [saved output excerpts](../results/lab09_source_outputs.txt) and [extracted values](../results/lab09_historical.json).

Limits:

- Clips are shuffled and split 80/10/10, then capped. They are not grouped by song or artist; this does not test unseen-artist performance.
- The top 50 tags are chosen using all available clips before splitting.
- The original run loaded existing embedding caches. The original cache names did not encode clip identities, label order or dataset contents; exact reproducibility cannot be established from those names.
- The original loader could substitute silence for unreadable audio. The edited loader raises an error instead.
- The saved configuration uses 16 kHz. The encoder's expected sample rate was not established from a model card during curation; verify it before interpreting a new benchmark.
- The original training cell resumed a previous checkpoint. The printed execution ends at epoch 66; there is no basis for treating it as a clean, uninterrupted run.

## Lab 10: text–audio alignment

The saved dataset output contains 4,816 MusicCaps training rows, 536 validation rows and 746 Song Describer evaluation rows. Inputs use the first two seconds at 24 kHz. Audio and text encoders are frozen; only the projection heads and temperature are trained.

The loss is symmetric across directions. **The reported Recall@K is audio→text**, over the full candidate split, and accepts only the matching row as positive. The free-text demo runs text→audio and is not the source of these scores.

### Separate head comparison — source cell 45

| Head | Validation R@10 | Song Describer R@1 | R@5 | R@10 |
| --- | ---: | ---: | ---: | ---: |
| Linear | 0.427239 | 0.016086 | 0.044236 | 0.073727 |
| MLP | 0.449627 | 0.017426 | 0.052279 | 0.076408 |
| Transformer | 0.304104 | 0.012064 | 0.032172 | 0.050938 |

Values are transcribed at the six-decimal precision printed in the original dataframe. The MLP exceeds linear R@10 by 0.002681, or about **0.27 percentage points**, in this comparison. The transformer performs worse in this run. No repeated-seed study or statistical significance test was recorded.

### Main run — source cell 43

A separately trained main model reports Song Describer R@1 = 0.0160857905, R@5 = 0.0469168909 and R@10 = 0.0831099227. It is not the MLP row from the separate comparison. The notebook contains non-sequential execution counts and modified cells; saved outputs should be read as historical records, not proof that the edited source reproduces them.

Evidence: [saved output excerpts](../results/lab10_source_outputs.txt), [comparison CSV](../results/lab10_head_comparison.csv) and [extracted values](../results/lab10_historical.json).

Limits:

- Song Describer includes multiple captions for some tracks. Exact-row evaluation treats other captions for the same track as negatives. It is not a multi-positive, track-level retrieval benchmark.
- The transformer reshapes a pooled embedding into tokens; it does not process a temporal sequence of audio frames.
- The heads run sequentially without resetting the seed for each architecture. This is a single-run comparison, not a controlled estimate of architecture effects.
- Dataset and model revision IDs were not recorded for the original run. The curation does not establish whether the pretrained encoders saw any evaluation material.
- Two seconds can omit vocals, structure or instruments described elsewhere in a recording.
- Decoding failures can change the evaluated subset. The edited builder records skipped rows and keeps source-row mapping for the demo.
- Full-matrix retrieval uses quadratic memory in the number of candidates. The notebook is intended for these small experiments.

## Resource measurements

Timing and emissions are not headline results here. Lab 9 samples system RAM, whereas Lab 10 records process RSS. Cache hits and the stage being measured also change the cost. Optional CodeCarbon values are estimates; the original outputs do not support a general claim about energy savings.
