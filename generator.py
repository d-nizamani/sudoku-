import copy
import random

EMPTY_CELLS = {
    "Easy": 35,
    "Medium": 45,
    "Hard": 51,
    "Expert": 55,
}

def candidates(board, row, col):
    used = set(board[row])
    used.update(board[r][col] for r in range(9))
    r0, c0 = (row // 3) * 3, (col // 3) * 3
    for r in range(r0, r0 + 3):
        for c in range(c0, c0 + 3):
            used.add(board[r][c])
    used.discard(0)
    return [n for n in range(1, 10) if n not in used]

def find_best_empty(board):
    best_cell, best_options = None, None
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                options = candidates(board, r, c)
                if best_options is None or len(options) < len(best_options):
                    best_cell, best_options = (r, c), options
                if len(options) <= 1:
                    return best_cell, best_options
    return best_cell, best_options

def solve(board):
    cell, options = find_best_empty(board)
    if cell is None:
        return True
    if not options:
        return False
    random.shuffle(options)
    row, col = cell
    for n in options:
        board[row][col] = n
        if solve(board):
            return True
        board[row][col] = 0
    return False

def count_solutions(board, limit=2):
    cell, options = find_best_empty(board)
    if cell is None:
        return 1
    if not options:
        return 0
    row, col = cell
    total = 0
    for n in options:
        board[row][col] = n
        total += count_solutions(board, limit - total)
        board[row][col] = 0
        if total >= limit:
            return total
    return total

def generate_puzzle(difficulty):
    solution = [[0] * 9 for _ in range(9)]
    solve(solution)
    puzzle = copy.deepcopy(solution)
    cells = list(range(81))
    random.shuffle(cells)
    target = EMPTY_CELLS[difficulty]
    removed = 0
    for index in cells:
        if removed >= target:
            break
        row, col = divmod(index, 9)
        old = puzzle[row][col]
        puzzle[row][col] = 0
        if count_solutions(copy.deepcopy(puzzle)) == 1:
            removed += 1
        else:
            puzzle[row][col] = old
    return puzzle, solution
