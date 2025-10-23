"""
UEFA Champions League Draw Simulator

A constraint satisfaction algorithm for simulating UEFA Champions League draws.
"""

__version__ = "1.0.0"
__author__ = "Iliass Sijelmassi"

from src.champions_league_draw import (
    Team,
    DrawConstraints,
    ChampionsLeagueDraw,
    create_sample_teams,
)

__all__ = [
    "Team",
    "DrawConstraints",
    "ChampionsLeagueDraw",
    "create_sample_teams",
]

