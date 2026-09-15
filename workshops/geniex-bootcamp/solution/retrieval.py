"""A small lexical retriever with explicit source and context policies."""
import re

STOPWORDS = set("a an the is are who what where when will can must be by at to of for in on and or it after all".split())

def words(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOPWORDS

def select_context(question, documents, max_chars=360):
    if max_chars < 1:
        raise ValueError("max_chars must be positive")
    query = words(question)
    ranked = []
    for document in documents:
        if document.get("status") != "current":
            continue
        score = len(query & words(document["text"]))
        if score:
            ranked.append((score, document))
    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))
    selected = []
    used = 0
    for _, document in ranked:
        cost = len(document["id"]) + len(document["text"]) + 4
        if used + cost <= max_chars:
            selected.append(document)
            used += cost
    return selected
