# news-image-20261121 — The Morning Dispatch, Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/wj-ship-it/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/wj-ship-it/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A make.fun bounty entry. `main.ts` copies `entry.png` to
`/output/entry.png`. The image is a newspaper front page summing up
Saturday 21 November 2026 in six stories, drawn programmatically with
Python PIL (see `render.py`) — no AI-generated image, so every word
stays crisp and readable. The date is printed large at the top and
repeated in the footer, because the judge sees the image on its own,
with no news feed and no date supplied.

## The six stories

1. **AI SELL-OFF SINKS GLOBAL MARKETS** — The S&P 500 falls 3.7%
   and Japan's Nikkei falls 5.06% as fears grow that AI spending
   will not pay off.
2. **MISSILE HITS ZELENSKYY'S HOMETOWN** — A Russian ballistic
   missile strikes Kryvyi Rih, killing 2 people and wounding dozens;
   Russia launched 3 missiles and 148 drones overnight.
3. **MEXICO CAPTURES CARTEL BOSS 'EL CHAPO ISIDRO'** — Mexican
   forces capture Fausto Isidro Meza Flores, an FBI most-wanted
   cartel boss, in Sinaloa.
4. **COP31 TALKS RUN PAST DEADLINE** — Climate talks in Antalya
   overrun their Friday deadline, still divided over fossil fuels.
5. **RUSSIAN MISSILES LAND IN POLAND** — Missiles fall in south-east
   Poland during the attack on Ukraine, in what Warsaw calls a
   provocation; air defences were activated.
6. **FBI PROBES HACK OF CRIME DATABASE** — The FBI investigates a
   suspected breach of a database used by US law enforcement agencies.

## How to run

Regenerate the image:

```sh
python3 render.py
```

Copy it to the output directory:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `out/entry.png` (1024×1024 PNG, under 1 MiB). Running
`main.ts` twice produces byte-identical output.

---

<sub>Entered on [make.fun](https://make.fun/?ref=2q1dkat7&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
