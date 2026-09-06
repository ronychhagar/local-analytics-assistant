import pandas as pd

from task_2.train_classifier import load_labelled_data, train_classifier


def test_labelled_data_is_merged():
    merged = load_labelled_data()
    assert 'Type' in merged.columns
    assert 'ID' in merged.columns
    assert merged.shape[0] > 0


def test_classifier_runs_and_returns_accuracy():
    result = train_classifier()
    assert 'accuracy' in result
    assert 0.0 <= result['accuracy'] <= 1.0
