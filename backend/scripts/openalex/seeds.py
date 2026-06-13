"""Curated, origin-relevant seed researchers — one per discipline (demo).

Why seeds instead of raw concept top-citations: OpenAlex's most-cited work *inside a
concept* is usually a methods/tooling paper or a name-collision (e.g. "Architecture"
returns a CNN paper). These researchers are real, modern, indexed in OpenAlex with
abstracts, AND actually think about origins. The pipeline still fetches their REAL
top paper from OpenAlex; nothing here is fabricated — the topic hint just steers to
their origin-relevant high-cited work rather than an incidental methods paper.

Entry: (domain, discipline, author_name, topic_hint, origin_lens)
"""

from __future__ import annotations

SEEDS: list[tuple[str, str, str, str, str]] = [
    # A. Formal Sciences
    ("Formal Sciences", "Mathematics & Logic", "Gregory Chaitin", "algorithmic information randomness", "irreducible randomness and the limits of formal systems"),
    ("Formal Sciences", "Theory of Computation", "Stephen Wolfram", "computational universe cellular automata", "is physics itself a computation"),
    ("Formal Sciences", "Information Theory", "Edwin T. Jaynes", "maximum entropy", "inference and entropy as the bridge between information and physics"),
    ("Formal Sciences", "Statistics & Probability", "Judea Pearl", "causality causal inference", "causation beneath correlation"),
    # B. Physical Sciences
    ("Physical Sciences", "Cosmology", "Roger Penrose", "entropy singularity cosmology", "why the universe began in such a low-entropy state"),
    ("Physical Sciences", "Quantum Foundations", "Anton Zeilinger", "quantum entanglement measurement", "the role of observation and information in reality"),
    ("Physical Sciences", "Particle Physics & Unification", "Steven Weinberg", "unified theory symmetry", "the search for a single underlying law"),
    ("Physical Sciences", "Thermodynamics & Statistical Mechanics", "Jeremy L. England", "dissipation driven adaptation", "life as a thermodynamically favored structure"),
    ("Physical Sciences", "Astrophysics & Planetary Science", "Sara Seager", "exoplanet atmosphere biosignature", "detecting life across cosmic distance"),
    ("Physical Sciences", "Origin-of-Life Chemistry", "Jack W. Szostak", "origin of life protocell RNA", "from chemistry to self-replication"),
    ("Physical Sciences", "Earth System & Geoscience", "Timothy M. Lenton", "Gaia earth system feedback", "life and planet as one self-regulating system"),
    # C. Life Sciences
    ("Life Sciences", "Evolutionary Biology", "Stuart A. Kauffman", "self-organization origin order", "spontaneous order that precedes natural selection"),
    ("Life Sciences", "Molecular Biology & Genetics", "Svante Paabo", "ancient DNA human origins", "the genetic record of where we came from"),
    ("Life Sciences", "Neuroscience", "Karl J. Friston", "free energy principle", "the brain as a self-organizing prediction engine"),
    ("Life Sciences", "Ecology & Systems Biology", "Simon A. Levin", "complexity ecosystems self-organization", "emergent order across biological scales"),
    ("Life Sciences", "Astrobiology", "Steven A. Benner", "synthetic biology weird life", "life not as we know it"),
    # D. Cognitive & Interdisciplinary
    ("Cognitive & Interdisciplinary", "Cognitive Science", "Joshua B. Tenenbaum", "computational cognition learning", "how minds build models of the world"),
    ("Cognitive & Interdisciplinary", "Artificial Intelligence", "Geoffrey E. Hinton", "deep learning representation", "meaning emerging from statistics"),
    ("Cognitive & Interdisciplinary", "Consciousness Studies", "Giulio Tononi", "integrated information consciousness", "consciousness as intrinsic, integrated information"),
    ("Cognitive & Interdisciplinary", "Complex Systems & Self-Organization", "Per Bak", "self-organized criticality", "complexity poised at the critical edge"),
    ("Cognitive & Interdisciplinary", "Network Science", "Albert-Laszlo Barabasi", "scale-free network emergence", "why hub structure emerges everywhere"),
    ("Cognitive & Interdisciplinary", "Semiotics", "Umberto Eco", "semiotics interpretation sign", "how anything comes to mean"),
    # E. Social Sciences
    ("Social Sciences", "Psychology", "Daniel Kahneman", "prospect theory judgment heuristics", "the architecture of human judgment"),
    ("Social Sciences", "Depth Psychology & Psychoanalysis", "Mark Solms", "consciousness affect unconscious", "the hidden, affective roots of the self"),
    ("Social Sciences", "Anthropology", "Joseph Henrich", "cultural evolution cooperation", "how culture made our species"),
    ("Social Sciences", "Archaeology & Paleoanthropology", "Ian Hodder", "symbolic archaeology origins", "the birth of symbolic culture"),
    ("Social Sciences", "Linguistics", "Noam Chomsky", "language faculty syntax universal", "an innate origin of language"),
    ("Social Sciences", "Sociology", "Niklas Luhmann", "social systems autopoiesis", "society as self-producing communication"),
    ("Social Sciences", "Economics & Game Theory", "Robert Axelrod", "evolution of cooperation", "the origin of cooperation"),
    ("Social Sciences", "Political Science", "Peter Turchin", "cliodynamics social complexity", "laws behind the rise and fall of societies"),
    # F. Humanities
    ("Humanities", "Metaphysics & Ontology", "Tim Maudlin", "metaphysics of physics time", "what physics implies about what exists"),
    ("Humanities", "Epistemology", "Alvin I. Goldman", "epistemology knowledge justification", "what it is to know"),
    ("Humanities", "Philosophy of Mind", "David J. Chalmers", "hard problem consciousness", "why there is subjective experience at all"),
    ("Humanities", "Philosophy of Science", "Nancy Cartwright", "laws of nature scientific explanation", "whether the laws we write are really true"),
    ("Humanities", "Ethics & Value Theory", "Peter Singer", "ethics moral value", "the ground and scope of value"),
    ("Humanities", "Religious Studies & Theology", "Ara Norenzayan", "cognitive science of religion big gods", "the cognitive origin of the sacred"),
    ("Humanities", "History", "Jared Diamond", "societies collapse civilization", "the deep drivers of human history"),
    ("Humanities", "Classics & Mythology", "Michael Witzel", "comparative mythology origins", "the deep ancestry of origin myths"),
    # G. Arts
    ("Arts", "Aesthetics", "Semir Zeki", "neuroaesthetics beauty brain", "the neural basis of beauty"),
    ("Arts", "Visual Art", "Vilayanur S. Ramachandran", "neuroaesthetics art perception", "why art moves the brain"),
    ("Arts", "Music", "Aniruddh D. Patel", "music language brain evolution", "music, language, and the mind's origins"),
    ("Arts", "Architecture & Design", "Christopher Alexander", "pattern language wholeness order", "the nature of order and living structure"),
    ("Arts", "Literature", "Franco Moretti", "distant reading quantitative literature", "the large-scale shape of literature"),
]
