from __future__ import annotations
from typing import Iterable


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid: list[str] = []

        for puzzle_row in puzzle:
            row = ""

            for element in puzzle_row:
                row += str(element)

            self._grid.append(row)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[y] = self._grid[y][:x] + str(value) + self._grid[y][x + 1:]

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self._grid[y] = self._grid[y][:x] + "0" + self._grid[y][x + 1:]

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        return int(self._grid[y][x])

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        # Remove all values from the row
        row_values = set(self.row_values(y))
        options = options.difference(row_values)

        # Remove all values from the column
        column_values = set(self.column_values(x))
        options = options.difference(column_values)

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # Remove all values from the block
        block_values = set(self.block_values(block_index))
        options = options.difference(block_values)

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        next_x, next_y = -1, -1

        for y in range(9):
            if "0" in self._grid[y]:
                return self._grid[y].index("0"), y

        return next_x, next_y

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""
        return map(int, self._grid[i])

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        values = []

        for j in range(9):
            values.append(self._grid[j][i])

        return map(int, values)

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        row1 = list(self._grid[y_start][x_start:x_start + 3])
        row2 = list(self._grid[y_start + 1][x_start:x_start + 3])
        row3 = list(self._grid[y_start + 2][x_start:x_start + 3])

        return map(int, row1 + row2 + row3)

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        result = True

        for i in range(9):
            column_values = set(self.column_values(i))
            row_values = set(self.row_values(i))
            block_values = set(self.block_values(i))

            if column_values.difference(values) or row_values.difference(values) or block_values.difference(values):
                result = False
                return result

        return result

    def __str__(self) -> str:
        representation = ""

        for row in self._grid:
            representation += row + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
