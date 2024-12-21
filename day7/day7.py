from collections import defaultdict

from enum import Enum

FILENAME = './input.txt'


class Solver(object):

  def __init__(self):
    self.targets = []
    self.nums = []

  def initialize_object(self, filename):
    with open(filename, 'r') as f:
      for line in f:
        target_nums_split = line.split(':')
        self.targets.append(int(target_nums_split[0]))
        self.nums.append([int(x) for x in target_nums_split[1].strip().split(' ')])

  def is_target_achievable(self, target, nums, index_to_consider, intermediary_expression):
    assert(index_to_consider < len(nums))
    if intermediary_expression > target:
      return False
    if len(nums) == 1:
      return target == nums[0]
    if index_to_consider == 0:
      return self.is_target_achievable(target, nums, index_to_consider + 1, nums[0])
    if index_to_consider == len(nums) - 1:
      last_num = nums[index_to_consider]
      return target == intermediary_expression + last_num or target == intermediary_expression * last_num

    return self.is_target_achievable(target, nums, index_to_consider + 1, intermediary_expression + nums[index_to_consider]) or self.is_target_achievable (target, nums, index_to_consider + 1, intermediary_expression * nums[index_to_consider])

  def is_target_achievable_part_2(self, target, nums, index_to_consider, intermediary_expression):
    assert(index_to_consider < len(nums))
    if intermediary_expression > target:
      return False
    if len(nums) == 1:
      return target == nums[0]
    if index_to_consider == 0:
      return self.is_target_achievable_part_2(target, nums, index_to_consider + 1, nums[0])
    if index_to_consider == len(nums) - 1:
      last_num = nums[index_to_consider]
      return target == intermediary_expression + last_num or target == intermediary_expression * last_num or target == int(str(intermediary_expression) + str(last_num))

    return (self.is_target_achievable_part_2(target, nums, index_to_consider + 1, intermediary_expression + nums[index_to_consider])
      or self.is_target_achievable_part_2 (target, nums, index_to_consider + 1, intermediary_expression * nums[index_to_consider])
      or self.is_target_achievable_part_2 (target, nums, index_to_consider + 1, int(str(intermediary_expression) + str(nums[index_to_consider]))))

  def solve_part_1(self):
    target_sum = 0
    for target, nums in zip(self.targets, self.nums):
      if self.is_target_achievable(target, nums, 0, 0):
        target_sum += target
    return target_sum

  def solve_part_2(self):
    target_sum = 0
    for target, nums in zip(self.targets, self.nums):
      if self.is_target_achievable_part_2(target, nums, 0, 0):
        target_sum += target
    return target_sum




if __name__=="__main__":
  solver = Solver()

  solver.initialize_object(FILENAME)
  print('PART 1')
  print(solver.solve_part_1())

  print('PART 2')
  print(solver.solve_part_2())


