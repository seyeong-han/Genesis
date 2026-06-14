import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { COLORS, VIDEO_HEIGHT, VIDEO_WIDTH } from "../constants";
import { CENTER_NODE, RING_NODES, SPOKE_EDGES, WEB_EDGES } from "../graph";
import { Edge, NodeDot, bodyFont, ramp, titleFont } from "../components";

// Scene 4 — discipline nodes bloom around the lone researcher and connect into
// a living knowledge graph.
export const Scene4Together: React.FC = () => {
  const frame = useCurrentFrame();

  const nodeAppear = (i: number) => ramp(frame, 18 + i * 11, 22);
  const spokeDraw = (i: number) => ramp(frame, 24 + i * 11, 26);
  const webDraw = (i: number) => ramp(frame, 200 + i * 6, 30);

  const titleAppear = ramp(frame, 6, 24);

  return (
    <AbsoluteFill>
      <svg
        width={VIDEO_WIDTH}
        height={VIDEO_HEIGHT}
        style={{ position: "absolute", inset: 0 }}
      >
        {SPOKE_EDGES.map(([a, b], i) => (
          <Edge key={`s${i}`} from={a} to={b} progress={spokeDraw(i)} />
        ))}
        {WEB_EDGES.map(([a, b], i) => (
          <Edge key={`w${i}`} from={a} to={b} progress={webDraw(i)} width={1.5} />
        ))}
      </svg>

      <NodeDot node={CENTER_NODE} appear={1} glow={0.4} radius={20} showLabel={false} />
      {RING_NODES.map((n, i) => (
        <NodeDot key={n.id} node={n} appear={nodeAppear(i)} labelBelow={n.y > CENTER_NODE.y} />
      ))}

      <div
        style={{
          position: "absolute",
          bottom: 70,
          width: "100%",
          textAlign: "center",
          opacity: titleAppear,
        }}
      >
        <div style={{ fontFamily: titleFont, fontSize: 60, fontWeight: 700, color: COLORS.text }}>
          Now bring them <span style={{ color: COLORS.gold }}>together.</span>
        </div>
        <div style={{ fontFamily: bodyFont, fontSize: 28, color: COLORS.textDim, marginTop: 12 }}>
          researchers from every discipline, one table
        </div>
      </div>
    </AbsoluteFill>
  );
};
