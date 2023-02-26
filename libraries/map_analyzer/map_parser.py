# Imports:

# StarCraft II:
# > Position:
from sc2.position import Point3, Point2

# > Bot AI:
from sc2.bot_ai import BotAI

# Typing:
import typing

# Numpy:
import numpy

# JSON:
import json


# Classes:
class MapParser:
    """
    Map parser library.
    Allows for cached information about the map, like ramp tiles.
    """

    # Initialization:
    def __init__(self, DRAW_RAMP_TILES: bool = False) -> None:
        # Booleans:
        self.DRAW_RAMP_TILES: bool = DRAW_RAMP_TILES

        # Lists:
        self.chokepoint_tiles: typing.List[Point2] = []
        self.ramp_tiles: typing.List[Point2] = []

    # Properties:
    @property
    def RAMP_TILE_COLOR(self) -> Point3:
        return Point3((255, 255, 0))

    # Methods:
    def is_ramp_tile(self, coordinate: Point2, AI: BotAI):
        if AI.game_info.pathing_grid[coordinate.x, coordinate.y] == 1:
            coordinate_neighbors = [
                Point2((coordinate.x + delta_x, coordinate.y + delta_y))
                for delta_x, delta_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            ]

            walkable_neighbors = [
                coordinate_neighbor
                for coordinate_neighbor in coordinate_neighbors
                if AI.game_info.pathing_grid[
                    coordinate_neighbor.x, coordinate_neighbor.y
                ]
                == 1
            ]

            if len(walkable_neighbors) < 4:
                return True
            else:
                for walkable_neighbor in walkable_neighbors:
                    if (
                        abs(
                            AI.game_info.terrain_height[
                                walkable_neighbor.x, walkable_neighbor.y
                            ]
                            - AI.game_info.terrain_height[coordinate.x, coordinate.y]
                        )
                        > 1
                    ):
                        self.ramp_tiles.append(coordinate)
                        return False

    async def analyze(self, AI: BotAI) -> typing.Any:
        # Debugging:
        if self.DRAW_RAMP_TILES is True:
            for coordinate in self.ramp_tiles:
                three_dimensional_coordinate: Point3 = Point3(
                    (coordinate.x, coordinate.y, AI.get_terrain_z_height(coordinate))
                )

                AI.client.debug_box2_out(
                    pos=three_dimensional_coordinate,
                    half_vertex_length=0.5,
                    color=self.RAMP_TILE_COLOR,
                )

        # Reading:
        with open("bot/libraries/map_analyzer/map_data.json", "r") as json_file:
            map_data = json.load(json_file)

            if AI.game_info.map_name in map_data:
                return map_data[AI.game_info.map_name]

        # Writing:
        with open("bot/libraries/map_analyzer/map_data.json", "w") as json_file:
            # Getting Data:
            map_matrix: numpy.ndarray = numpy.array(AI.game_info.map_size)

            for x in range(map_matrix[0]):
                for y in range(map_matrix[1]):
                    coordinate: Point2 = Point2((x, y))

                    if self.is_ramp_tile(coordinate, AI) is True:
                        self.chokepoint_tiles.append(coordinate)

            # Dumping Data:
            json.dump(
                {
                    AI.game_info.map_name: {
                        "chokepoint_tiles:": self.chokepoint_tiles,
                        "ramp_tiles": self.ramp_tiles,
                    }
                },
                json_file,
            )

        # Returning:
        with open("bot/libraries/map_analyzer/map_data.json", "r") as json_file:
            return json.load(json_file)[AI.game_info.map_name]
