import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { COLORS } from "../constants";
import { bodyFont, ramp, titleFont } from "../components";

const BEATS: { t: number; title: string; note?: string }[] = [
  { t: 0, title: "Controlling many drones at once", note: "Ringelmann effect: more agents, less efficiency" },
  { t: 100, title: "Biology  →  Robotics" },
  { t: 200, title: "Weaver ants · the \u201cForce Ratchet\u201d" },
  { t: 300, title: "Hundreds of robots self-organize", note: "no central controller" },
];

// deterministic scattered start positions for the drone swarm
const SCATTER = Array.from({ length: 16 }, (_, i) => {
  const seed = Math.sin(i * 12.9898) * 43758.5453;
  const f = seed - Math.floor(seed);
  const seed2 = Math.sin(i * 78.233) * 12543.123;
  const g = seed2 - Math.floor(seed2);
  return { dx: (f - 0.5) * 280, dy: (g - 0.5) * 280 };
});

export const Scene2Example: React.FC = () => {
  const frame = useCurrentFrame();
  const beat = [...BEATS].reverse().find((b) => frame >= b.t) ?? BEATS[0];
  const beatLocal = frame - beat.t;
  const beatAppear = ramp(beatLocal, 0, 18);

  const pull = (Math.sin((frame / 12) * Math.PI) + 1) / 2; // ant pulling oscillation
  const assemble = interpolate(frame, [60, 360], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const cxL = 300;
  const cxR = 780;
  const cy = 380;

  return (
    <AbsoluteFill>
      {/* center divider arrow Biology → Robotics */}
      <div
        style={{
          position: "absolute",
          left: 0,
          top: cy,
          width: "100%",
          textAlign: "center",
          color: COLORS.textDim,
          fontFamily: bodyFont,
          fontSize: 26,
          letterSpacing: 2,
          transform: "translateY(-50%)",
        }}
      >
        ⟶
      </div>

      {/* LEFT: weaver ants + leaf + force ratchet */}
      <div style={{ position: "absolute", left: cxL, top: cy, transform: "translate(-50%,-50%)" }}>
        <div
          style={{
            width: 180,
            height: 110,
            borderRadius: "60% 60% 60% 60% / 80% 80% 40% 40%",
            background: "rgba(110,168,255,0.18)",
            border: `2px solid ${COLORS.blue}`,
            transform: `translateX(${-pull * 14}px) rotate(-12deg)`,
          }}
        />
        {[0, 1, 2, 3].map((i) => (
          <div key={i} style={{ position: "absolute", left: 90 + i * 18, top: -10 + i * 22 }}>
            <div style={{ width: 14, height: 14, borderRadius: "50%", background: COLORS.gold, boxShadow: `0 0 12px ${COLORS.gold}` }} />
            <div
              style={{
                position: "absolute",
                left: 14,
                top: 5,
                width: 26 + pull * 14,
                height: 3,
                background: COLORS.goldHot,
                opacity: 0.8,
              }}
            />
          </div>
        ))}
      </div>

      {/* RIGHT: drone swarm assembling into a 4x4 lattice */}
      <div style={{ position: "absolute", left: cxR, top: cy, transform: "translate(-50%,-50%)" }}>
        {SCATTER.map((s, i) => {
          const gx = (i % 4) * 60 - 90;
          const gy = Math.floor(i / 4) * 60 - 90;
          const x = interpolate(assemble, [0, 1], [s.dx, gx]);
          const y = interpolate(assemble, [0, 1], [s.dy, gy]);
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: x,
                top: y,
                width: 16,
                height: 16,
                borderRadius: 4,
                background: COLORS.purple,
                boxShadow: `0 0 ${6 + assemble * 10}px ${COLORS.purple}`,
              }}
            />
          );
        })}
      </div>

      {/* caption beats */}
      <div
        style={{
          position: "absolute",
          bottom: 170,
          width: "100%",
          textAlign: "center",
          padding: "0 90px",
          opacity: beatAppear,
          transform: `translateY(${interpolate(beatAppear, [0, 1], [16, 0])}px)`,
        }}
      >
        <div style={{ fontFamily: titleFont, fontSize: 58, fontWeight: 700, color: COLORS.text }}>
          {beat.title}
        </div>
        {beat.note && (
          <div style={{ fontFamily: bodyFont, fontSize: 30, color: COLORS.textDim, marginTop: 14 }}>
            {beat.note}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
