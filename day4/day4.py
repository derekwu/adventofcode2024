from enum import Enum

FILENAME = './input.txt'

XMAS = 'XMAS'


class Solver(object):

  def __init__(self):
    self.board = []
    self.width = None
    self.height = None

  def parse_line(self, line):
    self.board.append([x for x in line])

  def initialize_object(self, filename):
    with open(filename, 'r') as f:
      for line in f:
        self.parse_line(line)

    self.width = len(self.board[0])
    self.height = len(self.board)

  def return_xmas_element_match(self, i, j, char):
    if i < 0 or i >= self.height or j < 0 or j >= self.width:
      return False
    return self.board[i][j] == char

  def return_char_or_empty(self, i, j):
    if i < 0 or i >= self.height or j < 0 or j >= self.width:
      return ''
    return self.board[i][j]

  def check_corner_chars(self, i1, j1, i2, j2):
    first_char = self.return_char_or_empty(i1, j1)
    second_char = self.return_char_or_empty(i2, j2)
    return (first_char == 'M' and second_char == 'S') or (first_char == 'S' and second_char == 'M')


  def count_xmas(self, i, j):
    i_dirs = [-1, 0, 1]
    j_dirs = [-1, 0, 1]

    valid_xmas_from_ij = 0

    for i_dir in i_dirs:
      for j_dir in j_dirs:
        if i_dir == 0 and j_dir == 0:
          continue
        match = True
        for match_index in range(len(XMAS)):
          new_i = i + match_index * i_dir
          new_j = j + match_index * j_dir
          if not self.return_xmas_element_match(new_i, new_j, XMAS[match_index]):
            match = False
            break
        if match:
          valid_xmas_from_ij += 1
    return valid_xmas_from_ij

  def is_cross_mas(self, i, j):
    if self.board[i][j] != 'A':
      return False
    # Center character is good, check cross:
    # +1, +1 and -1, -1
    # +1, -1 and -1, +1
    if not self.check_corner_chars(i + 1, j + 1, i - 1, j - 1):
      return False
    if not self.check_corner_chars(i + 1, j - 1, i - 1, j + 1):
      return False
    return True


    
  def solve_part_1(self):
    total_valid_xmas = 0
    for i in range(self.height):
      for j in range(self.width):
        total_valid_xmas += self.count_xmas(i, j)
    return total_valid_xmas

  def solve_part_2(self):
    total_valid_cross_mas = 0
    for i in range(self.height):
      for j in range(self.width):
        total_valid_cross_mas += self.is_cross_mas(i, j)
    return total_valid_cross_mas

if __name__=="__main__":
  solver = Solver()

  solver.initialize_object(FILENAME)
  print('PART 1')
  print(solver.solve_part_1())

  print('PART 2')
  print(solver.solve_part_2())


