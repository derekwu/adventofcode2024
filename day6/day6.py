from collections import defaultdict

from enum import Enum

FILENAME = './input.txt'


# UP, RIGHT, DOWN, LEFT
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Solver(object):

  def __init__(self):
    self.board = []
    self.start_position = None

  def initialize_object(self, filename):
    with open(filename, 'r') as f:
      row = 0
      for line in f:
        self.board.append([char for char in line])
        # lazy way to get start position
        if '^' in line:
          self.start_position = (row, self.board[-1].index('^'))
        row += 1



  def in_bounds(self, i, j):
    return i >=0 and i < len(self.board) and j >= 0 and j < len(self.board[0])
    
  def solve_part_1(self):
    curr_i, curr_j = self.start_position
    visited = {}
    unique_path_squares = 0
    guard_direction_index = 0 # starts up via manual inspection
    while self.in_bounds(curr_i, curr_j):
      if self.board[curr_i][curr_j] == '#':
        # obstacle, go back and switch directions
        i_delta, j_delta = DIRECTIONS[guard_direction_index]
        guard_direction_index += 1
        guard_direction_index %= 4
        new_i_delta, new_j_delta = DIRECTIONS[guard_direction_index]
        curr_i, curr_j = curr_i - i_delta + new_i_delta, curr_j - j_delta + new_j_delta
      else:
        if (curr_i, curr_j) not in visited:
          visited[(curr_i, curr_j)] = 'X'  # doesn't matter what I do here
          unique_path_squares += 1
        i_delta, j_delta = DIRECTIONS[guard_direction_index]
        curr_i, curr_j =  curr_i + i_delta, curr_j + j_delta
    return unique_path_squares

  def solve_part_2(self):
    valid_loop_modifications = 0
    for i in range(len(self.board)):
      for j in range(len(self.board[0])):
        if self.board[i][j] != '.':
          continue
        curr_i, curr_j = self.start_position
        visited = {}
        guard_direction_index = 0
        while self.in_bounds(curr_i, curr_j):
          if self.board[curr_i][curr_j] == '#' or (curr_i == i and curr_j == j):
            # obstacle, go back and switch directions
            i_delta, j_delta = DIRECTIONS[guard_direction_index]
            guard_direction_index += 1
            guard_direction_index %= 4
            new_i_delta, new_j_delta = DIRECTIONS[guard_direction_index]
            old_i, old_j = curr_i - i_delta, curr_j - j_delta
            if (old_i, old_j) not in visited: # unlikely that this occurs
              visited[(old_i, old_j)] = set([guard_direction_index])
            elif guard_direction_index in visited[(old_i, old_j)]:
              # We find ourselves in a loop!
              valid_loop_modifications += 1
              break
            else:
              visited[(old_i, old_j)].add(guard_direction_index)
            curr_i, curr_j = old_i+ new_i_delta, old_j + new_j_delta
          else:
            if (curr_i, curr_j) not in visited:
              visited[(curr_i, curr_j)] = set([guard_direction_index])
            elif guard_direction_index in visited[(curr_i, curr_j)]:
              # We find ourselves in a loop!
              valid_loop_modifications += 1
              break
            else:
              visited[(curr_i, curr_j)].add(guard_direction_index)
            i_delta, j_delta = DIRECTIONS[guard_direction_index]
            curr_i, curr_j =  curr_i + i_delta, curr_j + j_delta
    return valid_loop_modifications



if __name__=="__main__":
  solver = Solver()

  solver.initialize_object(FILENAME)
  print('PART 1')
  print(solver.solve_part_1())

  print('PART 2')
  print(solver.solve_part_2())


