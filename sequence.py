# Imports:

# StarCraft II:
# > IDs:
from sc2.ids.unit_typeid import UnitTypeId

# Typing:
import typing

# Wrappers:
from .wrappers import CustomWrapper, SupplyWrapper

# Requests:
from .requests import BuildRequest, TrainRequest

# Lists:
BEGINNER_SEQUENCE: typing.List[
    typing.Union[CustomWrapper, SupplyWrapper, BuildRequest, TrainRequest]
] = [
    SupplyWrapper(supply_trigger=12, request=TrainRequest, id=UnitTypeId.DRONE),
    SupplyWrapper(supply_trigger=13, request=TrainRequest, id=UnitTypeId.OVERLORD),
    CustomWrapper(
        condition=lambda AI: AI.already_pending(UnitTypeId.OVERLORD) == 1
        and AI.can_afford(UnitTypeId.DRONE),
        request=TrainRequest,
        id=UnitTypeId.DRONE,
    ),
]
