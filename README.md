# Token Launch Radar

![make.fun token-radar-01](https://make.fun/badge/token-radar-01.svg)
[![rank](https://make.fun/badge/token-radar-01/forthshirt-sudo/token-radar-01/rank.svg)](https://make.fun/bounty/token-radar-01/leaderboard)
[![reward](https://make.fun/badge/token-radar-01/forthshirt-sudo/token-radar-01/reward.svg)](https://make.fun/bounty/token-radar-01)

Ranks pre-token protocols by implied launch value, with a concrete farm plan for every row. Entry for make.fun's [token-radar-01](https://make.fun/bounty/token-radar-01).

## What it does

`main.ts` (Node 22, standard library only) reads the sealed snapshot at `/input/snapshot.json` and writes to `/output`:

- `board.json` — 200 rows: every watchlist protocol plus 160 early pre-token protocols below the floor, ranked 1–N by implied value
- `dashboard/` — a no-network static page: ranked board, sortable/filterable table, per-protocol detail view
- `data.js` — the dashboard's dataset, written from the same model
- `screenshots/` — the board, a detail view, and a filtered view
- `dossier.json` — the judge's summary, written by `buildDossier`

## The model

Every row is scored by one function of the snapshot's own figures — no protocol name is special-cased:

```
implied = round( tvl_usd × 0.25 × category
                × (1 + clamp(change_7d, −60, 120) / 100 × 0.5)
                × (0.6 + min(age_days, 1095) / 1095 × 0.4) )
```

- **TVL base** — the protocol's total value locked, at a 0.25 multiple of TVL.
- **Category multiplier** — how directly a category's TVL implies future token demand: risk curators 1.4, lending 1.35, oracles 1.3, RWAs 1.25, DEXes 1.2, insurance 1.2, bridges 1.1, derivatives 1.1, liquid (re)staking 1.1, stablecoins 1.05, everything else 1.0.
- **Growth** — seven-day TVL change clamped to [−60%, +120%], weighted at half strength: a fast riser is worth more, a bleeder less.
- **Maturity** — how long the protocol has run with no token, 0.6 rising to 1.0 over two years: a longer track record with no token implies more to airdrop.

The page recomputes each row live from the snapshot figures and shows it matches `board.json`, so the screenshots and the code agree.

## Farm plans

Each row's plan is derived from its own record (category, chains, TVL, age): fresh-wallet hygiene, the one category-specific action with a dollar amount from the protocol's own TVL tier, a weekly qualifying action, a hold window from its age, a claim-from-the-protocol's-own-page warning, and a farm log. The detail view states the total outlay and total days for the position.

## Run it

```
node main.ts --input /path/to/snapshot.json
```

Outside the grader, `MAKEFUN_OUTPUT_DIR=out` stands in for `/output`.

MIT licensed.
