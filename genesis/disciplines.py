"""The 43-discipline taxonomy used to query OpenAlex.

Each entry: (domain, discipline, openalex_search_term). The search term is resolved
to an OpenAlex concept id at ingest time, then we pull the highest-cited works in
that concept. Keeping this as data (not code) makes the roster reproducible: change
a term, re-run `ingest.py`, get a new — but still real — roster.
"""

from __future__ import annotations

# (domain, discipline, search_term)
DISCIPLINES: list[tuple[str, str, str]] = [
    # A. Formal Sciences
    ("Formal Sciences", "Mathematics & Logic", "mathematical logic"),
    ("Formal Sciences", "Theory of Computation", "theory of computation"),
    ("Formal Sciences", "Information Theory", "information theory"),
    ("Formal Sciences", "Statistics & Probability", "probability theory"),
    # B. Physical Sciences
    ("Physical Sciences", "Cosmology", "cosmology"),
    ("Physical Sciences", "Quantum Foundations", "interpretations of quantum mechanics"),
    ("Physical Sciences", "Particle Physics & Unification", "particle physics"),
    ("Physical Sciences", "Thermodynamics & Statistical Mechanics", "statistical mechanics"),
    ("Physical Sciences", "Astrophysics & Planetary Science", "astrophysics"),
    ("Physical Sciences", "Origin-of-Life Chemistry", "abiogenesis"),
    ("Physical Sciences", "Earth System & Geoscience", "earth system science"),
    # C. Life Sciences
    ("Life Sciences", "Evolutionary Biology", "evolutionary biology"),
    ("Life Sciences", "Molecular Biology & Genetics", "molecular biology"),
    ("Life Sciences", "Neuroscience", "neuroscience"),
    ("Life Sciences", "Ecology & Systems Biology", "ecology"),
    ("Life Sciences", "Astrobiology", "astrobiology"),
    # D. Cognitive & Interdisciplinary
    ("Cognitive & Interdisciplinary", "Cognitive Science", "cognitive science"),
    ("Cognitive & Interdisciplinary", "Artificial Intelligence", "artificial intelligence"),
    ("Cognitive & Interdisciplinary", "Consciousness Studies", "consciousness"),
    ("Cognitive & Interdisciplinary", "Complex Systems & Self-Organization", "self-organization"),
    ("Cognitive & Interdisciplinary", "Network Science", "complex network"),
    ("Cognitive & Interdisciplinary", "Semiotics", "semiotics"),
    # E. Social Sciences
    ("Social Sciences", "Psychology", "cognitive psychology"),
    ("Social Sciences", "Depth Psychology & Psychoanalysis", "psychoanalysis"),
    ("Social Sciences", "Anthropology", "cultural anthropology"),
    ("Social Sciences", "Archaeology & Paleoanthropology", "paleoanthropology"),
    ("Social Sciences", "Linguistics", "linguistics"),
    ("Social Sciences", "Sociology", "sociology"),
    ("Social Sciences", "Economics & Game Theory", "game theory"),
    ("Social Sciences", "Political Science", "political philosophy"),
    # F. Humanities
    ("Humanities", "Metaphysics & Ontology", "metaphysics"),
    ("Humanities", "Epistemology", "epistemology"),
    ("Humanities", "Philosophy of Mind", "philosophy of mind"),
    ("Humanities", "Philosophy of Science", "philosophy of science"),
    ("Humanities", "Ethics & Value Theory", "ethics"),
    ("Humanities", "Religious Studies & Theology", "religious studies"),
    ("Humanities", "History", "historiography"),
    ("Humanities", "Classics & Mythology", "mythology"),
    # G. Arts
    ("Arts", "Aesthetics", "aesthetics"),
    ("Arts", "Visual Art", "art history"),
    ("Arts", "Music", "music theory"),
    ("Arts", "Architecture & Design", "architecture"),
    ("Arts", "Literature", "literary theory"),
]


def slugify(discipline: str) -> str:
    keep = []
    for ch in discipline.lower():
        if ch.isalnum():
            keep.append(ch)
        elif ch in (" ", "-", "&", "/"):
            keep.append("_")
    slug = "".join(keep)
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug.strip("_")
