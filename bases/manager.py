# Imports:

# StarCraft II:
# > Unit:
from sc2.unit import Unit


# Classes:
class Manager:
    """
    Base class for managers.

    TODO: Finish the rest of functions from BotAI clsas.
    """

    # Initialization:
    def __init__(self) -> None:
        pass

    # Methods:
    async def on_unit_destroyed(self, unit_tag: int) -> None:
        """
        Is called every time a unit is destroyed or dies.
        Meant to be overriden.

        :param unit_tag:
        """

    async def on_unit_created(self, unit: Unit) -> None:
        """
        Is called every time a unit is created.
        Meant to be overriden.

        :param unit:
        """

    async def on_start(self) -> None:
        """
        Is called at the start of a game.
        Meant to be overriden.
        """

    async def on_step(self, iteration: int) -> None:
        """
        Is called every frame.
        Meant to be overriden.

        :param iteration:
        """
