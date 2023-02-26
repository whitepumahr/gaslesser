# Imports:

# StarCraft II:
# > Position:
from sc2.position import Point2

# > Bot AI:
from sc2.bot_ai import BotAI

# > Unit:
from sc2.units import Unit

# > IDs:
from sc2.ids.unit_typeid import UnitTypeId

# Dataclasses:
import dataclasses

# Typing:
import typing

# Bases:
from bot.bases import Request


# Classes:
@dataclasses.dataclass
class ScoutRequest(Request):
    """
    Scouts using requested unit type.

    :param patrol_positions:

    :param prioritize_main:
    :param return_back:
    """

    patrol_positions: typing.List[Point2]

    prioritize_main: bool
    return_back: bool = True

    queued: bool = dataclasses.field(default_factory=lambda: False)

    # Methods:
    async def execute(self, AI: BotAI) -> bool:
        if not hasattr(self, "unit_tag"):
            self.unit_tag: typing.Union[int, None] = (
                AI.units.of_type(self.id).closest_to(AI.expansion_locations_list[0]).tag
            )

        unit: Unit = AI.units.find_by_tag(self.unit_tag)

        if unit is None:
            return True

        if self.queued is False:
            self.queued = True

            await self.queue_orders(AI)

        if unit.position.distance_to(AI.enemy_start_locations[0]) < 10:
            return True

        if self.unit_tag not in AI.scouting_units:
            AI.scouting_units.add(self.unit_tag)

        return False

    async def queue_orders(self, AI: BotAI) -> None:
        if not hasattr(self, "unit_tag"):
            return None

        unit: Unit = AI.units.find_by_tag(self.unit_tag)
        if unit is None:
            return None

        unit.move(position=self.patrol_positions[0])

        if len(self.patrol_positions) > 1:
            for iteration in range(1, len(self.patrol_positions) + 1):
                unit.move(self.patrol_positions[iteration], queue=True)

        if self.return_back is True:
            unit.move(position=AI.townhalls.first.position, queue=True)

            AI.drone_assignment.add(self.unit_tag)
