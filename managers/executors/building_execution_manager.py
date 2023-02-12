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

# Bases:
from bot.bases import Manager, Request


# Classes:
class BuildingExecutionManager(Manager):
    """ """

    # Initialization:
    def __init__(self) -> None:
        # Dictionaries:
        self.structure_projections: typing.Dict[UnitTypeId, int] = {}
        self.structures: typing.Dict[int, typing.List[UnitTypeId, Point2]]

        # Lists:
        self.requests: list = []

        # Sets:
        self.verifying: list = []

    # Methods:
    async def on_building_construction_started(self, unit: Unit) -> None:
        self.structures[unit.tag] = [unit.type_id, unit.position]

    async def queue_request(self, request: Request) -> bool:
        if request in self.requests:
            return False

        self.requests.append(request)
        return True

    async def on_frame(self, iteration: int, AI: BotAI) -> None:
        cleanup: list = []

        # Executing Requests:
        for request in self.requests:
            result: bool = await request.execute(AI)

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
                await request.execute(AI)

        # Cleaning Requests:
        for request in cleanup:
            if request in self.verifying:
                self.verifying.remove(request)
