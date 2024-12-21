from collections import defaultdict
import math

from enum import Enum

FILENAME = './input.txt'


class Solver(object):

  def __init__(self):
    self.antenna_map = defaultdict(list)
    self.rows = None
    self.columns = None

  def initialize_object(self, filename):
    with open(filename, 'r') as f:
      row = 0
      for line in f:
        if self.columns == None:
          # determine num of columns from first line
          self.columns = len(line.strip())
        if not line.strip():
          # if line is empty, exit
          break
        for col, char in enumerate(line):
          if char != '.':
            self.antenna_map[char].append((row, col))
        row += 1
      self.rows = row

  def in_bounds(self, row, col):
    return row >= 0 and row < self.rows and col >= 0 and col < self.columns

  def solve_part_1(self):
    antinodes = set()
    for antenna_type, locations in self.antenna_map.items():
      if len(locations) < 2:
        continue
      for i in range(len(locations) - 1):
        for j in range(i + 1, len(locations)):
          loc1 = locations[i]
          loc2 = locations[j]
          row_diff = loc1[0] - loc2[0]
          col_diff = loc1[1] - loc2[1]
          antinode1 = (loc1[0] + row_diff, loc1[1] + col_diff)
          antinode2 = (loc2[0] - row_diff, loc2[1] - col_diff)
          if self.in_bounds(antinode1[0], antinode1[1]):
            antinodes.add(antinode1)
          if self.in_bounds(antinode2[0], antinode2[1]):
            antinodes.add(antinode2)
    return len(antinodes)

  def solve_part_2(self):
    antinodes = set()
    for antenna_type, locations in self.antenna_map.items():
      if len(locations) < 2:
        continue
      for i in range(len(locations) - 1):
        for j in range(i + 1, len(locations)):
          loc1 = locations[i]
          loc2 = locations[j]
          row_diff = loc1[0] - loc2[0]
          col_diff = loc1[1] - loc2[1]
          gcd = math.gcd(row_diff, col_diff)
          row_diff /= gcd
          col_diff /= gcd
          curr_row = loc1[0]
          curr_col = loc1[1]
          while self.in_bounds(curr_row, curr_col):
            antinodes.add((curr_row, curr_col))
            curr_row += row_diff
            curr_col += col_diff
          curr_row = loc1[0]
          curr_col = loc1[1]
          while self.in_bounds(curr_row, curr_col):
            antinodes.add((curr_row, curr_col))
            curr_row -= row_diff
            curr_col -= col_diff
    return len(antinodes)




if __name__=="__main__":
  solver = Solver()

  solver.initialize_object(FILENAME)
  print('PART 1')
  print(solver.solve_part_1())

  print('PART 2')
  print(solver.solve_part_2())


