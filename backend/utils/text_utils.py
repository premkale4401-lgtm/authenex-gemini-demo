import re
from collections import Counter

def sentence_length_variance(text: str) -> float:
    sentences = re.split(r'[.!?]', text)
    lengths = [len(s.split()) for s in sentences if len(s.split()) > 2]

    if not lengths:
        return 0.0

    mean = sum(lengths) / len(lengths)
    return sum((l - mean) ** 2 for l in lengths) / len(lengths)


def repetition_score(text: str) -> float:
    words = text.lower().split()
    counts = Counter(words)

    repeated = sum(1 for w, c in counts.items() if c > 3)
    return repeated / max(len(counts), 1)


def lexical_diversity(text: str) -> float:
    words = text.lower().split()
    if not words:
        return 0.0
    return len(set(words)) / len(words)
