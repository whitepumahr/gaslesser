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

# Libraries:
from .libraries import MapParser

# Requests:
from .requests import ScoutRequest

# Sequence:
from .sequence import BEGINNER_SEQUENCE

# Managers:
from .managers import (
    BuildingExecutionManager,
    TrainingExecutionManager,
    ScoutingExecutionManager,
    EnemyTrackerManager,
    DebuggingManager,
    ReactionManager,
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
        self.ScoutingExecutionManager: ScoutingExecutionManager = (
            ScoutingExecutionManager()
        )

        self.EnemyTrackerManager: EnemyTrackerManager = EnemyTrackerManager(self)
        self.DebuggingManager: DebuggingManager = DebuggingManager(
            DRAW_OPPONENT_BASE_LOCATIONS=True,
            DRAW_VISIBLITY_PIXELMAP=False,
            DRAW_PLACEMENT_GRID=False,
            DRAW_PATHING_GRID=False,
            DRAW_EXPANSIONS=True,
        )
        self.ReactionManager: ReactionManager = ReactionManager()

        # Library References:
        self.MapParser: MapParser = MapParser(DRAW_RAMP_TILES=True)

        # Miscellaneous:
        await self.chat_send(
            "You can thank Chronicles, Ratosh and the rest of the very helpful botting community for what is about to happen to you"
        )

        self.map_parser_json = await self.MapParser.analyze(self)

        # Starter Buildorder:
        for request in BEGINNER_SEQUENCE:
            await self.TrainingExecutionManager.queue_request(request)

        # Lists:
        self.managers: list = [
            self.BuildingExecutionManager,
            self.TrainingExecutionManager,
            self.ScoutingExecutionManager,
            self.EnemyTrackerManager,
            self.DebuggingManager,
            self.ReactionManager,
        ]

        # Sets:
        self.drone_assignment: typing.Set[int] = set()
        self.scouting_units: typing.Set[UnitTypeId] = set()

        # Miscellaneous:
        await self.ScoutingExecutionManager.queue_request(
            ScoutRequest(
                patrol_positions=[self.enemy_start_locations[0]],
                id=UnitTypeId.DRONE,
                prioritize_main=False,
                return_back=True,
            )
        )

    async def on_step(self, iteration: int):
        # Updating Managers:
        for manager in self.managers:
            await manager.on_step(iteration, self)

        await self.MapParser.analyze(self)
