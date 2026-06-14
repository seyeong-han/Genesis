import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { CENTER, COLORS, VIDEO_HEIGHT, VIDEO_WIDTH } from "../constants";
import { Spark, bodyFont, ramp, titleFont } from "../components";

// Scene 1 — two points of light drift in from opposite corners, cross at
// center, and ignite a confluence spark. Sets the motif for the whole film.
export const Scene1Hook: React.FC = () => {
  const frame = useCurrentFrame();

  const travel = interpolate(frame, [10, 95], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const a = {
    x: interpolate(travel, [0, 1], [120, CENTER.x]),
    y: interpolate(travel, [0, 1], [120, CENTER.y]),
  };
  const b = {
    x: interpolate(travel, [0, 1], [VIDEO_WIDTH - 120, CENTER.x]),
    y: interpolate(travel, [0, 1], [VIDEO_HEIGHT - 120, CENTER.y]),
  };

  const sparkProgress = interpolate(frame, [95, 165], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const textAppear = ramp(frame, 120, 30);

  return (
    <AbsoluteFill>
      {[a, b].map((p, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: p.x,
            top: p.y,
            transform: "translate(-50%, -50%)",
            width: 22,
            height: 22,
            borderRadius: "50%",
            background: i === 0 ? COLORS.blue : COLORS.purple,
            boxShadow: `0 0 50px 14px ${i === 0 ? COLORS.blue : COLORS.purple}`,
            opacity: 1 - sparkProgress * 0.5,
          }}
        />
      ))}

      {sparkProgress > 0 && (
        <Spark x={CENTER.x} y={CENTER.y} progress={sparkProgress} maxRadius={200} />
      )}

      <div
        style={{
          position: "absolute",
          top: "62%",
          width: "100%",
          textAlign: "center",
          opacity: textAppear,
          transform: `translateY(${interpolate(textAppear, [0, 1], [20, 0])}px)`,
          padding: "0 80px",
        }}
      >
        <div
          style={{
            fontFamily: bodyFont,
            fontSize: 40,
            color: COLORS.textDim,
            fontWeight: 400,
          }}
        >
          The best ideas come from
        </div>
        <div
          style={{
            fontFamily: titleFont,
            fontSize: 84,
            fontWeight: 800,
            color: COLORS.text,
            marginTop: 8,
            letterSpacing: -1,
          }}
        >
          a different field.
        </div>
      </div>
    </AbsoluteFill>
  );
};
