# Balanced Mega-Simulation 3.0 — Implemented enhancements

> **This is a numerical, strategic sandbox, not Civilization V, Community Patch v151, or faithful custom-civilization Lua execution.** All special-civ rules below remain proxies. Actual balance cannot be inferred from one seed.

## How to run

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python engine/sim56_v3.py --seed 20261103 --snapshot-every 25 --max-turn 1450
python replay/build_war56_v3_replay.py
```

The results, political maps, campaign report, CSV standings and offline HTML replay go to `output/`. The original v2 runner remains available and has not been modified.

To change profiles, edit `config/roster.json` or pass another file with `--roster`. The engine validates 56 profiles, distinct names, recognized victory types and finite trait values. The saved results include the SHA-256 fingerprint of that configuration. Use `--output-dir` for alternate storage, `--seed` for randomized worlds and `--snapshot-every` for map frequency.

## V3 systems

- **War and sieges:** defenders enter a readiness alert when attacked, slightly increasing military recruitment and defensive pressure. High city fortifications slow sieges. Siege progress regresses without maintained attacks, and protracted attritional wars may conclude in a peace settlement.
- **Victory alarms:** civilization-specific progress can cross 50%, 70%, 85%, and 95% warning thresholds, with escalating strategic awareness. The old model's cross-border victory-denial wars and influence-defense responses remain.
- **Triumphal Imperium:** qualifying military victory raises capped Momentum; no victory in the owner's turn cycle causes decay. Bonuses affect combat and **military recruitment**, not global economic income. Each conquered city site grants the one-time conquest reward at most once. Hall eligibility is approximated.
- **T1 ZOFGK:** technology-era upgrades cost Gold; equipment development no longer happens from winning battles. Model veteran roles can be lost to battle attrition; replacement training requires city capacity and a recovery period, without inherited veteran experience.
- **Lantern Fleet:** modeled coastal city guard requirements limit naval science and culture bonuses, with an additional lighthouse-development proxy. This estimates garrison commitments; there is no tile-level naval simulation.
- **Republic of First Drafts:** the model stores distinct first-possessed building classes. Each class can grant a one-time Marathon-scaled culture/gold payout; Science rewards depend on that accumulated diversity. It does **not** read Civ V's actual building definitions.
- **Boundless City:** the one-city limitation is enforced for conquest by destroying captured sites in the abstract world map rather than retaining them. Ruins remain in historical data for accurate earlier replay frames. This is an abstraction of the custom mod's razing requirement, not vanilla Civ V rules.
- **Replay:** the inspector displays more specialty state (T1 roster, guarded harbors, building diversity), and supports a run cut short without a winner.

## What remains approximate

The simulation doesn't move actual Civ V units, execute promotions, move naval units into coastal cities, select policies in the real game, or use real map pathfinding/CP v151. Culture, Science, Gold, alliances, army strength, urban growth and sieges are synthesized scalar models. Expert-play, victory blocking and player-only civ AI are hypothetical behaviors chosen for the simulation.

For meaningful **balance comparisons**, run many seeded games, vary map configurations, summarize win rates with uncertainty and examine how assumptions change those outcomes.
