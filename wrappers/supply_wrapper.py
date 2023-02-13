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
class SupplyWrapper:
    # Initialization:
    def __init__(
        self,
        supply_trigger: int,
        request: typing.Union[BuildRequest, TrainRequest],
        *args,
        **kwargs
    ) -> None:
        # Initialization:
        self.request: typing.Union[BuildRequest, TrainRequest] = request(
            *args, **kwargs
        )

        # Integers:
        self.supply_trigger: int = supply_trigger

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
        if AI.supply_used >= self.supply_trigger or self.valid_attempts > 0:
            await self.request.execute(AI)

            return True

        return False
