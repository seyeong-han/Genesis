import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { COLORS } from "../constants";
import { bodyFont, ramp, titleFont } from "../components";

const BRIEF = [
  "Bridge: force-ratchet coordination (entomology) → decentralized swarm control",
  "Mechanism: local tension sensing replaces a central controller",
  "Next test: scale-free efficiency vs. agent count on a physical swarm",
];

const CONTRIBUTORS = [
  { name: "Ashish Vaswani", weight: 0.42, color: COLORS.blue },
  { name: "Jonathan Ho", weight: 0.34, color: COLORS.gold },
  { name: "Yann LeCun", weight: 0.24, color: COLORS.purple },
];

export const Scene8Verdict: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cardAppear = ramp(frame, 8, 26);
  const briefAppear = (i: number) => ramp(frame, 50 + i * 26, 24);
  const barGrow = (i: number) => ramp(frame, 150 + i * 16, 30);

  const stampSpring = spring({ frame: frame - 250, fps, config: { damping: 10, mass: 0.9 } });
  const stampScale = interpolate(stampSpring, [0, 1], [1.9, 1]);
  const stampRot = interpolate(stampSpring, [0, 1], [-16, -8]);

  const taglineAppear = ramp(frame, 320, 26);

  return (
    <AbsoluteFill>
      {/* report card */}
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: 250,
          transform: `translate(-50%,-50%) translateY(${interpolate(cardAppear, [0, 1], [30, 0])}px)`,
          width: 880,
          background: COLORS.cardBg,
          border: `1.5px solid ${COLORS.cardBorder}`,
          borderRadius: 22,
          padding: "34px 40px",
          opacity: cardAppear,
          boxShadow: "0 20px 60px rgba(0,0,0,0.55)",
        }}
      >
        <div style={{ fontFamily: titleFont, fontSize: 38, fontWeight: 700, color: COLORS.text }}>
          Hypothesis Brief
        </div>
        <div style={{ height: 2, background: COLORS.cardBorder, margin: "16px 0 20px" }} />
        {BRIEF.map((b, i) => (
          <div
            key={i}
            style={{
              display: "flex",
              gap: 12,
              marginBottom: 14,
              opacity: briefAppear(i),
              transform: `translateX(${interpolate(briefAppear(i), [0, 1], [-16, 0])}px)`,
            }}
          >
            <span style={{ color: COLORS.gold, fontSize: 24 }}>▸</span>
            <span style={{ fontFamily: bodyFont, fontSize: 25, color: COLORS.text, lineHeight: 1.35 }}>{b}</span>
          </div>
        ))}
      </div>

      {/* contributor glow bars */}
      <div style={{ position: "absolute", left: "50%", top: 560, transform: "translateX(-50%)", width: 880 }}>
        <div style={{ fontFamily: bodyFont, fontSize: 22, color: COLORS.textDim, marginBottom: 14, letterSpacing: 1 }}>
          CONTRIBUTORS · by influence
        </div>
        {CONTRIBUTORS.map((c, i) => (
          <div key={c.name} style={{ display: "flex", alignItems: "center", marginBottom: 14, opacity: ramp(frame, 150 + i * 16, 20) }}>
            <div style={{ width: 220, fontFamily: bodyFont, fontSize: 23, color: COLORS.text }}>{c.name}</div>
            <div style={{ flex: 1, height: 18, background: "rgba(255,255,255,0.06)", borderRadius: 999, overflow: "hidden" }}>
              <div
                style={{
                  width: `${c.weight * 100 * barGrow(i)}%`,
                  height: "100%",
                  background: c.color,
                  borderRadius: 999,
                  boxShadow: `0 0 16px ${c.color}`,
                }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* NOVEL verdict stamp */}
      {stampSpring > 0.01 && (
        <div
          style={{
            position: "absolute",
            right: 96,
            top: 96,
            transformOrigin: "100% 50%",
            transform: `translateY(-50%) scale(${stampScale}) rotate(${stampRot}deg)`,
            padding: "12px 30px",
            border: `4px solid ${COLORS.novel}`,
            borderRadius: 14,
            color: COLORS.novel,
            fontFamily: titleFont,
            fontSize: 52,
            fontWeight: 800,
            letterSpacing: 3,
            boxShadow: `0 0 40px rgba(92,255,176,0.4)`,
            background: "rgba(10,30,22,0.7)",
          }}
        >
          NOVEL
        </div>
      )}

      {/* closing tagline + CTA */}
      <div style={{ position: "absolute", bottom: 90, width: "100%", textAlign: "center", opacity: taglineAppear }}>
        <div style={{ fontFamily: titleFont, fontSize: 64, fontWeight: 800, color: COLORS.text }}>
          Grounded. Novel. <span style={{ color: COLORS.gold }}>Testable.</span>
        </div>
        <div style={{ fontFamily: bodyFont, fontSize: 28, color: COLORS.textDim, marginTop: 14 }}>
          github.com/seyeong-han/Genesis
        </div>
      </div>
    </AbsoluteFill>
  );
};
