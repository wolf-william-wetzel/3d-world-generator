from pathlib import Path
import functools

import pygame as pg

from typing import Callable, Sequence, Optional


def toggle_fullscreen(size: Sequence[float], fullscreen: bool, flags: int = 0) -> pg.Surface:
    """Toggle the display to and from fullscreen. Fullscreen resolution is the display size."""
    if fullscreen:
        return pg.display.set_mode((0, 0), pg.FULLSCREEN | flags)
    return pg.display.set_mode(size, flags)  # noqa


@functools.cache
def make_color_image(size: tuple[int, int], color: tuple[int, int, int]) -> pg.Surface:
    """Return a Surface of the required size and color."""
    surf = pg.Surface(size)
    surf.fill(color)
    return surf


def array2d[T, R](size: Sequence[int], default: T | Callable[[int, int], R]) -> list[list[T | R]]:
    """Create and return a 2d array of the specified size filled with ``default``.

    You can also pass in a callable that takes in the current (x, y) and produces a value.
    """
    return [[default(x, y) if callable(default) else default for y in range(size[1])] for x in range(size[0])]


def array3d[T, R](size: Sequence[int], default: T | Callable[[int, int, int], R]) -> list[list[list[T | R]]]:
    """Create and return a 3d array of the specified size filled with ``default``.

    You can also pass in a callable that takes in the current (x, y, z) and produces a value.
    """
    return [[[default(x, y, z) if callable(default) else default for z in range(size[2])]
             for y in range(size[1])] for x in range(size[0])]


def in_bounds2d[T](pos: Sequence[int], array: list[list[T]], no_value=False) -> type("no_value") | T:
    """Return ``no_value`` if the position is not in the bounds of the array.

    Otherwise, return the object at the position.
    """
    if pos[0] < 0 or pos[1] < 0:
        return no_value
    try:
        return array[pos[0]][pos[1]]
    except IndexError:
        return no_value


def in_bounds3d[T](pos: Sequence[int], array: list[list[list[T]]], no_value=False) -> type("no_value") | T:
    """Return ``no_value`` if the position is not in the bounds of the array.

    Otherwise, return the object at the position.
    """
    if pos[0] < 0 or pos[1] < 0 or pos[2] < 0:
        return no_value
    try:
        return array[pos[0]][pos[1]][pos[2]]
    except IndexError:
        return no_value


class TileLoader:
    """Utility class for clipping and coloring tiles from a sheet."""
    def __init__(self, img_path: Path, tile_size: tuple[int, int]):
        self.image = pg.image.load(img_path).convert()
        self.tile_size = tile_size
        self.sheet_size = self.image.width // tile_size[0], self.image.height // tile_size[1]

    @functools.cache
    def get_tile(self, tile: tuple[int, int], color: tuple[int, int, int],
                 color_key: Optional[tuple[int, int, int]] = (0, 0, 0)) -> pg.Surface:
        """Return the (x, y) tile, tinted with the given color and with the given key transparency."""
        tile_surf = pg.Surface(self.tile_size)  # Create the tile surface.
        tile_surf.blit(self.image, (0, 0),  # Blit the sheet onto the tile surface.
                       (tile[0] * self.tile_size[0], tile[1] * self.tile_size[1], *self.tile_size))
        tile_surf.fill(color, special_flags=pg.BLEND_MULT)  # Color the tile surface with the given color.
        if color_key is not None:  # Set the key transparency, if not None.
            tile_surf.set_colorkey(color_key)
        return tile_surf
