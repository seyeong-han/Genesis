# Genesis — Demo Video Script

> Cross-disciplinary research debate engine. Convene a panel of *real* researchers
> over their *actual* papers, watch them debate your question, and surface novel,
> grounded, testable hypotheses — with DOIs you can verify.
>
> Format: 1080×1080 (square), 30 fps. Target length ≈ 90s (2700 frames).
> Each scene below lists: narration (voiceover), on-screen text, and visual direction.

---

## Scene 1 — The hook (0:00–0:08 · frames 0–240)

**Narration:** "Some of the biggest breakthroughs didn't come from inside a field — they came from somewhere else entirely."

**On-screen text:**
- Line 1: "The best ideas come from"
- Line 2: "**a different field.**"

**Visual:** Dark canvas. A single point of light drifts in from one corner, then a second from the opposite corner. They cross — and where they meet, a brighter spark ignites. Sets the "confluence" motif used throughout.

---

## Scene 2 — A concrete example (0:08–0:22 · frames 240–660)

**Narration:** "In 2026, engineers solved a hard problem in multi-drone control — not with better code, but with biology. Studying how weaver ants haul a leaf, they found a 'force ratchet': while one ant pulls, others anchor and lock the energy in place. The more ants, the *more* efficient the swarm."

**On-screen text (animated captions, one beat at a time):**
- "Problem: controlling many drones at once" → small label "(Ringelmann effect: more agents, less efficiency)"
- "Biology → Robotics"
- "Weaver ants · 'Force Ratchet'"
- "Result: hundreds of robots self-organize — no central controller"

**Visual:** Split screen. LEFT: stylized ants pulling a leaf, tiny force/anchor arrows pulsing. RIGHT: a swarm of drone dots assembling a structure in sync. An arrow labeled "Biology → Robotics" sweeps from left to right. End on the swarm clicking into formation.

---

## Scene 3 — One researcher is strong (0:22–0:30 · frames 660–900)

**Narration:** "One great researcher is powerful…"

**On-screen text:** "One mind. One field."

**Visual:** A single glowing node (a researcher avatar) inside a circle, pulsing gently at center. Their field label orbits them: e.g. "Robotics." It looks impressive but isolated — alone in the dark.

---

## Scene 4 — …but a panel is unstoppable (0:30–0:42 · frames 900–1260)

**Narration:** "…but what happens when researchers from completely different fields sit at the same table and share what they've found?"

**On-screen text:** "Now bring them **together.**"

**Visual:** More nodes fade in around the lone researcher — labeled by discipline: Biology, Philosophy, Entomology, AI, Physics, Neuroscience, Network Science… Edges draw between them one by one until a living knowledge graph fills the frame, gently rotating. Each node carries a tiny avatar + field tag.

---

## Scene 5 — Breakthroughs emerge at the bridges (0:42–0:52 · frames 1260–1560)

**Narration:** "That's where new breakthroughs are born — at the bridges between fields."

**On-screen text:** "Cross-disciplinary bridges → **new discoveries.**"

**Visual:** Two distant nodes in the graph fire a beam toward each other; the edge between them lights up and a brand-new "bridge" node blooms at the midpoint with a burst (callback to Scene 1's spark). A couple more bridges ignite across the graph.

---

## Scene 6 — Introducing Genesis (0:52–1:02 · frames 1560–1860)

**Narration:** "This is Genesis. You ask a question. Genesis searches OpenAlex and convenes real researchers across 43 disciplines — from physics and AI to philosophy and nature — to debate it."

**On-screen text:**
- Title: "**GENESIS**"
- Subtitle: "Cross-disciplinary research debate engine"
- Chip row: "43 disciplines · real researchers · real papers"

**Visual:** The Genesis logo/title locks in over a faint full graph. A search bar types out an example question — e.g. *"Do we need a hybrid LLM: diffusion + transformers + CNN?"* — and on submit, dozens of discipline nodes light up and snap into the roster.

---

## Scene 7 — Grounded debate over real papers (1:02–1:16 · frames 1860–2280)

**Narration:** "Every agent is a real researcher, grounded in their actual papers through RAG. They make claims, push back, and build on each other — and every claim becomes an edge in a shared knowledge graph."

**On-screen text (label beats):**
- "Each agent = one real researcher + their papers (RAG)"
- "Claim · Rebuttal · Bridge"
- "Stored in a temporal knowledge graph (Zep)"

**Visual:** Zoom into three named avatars debating (mirroring the demo set: a Transformers researcher, a CNN researcher, a Diffusion researcher). Speech-bubble snippets fly out as short claim cards, each stamped with a DOI chip. As they fire, matching edges draw into the graph behind them.

---

## Scene 8 — The verdict: grounded, novel, testable (1:16–1:30 · frames 2280–2700)

**Narration:** "Opus synthesizes a hypothesis brief — every claim cited, every contributor tracked. Then a Novelty Audit searches OpenAlex to check if the bridge already exists, and returns a verdict: NOVEL, PARTIAL, or KNOWN — with the nearest papers and DOIs. Genesis doesn't hand you answers. It hands you grounded, novel, testable leads."

**On-screen text:**
- A clean report card slides in:
  - "Hypothesis Brief" (a few bullet lines + DOI chips)
  - Contributor "glow" bar: top researchers by influence
- A stamped verdict badge: "**NOVEL**" (with PARTIAL / KNOWN shown as alternates)
- Closing tagline: "**Grounded. Novel. Testable.**"

**Visual:** The graph collapses into a report panel. Influential nodes glow brighter (provenance/contribution weighting). A verdict badge stamps onto the card. Final frame: Genesis wordmark + tagline, with the full graph softly pulsing behind, and a one-line CTA: "github.com/seyeong-han/Genesis".

---

## Production notes

- **Motif:** carry the "two lights cross → spark" idea from Scene 1 into the bridge nodes (Scene 5) and the verdict stamp (Scene 8) for visual cohesion.
- **Palette:** dark background; cool blues/purples for nodes, warm gold for bridges/sparks and the NOVEL verdict.
- **Typography:** one bold sans for titles, lighter weight for captions. Use Google Fonts via `@remotion/google-fonts`.
- **Animation:** drive everything with `useCurrentFrame()` + `interpolate()` / `spring()`. No CSS transitions or Tailwind animation classes.
- **Audio:** ElevenLabs voiceover per the narration lines (see `rules/voiceover.md`); soft ambient pad underneath; a subtle "chime" on each bridge ignition and on the verdict stamp.
- **Assets:** researcher avatars + discipline labels can come from `data/roster.json` / `researcher.md`; place images in `public/`.
- **Timing is approximate** — adjust scene `durationInFrames` to match the rendered voiceover length.
