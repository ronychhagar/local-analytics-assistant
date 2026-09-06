# Task 3 — Similarity-based part replacement

## Data findings

1. The descriptions are highly structured, mixing product family language, ratings, material, dimensions, and application contexts. This makes textual similarity a sensible way to retrieve alternatives.
2. The same component appears in several variants with slight changes in current, voltage, material, and enclosure. Those small changes can be semantically meaningful and therefore require careful normalization rather than plain exact string matching.
3. Some rows have missing or sparse descriptions. These should be handled by treating missing text as empty strings and falling back to other metadata if necessary so the algorithm does not fail on null values.

## Difficulties

- Inconsistent formatting: text contains numbers, abbreviations, dimensional values, and mixed case.
- Repeated product families: many rows differ only in current rating or package type.
- Partial missing values: some rows have empty `DESCRIPTION` or columns with missing fields.

## Handling strategy

- Lowercase and normalize punctuation before tokenization.
- Use a TF-IDF + cosine similarity pipeline to compare description text at the semantic level.
- Exclude the part itself from its candidate list.
- Return the top five nearest neighbours for each row.

## Why the chosen approach

TF-IDF is interpretable, lightweight, and well suited for short technical descriptions where lexical overlap matters strongly. It also works well without GPU or external language models, which makes it suitable for a local, efficient retrieval system.

## Run

```bash
python task_3/part_similarity.py
```
