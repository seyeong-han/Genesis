# Demo Researchers — "Do we need a hybrid approach (diffusion + transformers + CNN)?"

> The default 43-discipline roster (`researcher.md`) is built for *origins* questions.
> This question is an **ML-architecture debate**, so we add AI/ML researchers whose
> real papers ground the three architectures in tension: transformers, diffusion, CNNs.
> All fetched from OpenAlex (no key needed) into `data/demo_corpus/`.

## The question
"Do we need the hybrid approach for LLM: diffusion + transformers + CNN?"
→ Is combining architectures necessary, or does one paradigm subsume the others?

## Demo-test set (3 researchers — run the flow with these)

| # | Researcher | Architecture | OpenAlex topic hint | Debate stance |
|---|---|---|---|---|
| 1 | **Ashish Vaswani** | Transformers | "attention is all you need transformer" | Attention is general-purpose; transformers increasingly subsume vision + generation → maybe hybrid is unnecessary |
| 2 | **Yann LeCun** | CNN / energy-based | "convolutional networks gradient-based learning" | Inductive biases (convolution) matter; pure autoregressive LLMs are insufficient → advocates different/hybrid architectures |
| 3 | **Jonathan Ho** | Diffusion | "denoising diffusion probabilistic models" | Diffusion is a distinct generative paradigm; hybridization (diffusion with transformer backbones) is already the frontier |

These three create a genuine three-way collision: **"transformers are enough" vs "we need conv/other inductive biases" vs "diffusion is its own pillar."** Perfect for testing that claims, rebuttals, bridges, and the novelty audit all fire.

## Fuller add-list (for scaling the roster beyond the 3-agent test)

| Researcher | Architecture / contribution | Topic hint |
|---|---|---|
| **Kaiming He** | ResNet — very deep CNNs | "deep residual learning image recognition" |
| **Yoshua Bengio** | Deep learning foundations, attention precursors | "deep learning representation learning" |
| **Yang Song** | Score-based generative models (diffusion theory) | "score-based generative modeling stochastic differential equations" |
| **Geoffrey Hinton** | AlexNet / backprop (already in `data/corpus/`) | "deep convolutional neural networks" |
| **Alec Radford** | GPT / CLIP — multimodal + autoregressive scaling | "language models unsupervised multitask CLIP" |

## How to (re)build this corpus

```bash
cd Genesis
# Fetch the 3 demo researchers into data/demo_corpus/ (keyless OpenAlex)
python backend/scripts/openalex/demo_ingest.py
# Import into a project (isolated 3-researcher corpus)
python backend/scripts/import_openalex_corpus.py --auto --corpus-dir data/demo_corpus
```

Each researcher → one Genesis agent grounded in their real paper abstract (RAG).
sim agents = `claude-sonnet-4-6`, report/synthesis = `claude-opus-4-8`.
