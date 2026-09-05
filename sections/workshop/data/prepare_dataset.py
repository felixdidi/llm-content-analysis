"""
Prepares the workshop dataset from the Real World Worry Waves Dataset (RW3D).

Source: van der Vegt, I., & Kleinberg, B. (2023). A multi-modal panel dataset
to understand the psychological impact of the pandemic. Scientific Data, 10(1),
537. https://doi.org/10.1038/s41597-023-02438-y
Data: https://osf.io/9b85r/ (CC-BY 4.0)

We use wave 1 (April 2020) only for the core workshop exercise: each participant
wrote a long free-text response (>= 500 characters) about how they felt about the
COVID-19 situation, then chose which single emotion (of anger, anxiety, desire,
disgust, fear, happiness, relaxation, sadness) best represented their feeling.
That self-chosen label is a genuine self-report gold standard, not a third-party
annotation and not a fill-in-the-blank template.

Two output files:
- rw3d_wave1_full.csv:      all wave-1 respondents (English, native or fluent).
                             Not used directly in an exercise, but kept
                             around for the evaluation module / in case it's
                             needed again.
- rw3d_workshop_sample.csv: 150 cases, balanced across the three emotions used
                             in the exercises (anger, fear, sadness): 50 cases
                             per emotion, split into 25 "low" and 25 "high" on
                             that emotion's own 9-point intensity rating, drawn
                             only from respondents whose self-chosen main
                             emotion was anger, fear, or sadness. See
                             LOW_THRESHOLD / HIGH_THRESHOLD below for the exact
                             cutoffs and why they're not fully symmetric.
"""

import csv
import random

SOURCE = "real_world_worry_waves_dataset.csv"
SAMPLE_EMOTIONS = ["anger", "fear", "sadness"]
PER_LEVEL = 25  # 25 low + 25 high per emotion = 150 rows total
# Ratings are on a 1-9 scale. "low" / "high" are defined by one shared rule
# applied to all three emotions. The tightest symmetric rule (low < 2, i.e.
# just a rating of 1; high > 8, i.e. just a rating of 9) doesn't leave enough
# cases once we also require the respondent's main emotion to be anger, fear,
# or sadness: only 8 respondents chose sadness as their main emotion while
# rating their own sadness as a 1. LOW_THRESHOLD = 5 (ratings 1-4 count as
# low) is the loosest cutoff needed to get 25 low-sadness cases; HIGH_THRESHOLD
# = 7 (ratings 8-9 count as high) is needed because only 17 anger-pool
# respondents rated their anger a 9. Within each band, the most extreme values
# are always preferred first, so most low/high cases end up at 1 or 9 anyway.
LOW_THRESHOLD = 5   # rating < LOW_THRESHOLD counts as "low"
HIGH_THRESHOLD = 7  # rating > HIGH_THRESHOLD counts as "high"
SEED = 42

KEEP_COLUMNS = {
    "id": "id",
    "text_long_wave1": "text",
    "text_short_wave1": "text_short",
    "chosen_emotion_wave1": "emotion_gold",
    "worry_wave1": "worry",
    "anger_wave1": "anger",
    "disgust_wave1": "disgust",
    "fear_wave1": "fear",
    "anxiety_wave1": "anxiety",
    "sadness_wave1": "sadness",
    "happiness_wave1": "happiness",
    "relaxation_wave1": "relaxation",
    "desire_wave1": "desire",
    "nchar_long_wave1": "nchar",
    "ntok_long_wave1": "ntok",
}


def load_wave1(path):
    with open(path, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    kept = []
    for row in rows:
        text = row.get("text_long_wave1", "").strip()
        if not text:
            continue
        if row.get("cld_lang_long_wave1") != "en":
            continue
        if row.get("eng_native_wave1") not in ("Yes", "No but I speak it fluently"):
            continue
        record = {new: row[old] for old, new in KEEP_COLUMNS.items()}
        record["emotion_gold"] = record["emotion_gold"].lower()
        kept.append(record)
    return kept


def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def build_balanced_sample(rows, rng):
    """25 low + 25 high per emotion in SAMPLE_EMOTIONS, from respondents whose
    main emotion is one of SAMPLE_EMOTIONS, with no respondent used twice."""
    pool = [r for r in rows if r["emotion_gold"] in SAMPLE_EMOTIONS]

    groups = []
    for emotion in SAMPLE_EMOTIONS:
        low = [r for r in pool if float(r[emotion]) < LOW_THRESHOLD]
        high = [r for r in pool if float(r[emotion]) > HIGH_THRESHOLD]
        groups.append((emotion, "low", low))
        groups.append((emotion, "high", high))

    # Fill the scarcest group first so it isn't starved by rows already
    # claimed by a more plentiful group.
    groups.sort(key=lambda g: len(g[2]))

    used_ids = set()
    sample = []
    for emotion, level, candidates in groups:
        available = [r for r in candidates if r["id"] not in used_ids]
        if level == "low":
            available.sort(key=lambda r: (float(r[emotion]), rng.random()))
        else:
            available.sort(key=lambda r: (-float(r[emotion]), rng.random()))
        chosen = available[:PER_LEVEL]
        if len(chosen) < PER_LEVEL:
            raise ValueError(
                f"Only {len(chosen)} available for {emotion} {level}, "
                f"need {PER_LEVEL}. Loosen LOW_THRESHOLD/HIGH_THRESHOLD."
            )
        used_ids.update(r["id"] for r in chosen)
        sample.extend(chosen)
        print(f"  {emotion:8s} {level:4s}: {len(chosen)} cases")

    return sample


def main():
    rows = load_wave1(SOURCE)
    fieldnames = list(KEEP_COLUMNS.values())

    write_csv("rw3d_wave1_full.csv", rows, fieldnames)
    print(f"Full wave-1 sample: {len(rows)} texts -> rw3d_wave1_full.csv")

    rng = random.Random(SEED)
    sample = build_balanced_sample(rows, rng)
    rng.shuffle(sample)

    sample_fieldnames = ["id", "text", "main_emotion", "anger", "fear", "sadness"]
    sample_rows = [
        {
            "id": i,
            "text": r["text"],
            "main_emotion": r["emotion_gold"],
            "anger": int(float(r["anger"])),
            "fear": int(float(r["fear"])),
            "sadness": int(float(r["sadness"])),
        }
        for i, r in enumerate(sample, start=1)
    ]
    write_csv("rw3d_workshop_sample.csv", sample_rows, sample_fieldnames)
    print(f"Workshop sample: {len(sample_rows)} texts -> rw3d_workshop_sample.csv")


if __name__ == "__main__":
    main()
