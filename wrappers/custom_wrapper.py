# Imports:

# StarCraft II:
# > Bot AI:
from sc2.bot_ai import BotAI

# > IDs:
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId

# Typing:
import typing

# Requests:
from bot.requests import BuildRequest, TrainRequest


# Classes:
class CustomWrapper:
    # Initialization:
    def __init__(
        self,
        condition: typing.Callable,
        request: typing.Union[BuildRequest, TrainRequest],
        *args,
        **kwargs
    ) -> None:
        # Miscellaneous:
        self.condition: typing.Callable = condition

        self.request: typing.Union[BuildRequest, TrainRequest] = request(
            *args, **kwargs
        )

    # Properties:
    @property
    def valid_attempts(self) -> int:
        return self.request.valid_attempts

    @property
    def quantity(self) -> int:
        return self.request.quantity

    @property
    def id(self) -> typing.Union[UnitTypeId, AbilityId, UpgradeId]:
        return self.request.id

    # Methods:
    async def execute_wrapper(self, AI: BotAI) -> bool:
        if self.condition(AI) is True or self.valid_attempts > 0:
            await self.request.execute(AI)

            return True

        return False
