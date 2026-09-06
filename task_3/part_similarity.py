from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parent.parent


def normalize_text(text):
    if pd.isna(text):
        return ''
    text = str(text).lower()
    text = text.replace('x', ' x ')
    text = text.replace('/', ' ')
    text = ''.join(ch if ch.isalnum() or ch.isspace() else ' ' for ch in text)
    return ' '.join(text.split())


def load_parts(base_dir: Path = ROOT) -> pd.DataFrame:
    df = pd.read_csv(base_dir / 'Parts.csv', sep=';')
    df['DESCRIPTION'] = df['DESCRIPTION'].fillna('').astype(str)
    df['normalized_description'] = df['DESCRIPTION'].apply(normalize_text)
    return df


def find_similar_parts(n_top: int = 5):
    df = load_parts()
    texts = df['normalized_description'].tolist()
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), min_df=1)
    matrix = vectorizer.fit_transform(texts)
    cosine = cosine_similarity(matrix)

    recommendations = []
    for idx, row in df.iterrows():
        similarities = cosine[idx].copy()
        similarities[idx] = -1.0
        top_indices = np.argsort(similarities)[::-1][:n_top]
        top_ids = [df.iloc[i]['ID'] for i in top_indices]
        top_scores = [float(similarities[i]) for i in top_indices]
        recommendations.append({
            'query_id': row['ID'],
            'query_description': row['DESCRIPTION'],
            'similar_ids': top_ids,
            'similarity_scores': top_scores,
        })

    return pd.DataFrame(recommendations), df


if __name__ == '__main__':
    results, df = find_similar_parts()
    print('Top similar replacement candidates:')
    for _, row in results.head(5).iterrows():
        print(f"{row['query_id']} -> {row['similar_ids']}")
