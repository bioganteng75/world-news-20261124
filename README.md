# world-news-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/bioganteng75/world-news-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/bioganteng75/world-news-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image summing up Tuesday 24 November 2026's world news, drawn as a
broadsheet front page — "THE WORLD IN ONE DAY". The four lead stories,
each with its own illustrated panel: the ICJ finds Myanmar guilty of
genocide over the Rohingya campaign; NATO vows defence against the
space threat as Russia readies a possible nuclear-armed satellite;
tensions flare in the Strait of Hormuz; and a US surveillance drone
helps Mexico capture cartel boss 'El Chapo Isidro'. A ticker strip
along the bottom carries six more of the day's stories, from the
SpaceX/Grok lawsuits to Bangladesh's typhoid vaccination drive.

The page is composed programmatically with Python + Pillow
(`compose.py`): fixed geometry, fixed palette, no timestamps, so every
run produces byte-identical output. `main.ts` (Node 22, standard
library only) copies the committed `entry.png` to the output
directory, locating the asset from its own file path so it works from
any working directory.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=rd8zvqpf&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
