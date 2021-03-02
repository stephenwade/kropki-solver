#!/usr/bin/env python3

import copy

class Dot:
    def __init__(self, first_ref, second_ref, color):
        self.first_ref = first_ref
        self.second_ref = second_ref
        self.color = color

    def __str__(self):
        return f"{color} dot in between {first_ref} and {second_ref}"

    def __repr__(self):
        return (f"Dot({repr(self.first_ref)}, {repr(self.second_ref)}, "
                f"{repr(self.color)})")

    def to_char(self):
        if self.color == "black":
            return "●"
        if self.color == "white":
            return "○"

class Board:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = [[None for _ in range(board_size)]
                      for _ in range(board_size)]
        self.dots = []

    def add_dot(self, dot):
        self.dots.append(dot)

    def lookup_dot(self, first_ref, second_ref):
        for dot in self.dots:
            if dot.first_ref == first_ref and dot.second_ref == second_ref:
                return dot

    def get_next_empty_cell_ref(self):
        for row, row_list in enumerate(self.board):
            for col, cell in enumerate(row_list):
                if not cell:
                    return (row, col)

    def is_cell_valid(self, cell_ref):
        cell = self[cell_ref]

        # check cells in the same row
        for col in range(self.board_size):
            if col == cell_ref[1]:
                continue
            if cell == self[(cell_ref[0], col)]:
                return False

        # check cells in the same column
        for row in range(self.board_size):
            if row == cell_ref[0]:
                continue
            if cell == self[(row, cell_ref[1])]:
                return False

        # check dots
        def is_cell_pair_valid(first, second, dot_color):
            if second is None:
                return True

            if dot_color == "black":
                return first * 2 == second or first == second * 2
            if dot_color == "white":
                return first + 1 == second or first == second + 1
            return (not is_cell_pair_valid(first, second, "black")
                    and not is_cell_pair_valid(first, second, "white"))

        cell_up_ref = (cell_ref[0]-1, cell_ref[1])
        try:
            cell_up = self[cell_up_ref]

            dot_up = self.lookup_dot(cell_up_ref, cell_ref)
            if dot_up is None:
                pass

            if not is_cell_pair_valid(cell, cell_up,
                                      dot_up.color if dot_up else None):
                return False
        except IndexError:
            pass

        cell_down_ref = (cell_ref[0]+1, cell_ref[1])
        try:
            cell_down = self[cell_down_ref]

            dot_down = self.lookup_dot(cell_down_ref, cell_ref)
            if dot_down is None:
                pass

            if not is_cell_pair_valid(cell, cell_down,
                                      dot_down.color if dot_down else None):
                return False
        except IndexError:
            pass

        cell_left_ref = (cell_ref[0], cell_ref[1]-1)
        try:
            cell_left = self[cell_left_ref]

            dot_left = self.lookup_dot(cell_left_ref, cell_ref)
            if dot_left is None:
                pass

            if not is_cell_pair_valid(cell, cell_left,
                                      dot_left.color if dot_left else None):
                return False
        except IndexError:
            pass

        cell_right_ref = (cell_ref[0], cell_ref[1]+1)
        try:
            cell_right = self[cell_right_ref]

            dot_right = self.lookup_dot(cell_right_ref, cell_ref)
            if dot_right is None:
                pass

            if not is_cell_pair_valid(cell, cell_right,
                                      dot_right.color if dot_right else None):
                return False
        except IndexError:
            pass

        return True

    def is_completed(self):
        return self.get_next_empty_cell_ref() is None

    def __getitem__(self, key):
        return self.board[key[0]][key[1]]

    def __setitem__(self, key, value):
        self.board[key[0]][key[1]] = value

    def __str__(self):
        top_line = ("┌"
                    + "┬".join(["───" for _ in range(self.board_size)])
                    + "┐")
        bottom_line = ("└"
                       + "┴".join(["───" for _ in range(self.board_size)])
                       + "┘")
        VERTICAL_BAR = "│"
        HORIZONTAL_BAR = "─"
        LEFT_EDGE_LINE = "├"
        RIGHT_EDGE_LINE = "┤"
        INTERSECTION = "┼"

        def get_str_row(row):
            result = VERTICAL_BAR
            for col, cell in enumerate(self.board[row]):
                if cell:
                    result += f" {cell} "
                else:
                    result += "   "
                if col < self.board_size - 1:
                    dot = self.lookup_dot((row, col), (row, col+1))
                    if dot:
                        dot_char = dot.to_char()
                        if dot_char:
                            result += dot_char
                        else:
                            result += VERTICAL_BAR
                    else:
                        result += VERTICAL_BAR
                else:
                    result += VERTICAL_BAR
            return result

        def get_str_row_below(row):
            result = LEFT_EDGE_LINE
            for col in range(len(self.board[row])):
                dot = self.lookup_dot((row, col), (row+1, col))
                if dot:
                    dot_char = dot.to_char()
                    if dot_char:
                        result += f"─{dot_char}─"
                    else:
                        result += "───"
                else:
                    result += "───"
                if col < self.board_size - 1:
                    result += INTERSECTION
                else:
                    result += RIGHT_EDGE_LINE
            return result

        board_str = top_line + "\n"
        for row in range(self.board_size):
            board_str += get_str_row(row) + "\n"
            if row < self.board_size - 1:
                board_str += get_str_row_below(row) + "\n"
        board_str += bottom_line

        return board_str

def get_board():
    board_size = None
    while type(board_size) != int or board_size < 4 or board_size > 9:
        try:
            board_size_str = input("Board size: ")
            board_size = int(board_size_str)
        except ValueError:
            pass

    board = Board(board_size)

    def get_dots_lr(row):
        dots_str = input("|")
        for col, char in enumerate(dots_str):
            if char.lower() == "b":
                board.add_dot(Dot((row, col), (row, col+1), "black"))
            elif char.lower() == "w":
                board.add_dot(Dot((row, col), (row, col+1), "white"))

    def get_dots_ud(row):
        dots_str = input("-")
        for col, char in enumerate(dots_str):
            if char.lower() == "b":
                board.add_dot(Dot((row, col), (row+1, col), "black"))
            elif char.lower() == "w":
                board.add_dot(Dot((row, col), (row+1, col), "white"))

    for row in range(board_size):
        get_dots_lr(row)
        if row < board_size - 1:
            get_dots_ud(row)

    print()
    return board

def solve_board(board):
    if board.is_completed():
        return board

    cell_ref = board.get_next_empty_cell_ref()

    for i in range(1, board.board_size + 1):
        board[cell_ref] = i
        if board.is_cell_valid(cell_ref):
            maybe_solved_board = solve_board(board)
            if maybe_solved_board:
                return maybe_solved_board
        board[cell_ref] = None

def main():
    board = get_board()
    board = solve_board(board)
    print(board)

if __name__ == "__main__":
    main()
