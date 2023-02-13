# Imports:

# StarCraft II:
# > IDs:
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId

# Typing:
import typing

# Dictionaries:
LARVA_MORPH_ABILITIES: typing.Dict[UnitTypeId, AbilityId] = {
    UnitTypeId.DRONE: AbilityId.LARVATRAIN_DRONE,
    UnitTypeId.ZERGLING: AbilityId.LARVATRAIN_ZERGLING,
    UnitTypeId.OVERLORD: AbilityId.LARVATRAIN_OVERLORD,
    UnitTypeId.ROACH: AbilityId.LARVATRAIN_ROACH,
    UnitTypeId.HYDRALISK: AbilityId.LARVATRAIN_HYDRALISK,
    UnitTypeId.INFESTOR: AbilityId.LARVATRAIN_INFESTOR,
    UnitTypeId.CORRUPTOR: AbilityId.LARVATRAIN_CORRUPTOR,
    UnitTypeId.ULTRALISK: AbilityId.LARVATRAIN_ULTRALISK,
    UnitTypeId.VIPER: AbilityId.LARVATRAIN_VIPER,
    UnitTypeId.MUTALISK: AbilityId.LARVATRAIN_MUTALISK,
}

# TODO: There is no swarmhost one... Might have to do special ones for that later.
