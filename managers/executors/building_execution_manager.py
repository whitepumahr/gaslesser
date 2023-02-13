# Imports:

# StarCraft II:
# > Positions:
from sc2.position import Point2

# > Bot AI:
from sc2.bot_ai import BotAI

# > Unit:
from sc2.unit import Unit

# > IDs:
from sc2.ids.unit_typeid import UnitTypeId

# Typing:
import typing

# Requests:
from bot.requests import BuildRequest

# Bases:
from bot.bases import Manager, Request


# Classes:
class BuildingExecutionManager(Manager):
    """
    Parses building requests and executes them.
    Also will rebuild dead structures.

    TODO: Add functionality for geysers.
    TODO: Potentially add safe checks to build requests, e.g make sure no threatning units are near it that can kill it right when it builds to save minerals.
    """

    # Initialization:
    def __init__(self) -> None:
        # Dictionaries:
        self.structure_projections: typing.Dict[UnitTypeId, int] = {}
        self.structures: typing.Dict[int, typing.List[UnitTypeId, Point2]] = {}

        # Lists:
        self.verifying: list = []
        self.requests: list = []

    # Methods:
    async def on_building_construction_started(self, unit: Unit) -> None:
        self.structures[unit.tag] = [unit.type_id, unit.position]

    async def on_unit_destroyed(
        self, tag_of_a_unit_or_structure_that_just_died: int
    ) -> None:
        if tag_of_a_unit_or_structure_that_just_died not in self.structures:
            return None

        structure_information: typing.List[UnitTypeId, Point2] = self.structures[
            tag_of_a_unit_or_structure_that_just_died
        ]

        await self.queue_request(
            BuildRequest(id=structure_information[0], position=structure_information[1])
        )

        del self.structures[tag_of_a_unit_or_structure_that_just_died]

    async def execute_request(self, request: Request, AI: BotAI) -> bool:
        if hasattr(request, "execute_wrapper") is True:
            return await request.execute_wrapper(AI)
        else:
            return await request.execute(AI)

    async def queue_request(self, request: Request) -> bool:
        if request in self.requests:
            return False

        self.requests.append(request)
        return True

    async def on_frame(self, iteration: int, AI: BotAI) -> None:
        cleanup: list = []

        # Executing Requests:
        for request in self.requests:
            result: bool = await self.execute_request(request, AI)

            if result is True:
                self.verifying.append(request)

                self.structure_projections[request.id] = (
                    self.structure_projections.get(request.id, 0) + request.quantity
                )

        # Verifying Requests:
        for request in self.verifying:
            if request in self.requests:
                self.requests.remove(request)

            if (
                AI.structures.of_type(request.id).amount
                >= self.structure_projections[request.id]
            ):
                cleanup.append(request)
            else:
                await self.execute_request(request, AI)

        # Cleaning Requests:
        for request in cleanup:
            if request in self.verifying:
                self.verifying.remove(request)
