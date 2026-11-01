# Balanced Mega-Simulation 2.0 — current modeling contract

- Seeded, deterministic turn-by-turn **macro strategy model**, not an executable Civ V match.
- 56 entries: 18 Wacky I, 21 Wacky II, 8 Una Court, 9 carried-over standalones.
- 11 city-states; seven-continent procedural map; simulated Marathon-style calendar, **not** exact engine speed modifiers.
- Political map snapshots every 25 turns plus final frame, with city ownership, wars, scores, and logged major events.
- Civilizations optimize a preferred victory path but may respond to observed rival victory threats, diplomatically and militarily.
- Fictional civilization mechanics are approximated by tunable numerical trait modifiers rather than literally executing their mod scripts.
- No claim of game-accurate unit combat, AI, diplomacy, city yields, or statistically validated balance.

## Reproducibility

Run `python engine/sim56_v2.py`, then `python replay/build_war56_replay.py`. Keep the Python versions and dependency versions consistent when checking bit-for-bit outputs. Archived baseline seed: `20261102`.

## Proposed improvements

Move roster and balancing parameters into versioned configuration, add validation tests, document victory threshold formulas and build multiple-seed tournament analyses rather than inferring balance from one campaign.
