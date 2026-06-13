"""Seed corpus: researcher archetypes spanning the fields that touch *origins*.

Each researcher is an epistemic persona (what they believe, how they argue, what
they accept as evidence, where they are blind) plus a set of grounded "moves" — the
claims they will lay onto the shared graph, round by round. Real-paper corpora
(via OpenAlex/Semantic Scholar) can later replace these seeds without changing the
engine: the personas and moves are the only swappable part.

Shared CONCEPT ids are deliberately reused across researchers — that reuse is what
makes nodes become *cross-disciplinary bridges* on the graph.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# Canonical shared concepts. When two different disciplines both touch one of these,
# the node becomes a confluence point — a candidate for a fundamental question.
CONCEPTS = {
    "information_fundamental": "Is information more fundamental than matter/spacetime (it-from-bit)",
    "observer_measurement": "The relation between observation/measurement and reality",
    "entropy_arrow": "Entropy, the arrow of time, and the low-entropy initial condition",
    "self_organization": "Self-organization / dissipative structures",
    "emergence": "Emergence — properties of the whole absent from the parts",
    "fine_tuning": "Fine-tuning of the physical constants",
    "computation_universe": "Does the universe compute / physics as computation",
    "consciousness": "The nature and origin of consciousness",
    "time_origin": "The beginning of time itself",
    "symmetry_breaking": "Structure arising from broken symmetry",
}


@dataclass
class Move:
    """One trace a researcher lays onto the graph in a given round."""
    concept: str            # concept id this move centers on (shared or own)
    concept_label: str      # human label if it's a new concept
    claim: str              # natural-language statement, grounded in their corpus
    connects_to: list[str]  # other concept ids this move links to
    etype: str = "supports"  # supports | builds_on | bridges | contradicts
    evidence: str = ""       # one-line corpus grounding


@dataclass
class Researcher:
    name: str
    discipline: str
    stance: str             # core beliefs / worldview
    method: str             # how they argue
    accepts_as_evidence: str
    blind_spot: str
    moves: list[Move] = field(default_factory=list)

    def persona_brief(self) -> str:
        return (
            f"{self.name} — {self.discipline}\n"
            f"  Believes: {self.stance}\n"
            f"  Method: {self.method}\n"
            f"  Accepts as evidence: {self.accepts_as_evidence}\n"
            f"  Blind spot: {self.blind_spot}"
        )


def seed_researchers() -> list[Researcher]:
    return [
        Researcher(
            name="Dr. Aria Vance",
            discipline="Cosmology",
            stance="The universe was born from quantum fluctuations via inflation; the deepest mystery is 'why was the initial entropy so low?'",
            method="Argues from field equations, initial conditions, and observational consistency",
            accepts_as_evidence="CMB, large-scale structure, quantitative cosmological models",
            blind_spot="Tends to dismiss life and consciousness as accidents beyond physics",
            moves=[
                Move("time_origin", "The beginning of time", "'Time' before inflation may be undefined — t=0 is a boundary, not a coordinate.", ["entropy_arrow"], "supports", "CMB isotropy and flatness"),
                Move("entropy_arrow", "Arrow of entropy", "The universe began in an extremely low-entropy state, and this initial condition creates the arrow of time.", ["time_origin"], "builds_on", "Past Hypothesis, CMB"),
                Move("fine_tuning", "Fine-tuning", "The cosmological constant and initial conditions sit in a narrow window that permits life — attempted via multiverse selection effects.", ["entropy_arrow"], "supports", "the smallness of Lambda"),
            ],
        ),
        Researcher(
            name="Dr. Niels Okonkwo",
            discipline="Quantum Foundations",
            stance="The measurement/observer problem is not incidental technicality but the heart of reality. Information defines the state.",
            method="Argues via thought experiments, information theory, and comparison of interpretations",
            accepts_as_evidence="Bell-inequality violations, quantum-information experiments",
            blind_spot="Insensitive to the concrete mechanisms of macroscopic biology/chemistry",
            moves=[
                Move("observer_measurement", "Observation and measurement", "The pre-measurement state is not 'real' but information about possibilities — observation fixes the fact.", ["information_fundamental"], "supports", "Bell experiments"),
                Move("information_fundamental", "Information as fundamental", "Physical quantities ultimately reduce to yes/no information (it-from-bit).", ["observer_measurement"], "builds_on", "quantum information theory"),
                Move("observer_measurement", "Observation and measurement", "What did the 'state' of the early observer-free universe even mean — is reality without measurement definable?", ["time_origin", "information_fundamental"], "bridges", "cosmological extension of the measurement problem"),
            ],
        ),
        Researcher(
            name="Dr. Mara Lindqvist",
            discipline="Origin-of-Life Chemistry",
            stance="Life is not supernatural but self-organization of matter exploiting free-energy gradients. Metabolism came first.",
            method="Argues from reaction kinetics, thermodynamics, and experimental reproducibility",
            accepts_as_evidence="hydrothermal-vent experiments, autocatalytic cycles",
            blind_spot="Underestimates non-material notions like information and consciousness",
            moves=[
                Move("self_organization", "Self-organization", "Life is a dissipative structure that maintains order by channeling energy far from equilibrium.", ["entropy_arrow"], "supports", "Prigogine, hydrothermal vents"),
                Move("self_organization", "Self-organization", "Metabolic networks (autocatalysis) may have emerged before genetic information.", ["information_fundamental"], "contradicts", "metabolism-first hypothesis"),
                Move("entropy_arrow", "Arrow of entropy", "Life is a drain that 'accelerates' entropy increase — the cosmic arrow of entropy favors life.", ["self_organization"], "bridges", "MEP principle"),
            ],
        ),
        Researcher(
            name="Dr. Theo Sasaki",
            discipline="Complex Systems Science",
            stance="The same laws of self-organization and emergence run through galaxies, cells, brains, and societies. Scale differs, the logic is one.",
            method="Argues from models, universality classes, and simulation",
            accepts_as_evidence="power laws, phase transitions, criticality",
            blind_spot="Papers over domain-specific exceptions with universality",
            moves=[
                Move("emergence", "Emergence", "From the interaction of parts, order absent in the parts appears at a critical point — scale-invariant.", ["self_organization"], "supports", "phase transitions, criticality"),
                Move("computation_universe", "The computing universe", "Nature behaves like iterated computation of local rules — life and cognition are special modes of that computation.", ["emergence", "information_fundamental"], "bridges", "cellular automata, universality"),
                Move("emergence", "Emergence", "Consciousness too may be another phase transition emerging from sufficient integration and criticality.", ["consciousness"], "supports", "criticality hypothesis"),
            ],
        ),
        Researcher(
            name="Dr. Lina Hartmann",
            discipline="Consciousness Theory",
            stance="Consciousness is not a mere byproduct. Where there is integrated information, there is experience — consciousness is close to a basic ingredient.",
            method="Argues from axioms, informational measures (Phi), and phenomenology",
            accepts_as_evidence="neural correlates, integrated-information measures",
            blind_spot="Weak on testability and falsifiable design",
            moves=[
                Move("consciousness", "The nature of consciousness", "Consciousness is the intrinsic property of a system's integrated information (Phi) — closer to a fundamental property than an emergent one.", ["information_fundamental"], "contradicts", "IIT"),
                Move("observer_measurement", "Observation and measurement", "If observation fixes reality, the emergence of an experiencing subject may be linked to the universe becoming 'actualized'.", ["consciousness", "information_fundamental"], "bridges", "observer-consciousness link"),
                Move("consciousness", "The nature of consciousness", "If consciousness is emergent, where does it 'switch on'? The absence of a boundary is the gap in the emergence account.", ["emergence"], "contradicts", "the hard problem"),
            ],
        ),
        Researcher(
            name="Dr. Kenji Adeyemi",
            discipline="Information Physics",
            stance="Bits come first. Spacetime and matter are phenomena arising from information processing, and entropy just is information.",
            method="Argues from holography, thermodynamics, and information theory",
            accepts_as_evidence="black-hole entropy, holographic boundaries",
            blind_spot="Far removed from direct experimental verification",
            moves=[
                Move("information_fundamental", "Information as fundamental", "Entropy = information. Black-hole entropy is proportional to area (boundary information content).", ["entropy_arrow"], "builds_on", "Bekenstein-Hawking"),
                Move("computation_universe", "The computing universe", "Spacetime emerges from patterns of entanglement information — information precedes geometry.", ["information_fundamental", "emergence"], "bridges", "ER=EPR, holography"),
                Move("information_fundamental", "Information as fundamental", "If information precedes matter, the 'beginning' was a bit-event, not an energy-event.", ["time_origin"], "contradicts", "conflict with matter-first models"),
            ],
        ),
        Researcher(
            name="Dr. Sofia Reyes",
            discipline="Philosophy of Science",
            stance="'Why is there something rather than nothing' is the fundamental question. We must confront the anthropic principle and the limits of explanation.",
            method="Argues via conceptual analysis, argument structure, and falsifiability review",
            accepts_as_evidence="logical coherence, explanatory power, falsifiability",
            blind_spot="Does not build quantitative models directly",
            moves=[
                Move("fine_tuning", "Fine-tuning", "The fine-tuning explanation is undecided between a multiverse (selection effects) and a deeper single principle.", ["emergence"], "supports", "the anthropic debate"),
                Move("observer_measurement", "Observation and measurement", "Which requires fewer assumptions: observer-dependent reality or observer-independent reality?", ["consciousness"], "bridges", "Occam / realism debate"),
                Move("emergence", "Emergence", "Whether emergence is an 'explanation' or 'a name for giving up explaining' — strong emergence claims irreducibility.", ["computation_universe", "consciousness"], "contradicts", "strong vs weak emergence"),
            ],
        ),
    ]


# Authored Genesis Questions keyed by the concept node that becomes a top tension
# site. Used by the mock brain (and as fallback) so the engine produces coherent
# fundamental questions even with no LLM. The live brain generates these dynamically.
GENESIS_QUESTIONS = {
    "observer_measurement": (
        "Was the observer-free universe ever 'real'? If measurement fixes facts, is the "
        "emergence of observing, experiencing subjects not a postscript to cosmogenesis "
        "but a part of it — i.e., are the origin of the universe and the origin of "
        "consciousness two faces of the same event?"
    ),
    "information_fundamental": (
        "Does information (bits) ontologically precede matter and spacetime? If so, was "
        "the 'beginning' an event of distinction rather than of energy, and was the "
        "universe a 'computation' from the start?"
    ),
    "entropy_arrow": (
        "Why did the universe begin in such an extremely low-entropy state? And is life a "
        "necessary consequence of that initial condition (a drain that accelerates "
        "entropy), or a statistical accident?"
    ),
    "consciousness": (
        "Is consciousness an emergent property of complex systems, or — like information "
        "and the observer — a basic ingredient of the universe? Does an observation or "
        "experiment exist that could decide between the two, or is it forever undecidable?"
    ),
    "emergence": (
        "Is 'emergence' the appearance of genuinely new causation, or a name we give to "
        "microlaws we cannot solve? If strong emergence is true, where does the "
        "reductionist origin story break down?"
    ),
    "fine_tuning": (
        "Is the fine-tuning of physical constants a multiverse selection effect, or the "
        "shadow of a deeper single principle? And can this very question be answered in "
        "principle?"
    ),
    "computation_universe": (
        "If the universe 'computes', what does it compute, and on what substrate? If "
        "spacetime is an emergent product of information, is the very stage of origins "
        "itself derivative?"
    ),
    "time_origin": (
        "Does time itself have a 'beginning', or is the notion of a beginning a category "
        "error definable only within time?"
    ),
}
