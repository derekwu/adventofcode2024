from collections import defaultdict

FILENAME = './input.txt'

SAFE_ROWS = 0
SAFE_ROWS_WITH_TOLERATION = 0

def is_safe_row(nums):
  if len(nums) <= 1:
    return True

  positive_diffs = 0
  negative_diffs = 0

  for i in range(len(nums) - 1):
    first_num = nums[i]
    second_num = nums[i + 1]
    diff = second_num - first_num
    if abs(diff) < 1 or abs(diff) > 3:
      return False
    # diff must be nonzero due to above check, so first_num != second_num
    if diff > 0:
      positive_diffs += 1
    else:
      negative_diffs += 1

  return positive_diffs == 0 or negative_diffs == 0

def parse_line(line):
	global SAFE_ROWS
	global SAFE_ROWS_WITH_TOLERATION
	nums = [int(x) for x in line.split()]
	SAFE_ROWS += is_safe_row(nums)
	tolerable_row = False
	for i in range(len(nums)):
		if is_safe_row(nums[:i] + nums[i+1:]):
			tolerable_row = True
			break
	SAFE_ROWS_WITH_TOLERATION += tolerable_row


def parse_file_by_line(filename):
	with open(filename, 'r') as f:
		for line in f:
			parse_line(line)

if __name__=="__main__":
    parse_file_by_line(FILENAME)
    print('PART 1')
    print(SAFE_ROWS)
    print('PART 2')
    print(SAFE_ROWS_WITH_TOLERATION)

