# Imports:

# StarCraft II:
# > Position:
from sc2.position import Point2

# > Bot AI:
from sc2.bot_ai import BotAI, Race

# > IDs:
from sc2.ids.unit_typeid import UnitTypeId

# Typing:
import typing

# Bases:
from bot.bases import Manager


# Classes:
class EnemyTrackerManager(Manager):
    """
    Tracks enemy game data.

    # TODO: Add better description later.
    # TODO: Track enemy race
    """

    # Initialization:
    def __init__(self, AI: BotAI) -> None:
        # Miscellaneous:
        self.enemy_race = AI.enemy_race

        # Dictionaries:
        self.enemy_structures: typing.Dict[int, typing.List[UnitTypeId, Point2]] = {}
        self.enemy_units: typing.Dict[int, UnitTypeId] = {}

    # Methods:
    async def on_step(self, iteration: int, AI: BotAI) -> None:
        # Identify Enemy Race:
        if self.enemy_race == Race.Random:
            for enemy_unit in AI.all_enemy_units:
                self.enemy_race = enemy_unit.race

        for enemy_structure in AI.enemy_structures:
            if enemy_structure.tag in self.enemy_structures:
                continue

            self.enemy_structures[enemy_structure.tag] = [
                enemy_structure.type_id,
                Point2,
            ]

        for enemy_unit in AI.enemy_units:
            if enemy_unit.tag in self.enemy_units:
                continue

            self.enemy_units[enemy_unit.tag] = enemy_unit.type_id
