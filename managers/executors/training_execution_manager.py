# Imports:

# StarCraft II:
# > Bot AI:
from sc2.bot_ai import BotAI

# Bases:
from bot.bases import Manager, Request


# Classes:
class TrainingExecutionManager(Manager):
    """
    Parses training requests and executes them.
    """

    # Initialization:
    def __init__(self) -> None:
        # Lists:
        self.verifying: list = []
        self.requests: list = []

    # Methods:
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

        # Verifying Requests:
        for request in self.verifying:
            if request in self.requests:
                self.requests.remove(request)

            await self.execute_request(request, AI)

            if request.valid_attempts == request.quantity:
                cleanup.append(request)

        # Cleaning Requests:
        for request in cleanup:
            if request in self.verifying:
                self.verifying.remove(request)
