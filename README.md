# Open Source LLMs for Content Analysis

Companion website to the article:

> Possler, D., Dietrich, F., Scheper, J., Lammers, A., & Spatzenegger, A. (2026). Gebrauchsfertige, Open Source Large Language Models auf Hugging Face als Forschungsinfrastruktur für die standardisierte Inhaltsanalyse von Texten. *Publizistik*.

The website is available at: [llm-content-analysis.com](https://llm-content-analysis.com)

## Content

The site has three sections:

1. **Tutorials** (`sections/tutorials/`) — English-language, step-by-step guide to text classification
2. **Paper** (`sections/paper/`) — the German-language supplementary website for the *Publizistik* article
3. **Workshop** (`sections/workshop/`) — materials for the hands-on workshop

Shared assets (theme, bibliography, images, R environment) live at the repo root and are reused across all three sections.

## Requirements

- Python (installation guide in `sections/tutorials/huggingface-transformers/installation.qmd`)
- [Quarto](https://quarto.org) (to render the website)
- R with [renv](https://rstudio.github.io/renv/) (for the Paper section's data tables; run `renv::restore()` on first use)

## Render the website locally

```bash
quarto render
```
