import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { COLORS, VIDEO_HEIGHT, VIDEO_WIDTH } from "../constants";
import { CENTER_NODE, RING_NODES, SPOKE_EDGES, WEB_EDGES } from "../graph";
import { Chip, Edge, NodeDot, bodyFont, ramp, titleFont } from "../components";

const QUESTION = "Do we need a hybrid LLM: diffusion + transformers + CNN?";

// Scene 6 — the brand moment. Logo locks in over a faint graph; a question is
// typed and "submitted", lighting up the 43-discipline roster.
export const Scene6Genesis: React.FC = () => {
  const frame = useCurrentFrame();

  const logoAppear = ramp(frame, 6, 26);
  const subAppear = ramp(frame, 26, 24);

  const typeStart = 60;
  const chars = Math.max(0, Math.floor((frame - typeStart) * 1.5));
  const typed = QUESTION.slice(0, chars);
  const caret = Math.floor(frame / 8) % 2 === 0;
  const submitted = frame >= 180;
  const pulse = submitted ? (Math.sin(((frame - 180) / 14) * Math.PI) + 1) / 2 : 0;

  const chipAppear = (i: number) => ramp(frame, 200 + i * 14, 20);

  return (
    <AbsoluteFill>
      {/* faint background graph */}
      <div style={{ opacity: 0.22 }}>
        <svg width={VIDEO_WIDTH} height={VIDEO_HEIGHT} style={{ position: "absolute", inset: 0 }}>
          {SPOKE_EDGES.map(([a, b], i) => (
            <Edge key={`s${i}`} from={a} to={b} progress={1} width={1} />
          ))}
          {WEB_EDGES.map(([a, b], i) => (
            <Edge key={`w${i}`} from={a} to={b} progress={1} width={1} />
          ))}
        </svg>
        {RING_NODES.map((n) => (
          <NodeDot key={n.id} node={n} appear={1} glow={pulse * 0.6} radius={10} showLabel={false} />
        ))}
        <NodeDot node={CENTER_NODE} appear={1} radius={12} showLabel={false} />
      </div>

      {/* brand */}
      <div style={{ position: "absolute", top: "26%", width: "100%", textAlign: "center" }}>
        <div
          style={{
            fontFamily: titleFont,
            fontSize: 128,
            fontWeight: 800,
            letterSpacing: 6,
            color: COLORS.text,
            opacity: logoAppear,
            transform: `translateY(${interpolate(logoAppear, [0, 1], [24, 0])}px)`,
            textShadow: `0 0 50px rgba(255,206,92,0.35)`,
          }}
        >
          GENESIS
        </div>
        <div style={{ fontFamily: bodyFont, fontSize: 32, color: COLORS.textDim, opacity: subAppear }}>
          Cross-disciplinary research debate engine
        </div>
      </div>

      {/* search bar */}
      <div
        style={{
          position: "absolute",
          top: "52%",
          left: "50%",
          transform: "translateX(-50%)",
          width: 820,
          minHeight: 76,
          borderRadius: 18,
          border: `1.5px solid ${submitted ? COLORS.gold : COLORS.cardBorder}`,
          background: COLORS.cardBg,
          display: "flex",
          alignItems: "center",
          padding: "0 28px",
          opacity: ramp(frame, 50, 20),
          boxShadow: submitted ? `0 0 30px rgba(255,206,92,0.3)` : "none",
        }}
      >
        <span style={{ color: COLORS.textDim, fontSize: 30, marginRight: 16 }}>⌕</span>
        <span style={{ fontFamily: bodyFont, fontSize: 30, color: COLORS.text }}>
          {typed}
          {!submitted && caret ? <span style={{ color: COLORS.gold }}>|</span> : null}
        </span>
      </div>

      {/* roster chips */}
      <div style={{ position: "absolute", top: "66%", width: "100%", textAlign: "center", padding: "0 80px" }}>
        <Chip color={COLORS.gold} appear={chipAppear(0)}>
          43 disciplines
        </Chip>
        <Chip color={COLORS.blue} appear={chipAppear(1)}>
          real researchers
        </Chip>
        <Chip color={COLORS.purple} appear={chipAppear(2)}>
          real papers
        </Chip>
      </div>
    </AbsoluteFill>
  );
};
