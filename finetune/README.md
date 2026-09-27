# Pik models: our multilingual retriever

Status: **trained.** Carl fine-tuned a multilingual retriever on Japanese and English on his laptop (Sep 27, 2026), so a Japanese Slack thread can answer an English ask and the other way round. It sits between the core database and the confidence per task (deck slides 07 and 09).

**To add (Carl):** the training script, the base model name, the training data description and the evaluation numbers, in this folder. Weights stay out of git; put a download link or a Hugging Face / Vertex AI model id here instead.

## What it learns from
- Pairs of an ask and the evidence that answers it, in Japanese and English.
- Per customer, inside that customer's cloud project; never pooled across customers.
- Never: direct messages, private channels, protected attributes.

## Output
Retrieved evidence with its source, used to compute a confidence for one task. Never a grade of a person; the person named sees the same page.

## Next (not built)
More layers of capture, all opt-in: screenshots read with OCR, screens and designs read with a vision-language model, and connectors for vertical systems such as hospital shift rosters or airline crew logs.

## Files
- `config.example.yaml`: placeholder configuration for per-customer training on Vertex AI.
