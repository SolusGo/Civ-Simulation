## New in v3: stronger strategy model

The original **v2 engine and War of 56 archive are preserved**. Version 3 adds externally configurable civilization profiles, more realistic siege defense and fatigue, and explicit (still approximate) mechanics for T1, Triumphal Imperium, Lantern Fleet, First Drafts and Boundless City.

```bash
python -m unittest discover -s tests -v
python engine/sim56_v3.py --seed 20261103 --snapshot-every 25
python replay/build_war56_v3_replay.py
```

Open `output/war56_v3_interactive_replay.html`. The baseline v3 showcase is seed `20261103`; see [v3 design notes](docs/V3_UPGRADE.md) for limitations. **Neither v2 nor v3 plays real Civ V or executes the mods' Lua logic.**

---

# Civ Simulation

A reproducible **strategic macro-simulator** for custom *Civilization V: Brave New World* civilizations. The current baseline is **War of 56 — Balanced Mega-Simulation 2.0**, using an approximate Marathon calendar, 56 civilization profiles, 11 City-States, turn-by-turn model decisions, and political-map checkpoints every 25 turns.

> **Important:** This is **not** the Civilization V game executable. It does not run Community Patch v151, custom Lua abilities, the game's AI, native combat, or exact game-speed yields. This is an original Python strategy sandbox with hand-tuned civilization traits, suitable for storytelling, testing proposed model rules, and comparing simulated runs—not establishing real in-game balance.

## Getting started

From the repository root, using Python 3.10+:

```bash
python -m pip install -r requirements.txt
python engine/sim56_v2.py
python replay/build_war56_replay.py
```

The engine creates `output/war56_results.json`, an illustrated atlas, final map, final CSV scoreboard, and campaign report. The second command uses that JSON to create a self-contained `output/war56_interactive_replay.html` you can open in a local browser.

Generated `output/` files are ignored by Git. For a preserved example, see `examples/war56/`.

## Structure

| Path | Contents |
| --- | --- |
| `engine/sim56_v2.py` | Seeded simulation, terrain, cities, conflict, victory race, JSON/map/report exporter |
| `replay/build_war56_replay.py` | Offline HTML timeline/replay generator |
| `docs/SIMULATION_RULES.md` | Current approximated balance and simulation contract |
| `examples/war56/war56_results.json` | Archived Turn 866 campaign including 36 map checkpoints and event timeline |
| `examples/war56/war56_campaign_report.md` | Historic narrative report |
| `examples/war56/war56_final_roster.csv` | Final archived standings |
| `requirements.txt` | Python dependencies |

## Determinism and caveats

The fixed baseline seed is `20261102`. On the verified local environment, re-running the engine reproduced the archived JSON data and the replay generator generated its HTML file. Python/library versions can affect exact floating-point behavior or output files across environments.

The **56 profiles are currently hardcoded**; there is no automatic GitHub synchronization with the source Civilization V mods. They are not guaranteed to be currently complete or to match every native Lua mechanic. The repository is a foundation for future enhancements, not a literal Civ V combat simulator.

## Next improvements

1. Extract civilization profiles, victory conditions, and map presets into versioned configuration.
2. Add automated tests, reproducibility manifests and a CI check.
3. Model specific unique abilities through explicit, testable state transitions rather than only numeric trait modifiers.
4. Run many seeds before drawing balance conclusions and document uncertainty.

## Status

Initial import through a review pull request. Engine Python compilation, deterministic archive comparison, and HTML replay generation were checked locally.
