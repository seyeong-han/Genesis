export const FPS = 30;
export const VIDEO_WIDTH = 1080;
export const VIDEO_HEIGHT = 1080;
export const CENTER = { x: VIDEO_WIDTH / 2, y: VIDEO_HEIGHT / 2 };

// Scene durations (frames @ 30fps). Sum drives the composition length.
export const SCENE_FRAMES = {
  hook: 240, // 0:00 - 0:08
  example: 420, // 0:08 - 0:22
  oneResearcher: 240, // 0:22 - 0:30
  together: 360, // 0:30 - 0:42
  bridges: 300, // 0:42 - 0:52
  genesis: 300, // 0:52 - 1:02
  debate: 420, // 1:02 - 1:16
  verdict: 420, // 1:16 - 1:30
} as const;

export type SceneName = keyof typeof SCENE_FRAMES;

export const SCENE_ORDER: SceneName[] = [
  "hook",
  "example",
  "oneResearcher",
  "together",
  "bridges",
  "genesis",
  "debate",
  "verdict",
];

// Cumulative start frame for each scene.
export const SCENE_STARTS: Record<SceneName, number> = (() => {
  const out = {} as Record<SceneName, number>;
  let acc = 0;
  for (const name of SCENE_ORDER) {
    out[name] = acc;
    acc += SCENE_FRAMES[name];
  }
  return out;
})();

export const TOTAL_FRAMES = SCENE_ORDER.reduce(
  (sum, name) => sum + SCENE_FRAMES[name],
  0,
);

// Palette — dark canvas, cool nodes, warm gold for bridges / sparks / verdict.
export const COLORS = {
  bg0: "#05060e",
  bg1: "#0b0f24",
  text: "#f5f7ff",
  textDim: "#9aa3c0",
  blue: "#6ea8ff",
  purple: "#a98cff",
  gold: "#ffce5c",
  goldHot: "#ffb347",
  edge: "rgba(150,170,255,0.32)",
  edgeHot: "rgba(255,206,92,0.9)",
  cardBg: "rgba(16,21,46,0.92)",
  cardBorder: "rgba(150,170,255,0.28)",
  novel: "#5cffb0",
} as const;
