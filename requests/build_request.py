# Imports:

# StarCraft II:
# > Position:
from sc2.position import Point2

# > Bot AI:
from sc2.bot_ai import BotAI

# > Unit:
from sc2.unit import Unit

# Dataclasses:
import dataclasses

# Typing:
import typing

# Loguru:
import loguru

# Bases:
from bot.bases import Request


# Classes:
@dataclasses.dataclass
class BuildRequest(Request):
    """
    Builds the structure requested.

    :param position:
    :param quantity:
    """

    position: typing.Union[typing.List[Point2], Point2, typing.List[Unit], Unit]

    valid_attempts: int = 0
    quantity: int = 1

    queued_positions: typing.Dict[int, Point2] = dataclasses.field(
        default_factory=lambda: dict()
    )
    en_route: set = dataclasses.field(default_factory=lambda: set())

    # Methods:
    async def verify_able(self, AI: BotAI) -> bool:
        if AI.can_afford(self.id) is False:
            return False

    async def find_drone(self, position: Point2, AI: BotAI) -> typing.Optional[Unit]:
        return AI.workers.filter(
            lambda worker: not worker.is_carrying_resource
            and worker.tag not in self.en_route
        ).closest_to(position)

    async def is_dead(self, tag: int, AI: BotAI) -> bool:
        return AI.workers.find_by_tag(tag) is None

    async def cleanup(self, AI: BotAI) -> None:
        en_route_cleanup: set = set()

        for drone_tag in self.en_route:
            if await self.is_dead(drone_tag, AI) is True:
                en_route_cleanup.add(drone_tag)

        for drone_tag in en_route_cleanup:
            if drone_tag in self.queued_positions:
                self.position.add(self.queued_positions[drone_tag])
                del self.queued_positions[drone_tag]

            self.valid_attempts -= 1

            self.en_route.remove(drone_tag)

    async def execute(self, AI: BotAI) -> bool:
        await self.cleanup(AI)

        if self.valid_attempts == self.quantity:
            return True

        if await self.verify_able(AI) is False:
            return False

        for iteration in range(self.quantity):
            await self.cleanup(AI)

            for drone_tag in self.queued_positions:
                drone: typing.Optional[Unit] = AI.workers.find_by_tag(drone_tag)
                if drone is not None:
                    drone.build(self.id, self.queued_positions[drone_tag])

            if self.valid_attempts == self.quantity:
                return True

            if await self.verify_able(AI) is False:
                return False

            if isinstance(self.position, list):
                if len(self.position) > 0:
                    position: typing.Union[Point2, Unit] = self.position.pop()

                    drone_selection_position = position
                    if isinstance(drone_selection_position, Unit):
                        drone_selection_position = position.position

                    drone: typing.Optional[Unit] = await self.find_drone(
                        drone_selection_position, AI
                    )
                    if drone is not None:
                        self.en_route.add(drone.tag)

                        drone.build(self.id, position)

                        self.queued_positions[drone.tag] = position
                        self.valid_attempts += 1
                    else:
                        self.position.add(position)

            elif isinstance(self.position, Point2):
                drone: typing.Optional[Unit] = await self.find_drone(self.position, AI)
                if drone is not None:
                    self.en_route.add(drone.tag)

                    drone.build(self.id, self.position)

                    self.valid_attempts += 1

            elif isinstance(self.position, Unit):
                drone: typing.Optional[Unit] = await self.find_drone(
                    self.position.position, AI
                )
                if drone is not None:
                    self.en_route.add(drone.tag)

                    drone.build(self.id, self.position)

                    self.valid_attempts += 1
