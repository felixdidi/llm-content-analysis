"""
Generates a reference predictions file for the workshop sample, running the
three classifiers built in the workshop notebooks (02-encoder, 03-decoder) on
all 150 texts in the workshop sample:

1. Category-specific encoder: SamLowe/roberta-base-go_emotions
   (fine-tuned on GoEmotions; "anger", "fear", and "sadness" are labels the
   model already uses natively, so we just read off their scores)
2. Task-specific (NLI) encoder: MoritzLaurer/deberta-v3-base-zeroshot-v2.0
   (zero-shot classification directly against anger/fear/sadness)
3. Universal decoder: Qwen/Qwen2.5-1.5B-Instruct (JSON-prompted classification
   for all three emotions at once plus a short reasoning string -- the
   completed version of notebook 03's "Your turn" exercise)

This is a *reference* file: it lets people check their own notebook 02/03
results against something, without having to run all three models
themselves. It is not a substitute for running the models yourself.

All three models are openly accessible (no gated-repo access request needed).
"""

import csv
import json
import time

from transformers import pipeline

LABELS = ["anger", "fear", "sadness"]

NLI_HYPOTHESIS_TEMPLATE = "This text expresses {}."

DECODER_SYSTEM_PROMPT = (
    "You are a trained assistant for content analysis who determines whether "
    "a text expresses anger, fear, and sadness. Always answer precisely in "
    "JSON format with anger (true or false), fear (true or false), sadness "
    "(true or false), and reasoning (a short justification in English). "
    "Return only the JSON response, starting with '{' and ending with '}', "
    "with these four parameters."
)


def load_sample(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def run_encoder(rows):
    print("Loading category-specific encoder (SamLowe/roberta-base-go_emotions)...")
    clf = pipeline(
        "text-classification",
        model="SamLowe/roberta-base-go_emotions",
        top_k=None,
        truncation=True,
    )
    t0 = time.time()
    texts = [r["text"] for r in rows]
    results = clf(texts, batch_size=16)
    for row, scores in zip(rows, results):
        scores_by_label = {item["label"]: item["score"] for item in scores}
        for label in LABELS:
            row[f"encoder_{label}"] = scores_by_label[label]
    print(f"  done in {time.time() - t0:.0f}s")


def run_nli(rows):
    print("Loading task-specific NLI encoder (MoritzLaurer/deberta-v3-base-zeroshot-v2.0)...")
    clf = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0")
    t0 = time.time()
    texts = [r["text"] for r in rows]
    results = clf(
        texts,
        candidate_labels=LABELS,
        hypothesis_template=NLI_HYPOTHESIS_TEMPLATE,
        multi_label=True,
    )
    for row, result in zip(rows, results):
        scores_by_label = dict(zip(result["labels"], result["scores"]))
        for label in LABELS:
            row[f"nli_{label}"] = scores_by_label[label]
    print(f"  done in {time.time() - t0:.0f}s")


def parse_decoder_response(response):
    response = response.strip().strip("`").removeprefix("json").strip()
    try:
        parsed = json.loads(response)
        return parsed["anger"], parsed["fear"], parsed["sadness"], parsed["reasoning"]
    except (json.JSONDecodeError, KeyError):
        return None, None, None, None


def run_decoder(rows):
    print("Loading generative decoder (Qwen/Qwen2.5-1.5B-Instruct)...")
    gen = pipeline("text-generation", model="Qwen/Qwen2.5-1.5B-Instruct", device_map="auto")
    t0 = time.time()
    for i, row in enumerate(rows):
        instructions = [
            {"role": "system", "content": DECODER_SYSTEM_PROMPT},
            {"role": "user", "content": row["text"]},
        ]
        out = gen(instructions, max_new_tokens=256, do_sample=False)
        raw = out[0]["generated_text"][-1]["content"]
        anger, fear, sadness, reasoning = parse_decoder_response(raw)
        row["decoder_anger"] = anger
        row["decoder_fear"] = fear
        row["decoder_sadness"] = sadness
        row["decoder_reasoning"] = reasoning
        row["decoder_raw"] = raw
        if i % 25 == 0:
            print(f"  {i}/{len(rows)} ({time.time() - t0:.0f}s elapsed)")
    print(f"  done in {time.time() - t0:.0f}s")


def main():
    rows = load_sample("rw3d_workshop_sample.csv")
    rows = [
        {
            "id": r["id"],
            "text": r["text"],
            "main_emotion": r["main_emotion"],
            "self_report_anger": r["anger"],
            "self_report_fear": r["fear"],
            "self_report_sadness": r["sadness"],
        }
        for r in rows
    ]

    run_encoder(rows)
    run_nli(rows)
    run_decoder(rows)

    fieldnames = [
        "id", "text", "main_emotion",
        "self_report_anger", "self_report_fear", "self_report_sadness",
        "encoder_anger", "encoder_fear", "encoder_sadness",
        "nli_anger", "nli_fear", "nli_sadness",
        "decoder_anger", "decoder_fear", "decoder_sadness",
        "decoder_reasoning", "decoder_raw",
    ]
    with open("classification_results_reference.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print("Wrote classification_results_reference.csv")


if __name__ == "__main__":
    main()
