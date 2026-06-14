import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { COLORS, VIDEO_HEIGHT, VIDEO_WIDTH } from "../constants";
import {
  BRIDGE_EDGES,
  CENTER_NODE,
  RING_NODES,
  SPOKE_EDGES,
  WEB_EDGES,
  nodeById,
} from "../graph";
import { Edge, NodeDot, Spark, ramp, titleFont } from "../components";

const BRIDGE_START = [24, 104, 184];

// Scene 5 — distant nodes fire beams at each other; new "bridge" nodes bloom at
// the midpoints (callback to Scene 1's spark).
export const Scene5Bridges: React.FC = () => {
  const frame = useCurrentFrame();
  const titleAppear = ramp(frame, 4, 22);

  return (
    <AbsoluteFill>
      <svg width={VIDEO_WIDTH} height={VIDEO_HEIGHT} style={{ position: "absolute", inset: 0 }}>
        {/* dimmed existing web */}
        {SPOKE_EDGES.map(([a, b], i) => (
          <Edge key={`s${i}`} from={a} to={b} progress={0.35} width={1} />
        ))}
        {WEB_EDGES.map(([a, b], i) => (
          <Edge key={`w${i}`} from={a} to={b} progress={1} width={1.2} />
        ))}
        {/* igniting bridges */}
        {BRIDGE_EDGES.map(([a, b], i) => {
          const p = ramp(frame, BRIDGE_START[i], 34);
          return <Edge key={`b${i}`} from={a} to={b} progress={p} hot width={3} />;
        })}
      </svg>

      <NodeDot node={CENTER_NODE} appear={1} glow={0.3} radius={18} showLabel={false} />
      {RING_NODES.map((n) => {
        const inBridge = BRIDGE_EDGES.some(([a, b]) => a === n.id || b === n.id);
        return <NodeDot key={n.id} node={n} appear={1} glow={inBridge ? 0.5 : 0} labelBelow={n.y > CENTER_NODE.y} />;
      })}

      {/* spark blooms at each bridge midpoint */}
      {BRIDGE_EDGES.map(([a, b], i) => {
        const na = nodeById(a);
        const nb = nodeById(b);
        const sparkP = interpolate(frame, [BRIDGE_START[i] + 30, BRIDGE_START[i] + 90], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        if (sparkP <= 0) return null;
        return (
          <Spark
            key={`sp${i}`}
            x={(na.x + nb.x) / 2}
            y={(na.y + nb.y) / 2}
            progress={sparkP}
            maxRadius={90}
          />
        );
      })}

      <div style={{ position: "absolute", bottom: 70, width: "100%", textAlign: "center", opacity: titleAppear }}>
        <div style={{ fontFamily: titleFont, fontSize: 54, fontWeight: 700, color: COLORS.text }}>
          Breakthroughs are born at the <span style={{ color: COLORS.gold }}>bridges.</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
