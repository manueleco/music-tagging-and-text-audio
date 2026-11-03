# Data and pretrained models

## MagnaTagATune — tagging notebook

Obtain annotations, clip metadata and audio from the [City University MagnaTagATune page](https://mirg.city.ac.uk/codeapps/the-magnatagatune-dataset). Preserve the relative audio paths from `clip_info_final.csv`:

```text
magnatagatune/
  annotations_final.csv
  clip_info_final.csv
  audio/
    <relative MP3 paths from clip_info_final.csv>
```

`mp3/` is accepted instead of `audio/`. Set `MTAT_ROOT` to `magnatagatune/`. The notebook does not download this dataset. FFmpeg can be installed separately if torchaudio cannot decode an MP3.

Dataset credit: Edith Law, Kris West, Michael Mandel, Mert Bay and J. Stephen Downie, “Evaluation of algorithms using games: the case of music annotation,” ISMIR 2009, as cited by the dataset host.

## MusicCaps and Song Describer — retrieval notebook

The code loads these Hugging Face datasets:

- [CLAPv2/MusicCaps](https://huggingface.co/datasets/CLAPv2/MusicCaps): audio and captions, used for training and validation.
- [renumics/song-describer-dataset](https://huggingface.co/datasets/renumics/song-describer-dataset): audio and captions, used for evaluation.

These are the distributions used in the original notebook. Read their dataset pages and upstream references before downloading or reusing the audio. Song Describer has repeated track IDs with distinct captions; the retained metric is exact-row matching.

The `musiccaps_revision` and `songdescriber_revision` configuration fields accept dataset revision IDs. `None` uses the current default revision and does not reproduce a historical snapshot. Fingerprints and row counts are recorded for new runs.

## Encoders

- Audio: [mtg-upf/clap_omarrq_mp_small_music](https://huggingface.co/mtg-upf/clap_omarrq_mp_small_music), loaded with [OMAR-RQ](https://github.com/MTG/omar-rq), layer 6.
- Text: `sentence-transformers/all-mpnet-base-v2`, loaded with SentenceTransformers.

No weights are redistributed. The audio model page had no model card when checked during curation. In particular, this repository does not assert that its pretraining data are disjoint from the evaluation sets. Lab 9 retains its original 16 kHz setting; Lab 10 uses 24 kHz. Verify the encoder input requirements before designing a new comparison.

The notebooks originated in Manuel Castillo's Machine Learning for Music coursework at Universitat Pompeu Fabra. This repository does not claim to introduce the pretrained encoders or datasets. Assignment sheets and reference notebooks are not included.
