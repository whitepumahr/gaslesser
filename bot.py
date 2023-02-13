# Imports:

# StarCraft II:
# > Bot AI:
from sc2.bot_ai import BotAI, Race

# > Unit:
from sc2.unit import Unit

# > IDs:
from sc2.ids.unit_typeid import UnitTypeId

# Typing:
import typing

# Sequence:
from .sequence import BEGINNER_SEQUENCE

# Managers:
from .managers import (
    BuildingExecutionManager,
    TrainingExecutionManager,
    EnemyTrackerManager,
    DebuggingManager,
)


# Classes:
class Gasless(BotAI):
    """
    Base class for Gasless.
    """

    # Configuration:
    NAME: str = "Gasless"

    RACE: Race = Race.Zerg

    # Properties:
    @property
    def enemy_structure_tally(self) -> typing.Dict[UnitTypeId, int]:
        enemy_structure_tally: typing.Dict[UnitTypeId, int] = {}

        for structure_data in self.EnemyTrackerManager.enemy_structures.values():
            enemy_structure_tally[structure_data[0]] = (
                enemy_structure_tally.get(structure_data[0], 0) + 1
            )

        return enemy_structure_tally

    @property
    def enemy_unit_tally(self) -> typing.Dict[UnitTypeId, int]:
        enemy_unit_tally: typing.Dict[UnitTypeId, int] = {}

        for unit_type_id in self.EnemyTrackerManager.enemy_units.values():
            enemy_unit_tally[unit_type_id] = enemy_unit_tally.get(unit_type_id, 0) + 1

        return enemy_unit_tally

    # Events:
    async def on_building_construction_started(self, unit: Unit):
        await self.BuildingExecutionManager.on_building_construction_started(unit, self)

    async def on_unit_destroyed(self, tag: int):
        await self.BuildingExecutionManager.on_unit_destroyed(tag)

    async def on_start(self):
        # Manager References:
        self.BuildingExecutionManager: BuildingExecutionManager = (
            BuildingExecutionManager()
        )
        self.TrainingExecutionManager: TrainingExecutionManager = (
            TrainingExecutionManager()
        )
        self.EnemyTrackerManager: EnemyTrackerManager = EnemyTrackerManager(self)
        self.DebuggingManager: DebuggingManager = DebuggingManager(
            DRAW_OPPONENT_BASE_LOCATIONS=True,
            DRAW_VISIBLITY_PIXELMAP=False,
            DRAW_PLACEMENT_GRID=False,
            DRAW_PATHING_GRID=False,
            DRAW_EXPANSIONS=True,
        )

        # Miscellaneous:
        await self.chat_send(
            "You can thank Chronicles, Ratosh and the rest of the very helpful botting community for what is about to happen to you"
        )

        # Starter Buildorder:
        for request in BEGINNER_SEQUENCE:
            await self.TrainingExecutionManager.queue_request(request)

    async def on_step(self, iteration: int):
        # Updating Managers:
        await self.BuildingExecutionManager.on_frame(iteration, self)
        await self.TrainingExecutionManager.on_frame(iteration, self)
        await self.EnemyTrackerManager.on_step(iteration, self)
        await self.DebuggingManager.on_step(iteration, self)
