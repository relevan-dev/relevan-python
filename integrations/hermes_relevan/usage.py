"""Decide which recalled results an assistant reply used.

A result counts as used when the reply cites its id or its title, or when the
reply repeats enough of the result's distinctive words. A distinctive word is a
word of the text the model saw for that result that is not in the user's
message and not in most of the other results. So a reply that only echoes the
question, or that uses words every result shares, does not count.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_WORD = re.compile(r"[\w][\w'-]*", re.UNICODE)

_STOPWORDS = frozenset(
    [
        "about",
        "above",
        "after",
        "again",
        "against",
        "also",
        "although",
        "among",
        "another",
        "anything",
        "around",
        "because",
        "been",
        "before",
        "being",
        "below",
        "between",
        "both",
        "cannot",
        "could",
        "does",
        "doing",
        "down",
        "during",
        "each",
        "either",
        "else",
        "every",
        "from",
        "further",
        "have",
        "having",
        "here",
        "hers",
        "herself",
        "himself",
        "however",
        "into",
        "itself",
        "just",
        "like",
        "made",
        "make",
        "many",
        "might",
        "more",
        "most",
        "much",
        "must",
        "myself",
        "never",
        "only",
        "other",
        "ours",
        "ourselves",
        "over",
        "same",
        "shall",
        "should",
        "some",
        "such",
        "than",
        "that",
        "their",
        "theirs",
        "them",
        "themselves",
        "then",
        "there",
        "these",
        "they",
        "this",
        "those",
        "through",
        "under",
        "until",
        "upon",
        "very",
        "what",
        "when",
        "where",
        "whether",
        "which",
        "while",
        "whom",
        "whose",
        "will",
        "with",
        "within",
        "without",
        "would",
        "your",
        "yours",
        "yourself",
        "yourselves",
        "note",
        "notes",
    ]
)

MIN_SHARED_WORDS = 3
MIN_TITLE_LENGTH = 6


@dataclass(frozen=True)
class RecalledHit:
    """One search result that was put in front of the model."""

    object_id: str
    position: int
    title: str
    text: str


@dataclass(frozen=True)
class Usage:
    """A recalled result the reply used, and how strongly."""

    hit: RecalledHit
    grade: int
    reason: str


def _words(text: str) -> set[str]:
    return {w.lower() for w in _WORD.findall(text) if len(w) >= 4} - _STOPWORDS


def _normalise(text: str) -> str:
    return " ".join(_WORD.findall(text.lower()))


def used_results(hits: list[RecalledHit], user_text: str, reply: str) -> list[Usage]:
    """Return the hits the reply used, each with grade 2 (cited) or 1 (paraphrased)."""
    if not reply.strip():
        return []
    reply_norm = _normalise(reply)
    reply_words = _words(reply)
    query_words = _words(user_text)
    hit_words = [_words(f"{hit.title} {hit.text}") for hit in hits]
    common: set[str] = set()
    if len(hits) >= 3:
        counts: dict[str, int] = {}
        for words in hit_words:
            for word in words:
                counts[word] = counts.get(word, 0) + 1
        common = {word for word, count in counts.items() if count > len(hits) / 2}
    used: list[Usage] = []
    for hit, words in zip(hits, hit_words, strict=True):
        if re.search(rf"(?<![\w-]){re.escape(hit.object_id)}(?![\w-])", reply):
            used.append(Usage(hit, 2, "cited the result id"))
            continue
        title = _normalise(hit.title)
        if len(title) >= MIN_TITLE_LENGTH and f" {title} " in f" {reply_norm} ":
            used.append(Usage(hit, 2, "named the result title"))
            continue
        shared = (words - query_words - common) & reply_words
        if len(shared) >= MIN_SHARED_WORDS:
            used.append(Usage(hit, 1, f"repeated {len(shared)} distinctive words"))
    return used
