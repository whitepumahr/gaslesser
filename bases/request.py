# Imports:

# StarCraft II:
# > Bot AI:
from sc2.bot_ai import BotAI

# > IDs:
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId

# Dataclasses:
import dataclasses

# Typing:
import typing


# Classes:
@dataclasses.dataclass
class Request:
    """
    Base class for requests.

    Types of requests:
        Upgrade Request,
        Train Request,
        Build Request,
        Expand Request,
        Ability Request,

    :param id:
    """

    id: typing.Union[UnitTypeId, AbilityId, UpgradeId, None]

    # Methods:
    async def execute(self, AI: BotAI) -> None:
        """
        Executes the request.
        Meant to be overriden.
        """
