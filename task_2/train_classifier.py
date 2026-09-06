from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parent.parent


def load_labelled_data(base_dir: Path = ROOT) -> pd.DataFrame:
    table_1 = pd.read_csv(base_dir / 'table_1.csv', sep=';')
    table_2 = pd.read_csv(base_dir / 'table_2.csv', sep=';')
    merged = table_1.merge(table_2[['ID', 'Type']], on='ID', how='inner')
    merged['Type'] = merged['Type'].astype(str).str.strip().str.lower()
    return merged


def train_classifier(df: pd.DataFrame | None = None):
    data = load_labelled_data() if df is None else df

    feature_frame = data.drop(columns=['ID', 'Type'])
    target = data['Type'].map({'n': 0, 'y': 1})

    numeric_columns = feature_frame.select_dtypes(exclude=['object', 'string']).columns.tolist()
    categorical_columns = feature_frame.select_dtypes(include=['object', 'string']).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            (
                'numeric',
                Pipeline([
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler()),
                ]),
                numeric_columns,
            ),
            (
                'categorical',
                Pipeline([
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('onehot', OneHotEncoder(handle_unknown='ignore')),
                ]),
                categorical_columns,
            ),
        ]
    )

    model = Pipeline(
        steps=[
            ('preprocessor', preprocessor),
            ('classifier', LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        feature_frame,
        target,
        test_size=0.2,
        stratify=target,
        random_state=42,
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, target_names=['n', 'y'], output_dict=True)

    return {
        'model': model,
        'accuracy': accuracy,
        'report': report,
        'predictions': predictions,
        'y_test': y_test,
    }


if __name__ == '__main__':
    result = train_classifier()
    print(f"Test accuracy: {result['accuracy']:.4f}")
    print(classification_report(
        result['y_test'],
        result['predictions'],
        target_names=['n', 'y'],
    ))
