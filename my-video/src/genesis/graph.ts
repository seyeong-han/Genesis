import { COLORS, VIDEO_WIDTH } from "./constants";

// The graph is centered slightly above the geometric middle so the bottom ring
// nodes + labels clear the lower-third caption band.
export const GRAPH_CENTER = { x: VIDEO_WIDTH / 2, y: 470 };

export type GraphNode = {
  id: string;
  label: string;
  x: number;
  y: number;
  color: string;
};

export const polar = (
  cx: number,
  cy: number,
  r: number,
  angleDeg: number,
): { x: number; y: number } => {
  const a = (angleDeg * Math.PI) / 180;
  return { x: cx + r * Math.cos(a), y: cy + r * Math.sin(a) };
};

// 12 disciplines arranged on a circle around the center researcher.
const DISCIPLINES: { id: string; label: string; color: string }[] = [
  { id: "bio", label: "Biology", color: COLORS.blue },
  { id: "phys", label: "Physics", color: COLORS.purple },
  { id: "ai", label: "AI", color: COLORS.blue },
  { id: "phil", label: "Philosophy", color: COLORS.purple },
  { id: "neuro", label: "Neuroscience", color: COLORS.blue },
  { id: "net", label: "Networks", color: COLORS.purple },
  { id: "ento", label: "Entomology", color: COLORS.blue },
  { id: "cosmo", label: "Cosmology", color: COLORS.purple },
  { id: "chem", label: "Chemistry", color: COLORS.blue },
  { id: "ling", label: "Linguistics", color: COLORS.purple },
  { id: "math", label: "Mathematics", color: COLORS.blue },
  { id: "cplx", label: "Complexity", color: COLORS.purple },
];

const RADIUS = 340;

// Center node = the lone researcher (Scenes 3-4).
export const CENTER_NODE: GraphNode = {
  id: "center",
  label: "Robotics",
  x: GRAPH_CENTER.x,
  y: GRAPH_CENTER.y,
  color: COLORS.gold,
};

export const RING_NODES: GraphNode[] = DISCIPLINES.map((d, i) => {
  const angle = -90 + (360 / DISCIPLINES.length) * i;
  const { x, y } = polar(GRAPH_CENTER.x, GRAPH_CENTER.y, RADIUS, angle);
  return { id: d.id, label: d.label, x, y, color: d.color };
});

export const ALL_NODES: GraphNode[] = [CENTER_NODE, ...RING_NODES];

// Edges from center to each ring node (drawn in Scene 4).
export const SPOKE_EDGES: [string, string][] = RING_NODES.map((n) => [
  "center",
  n.id,
]);

// A handful of ring-to-ring edges so the graph reads as a web, not a star.
export const WEB_EDGES: [string, string][] = [
  ["bio", "ento"],
  ["ento", "net"],
  ["net", "ai"],
  ["ai", "neuro"],
  ["neuro", "phil"],
  ["phil", "cosmo"],
  ["cosmo", "phys"],
  ["phys", "chem"],
  ["chem", "bio"],
  ["math", "cplx"],
  ["cplx", "net"],
  ["ling", "phil"],
];

// Cross-field "bridges" that ignite in Scene 5 (distant pairs).
export const BRIDGE_EDGES: [string, string][] = [
  ["ento", "ai"], // ants → swarm robotics / AI
  ["phys", "neuro"], // physics → brain
  ["math", "ling"], // math → language
];

export const nodeById = (id: string): GraphNode =>
  ALL_NODES.find((n) => n.id === id) ?? CENTER_NODE;

// Researchers for the debate scene (real demo set from demo_researchers.md).
export type Researcher = {
  name: string;
  field: string;
  claim: string;
  doi: string;
  color: string;
};

export const DEBATE_RESEARCHERS: Researcher[] = [
  {
    name: "Ashish Vaswani",
    field: "Transformers",
    claim: "Attention is general-purpose — it may subsume vision and generation.",
    doi: "10.48550/arXiv.1706.03762",
    color: COLORS.blue,
  },
  {
    name: "Yann LeCun",
    field: "CNN / Energy-based",
    claim: "Inductive biases matter — pure autoregression is not enough.",
    doi: "10.1109/5.726791",
    color: COLORS.purple,
  },
  {
    name: "Jonathan Ho",
    field: "Diffusion",
    claim: "Diffusion is its own pillar — hybrid backbones are the frontier.",
    doi: "10.48550/arXiv.2006.11239",
    color: COLORS.gold,
  },
];
