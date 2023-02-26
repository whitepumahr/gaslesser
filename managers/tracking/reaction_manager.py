# Imports:

# StarCraft II:
# > Bot AI:
from sc2.bot_ai import BotAI, Race

# > IDs:
from sc2.ids.unit_typeid import UnitTypeId

# Typing:
import typing

# Bases:
from bot.bases import Manager


# Classes:
class ReactionManager(Manager):
    # Initialization:
    def __init__(self) -> None:
        pass

    # Methods:
    async def on_step(self, iteration: int, AI: BotAI) -> None:
        if hasattr(AI, "scouting_units") is False:
            AI.scouting_units: typing.Set[UnitTypeId] = set()
