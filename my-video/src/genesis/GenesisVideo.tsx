import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { SCENE_FRAMES, SCENE_STARTS } from "./constants";
import { Backdrop, SceneWrap } from "./components";
import { Scene1Hook } from "./scenes/Scene1Hook";
import { Scene2Example } from "./scenes/Scene2Example";
import { Scene3OneResearcher } from "./scenes/Scene3OneResearcher";
import { Scene4Together } from "./scenes/Scene4Together";
import { Scene5Bridges } from "./scenes/Scene5Bridges";
import { Scene6Genesis } from "./scenes/Scene6Genesis";
import { Scene7Debate } from "./scenes/Scene7Debate";
import { Scene8Verdict } from "./scenes/Scene8Verdict";

const SCENES = [
  { name: "hook" as const, Comp: Scene1Hook },
  { name: "example" as const, Comp: Scene2Example },
  { name: "oneResearcher" as const, Comp: Scene3OneResearcher },
  { name: "together" as const, Comp: Scene4Together },
  { name: "bridges" as const, Comp: Scene5Bridges },
  { name: "genesis" as const, Comp: Scene6Genesis },
  { name: "debate" as const, Comp: Scene7Debate },
  { name: "verdict" as const, Comp: Scene8Verdict },
];

export const GenesisVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#05060e" }}>
      <Backdrop />
      {SCENES.map(({ name, Comp }) => (
        <Sequence key={name} from={SCENE_STARTS[name]} durationInFrames={SCENE_FRAMES[name]}>
          <SceneWrap durationInFrames={SCENE_FRAMES[name]}>
            <Comp />
          </SceneWrap>
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
