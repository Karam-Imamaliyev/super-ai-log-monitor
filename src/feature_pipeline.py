import math
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

def compute_length(text: str) -> int:
    return len(text)

def compute_entropy(text: str) -> float:
    if not text:
        return 0.0
    prob = [text.count(c) / len(text) for c in set(text)]
    return -sum(p * math.log2(p) for p in prob)

def extract_features(messages: list[str]) -> dict:
    tfidf_matrix = vectorizer.transform(messages)
    lengths = np.array([compute_length(m) for m in messages]).reshape(-1, 1)
    entropies = np.array([compute_entropy(m) for m in messages]).reshape(-1, 1)
    return {
        "tfidf": tfidf_matrix,
        "length": lengths,
        "entropy": entropies
    }

def fit_vectorizer(messages: list[str]):
    vectorizer.fit(messages)

