# Open Source LLMs für die Inhaltsanalyse

Begleitende Materialien zum Artikel:

> Possler, D., Dietrich, F., Scheper, J., Lammers, A., & Spatzenegger, A. (2026). Gebrauchsfertige, Open Source Large Language Models auf Hugging Face als Forschungsinfrastruktur für die standardisierte Inhaltsanalyse von Texten. *Publizistik*.

Die Website ist verfügbar unter: [llm-content-analysis.com](https://llm-content-analysis.com)

## Inhalt

Schritt-für-Schritt-Anleitungen zur Textklassifikation mit drei LLM-Typen über die Hugging Face-Bibliothek:

1. **Kategoriespezifisches Encoder-Modell** – feinabgestimmte Encoder für spezifische Kategorien
2. **Aufgabenspezifisches Encoder-Modell** – Encoder für allgemeine NLP-Aufgaben (z. B. Zero-Shot)
3. **Universelles Decoder-Modell** – generative Decoder-Modelle via Prompt

Ergänzt durch eine empirische **Beispielstudie** mit Vergleich gegenüber diktionärsbasierter Analyse und überwachtem maschinellem Lernen.

## Voraussetzungen

- Python (Anleitung zur Installation in `01_installation.qmd`)
- [Quarto](https://quarto.org) (zum Rendern der Website)

## Website lokal rendern

```bash
quarto render
```
