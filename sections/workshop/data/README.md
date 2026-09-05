# Workshop data

Source: **Real World Worry Waves Dataset (RW3D)**, van der Vegt & Kleinberg (2023),
*Scientific Data*, 10(1), 537. https://doi.org/10.1038/s41597-023-02438-y
Data: https://osf.io/9b85r/ — licensed **CC-BY 4.0**.

`real_world_worry_waves_dataset.csv` and `data_codebook.xlsx` are the original
files downloaded from OSF, unmodified. `prepare_dataset.py` filters wave 1
(April 2020, English/native-or-fluent speakers only) and produces:

- `rw3d_wave1_full.csv` — all 1,142 eligible wave-1 respondents, one long
  free-text response each plus their self-chosen gold emotion label and
  8 emotion-intensity ratings (9-point scales). Naturally imbalanced
  (dominated by anxiety/sadness/relaxation). No longer used directly in an
  exercise, but kept for the evaluation module / in case it's needed again.
- `rw3d_workshop_sample.csv` — 150 cases balanced across the three emotions
  used in the exercises (anger, fear, sadness): 50 per emotion, split into 25
  "low" and 25 "high" on that emotion's own 9-point rating, drawn only from
  respondents whose self-chosen main emotion was anger, fear, or sadness.
  "Low"/"high" use one shared rule (rating < 5 / > 7) — see the comments next
  to `LOW_THRESHOLD`/`HIGH_THRESHOLD` in `prepare_dataset.py` for why that
  rule isn't fully symmetric. Columns: `id`, `text`, `main_emotion`, `anger`,
  `fear`, `sadness`.

Re-run `python3 prepare_dataset.py` to regenerate both files deterministically
(`SEED = 42`).

When using this data, please cite van der Vegt & Kleinberg (2023) per the
license.
