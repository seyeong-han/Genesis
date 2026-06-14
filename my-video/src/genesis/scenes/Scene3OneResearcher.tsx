import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { CENTER, COLORS } from "../constants";
import { bodyFont, ramp, titleFont } from "../components";

// Scene 3 — a single researcher glows inside a circle: powerful, but alone.
export const Scene3OneResearcher: React.FC = () => {
  const frame = useCurrentFrame();
  const appear = ramp(frame, 6, 26);
  const pulse = (Math.sin((frame / 26) * Math.PI) + 1) / 2;
  const ringR = 150;

  return (
    <AbsoluteFill>
      {/* enclosing circle */}
      <div
        style={{
          position: "absolute",
          left: CENTER.x,
          top: CENTER.y - 40,
          transform: "translate(-50%,-50%)",
          width: ringR * 2,
          height: ringR * 2,
          borderRadius: "50%",
          border: `2px solid ${COLORS.cardBorder}`,
          opacity: appear * 0.8,
        }}
      />
      {/* the researcher node */}
      <div
        style={{
          position: "absolute",
          left: CENTER.x,
          top: CENTER.y - 40,
          transform: `translate(-50%,-50%) scale(${interpolate(appear, [0, 1], [0.4, 1])})`,
          opacity: appear,
        }}
      >
        <div
          style={{
            width: 70,
            height: 70,
            borderRadius: "50%",
            background: COLORS.gold,
            boxShadow: `0 0 ${30 + pulse * 40}px ${10 + pulse * 8}px ${COLORS.gold}`,
          }}
        />
      </div>
      {/* orbiting field label */}
      <div
        style={{
          position: "absolute",
          left: CENTER.x,
          top: CENTER.y - 40 - ringR - 28,
          transform: "translateX(-50%)",
          fontFamily: bodyFont,
          fontSize: 26,
          color: COLORS.textDim,
          opacity: appear,
        }}
      >
        Robotics
      </div>

      <div
        style={{
          position: "absolute",
          top: "76%",
          width: "100%",
          textAlign: "center",
          opacity: appear,
        }}
      >
        <div style={{ fontFamily: titleFont, fontSize: 72, fontWeight: 700, color: COLORS.text }}>
          One mind. One field.
        </div>
      </div>
    </AbsoluteFill>
  );
};
