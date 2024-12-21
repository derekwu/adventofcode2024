from collections import defaultdict

from enum import Enum

FILENAME = './input.txt'

class Parsing(Enum):
  PARTIAL_ORDER = 1
  ORDERINGS = 2

class Solver(object):

  def __init__(self):
    # Map of page number to list of followed pages
    self.partial_order_map = defaultdict(list)
    # Map of followed pages to its preorder pages
    self.blocker_map = defaultdict(set)
    self.orderings = []

  def parse_partial_order_line(self, line):
    ordering = [int(x) for x in line.split('|')]
    preorder = ordering[0]
    postorder = ordering[1]
    self.partial_order_map[preorder].append(postorder)
    self.blocker_map[postorder].add(preorder)

  def parse_orderings_line(self, line):
    self.orderings.append([int(x) for x in line.split(',')])


  def initialize_object(self, filename):
    with open(filename, 'r') as f:
      stage = Parsing.PARTIAL_ORDER

      for line in f:
        if len(line.strip()) == 0:
          stage = Parsing.ORDERINGS
          continue
        if stage == Parsing.PARTIAL_ORDER:
          self.parse_partial_order_line(line)
          continue
        if stage == Parsing.ORDERINGS:
          self.parse_orderings_line(line)
          continue

  def valid_ordering(self, ordering):
    seen = set()
    for num in ordering:
      for postorder in self.partial_order_map[num]:
        if postorder in seen:
          return False
      seen.add(num)
    return True

  def return_key_with_empty_set(self, num_to_preorder_map):
    # assumes input is constrained to one unique key with empty set
    for key, value in num_to_preorder_map.items():
      if len(value) == 0:
        return key
    return None


  def validate_and_fix_ordering(self, ordering):
    seen = set()
    valid_ordering = True
    continue_searching = True
    for num in ordering:
      if continue_searching:
        for postorder in self.partial_order_map[num]:
          if postorder in seen:
            valid_ordering = False
            continue_searching = False
            break

        seen.add(num)
    if valid_ordering:
      return (True, ordering)

    all_nums_in_ordering = set(ordering)
    relevant_num_to_preorder = {}
    for num in ordering:
      if num not in relevant_num_to_preorder:
        relevant_num_to_preorder[num] = set()
      for preorder in self.blocker_map[num]:
        if preorder in all_nums_in_ordering:
          relevant_num_to_preorder[num].add(preorder)

    fixed_ordering = []
    while relevant_num_to_preorder:
      num_to_remove = self.return_key_with_empty_set(relevant_num_to_preorder)
      fixed_ordering.append(num_to_remove)
      del relevant_num_to_preorder[num_to_remove]
      for postorder in self.partial_order_map[num_to_remove]:
        if postorder in relevant_num_to_preorder:
          relevant_num_to_preorder[postorder].remove(num_to_remove)
    return (False, fixed_ordering)

    
  def solve_part_1(self):
    page_number_sum = 0
    for ordering in self.orderings:
      if self.valid_ordering(ordering):
        page_number_sum += ordering[int(len(ordering) / 2)]

    return page_number_sum

  def solve_part_2(self):
    page_number_sum = 0
    for ordering in self.orderings:
      valid, fixed = self.validate_and_fix_ordering(ordering)
      if not valid:
        page_number_sum += fixed[int(len(fixed) / 2)]

    return page_number_sum

if __name__=="__main__":
  solver = Solver()

  solver.initialize_object(FILENAME)
  print('PART 1')
  print(solver.solve_part_1())

  print('PART 2')
  print(solver.solve_part_2())


