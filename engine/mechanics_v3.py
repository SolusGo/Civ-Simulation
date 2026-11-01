"""Pure, testable numerical proxies for the War of 56 v3 model.
These functions do not execute native Civilization V or mod Lua mechanics.
"""
import math

def momentum_after_turn(momentum: int, victory_this_cycle: bool) -> int:
    """Quiet owner-turn cycles reduce Momentum by one."""
    return max(0, min(6, momentum - (0 if victory_this_cycle else 1)))

def momentum_after_victory(momentum: int, increment: int = 1) -> int:
    """Qualifying kill +1; first genuine conquest of a city site +2."""
    if increment not in (1, 2):
        raise ValueError("Momentum gain must be 1 or 2")
    return min(6, max(0, momentum) + increment)

def resolve_siege_pressure(power_ratio: float, is_capital: bool,
                           fortification: float, defense_alert: float,
                           random_factor: float) -> float:
    """Compute bounded progress; larger garrisons and forts slow breaches."""
    if power_ratio <= .58: return 0.0
    random_factor = max(.5, min(1.5, random_factor))
    raw = (1.0 + 2.8 * max(0., power_ratio - .6)) * random_factor
    if power_ratio < .85: raw *= .38
    if is_capital: raw *= .74
    raw *= max(.45, 1.0 - .0025 * min(100., max(0., fortification)))
    raw /= 1.0 + .2 * min(1., max(0., defense_alert))
    return round(max(0., raw), 6)

def victory_alarm_tier(progress: float) -> int:
    if not math.isfinite(progress):
        raise ValueError("Victory progress must be finite")
    if progress >= .95: return 4
    if progress >= .85: return 3
    if progress >= .70: return 2
    if progress >= .50: return 1
    return 0

def compute_roster_losses(casualties: float, remaining_army: float) -> float:
    """Approximate one veteran being lost when front-line casualties occur."""
    if casualties < 0 or remaining_army <= 0: return 0.0
    return min(.075, max(0., casualties / remaining_army * 1.9))
