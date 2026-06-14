import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { loadFont as loadMontserrat } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";
import { COLORS } from "./constants";
import type { GraphNode } from "./graph";
import { nodeById } from "./graph";

export const titleFont = loadMontserrat("normal", {
  weights: ["600", "700", "800"],
  subsets: ["latin"],
}).fontFamily;

export const bodyFont = loadInter("normal", {
  weights: ["400", "500", "600"],
  subsets: ["latin"],
}).fontFamily;

const EASE = Easing.bezier(0.16, 1, 0.3, 1);

/** Smooth 0→1 ramp over [start, start+len] frames. */
export const ramp = (frame: number, start: number, len: number): number =>
  interpolate(frame, [start, start + len], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: EASE,
  });

/** Background gradient + faint vignette, shared by every scene. */
export const Backdrop: React.FC = () => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(circle at 50% 42%, ${COLORS.bg1} 0%, ${COLORS.bg0} 70%)`,
    }}
  />
);

/**
 * Fades a scene's content in at the head and out at the tail so plain
 * back-to-back <Sequence>s read as soft cuts (no CSS transitions).
 */
export const SceneWrap: React.FC<{
  durationInFrames: number;
  children: React.ReactNode;
  fade?: number;
}> = ({ durationInFrames, children, fade = 14 }) => {
  const frame = useCurrentFrame();
  const opacity =
    interpolate(frame, [0, fade], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }) *
    interpolate(
      frame,
      [durationInFrames - fade, durationInFrames],
      [1, 0],
      { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
    );
  return <AbsoluteFill style={{ opacity }}>{children}</AbsoluteFill>;
};

/** A glowing graph node dot with an optional label. */
export const NodeDot: React.FC<{
  node: GraphNode;
  appear: number; // 0→1
  glow?: number; // 0→1 extra glow
  radius?: number;
  showLabel?: boolean;
  labelBelow?: boolean;
}> = ({ node, appear, glow = 0, radius = 13, showLabel = true, labelBelow }) => {
  const scale = interpolate(appear, [0, 1], [0.2, 1]);
  const glowSize = 18 + glow * 40;
  return (
    <>
      <div
        style={{
          position: "absolute",
          left: node.x,
          top: node.y,
          transform: `translate(-50%, -50%) scale(${scale})`,
          opacity: appear,
        }}
      >
        <div
          style={{
            width: radius * 2,
            height: radius * 2,
            borderRadius: "50%",
            background: node.color,
            boxShadow: `0 0 ${glowSize}px ${Math.round(
              4 + glow * 10,
            )}px ${node.color}`,
          }}
        />
      </div>
      {showLabel && (
        <div
          style={{
            position: "absolute",
            left: node.x,
            top: node.y + (labelBelow ? radius + 16 : -(radius + 30)),
            transform: "translateX(-50%)",
            opacity: appear,
            color: COLORS.text,
            fontFamily: bodyFont,
            fontSize: 22,
            fontWeight: 500,
            whiteSpace: "nowrap",
            textShadow: "0 2px 10px rgba(0,0,0,0.6)",
          }}
        >
          {node.label}
        </div>
      )}
    </>
  );
};

/** An SVG edge that "draws" from a→b as progress 0→1, optionally hot (gold). */
export const Edge: React.FC<{
  from: string;
  to: string;
  progress: number; // 0→1
  hot?: boolean;
  width?: number;
}> = ({ from, to, progress, hot = false, width = 2 }) => {
  const a = nodeById(from);
  const b = nodeById(to);
  const x2 = a.x + (b.x - a.x) * progress;
  const y2 = a.y + (b.y - a.y) * progress;
  return (
    <line
      x1={a.x}
      y1={a.y}
      x2={x2}
      y2={y2}
      stroke={hot ? COLORS.edgeHot : COLORS.edge}
      strokeWidth={hot ? width + 1.5 : width}
      strokeLinecap="round"
      style={hot ? { filter: "drop-shadow(0 0 6px rgba(255,206,92,0.8))" } : undefined}
    />
  );
};

/** A radial burst used for the recurring "confluence spark" motif. */
export const Spark: React.FC<{
  x: number;
  y: number;
  progress: number; // 0→1 life of the burst
  color?: string;
  maxRadius?: number;
}> = ({ x, y, progress, color = COLORS.gold, maxRadius = 120 }) => {
  const r = interpolate(progress, [0, 1], [0, maxRadius]);
  const opacity = interpolate(progress, [0, 0.25, 1], [0, 0.9, 0]);
  const core = interpolate(progress, [0, 0.3, 1], [0, 1, 0.6]);
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: "translate(-50%, -50%)",
      }}
    >
      <div
        style={{
          position: "absolute",
          left: -r,
          top: -r,
          width: r * 2,
          height: r * 2,
          borderRadius: "50%",
          border: `2px solid ${color}`,
          opacity,
        }}
      />
      <div
        style={{
          position: "absolute",
          left: -16,
          top: -16,
          width: 32,
          height: 32,
          borderRadius: "50%",
          background: color,
          opacity: core,
          boxShadow: `0 0 40px 12px ${color}`,
        }}
      />
    </div>
  );
};

/** Centered caption block with title + optional subtitle. */
export const CaptionBlock: React.FC<{
  appear: number;
  children: React.ReactNode;
  y?: string;
}> = ({ appear, children, y = "50%" }) => {
  const translateY = interpolate(appear, [0, 1], [24, 0]);
  return (
    <div
      style={{
        position: "absolute",
        top: y,
        left: 0,
        width: "100%",
        textAlign: "center",
        transform: `translateY(${translateY - 50}%)`,
        opacity: appear,
        padding: "0 80px",
      }}
    >
      {children}
    </div>
  );
};

/** Small rounded chip / pill. */
export const Chip: React.FC<{
  children: React.ReactNode;
  color?: string;
  appear?: number;
}> = ({ children, color = COLORS.blue, appear = 1 }) => (
  <span
    style={{
      display: "inline-block",
      padding: "8px 18px",
      margin: 6,
      borderRadius: 999,
      border: `1.5px solid ${color}`,
      color: COLORS.text,
      background: "rgba(110,168,255,0.08)",
      fontFamily: bodyFont,
      fontSize: 22,
      fontWeight: 500,
      opacity: appear,
    }}
  >
    {children}
  </span>
);

/** Spring helper for pop-in scales. */
export const usePop = (delay: number, config?: Parameters<typeof spring>[0]["config"]) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({
    frame: frame - delay,
    fps,
    config: { damping: 16, mass: 0.8, ...config },
  });
};
