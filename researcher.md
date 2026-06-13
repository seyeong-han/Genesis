# Researcher Roster — Real OpenAlex Agents (Demo)

> Generated from live OpenAlex data by `ingest.py` + `gen_roster_md.py`. Every
> researcher, paper, year, and citation count below is real and fetched from
> OpenAlex (no API key needed). Each becomes one Genesis Engine agent grounded
> in that paper's abstract (RAG). Demo scope: **one researcher + one paper per
> discipline**; scale up with `ingest.py --papers N` and a larger seed list.

## How this roster was built

1. **Seed** — one origin-relevant modern researcher per discipline (`genesis/seeds.py`).
   We seed by researcher (not by raw concept-citation) because OpenAlex's top-cited
   work *inside a concept* is usually a methods/tooling paper or a name collision
   (e.g. the "Architecture" concept's top paper is a neural-network paper).
2. **Verify + fetch** — resolve each name to a real OpenAlex author (name-matched,
   not just most-cited, to avoid collisions), then pull their top-cited paper that
   has an abstract, steered by a topic hint toward their origin-relevant work.
3. **Ground** — cache the paper's abstract to `data/corpus/<discipline>.json` for RAG.

- Disciplines populated: **43/43**
- Papers with abstract (RAG-ready): **43/43**
- Demo agents prepared: **43** (1 per discipline)

---

## Formal Sciences

| Discipline | Researcher | Institution | Top paper (OpenAlex, cited-by) | Link | Origin lens |
|---|---|---|---|---|---|
| Mathematics & Logic | **Gregory J. Chaitin** | Universidade Federal do Rio de Janeiro | A Theory of Program Size Formally Identical to Information Theory (1975) — 884 cites | [DOI](https://doi.org/10.1145/321892.321894) | irreducible randomness and the limits of formal systems |
| Theory of Computation | **Stephen Wolfram** | — | A New Kind of Science (2003) — 234 cites | [DOI](https://doi.org/10.1115/1.1553433) | is physics itself a computation |
| Information Theory | **E. T. Jaynes** | — | Information Theory and Statistical Mechanics (1957) — 12,912 cites | [DOI](https://doi.org/10.1103/physrev.106.620) | inference and entropy as the bridge between information and physics |
| Statistics & Probability | **Judea Pearl** | University of California, Los Angeles | Causal inference in statistics: An overview (2009) — 2,321 cites | [DOI](https://doi.org/10.1214/09-ss057) | causation beneath correlation |

## Physical Sciences

| Discipline | Researcher | Institution | Top paper (OpenAlex, cited-by) | Link | Origin lens |
|---|---|---|---|---|---|
| Cosmology | **Roger Penrose** | University of Oxford | The Nature of Space and Time (1996) — 348 cites | [DOI](https://doi.org/10.1038/scientificamerican0796-60) | why the universe began in such a low-entropy state |
| Quantum Foundations | **Anton Zeilinger** | Institute for Quantum Optics and Quantum Information Innsbruck | New High-Intensity Source of Polarization-Entangled Photon Pairs (1995) — 3,118 cites | [DOI](https://doi.org/10.1103/physrevlett.75.4337) | the role of observation and information in reality |
| Particle Physics & Unification | **Steven Weinberg** | University of North Carolina at Chapel Hill | A Model of Leptons (1967) — 7,277 cites | [DOI](https://doi.org/10.1103/physrevlett.19.1264) | the search for a single underlying law |
| Thermodynamics & Statistical Mechanics | **Jeremy L. England** | Bar-Ilan University | Self-Organized Resonance during Search of a Diverse Chemical Space (2017) — 52 cites | [DOI](https://doi.org/10.1103/physrevlett.119.038001) | life as a thermodynamically favored structure |
| Astrophysics & Planetary Science | **Sara Seager** | American Institute of Aeronautics and Astronautics | Exoplanet Atmospheres (2010) — 432 cites | [DOI](https://doi.org/10.1146/annurev-astro-081309-130837) | detecting life across cosmic distance |
| Origin-of-Life Chemistry | **Jack W. Szostak** | Howard Hughes Medical Institute | The Emergence of Competition Between Model Protocells (2004) — 451 cites | [DOI](https://doi.org/10.1126/science.1100757) | from chemistry to self-replication |
| Earth System & Geoscience | **Timothy M. Lenton** | University of Exeter | Planetary Boundaries: Exploring the Safe Operating Space for Humanity (2009) — 7,002 cites | [DOI](https://doi.org/10.5751/es-03180-140232) | life and planet as one self-regulating system |

## Life Sciences

| Discipline | Researcher | Institution | Top paper (OpenAlex, cited-by) | Link | Origin lens |
|---|---|---|---|---|---|
| Evolutionary Biology | **Stuart Kauffman** | — | The Origins of Order (1993) — 2,741 cites | [DOI](https://doi.org/10.1093/oso/9780195079517.001.0001) | spontaneous order that precedes natural selection |
| Molecular Biology & Genetics | **Svante Pääbo** | Okinawa Institute of Science and Technology Graduate University | Genetic history of an archaic hominin group from Denisova Cave in Siberia (2010) — 2,023 cites | [DOI](https://doi.org/10.1038/nature09710) | the genetic record of where we came from |
| Neuroscience | **Karl Friston** | Wellcome Centre for Human Neuroimaging | A theory of cortical responses (2005) — 4,759 cites | [DOI](https://doi.org/10.1098/rstb.2005.1622) | the brain as a self-organizing prediction engine |
| Ecology & Systems Biology | **Simon A. Levin** | Princeton University | Are We Consuming Too Much? (2004) — 831 cites | [DOI](https://doi.org/10.1257/0895330042162377) | emergent order across biological scales |
| Astrobiology | **Steven A. Benner** | Firebird Biomolecular Sciences (United States) | Setting the Stage: The History, Chemistry, and Geobiology behind RNA (2010) — 66 cites | [DOI](https://doi.org/10.1101/cshperspect.a003541) | life not as we know it |

## Cognitive & Interdisciplinary

| Discipline | Researcher | Institution | Top paper (OpenAlex, cited-by) | Link | Origin lens |
|---|---|---|---|---|---|
| Cognitive Science | **Joshua B. Tenenbaum** | Institute of Cognitive and Brain Sciences | Causal Inference in Multisensory Perception (2007) — 1,133 cites | [DOI](https://doi.org/10.1371/journal.pone.0000943) | how minds build models of the world |
| Artificial Intelligence | **Geoffrey E. Hinton** | — | ImageNet classification with deep convolutional neural networks (2017) — 75,705 cites | [DOI](https://doi.org/10.1145/3065386) | meaning emerging from statistics |
| Consciousness Studies | **Giulio Tononi** | Netherlands Institute for Neuroscience | An information integration theory of consciousness (2004) — 1,684 cites | [DOI](https://doi.org/10.1186/1471-2202-5-42) | consciousness as intrinsic, integrated information |
| Complex Systems & Self-Organization | **Per Bak** | — | Self-organized criticality: An explanation of the 1/<i>f</i>noise (1987) — 7,636 cites | [DOI](https://doi.org/10.1103/physrevlett.59.381) | complexity poised at the critical edge |
| Network Science | **Albert-Ĺaszló Barabási** | Brigham and Women's Hospital | Emergence of Scaling in Random Networks (1999) — 36,324 cites | [DOI](https://doi.org/10.1126/science.286.5439.509) | why hub structure emerges everywhere |
| Semiotics | **Umberto Eco** | — | On the ontology of fictional characters: A semiotic approach (2009) — 38 cites | [DOI](https://doi.org/10.12697/sss.2009.37.1-2.04) | how anything comes to mean |

## Social Sciences

| Discipline | Researcher | Institution | Top paper (OpenAlex, cited-by) | Link | Origin lens |
|---|---|---|---|---|---|
| Psychology | **Daniel Kahneman** | Princeton University | MAPS OF BOUNDED RATIONALITY: A PERSPECTIVE ON INTUITIVE JUDGMENT AND CHOICE (2003) — 867 cites | — | the architecture of human judgment |
| Depth Psychology & Psychoanalysis | **Mark Solms** | University of Cape Town | The Conscious Id (2013) — 271 cites | [DOI](https://doi.org/10.1080/15294145.2013.10773711) | the hidden, affective roots of the self |
| Anthropology | **Joseph Henrich** | Evolutionary Genomics (United States) | “Economic man” in cross-cultural perspective: Behavioral experiments in 15 small-scale societies (2005) — 1,923 cites | [DOI](https://doi.org/10.1017/s0140525x05000142) | how culture made our species |
| Archaeology & Paleoanthropology | **Ian Hodder** | Koç University | Variable kinship patterns in Neolithic Anatolia revealed by ancient genomes (2021) — 114 cites | [DOI](https://doi.org/10.1016/j.cub.2021.03.050) | the birth of symbolic culture |
| Linguistics | **Noam Chomsky** | Massachusetts Institute of Technology | The mystery of language evolution (2014) — 331 cites | [DOI](https://doi.org/10.3389/fpsyg.2014.00401) | an innate origin of language |
| Sociology | **Niklas Luhmann** | World Health Organization - Pakistan | Die Gesellschaft der Gesellschaft (2000) — 1,525 cites | [DOI](https://doi.org/10.2307/407978) | society as self-producing communication |
| Economics & Game Theory | **Robert Axelrod** | University of Michigan | The Complexity of Cooperation: Agent-Based Models of Competition and Collaboration (1997) — 1,732 cites | [DOI](https://doi.org/10.1515/9781400822300) | the origin of cooperation |
| Political Science | **Peter Turchin** | University of Oxford | Quantitative historical analysis uncovers a single dimension of complexity that structures global variation in human social organization (2017) — 282 cites | [DOI](https://doi.org/10.1073/pnas.1708800115) | laws behind the rise and fall of societies |

## Humanities

| Discipline | Researcher | Institution | Top paper (OpenAlex, cited-by) | Link | Origin lens |
|---|---|---|---|---|---|
| Metaphysics & Ontology | **Tim Maudlin** | — | The Metaphysics Within Physics (2007) — 1,280 cites | [DOI](https://doi.org/10.1093/acprof:oso/9780199218219.001.0001) | what physics implies about what exists |
| Epistemology | **Alvin I. Goldman** | — | Epistemology and Cognition. (1989) — 1,280 cites | [DOI](https://doi.org/10.2307/2185025) | what it is to know |
| Philosophy of Mind | **David J. Chalmers** | New York University | Facing Up to the Problem of Consciousness (1996) — 1,425 cites | [DOI](https://doi.org/10.7551/mitpress/6860.003.0003) | why there is subjective experience at all |
| Philosophy of Science | **Nancy Cartwright** | Durham University | How the Laws of Physics Lie (1983) — 3,011 cites | [DOI](https://doi.org/10.1093/0198247044.001.0001) | whether the laws we write are really true |
| Ethics & Value Theory | **Peter Singer** | Animal Welfare Institute | Ethics and SARS: lessons from Toronto (2003) — 270 cites | [DOI](https://doi.org/10.1136/bmj.327.7427.1342) | the ground and scope of value |
| Religious Studies & Theology | **Ara Norenzayan** | University of British Columbia Hospital | Moralistic gods, supernatural punishment and the expansion of human sociality (2016) — 504 cites | [DOI](https://doi.org/10.1038/nature16980) | the cognitive origin of the sacred |
| History | **Jared M. Diamond** | University of California, Los Angeles | Ecological collapses of past civilizations. (1994) — 33 cites | — | the deep drivers of human history |
| Classics & Mythology | **Michael Witzel** | — | Autochthonous Aryans? The Evidence from Old Indian and Iranian texts (2008) — 70 cites | [DOI](https://doi.org/10.11588/xarep.00000118) | the deep ancestry of origin myths |

## Arts

| Discipline | Researcher | Institution | Top paper (OpenAlex, cited-by) | Link | Origin lens |
|---|---|---|---|---|---|
| Aesthetics | **Semir Zeki** | University College London | Beauty in Architecture: Not a Luxury ‐ Only a Necessity (2019) — 36 cites | [DOI](https://doi.org/10.1002/ad.2473) | the neural basis of beauty |
| Visual Art | **Vilayanur S. Ramachandran** | University of California San Diego | Synaesthesia? A window into perception, thought and language (2001) — 1,593 cites | — | why art moves the brain |
| Music | **Aniruddh D. Patel** | Tufts University | The evolutionary neuroscience of musical beat perception: the Action Simulation for Auditory Prediction (ASAP) hypothesis (2014) — 532 cites | [DOI](https://doi.org/10.3389/fnsys.2014.00057) | music, language, and the mind's origins |
| Architecture & Design | **Christopher Alexander** | Tampere University | A Pattern Language: Towns, Buildings, Construction (1977) — 4,599 cites | — | the nature of order and living structure |
| Literature | **Franco Moretti** | Institute for Advanced Study | Teorie sítí a analýza syžetu (2019) — 1 cites | [DOI](https://doi.org/10.62804/aa.2019.003) | the large-scale shape of literature |

---

## From roster to agents

- Each row -> a `Researcher` agent: persona seeded from the origin lens; corpus =
  the cached abstract(s); the model (sonnet-4.6) argues grounded in that text.
- Reproduce / refresh: `python ingest.py` (re-fetch from OpenAlex) then
  `python gen_roster_md.py` (regenerate this file).
- Scale: raise papers-per-author (`--papers N`) and extend `genesis/seeds.py` to
  5 researchers per discipline to reach the full ~215-agent population.
