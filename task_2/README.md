# Task 2 — Binary classification of Type

This task uses the `ID` column as the join key between `table_1.csv` and `table_2.csv`. The merged dataset provides the feature set from the first table and the binary label from the second table.

## Approach

1. Read both tables.
2. Join on `ID` to create a single labelled dataset.
3. Map the label values `n` and `y` to numeric values `0` and `1`.
4. Split data into train and test sets.
5. Build a pipeline with:
   - numeric imputation and scaling
   - categorical imputation and one-hot encoding
   - logistic regression classifier
6. Evaluate using accuracy and classification report.

## Why this method

The target is binary and the feature space is a mix of numeric and categorical values, so a scikit-learn `ColumnTransformer` with logistic regression is a robust baseline. It is transparent, interpretable, and easy to maintain while delivering reliable performance on tabular data.

## Run

```bash
python task_2/train_classifier.py
```
