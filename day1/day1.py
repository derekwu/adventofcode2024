from collections import defaultdict

FILENAME = './input.txt'


LEFT_LIST = []
RIGHT_LIST = []

LEFT_FREQ_MAP = defaultdict(int)
RIGHT_FREQ_MAP = defaultdict(int)

def parse_line(line):
	nums = line.split()
	num1 = int(nums[0])
	num2 = int(nums[1])
	LEFT_LIST.append(num1)
	RIGHT_LIST.append(num2)
	LEFT_FREQ_MAP[num1] += 1
	RIGHT_FREQ_MAP[num2] += 1


def parse_file_by_line(filename):
	with open(filename, 'r') as f:
		for line in f:
			parse_line(line)

if __name__=="__main__":
    parse_file_by_line(FILENAME)
    LEFT_LIST.sort()
    RIGHT_LIST.sort()
    diff_sum = 0
    for left, right in zip(LEFT_LIST, RIGHT_LIST):
    	diff_sum += abs(left - right)
    print('PART 1')
    print(diff_sum)

    similarity_sum = 0

    for left_num, left_freq in LEFT_FREQ_MAP.items():
    	# if left_num doesn't exist in right list, default dict will 
    	# return 0, therefore adding nothing to the sum	
    	similarity_sum += left_num * left_freq * RIGHT_FREQ_MAP[left_num]

    print('PART 2')
    print(similarity_sum)

