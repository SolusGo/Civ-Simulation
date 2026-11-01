# War of 56 — Campaign 2026110202

**Model:** Balanced Mega-Simulation v3.0  
**Roster:** 56 civilizations and 11 City-States  
**Seed:** `2026110202`  
**Map checkpoints:** every 25 turns (35 total including Turn 845)  
**Campaign:** Turns 0–845 inclusive  
**Winner:** **The Luna Network**, modeled **Science Victory**, Turn **845**  
**Roster SHA-256:** `8f51358c986150c54277a342c8b49b6c31aa6af3f46a16ad55e837d8f7184fb6`  
**Provenance:** Fresh deterministic macro-simulation, not a Civilization V executable match.

## Summary

- 129 declarations of war; 106 peace agreements; 55 battle events.
- 84 non-capital city conquests, 7 original founding-capital conquests, 5 civilization eliminations.
- 208 cities founded beyond the 56 original capitals (264 recorded city sites total).
- 39 modeled victory-denial coalition interventions and 665 total logged events.
- 51 of 56 civilizations survived through the victory turn.
- Winner ranked **14th** by overall score (421), with five cities and a 119.35 modeled research total.

### Final score leaders

| Rank | Civilization | Score | Cities | Founding capitals |
| ---: | --- | ---: | ---: | ---: |
| 1 | The Jin Dynasty | 598 | 13 | 4 |
| 2 | The Republic of First Drafts | 561 | 4 | 1 |
| 3 | McPvP — The Endless Lobby | 523 | 14 | 2 |
| 4 | The Urgal | 518 | 12 | 3 |
| 5 | The Fleshborn Chorus | 459 | 9 | 1 |
| 8 | T1 — The ZOFGK Dynasty | 443 | 9 | 1 |
| 13 | The Lantern Fleet | 425 | 5 | 1 |
| **14** | **The Luna Network 🏆** | **421** | **5** | **1** |
| 18 | The Triumphal Imperium | 412 | 6 | 1 |

### Key events

- **Turn 172:** McPvP captures Soft Kitty Serenader's founding capital and eliminates the civilization.
- **Turn 226:** Jin conquers and eliminates the Fourth Generation White Room.
- **Turn 404:** Jin takes Sol Intellect's founding capital.
- **Turn 462:** Jin takes Wealthy of Una Court's founding capital, eliminating the civilization.
- **Turn 498:** Possession Browsers finishes eliminating Sol Intellect.
- **Turn 548:** Urgal takes The Kingdoms' founding capital.
- **Turn 624:** Indigo Champion takes Pigeon Republic's founding capital.
- **Turn 726:** Urgal captures Jetstar's founding capital and eliminates it.
- **Turn 819:** Triumphal Imperium declares victory-denial war on Luna Network.
- **Turn 828:** Viltrum, Azul Baronis and The Colony join the anti-Luna offensive.
- **Turn 845:** Luna finishes its modeled Science Victory.

## Reproduce the campaign

From this repository's root after `pip install -r requirements.txt`:

```sh
python engine/sim56_v3.py --seed 2026110202 --snapshot-every 25
python replay/build_war56_v3_replay.py
```

Results and the standalone HTML replay are written to `output/` (ignored by Git). Keep the v3 engine and roster unchanged to reproduce the archived findings. Large/binary replay artifacts are deliberately not checked into this branch.

> All military movement, city borders, diplomacy, science races and unique-ability effects are illustrative abstractions, not game-engine simulations or verified gameplay balance.
