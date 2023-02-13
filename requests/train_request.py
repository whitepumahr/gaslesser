# Imports:

# StarCraft II:
# > Bot AI:
from sc2.bot_ai import BotAI

# > Units:
from sc2.units import Units

# > Unit:
from sc2.unit import Unit

# > IDs:
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId

# Dataclasses:
import dataclasses

# Loguru:
import loguru

# Bases:
from bot.bases import Request

# Dicts:
from bot.dicts import LARVA_MORPH_ABILITIES


# Classes:
@dataclasses.dataclass
class TrainRequest(Request):
    """
    Trains the unit requested.

    :param quantity:
    """

    valid_attempts: int = 0
    quantity: int = 1

    # Methods:
    async def verify_able(self, AI: BotAI) -> bool:
        if AI.can_afford(self.id) is False:
            return False

        if AI.supply_left < AI.calculate_supply_cost(self.id):
            return False

    async def execute(self, AI: BotAI) -> bool:
        # Guardian Statements:
        if self.valid_attempts == self.quantity:
            return True

        if await self.verify_able(AI) is False:
            return False

        # Main:
        if self.id == UnitTypeId.QUEEN:
            for iteration in range(self.quantity):
                if self.valid_attempts == self.quantity:
                    return True

                if await self.verify_able(AI) is False:
                    return False

                available_hatcheries: Units = AI.townhalls.ready.idle
                if not any(available_hatcheries):
                    return False

                available_hatcheries.random.train(UnitTypeId.QUEEN)

                self.valid_attempts += 1
        else:
            larva: Units = AI.units.of_type(UnitTypeId.LARVA)
            if not any(larva):
                return False

            for iteration in range(self.quantity):
                if self.valid_attempts == self.quantity:
                    return True

                if await self.verify_able(AI) is False:
                    return False

                selected_larva: Unit = larva.random

                if LARVA_MORPH_ABILITIES[self.id] in await AI.get_available_abilities(
                    selected_larva
                ):
                    larva.random.train(self.id)

                    self.valid_attempts += 1
                else:
                    return False
