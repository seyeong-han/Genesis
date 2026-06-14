import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { COLORS, VIDEO_HEIGHT, VIDEO_WIDTH } from "../constants";
import { DEBATE_RESEARCHERS } from "../graph";
import { bodyFont, ramp, titleFont } from "../components";

const POS = [
  { x: 540, y: 380, cardDX: 0, cardDY: -158 },
  { x: 300, y: 650, cardDX: -10, cardDY: 150 },
  { x: 780, y: 650, cardDX: 10, cardDY: 150 },
];

const BEATS = [
  { t: 0, text: "Each agent = one real researcher, grounded in their papers (RAG)" },
  { t: 140, text: "Claim · Rebuttal · Bridge" },
  { t: 270, text: "Every claim becomes an edge in a shared knowledge graph (Zep)" },
];

const initials = (name: string) =>
  name.split(" ").map((p) => p[0]).join("").slice(0, 2).toUpperCase();

export const Scene7Debate: React.FC = () => {
  const frame = useCurrentFrame();
  const beat = [...BEATS].reverse().find((b) => frame >= b.t) ?? BEATS[0];
  const beatAppear = ramp(frame - beat.t, 0, 18);

  const edgeDraw = ramp(frame, 50, 60);
  const titleAppear = ramp(frame, 4, 20);

  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", top: 44, width: "100%", textAlign: "center", opacity: titleAppear }}>
        <div style={{ fontFamily: titleFont, fontSize: 42, fontWeight: 700, color: COLORS.text }}>
          A grounded debate over real papers
        </div>
      </div>

      {/* edges among the three researchers */}
      <svg width={VIDEO_WIDTH} height={VIDEO_HEIGHT} style={{ position: "absolute", inset: 0 }}>
        {[
          [0, 1],
          [1, 2],
          [2, 0],
        ].map(([a, b], i) => {
          const pa = POS[a];
          const pb = POS[b];
          const x2 = pa.x + (pb.x - pa.x) * edgeDraw;
          const y2 = pa.y + (pb.y - pa.y) * edgeDraw;
          return (
            <line key={i} x1={pa.x} y1={pa.y} x2={x2} y2={y2} stroke={COLORS.edge} strokeWidth={2} strokeLinecap="round" />
          );
        })}
      </svg>

      {DEBATE_RESEARCHERS.map((r, i) => {
        const p = POS[i];
        const appear = ramp(frame, 14 + i * 16, 22);
        const cardAppear = ramp(frame, 90 + i * 40, 26);
        return (
          <React.Fragment key={r.name}>
            {/* avatar */}
            <div
              style={{
                position: "absolute",
                left: p.x,
                top: p.y,
                transform: `translate(-50%,-50%) scale(${interpolate(appear, [0, 1], [0.4, 1])})`,
                opacity: appear,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
              <div
                style={{
                  width: 84,
                  height: 84,
                  borderRadius: "50%",
                  background: "rgba(16,21,46,0.95)",
                  border: `3px solid ${r.color}`,
                  boxShadow: `0 0 26px ${r.color}`,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontFamily: titleFont,
                  fontSize: 32,
                  fontWeight: 700,
                  color: r.color,
                }}
              >
                {initials(r.name)}
              </div>
              <div style={{ fontFamily: bodyFont, fontSize: 24, color: COLORS.text, marginTop: 10, fontWeight: 600 }}>
                {r.name}
              </div>
              <div style={{ fontFamily: bodyFont, fontSize: 19, color: COLORS.textDim }}>{r.field}</div>
            </div>

            {/* claim card */}
            <div
              style={{
                position: "absolute",
                left: p.x + p.cardDX,
                top: p.y + p.cardDY,
                transform: "translate(-50%,-50%)",
                width: 360,
                background: COLORS.cardBg,
                border: `1.5px solid ${r.color}`,
                borderRadius: 14,
                padding: "16px 18px",
                opacity: cardAppear,
                boxShadow: "0 8px 30px rgba(0,0,0,0.5)",
              }}
            >
              <div style={{ fontFamily: bodyFont, fontSize: 21, color: COLORS.text, lineHeight: 1.35 }}>
                {r.claim}
              </div>
              <div
                style={{
                  fontFamily: bodyFont,
                  fontSize: 16,
                  color: COLORS.gold,
                  marginTop: 10,
                  letterSpacing: 0.4,
                }}
              >
                DOI {r.doi}
              </div>
            </div>
          </React.Fragment>
        );
      })}

      <div style={{ position: "absolute", bottom: 64, width: "100%", textAlign: "center", padding: "0 90px", opacity: beatAppear }}>
        <div style={{ fontFamily: bodyFont, fontSize: 30, color: COLORS.textDim }}>{beat.text}</div>
      </div>
    </AbsoluteFill>
  );
};
